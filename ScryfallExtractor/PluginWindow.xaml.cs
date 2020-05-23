using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using Octgn.Library;
using Octgn.DataNew.Entities;
using Octgn.DataNew.FileDB;
using Octgn.Core;
using Octgn.Core.DataExtensionMethods;
using System.ComponentModel;
using System.IO;
using System.Windows.Media.Imaging;
using Octgn.DataNew;
using System.Collections.ObjectModel;
using System.Net;
using System.Drawing;
using Newtonsoft.Json.Linq;
using Newtonsoft.Json;
using System.Windows.Controls.Primitives;
using System.Drawing.Imaging;
using System.Runtime.Serialization;
using Image = System.Drawing.Image;
using System.Threading;
using MTGImageFetcher.Entities;

namespace MTGImageFetcher
{
    /// <summary>
    /// Interaction logic for PluginWindow.xaml
    /// </summary>
    /// 

    public partial class MainWindow : INotifyPropertyChanged
    {
        public Game game;
        public List<SetInfo> sets;
        public bool xl = false;
        public bool update = false;
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

        // private BackgroundWorker backgroundWorker = new BackgroundWorker();
        private CancellationTokenSource _cts;

        public MainWindow()
        {
            this.InitializeComponent();
            this.DataContext = this;
            if (game == null)
            {
                game = DbContext.Get().GameById(Guid.Parse("A6C8D2E8-7CD8-11DD-8F94-E62B56D89593")) ?? throw new Exception("MTG is not installed!");
            }

            JArray scryfallSetData;

            using (var webclient = new WebClient() { Encoding = Encoding.UTF8 })
            {
                scryfallSetData = (JsonConvert.DeserializeObject(webclient.DownloadString("https://api.scryfall.com/sets")) as JObject)["data"] as JArray;
            }

            sets = new List<SetInfo>();

            foreach (var jsonset in scryfallSetData)
            {
                var setInfo = new SetInfo();

                setInfo.Code = jsonset.Value<string>("code");
                setInfo.ParentCode = jsonset.Value<string>("parent_set_code") ?? setInfo.Code;
                setInfo.BlockCode = jsonset.Value<string>("block_code") ?? setInfo.Code;
                
                setInfo.Type = jsonset.Value<string>("set_type");
                setInfo.SearchUri = jsonset.Value<string>("search_uri");

                sets.Add(setInfo);
            }

            setList = new List<SetItem>();
            SetList.ItemsSource = setList;

            foreach (var set in game.Sets())
            {
                if (!set.Hidden && set.Cards.Count() > 0)
                {
                    // token set
                    if (set.Id.ToString() == "a584b75b-266f-4378-bed5-9ffa96cd3961")
                    {
                        var setItem = new SetItem();
                        setItem.set = set;

                        setItem.releaseDate = new DateTime(3000, 1, 1);
                        setItem.extraSets = new List<SetInfo>();
                        CountImageFiles(setItem);
                        setList.Add(setItem);
                    }
                    else
                    {

                        var setItem = new SetItem();
                        setItem.set = set;

                        var setCode = set.ShortName;

                        setItem.setData = sets.First(x => x.Code == setCode);

                        setItem.extraSets = new List<SetInfo>();

                        setItem.extraSets.AddRange(sets.Where(x => x.ParentCode == setItem.setData.Code));
                        if (setItem.setData.BlockCode != setItem.setData.Code)
                        {
                            setItem.extraSets.AddRange(sets.Where(x => x.ParentCode == setItem.setData.BlockCode));
                        }

                        setItem.releaseDate = set.ReleaseDate;
                        CountImageFiles(setItem);
                        setList.Add(setItem);
                    }
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
            UpdateImages.IsEnabled = false;
            SetList.IsEnabled = false;
            NameRadio.IsEnabled = false;
            DateRadio.IsEnabled = false;
            DownloadButton.Visibility = Visibility.Collapsed;
            DownloadAllButton.Visibility = Visibility.Collapsed;
            CancelButton.Visibility = Visibility.Visible;

            _cts = new CancellationTokenSource();
            var token = _cts.Token;

            var progressHandler = new Progress<WorkerItem>(value =>
            {
                ProgressChanged(value);
            });
            var progress = progressHandler as IProgress<WorkerItem>;

            var setProgressHandler = new Progress<int>(value =>
            {
                SetProgressBar.Value = value;
            });
            var setProgress = setProgressHandler as IProgress<int>;

            SetProgressBar.Maximum = sets.Count;
            SetProgressBar.Value = 0;
            await Task.Run(() =>
                {
                    var count = 0;
                    foreach (var set in sets)
                    {
                        CurrentSet = set.Name;
                        DownloadSet(set, progress);
                        count += 1;
                        setProgress.Report(count);
                    }
                });

            WorkerCompleted();
        }

        private void ClickSet(object sender, SelectionChangedEventArgs e)
        {
            if (e.AddedItems.Count > 0)
            {
                ProgressBar.Value = 0;
                var selectedSet = e.AddedItems[0] as SetItem;
                var card = selectedSet.set.Cards.FirstOrDefault();
                var cardImageUrl = FindLocalCardImages(selectedSet.set, card, card.Alternate).FirstOrDefault();

                BitmapImage local = cardImageUrl == null ? null : StreamToBitmapImage(UriToStream(cardImageUrl));
                LocalImage.Source = local;
                LocalDimensions.Text = local == null ? null : local.PixelWidth.ToString() + " x " + local.PixelHeight.ToString();

                var cardInfo = GetCardInfo(selectedSet, card, "");
                if (cardInfo == null)
                {
                    WebImage.Source = null;
                }
                else
                {
                    BitmapImage web = StreamToBitmapImage(UriToStream(cardInfo.NormalUrl));
                    WebImage.Source = web;
                }
            }
        }


        public CardInfo GetCardInfo(SetItem setItem, Card card, string alt)
        {
            CardInfo ret = null;

            if (setItem.set.Id.ToString() == "a584b75b-266f-4378-bed5-9ffa96cd3961")
            {
                var searchSet = sets.FirstOrDefault(x => x.Code == card.GetCardProperties(alt).FirstOrDefault(y => y.Key.Name == "Flags").Value?.ToString().ToLower());
                if (searchSet != null)
                {
                    ret = searchSet.FindCard(card, alt);
                }
            }
            else
            {
                ret = setItem.setData.FindCard(card, alt);
            }
            if (ret != null) return ret;

            foreach (var ex in setItem.extraSets)
            {
                ret = ex.FindCard(card, alt);
                if (ret != null) return ret;
            }

            return ret;
        }

        private void DownloadSet(SetItem setItem, IProgress<WorkerItem> progress)
        {
            var i = 0;
            var set = setItem.set; //TODO: remove this and use setItem
            var setSize = set.Cards.Count();

            foreach (var c in set.Cards)
            {
                i++;
                foreach (var alt in c.PropertySets)
                {
                    if (_cts.IsCancellationRequested) break;

                    var cardInfo = GetCardInfo(setItem, c, alt.Key);

                    var workerItem = new WorkerItem();
                    workerItem.set = setItem;
                    workerItem.alt = alt.Key;
                    workerItem.progress = (double)i / setSize;
                    workerItem.card = c;

                    // get local image info

                    var files = FindLocalCardImages(set, c, workerItem.alt);

                    if (cardInfo == null)
                    {
                        if (set.Id.ToString() != "a584b75b-266f-4378-bed5-9ffa96cd3961")
                            MessageBox.Show(String.Format("Cannot find scryfall data for card {0}.", c.Name));
                        progress.Report(workerItem);
                        continue;
                    }
                    workerItem.local = files.Length > 0 ? UriToStream(files.First()) : null;

                    if (workerItem.local != null && workerItem.local.Length == 0)  //sometimes an empty image file saves into the image database.  This makes sure it's not gonna break anything
                        workerItem.local = null;

                    var imageDownloadUrl = "";
                    var flipCard = false;

                    switch (cardInfo.Layout)
                    {
                        case "transform":
                            {
                                if (workerItem.alt == "transform")
                                    imageDownloadUrl = xl ? cardInfo.LargeBackUrl : cardInfo.NormalBackUrl;
                                else
                                    imageDownloadUrl = xl ? cardInfo.LargeUrl : cardInfo.NormalUrl;
                                break;
                            }
                        case "adventure":
                        case "split":
                            {
                                if (workerItem.alt == "")
                                    imageDownloadUrl = xl ? cardInfo.LargeUrl : cardInfo.NormalUrl;
                                break;
                            }
                        case "flip":
                            {
                                if (workerItem.alt == "flip")
                                    flipCard = true;
                                imageDownloadUrl = xl ? cardInfo.LargeUrl : cardInfo.NormalUrl;
                                break;
                            }
                        default:
                            {
                                imageDownloadUrl = xl ? cardInfo.LargeUrl : cardInfo.NormalUrl;
                                break;
                            }
                    }

                    // if the card has no web image
                    if (string.IsNullOrEmpty(imageDownloadUrl))
                    {
                        progress.Report(workerItem);
                        continue;
                    }

                    // check if the web image has a newer timestamp
                    var webTimestamp = Convert.ToInt32(imageDownloadUrl.Split('?')[1]);

                    if (workerItem.local != null)
                    {
                        try
                        {
                            using (var image = Image.FromStream(workerItem.local))
                            {
                                if ((image.Width > 600 && xl) || (image.Width < 500 && !xl))
                                {
                                    bool hires = (image.PropertyIdList.FirstOrDefault(x => x == 40094) == 0) ? false : Convert.ToBoolean(Encoding.Unicode.GetString(image.GetPropertyItem(40094).Value));
                                    if (hires && !update)
                                    {
                                        progress.Report(workerItem);
                                        continue;
                                    }

                                    int localTimestamp = (image.PropertyIdList.FirstOrDefault(x => x == 40092) == 0) ? 0 : Convert.ToInt32(Encoding.Unicode.GetString(image.GetPropertyItem(40092).Value));
                                    if (webTimestamp <= localTimestamp)
                                    {
                                        progress.Report(workerItem);
                                        continue;
                                    }
                                }
                            }
                        }
                        catch (ArgumentException ex)
                        {
                            // cleanly catches cases where the image or its headers can't be loaded
                        }
                    }


                    // download image

                    workerItem.web = UriToStream(imageDownloadUrl);

                    if (workerItem.web == null)
                    {
                        progress.Report(workerItem);
                        continue;
                    }

                    var garbage = Config.Instance.Paths.GraveyardPath;
                    if (!Directory.Exists(garbage)) Directory.CreateDirectory(garbage);

                    foreach (var f in files.Select(x => new FileInfo(x)))
                    {
                        f.MoveTo(Path.Combine(garbage, f.Name));
                    }

                    using (var newimg = Image.FromStream(workerItem.web))
                    {
                        if (flipCard)
                        {
                            newimg.RotateFlip(System.Drawing.RotateFlipType.Rotate180FlipNone);
                        }
                        else if (cardInfo.Layout == "planar")
                        {
                            newimg.RotateFlip(System.Drawing.RotateFlipType.Rotate90FlipNone);
                        }

                        var commentMetadata = (PropertyItem)FormatterServices.GetUninitializedObject(typeof(PropertyItem));

                        commentMetadata.Id = 40092; // this is the comments field
                        commentMetadata.Value = Encoding.Unicode.GetBytes(webTimestamp.ToString());
                        commentMetadata.Len = commentMetadata.Value.Length;
                        commentMetadata.Type = 1;

                        newimg.SetPropertyItem(commentMetadata);

                        var keywordsMetadata = (PropertyItem)FormatterServices.GetUninitializedObject(typeof(PropertyItem));

                        keywordsMetadata.Id = 40094; // this is the keywords field
                        keywordsMetadata.Value = Encoding.Unicode.GetBytes(cardInfo.HiRes.ToString());
                        keywordsMetadata.Len = keywordsMetadata.Value.Length;
                        keywordsMetadata.Type = 1;

                        newimg.SetPropertyItem(keywordsMetadata);


                        var imageUri = String.IsNullOrWhiteSpace(workerItem.alt) ? c.ImageUri : c.ImageUri + "." + workerItem.alt;
                        var newPath = Path.Combine(set.ImagePackUri, imageUri + ".jpg");
                        newimg.Save(newPath, ImageFormat.Jpeg);
                    }

                    progress.Report(workerItem);
                }
            }
        }

        public void CountImageFiles(SetItem setItem)
        {
            setItem.ImageCount = 0;
            setItem.CardCount = 0;

            foreach (var card in setItem.set.Cards)
            {
                foreach (var alt in card.PropertySets.Values)
                {
                    if (!alt.Type.Contains("split") && !alt.Type.Contains("adventure"))
                    {
                        setItem.CardCount += 1;
                        if (FindLocalCardImages(setItem.set, card, alt.Type).Count() > 0)
                        {
                            setItem.ImageCount += 1;
                        }
                    }
                }
            }
        }

        public string[] FindLocalCardImages(Set set, Card card, string alt)
        {

            var imageUri = card.ImageUri;
            if (!String.IsNullOrWhiteSpace(alt)) imageUri = imageUri + "." + alt;
            var files =
                Directory.GetFiles(set.ImagePackUri, imageUri + ".*")
                    .Where(x => System.IO.Path.GetFileNameWithoutExtension(x).Equals(imageUri, StringComparison.InvariantCultureIgnoreCase))
                    .OrderBy(x => x.Length)
                    .ToArray();
            return files;
        }

        private MemoryStream UriToStream(string uri)
        {
            MemoryStream ms = null;
            using (WebClient wc = new WebClient())
            {
                while (ms == null)
                {
                    try
                    {
                        byte[] bytes = wc.DownloadData(uri);
                        ms = new MemoryStream(bytes);
                    }
                    catch (WebException e)
                    {
                        var ret = MessageBox.Show(String.Format("{0}.  Try again?", e.Message), "Error", MessageBoxButton.YesNo);
                        if (ret != MessageBoxResult.Yes) return ms;
                    }
                }
            }
            return ms;
        }

        private BitmapImage StreamToBitmapImage(MemoryStream ms)
        {
            ms.Position = 0;
            var ret = new BitmapImage();
            ret.BeginInit();
            ret.StreamSource = ms;
            ret.CacheOption = BitmapCacheOption.OnLoad;
            ret.EndInit();
            ret.Freeze();
            return ret;
        }

        private void ProgressChanged(WorkerItem workerItem)
        {
            ProgressBar.Value = workerItem.progress;
            CurrentCard = workerItem.card.PropertySets[workerItem.alt].Name;
            if (workerItem.set != null && workerItem.local == null && workerItem.web != null)
            {
                workerItem.set.ImageCount += 1;
            }

            if (workerItem.local == null && workerItem.web == null)
            {
                return;
            }

            LocalImage.Source = null;
            WebImage.Source = null;

            if (workerItem.local != null)
            {
                BitmapImage local = StreamToBitmapImage(workerItem.local);
                LocalImage.Source = local;
                LocalDimensions.Text = local.PixelWidth.ToString() + " x " + local.PixelHeight.ToString();
            }
            if (workerItem.web != null)
            {
                BitmapImage web = StreamToBitmapImage(workerItem.web);
                WebImage.Source = web;
                if (LocalImage.Source == null)
                {
                    LocalImage.Source = web;
                }
            }
        }

        private void WorkerCompleted()
        {
            CurrentCard = "";
            CurrentSet = "";
            XLImages.IsEnabled = true;
            UpdateImages.IsEnabled = true;
            SetList.IsEnabled = true;
            NameRadio.IsEnabled = true;
            DateRadio.IsEnabled = true;
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

        private void Update_Checked(object sender, RoutedEventArgs e)
        {
            update = UpdateImages.IsChecked ?? false;
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
            setList = setList.OrderByDescending(x => x.releaseDate).ToList();
            SetList.ItemsSource = setList;
        }
    }
    

}
