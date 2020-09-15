using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using Octgn.Library;
using Octgn.DataNew.Entities;
using Octgn.Core.DataExtensionMethods;
using System.ComponentModel;
using System.IO;
using System.Windows.Media.Imaging;
using System.Net;
using System.Drawing.Imaging;
using System.Runtime.Serialization;
using Image = System.Drawing.Image;
using System.Threading;
using MTGImageFetcher.Entities;
using System.Net.Http;

namespace MTGImageFetcher
{
    /// <summary>
    /// Interaction logic for PluginWindow.xaml
    /// </summary>
    /// 

    public partial class PluginWindow : INotifyPropertyChanged
    {
        public bool xl = false;
        public bool onlyMissingImages = false;
        public string selectedLanguage;
        private string _currentCard;
        private string _currentSet;

        public string CurrentCard
        {
            get
            {
                return _currentCard;
            }
            set
            {
                if (_currentCard == value) return;
                _currentCard = value;
                OnPropertyChanged("CurrentCard");
            }
        }
        public string CurrentSet
        {
            get
            {
                return _currentSet;
            }
            set
            {
                if (_currentSet == value) return;
                _currentSet = value;
                OnPropertyChanged("CurrentSet");
            }
        }

        public List<SetItem> setList { get; private set; }

        private CancellationTokenSource _cts;

        public PluginWindow(Game game)
        {
            this.InitializeComponent();
            this.DataContext = this;

            setList = new List<SetItem>();
            SetList.ItemsSource = setList;

            foreach (var set in game.Sets())
            {
                if (!set.Hidden && set.Cards.Count() > 0)
                {
                    var setItem = new SetItem();
                    setItem.set = set;
                    setList.Add(setItem);
                }
            }
            
            this.Closing += CancelWorkers;
        }

        

        private void DownloadSingle(object sender, RoutedEventArgs e)
        {
            var selectedSet = SetList.SelectedItem as SetItem;
            if (selectedSet == null) return;
            Generate(new List<SetItem>() { selectedSet });
        }

        private void DownloadAll(object sender, RoutedEventArgs e)
        {
            Generate(setList.ToList());
        }

        private async void Generate(List<SetItem> sets)
        {
            XLImages.IsEnabled = false;
            MissingImages.IsEnabled = false;
            SetList.IsEnabled = false;
            NameRadio.IsEnabled = false;
            DateRadio.IsEnabled = false;
            LanguageBox.IsEnabled = false;
            DownloadButton.Visibility = Visibility.Collapsed;
            DownloadAllButton.Visibility = Visibility.Collapsed;
            CancelButton.Visibility = Visibility.Visible;

            selectedLanguage = ((ComboBoxItem)LanguageBox.SelectedItem).Tag.ToString();

            _cts = new CancellationTokenSource();
            var token = _cts.Token;

            var progressUpdater = new Progress<double>(ProgressChanged) as IProgress<double>;
            var setProgressUpdater = new Progress<int>(SetProgressChanged) as IProgress<int>;
            var localImageUpdater = new Progress<BitmapImage>(LocalImageChanged) as IProgress<BitmapImage>;
            var webImageUpdater = new Progress<BitmapImage>(WebImageChanged) as IProgress<BitmapImage>;
            var currentCardUpdater = new Progress<string>(CurrentCardChanged) as IProgress<string>;
            var currentSetUpdater = new Progress<string>(CurrentSetChanged) as IProgress<string>;

            var finishedHandler = new Progress<bool>(value =>
            {
                if (value == true)
                    WorkerCompleted();
            });
            var finished = finishedHandler as IProgress<bool>;

            SetProgressBar.Maximum = sets.Count;
            SetProgressBar.Value = 0;
            await Task.Run(() =>
                {
                    var setIndex = -1;
                    foreach (var setItem in sets)
                    {
                        setProgressUpdater.Report(setIndex++);
                        currentSetUpdater.Report(setItem.Name);

                        double i = 0.0;
                        var isTokenSet = setItem.set.Id.ToString() == "a584b75b-266f-4378-bed5-9ffa96cd3961";

                        foreach (var card in setItem.set.Cards)
                        {
                            foreach (var alt in card.PropertySets.Values)
                            {
                                progressUpdater.Report(i / setItem.CardCount);

                                if (_cts.IsCancellationRequested) break;
                                currentCardUpdater.Report(alt.Name);

                                string imageParameters = "?format=image";

                                if (xl == true)
                                    imageParameters += "&version=large";
                                else
                                    imageParameters += "&version=normal";

                                if (!isTokenSet)
                                {
                                    switch (alt.Type)
                                    {
                                        case "modal_dfc":
                                        case "meld":
                                        case "transform":
                                            {
                                                imageParameters += "&face=back";
                                                break;
                                            }
                                        case "flip":
                                        case "":
                                            {
                                                break;
                                            }
                                        default:
                                            {
                                                //skip any card that has an unusual alt type (like split cards)
                                                continue;
                                            }
                                    }
                                }
                                i++;

                                // local image file check

                                var files = FindLocalCardImages(setItem.set, card, alt.Type);
                                var localImagePath = files.FirstOrDefault();

                                string imageLanguage = null;
                                int imageTimeStamp = 0;
                                int imageWidth = 0;
                                if (localImagePath == null)
                                {
                                    localImageUpdater.Report(null);
                                }
                                else
                                {
                                    if (onlyMissingImages == true)
                                    {
                                        webImageUpdater.Report(null);
                                        continue;
                                    }
                                    try
                                    {
                                        using (var filestream = File.OpenRead(localImagePath))
                                        {
                                            var bitmap = StreamToBitmapImage(filestream);
                                            localImageUpdater.Report(bitmap);
                                            using (var image = Image.FromStream(filestream))
                                            {
                                                imageLanguage = Encoding.Unicode.GetString(image.PropertyItems.FirstOrDefault(x => x.Id == 40094)?.Value);
                                                imageTimeStamp = Convert.ToInt32(Encoding.Unicode.GetString(image.PropertyItems.FirstOrDefault(x => x.Id == 40092)?.Value));
                                                imageWidth = image.Width;
                                            }
                                        }
                                    }
                                    catch
                                    {

                                    }
                                }

                                // get web image data from headers

                                var setCode = isTokenSet ? card.GetProperty("Flags", alt.Type).ToString().ToLower() : setItem.set.ShortName;
                                var webImageLanguage = selectedLanguage;

                                var url = string.Format("https://api.scryfall.com/cards/{0}/{1}/{2}{3}",
                                                                                        setCode,
                                                                                        card.GetProperty("Number", alt.Type).ToString().TrimStart('0'),
                                                                                        selectedLanguage,
                                                                                        imageParameters);

                                var header = Client.SendAsync(new HttpRequestMessage(HttpMethod.Head, url)).Result;

                                if (header.StatusCode != HttpStatusCode.Found)
                                {
                                    webImageLanguage = "en";
                                    var englishUrl = string.Format("https://api.scryfall.com/cards/{0}/{1}/{2}{3}",
                                                                                            setCode,
                                                                                            card.GetProperty("Number", alt.Type).ToString().TrimStart('0'),
                                                                                            "en",
                                                                                            imageParameters);

                                    header = Client.SendAsync(new HttpRequestMessage(HttpMethod.Head, englishUrl)).Result;

                                    if (header.StatusCode != HttpStatusCode.Found)
                                    {
                                        var backupUrl = string.Format("https://api.scryfall.com/cards/{0}{1}",
                                                                                            card.Id,
                                                                                            imageParameters);
                                        header = Client.SendAsync(new HttpRequestMessage(HttpMethod.Head, backupUrl)).Result;
                                        if (header.StatusCode != HttpStatusCode.Found)
                                        {
                                            // no image found
                                            webImageUpdater.Report(null);
                                            continue;
                                        }
                                    }
                                }
                                var webImageUrl = header.Headers.Location;
                                var webTimestamp = Convert.ToInt32(webImageUrl.Query.TrimStart('?'));

                                // figure out if we should be downloading and updating this card image

                                if (localImagePath != null
                                    && imageWidth != 0
                                    && imageWidth > 600 == xl
                                    && imageLanguage.Equals(webImageLanguage,StringComparison.InvariantCultureIgnoreCase)
                                    && imageTimeStamp >= webTimestamp)
                                {
                                    webImageUpdater.Report(null);
                                    continue;
                                }

                                // download image

                                var webResponse = Client.GetAsync(webImageUrl).Result;
                                
                                using (var webImageStream = webResponse.Content.ReadAsStreamAsync().Result)
                                {
                                    if (webImageStream == null)
                                    {
                                        // if for whatever reason the image didn't download, skip the install.
                                        webImageUpdater.Report(null);
                                        continue;
                                    }
                                    using (var ms = new MemoryStream())
                                    {
                                        webImageStream.CopyTo(ms);
                                        webImageUpdater.Report(StreamToBitmapImage(ms));
                                    }
                                    using (var newimg = Image.FromStream(webImageStream))
                                    {
                                        if (alt.Type == "flip")
                                        {
                                            newimg.RotateFlip(System.Drawing.RotateFlipType.Rotate180FlipNone);
                                        }
                                        else if (alt.Size.Name == "Plane")
                                        {
                                            newimg.RotateFlip(System.Drawing.RotateFlipType.Rotate90FlipNone);
                                        }

                                        //comment metadata stores the timestamp data to compare updated images
                                        var commentMetadata = (PropertyItem)FormatterServices.GetUninitializedObject(typeof(PropertyItem));
                                        commentMetadata.Id = 40092; // this is the comments field
                                        commentMetadata.Value = Encoding.Unicode.GetBytes(webTimestamp.ToString());
                                        commentMetadata.Len = commentMetadata.Value.Length;
                                        commentMetadata.Type = 1;
                                        newimg.SetPropertyItem(commentMetadata);

                                        //keywords metadata stores language information
                                        var keywordsMetadata = (PropertyItem)FormatterServices.GetUninitializedObject(typeof(PropertyItem));
                                        keywordsMetadata.Id = 40094; // this is the keywords field
                                        keywordsMetadata.Value = Encoding.Unicode.GetBytes(webImageLanguage);
                                        keywordsMetadata.Len = keywordsMetadata.Value.Length;
                                        keywordsMetadata.Type = 1;
                                        newimg.SetPropertyItem(keywordsMetadata);

                                        var garbage = Config.Instance.Paths.GraveyardPath;
                                        if (!Directory.Exists(garbage)) Directory.CreateDirectory(garbage);

                                        if (files.Count() == 0)
                                            setItem.ImageCount++;

                                        foreach (var f in files.Select(x => new FileInfo(x)))
                                        {
                                            f.MoveTo(Path.Combine(garbage, f.Name));
                                        }

                                        var imageUri = String.IsNullOrWhiteSpace(alt.Type) ? card.ImageUri : card.ImageUri + "." + alt.Type;
                                        var newPath = Path.Combine(setItem.set.ImagePackUri, imageUri + ".jpg");
                                        newimg.Save(newPath, ImageFormat.Jpeg);
                                    }
                                }
                            }
                        }
                    }

                    finished.Report(true);
                });
        }

        private void ClickSet(object sender, SelectionChangedEventArgs e)
        {
            if (e.AddedItems.Count > 0)
            {
                ProgressBar.Value = 0;
                var selectedSet = e.AddedItems[0] as SetItem;
                var card = selectedSet.set.Cards.FirstOrDefault();
                var cardImageUrl = FindLocalCardImages(selectedSet.set, card, card.Alternate).FirstOrDefault();

                if (cardImageUrl != null)
                {
                    using (var filestream = File.OpenRead(cardImageUrl))
                    {
                        var bitmap = StreamToBitmapImage(filestream);
                        LocalImageChanged(bitmap);
                    }
                }
            }
        }

        private static HttpClient Client = new HttpClient(new HttpClientHandler() { AllowAutoRedirect = false });

        public static string[] FindLocalCardImages(Set set, Card card, string alt)
        {
            return FindLocalCardImages(set, string.IsNullOrWhiteSpace(alt) ? card.ImageUri : card.ImageUri + "." + alt);
        }
        public static string[] FindLocalCardImages(Set set, string imageUri)
        {
            var files =
                Directory.GetFiles(set.ImagePackUri, imageUri + ".*")
                    .Where(x => System.IO.Path.GetFileNameWithoutExtension(x).Equals(imageUri, StringComparison.InvariantCultureIgnoreCase))
                    .OrderBy(x => x.Length)
                    .ToArray();
            return files;
        }

        private BitmapImage StreamToBitmapImage(Stream stream)
        {
            var ret = new BitmapImage();
            stream.Position = 0;
            ret.BeginInit();
            ret.StreamSource = stream;
            ret.CacheOption = BitmapCacheOption.OnLoad;
            ret.EndInit();
            ret.Freeze();
            return ret;
        }

        private void LocalImageChanged(BitmapImage local)
        {
            if (local == null)
            {
                LocalImage.Source = null;
            }
            else
            {
                LocalImage.Source = local;
                LocalDimensions.Text = local.PixelWidth.ToString() + " x " + local.PixelHeight.ToString();
            }
        }
        private void WebImageChanged(BitmapImage web)
        {

            if (web == null)
            {
                WebImage.Source = null;
            }
            else
            {
                WebImage.Source = web;
            }
        }

        private void ProgressChanged(double progress)
        {
            ProgressBar.Value = progress;
        }
        private void SetProgressChanged(int progress)
        {
            SetProgressBar.Value = progress;
        }
        private void CurrentCardChanged(string name)
        {
            CurrentCard = name;
        }
        private void CurrentSetChanged(string name)
        {
            CurrentSet = name;
        }

        private void WorkerCompleted()
        {
            CurrentCard = "";
            CurrentSet = "";
            XLImages.IsEnabled = true;
            MissingImages.IsEnabled = true;
            SetList.IsEnabled = true;
            NameRadio.IsEnabled = true;
            DateRadio.IsEnabled = true;
            LanguageBox.IsEnabled = true;
            DownloadButton.Visibility = Visibility.Visible;
            DownloadAllButton.Visibility = Visibility.Visible;
            CancelButton.Visibility = Visibility.Collapsed;
        }

        private void CancelWorkers(object sender, EventArgs e)
        {
            if (_cts != null)
            {
                CurrentCard = "";
                CurrentSet = "";
                _cts.Cancel();
            }
        }

        private void XLImages_Checked(object sender, RoutedEventArgs e)
        {
            xl = XLImages.IsChecked ?? false;
        }
        private void MissingImages_Checked(object sender, RoutedEventArgs e)
        {

            onlyMissingImages = MissingImages.IsChecked ?? false;
        }

        #region INotifyPropertyChanged Members

        public event PropertyChangedEventHandler PropertyChanged;

        protected virtual void OnPropertyChanged(string propertyName)
        {
            if (PropertyChanged != null)
            {
                PropertyChanged(this, new PropertyChangedEventArgs(propertyName));
            }
        }

        #endregion

        private void NameRadioClick(object sender, RoutedEventArgs e)
        {
            setList = setList.OrderBy(x => x.Name).ToList();
            SetList.ItemsSource = setList;
        }

        private void DateRadioClick(object sender, RoutedEventArgs e)
        {
            setList = setList.OrderByDescending(x => x.ReleaseDate).ToList();
            SetList.ItemsSource = setList;
        }

    }


    [Serializable]
    public class MyException : Exception
    {
        public MyException() { }
        public MyException(string message) : base(message) { }
        public MyException(string message, Exception inner) : base(message, inner) { }
        protected MyException(
          SerializationInfo info,
          StreamingContext context) : base(info, context) { }
    }

}
