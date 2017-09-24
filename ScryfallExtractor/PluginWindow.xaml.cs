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
using Newtonsoft.Json.Linq;
using Newtonsoft.Json;
using System.Windows.Controls.Primitives;

namespace ScryfallExtractor
{
    /// <summary>
    /// Interaction logic for PluginWindow.xaml
    /// </summary>
    /// 
    
    public partial class MainWindow : Window
    {
        public Game game;
        public List<SetInfo> sets;
        public bool xl = false;
        public bool replace = false;
        public Set selectedSet;

        private BackgroundWorker backgroundWorker = new BackgroundWorker();

        public MainWindow()
        {
            this.InitializeComponent();
            if (game == null)
            {
                game = DbContext.Get().GameById(Guid.Parse("A6C8D2E8-7CD8-11DD-8F94-E62B56D89593")) ?? throw new Exception("MTG is not installed!");
            }
            
            JArray octgnSetData;
            JArray scryfallSetData;

            using (var webclient = new WebClient() { Encoding = Encoding.UTF8 })
            {
                octgnSetData = (JArray)JsonConvert.DeserializeObject(webclient.DownloadString("http://www.octgngames.com/forum/json.php"));
                scryfallSetData = (JsonConvert.DeserializeObject(webclient.DownloadString("https://api.scryfall.com/sets")) as JObject)["data"] as JArray;
            }

            sets = new List<SetInfo>();

            foreach (var set in game.Sets().OrderBy(x => x.Name))
            {
                if (!set.Hidden && set.Cards.Count() > 0)
                {
                    var setInfo = new SetInfo();
                    setInfo.Set = set;
                    var jsonset = octgnSetData.FirstOrDefault(x => x.Value<string>("guid") == set.Id.ToString());
                    if (jsonset == null) continue;
                    setInfo.Code = jsonset.Value<string>("octgn_code");

                    var scryfallset = scryfallSetData.FirstOrDefault(x => x.Value<string>("code") == setInfo.Code.ToLower());
                    if (scryfallset == null)
                        continue;
                    setInfo.SearchUri = scryfallset.Value<string>("search_uri");
                    var scryfalltokens = scryfallSetData.FirstOrDefault(x => x.Value<string>("parent_set_code") == setInfo.Code.ToLower() && x.Value<string>("set_type") == "token");
                    if (scryfalltokens != null)
                       setInfo.TokenUri = scryfalltokens.Value<string>("search_uri");


                    sets.Add(setInfo);
                }
            }

            SetList.ItemsSource = sets;


            this.Closing += CancelWorkers;
            backgroundWorker.WorkerReportsProgress = true;
            backgroundWorker.WorkerSupportsCancellation = true;
            backgroundWorker.ProgressChanged += ProgressChanged;
            backgroundWorker.RunWorkerCompleted += BackgroundWorker_RunWorkerCompleted;
        }
        
        private void Generate(object sender, RoutedEventArgs e)
        {
            if (backgroundWorker.IsBusy)
            {
                return;
            }

            if (selectedSet == null) return;
            ReplaceImages.IsEnabled = false;
            XLImages.IsEnabled = false;
            SetList.IsEnabled = false;
            DownloadButton.Visibility = Visibility.Collapsed;
            CancelButton.Visibility = Visibility.Visible;
            ProgressBar.Maximum = selectedSet.Cards.Count();

            backgroundWorker.DoWork += DownloadSet;
            backgroundWorker.RunWorkerAsync(true);
        }

        public class SetInfo
        {
            public List<CardInfo> Cards;
            public string SearchUri;
            public string TokenUri;
            public List<CardInfo> Tokens;
            public bool? IsHiRes;
            public string Code;
            public Set Set;

            public string Name
            {
                get
                {
                    return Set.Name;
                }
            }
            
        }

        public class CardInfo
        {
            public string NormalUrl;
            public string LargeUrl;
            public string Layout;

        }

        public void GetCardInfo()
        {

        }

        private void ClickSet(object sender, SelectionChangedEventArgs e)
        {
            if (e.AddedItems.Count == 0)
            {
                selectedSet = null;
            }
            else
            {
                Set set = e.AddedItems[0] as Set;

            }
        }

        private void DownloadSet(object sender, DoWorkEventArgs e)
        {
            var i = 0;
            
            var cards = new List<Card>();

            if ((bool)e.Argument)
                cards.AddRange(selectedSet.Cards);
            else
                cards.Add(selectedSet.Cards.First(x => x.Properties.Count == 1));

            foreach (var c in cards)
            {
                i++;
                foreach (var alt in c.Properties)
                {
                    if (alt.Key != "")
                    {

                    }
                    var card = c.Clone();
                    card.Alternate = alt.Key;
                    if (backgroundWorker.CancellationPending) break;


                    var workerItem = new WorkerItem();
                    workerItem.card = card;

                    // get local image info

                    var imageUri = card.GetImageUri();
                    var files =
                        Directory.GetFiles(selectedSet.ImagePackUri, imageUri + ".*")
                            .Where(x => System.IO.Path.GetFileNameWithoutExtension(x).Equals(imageUri, StringComparison.InvariantCultureIgnoreCase))
                            .OrderBy(x => x.Length)
                            .ToArray();

                    string Id;

                    if (selectedSet.Name == "Tokens")
                    {
                        Id = card.Properties[card.Alternate].Properties.First(x => x.Key.Name == "Flags").Value.ToString().ToLower() + "/" + card.Properties[card.Alternate].Properties.First(x => x.Key.Name == "Number").Value.ToString();
                    }
                    else
                        Id = card.Properties[""].Properties.First(x => x.Key.Name == "MultiverseId").Value.ToString();
                    if (string.IsNullOrEmpty(Id.ToString()) || Id.Contains("?"))
                    {
                        //TOOD: handle cards that are missing their multiverseIds
                        backgroundWorker.ReportProgress(i, workerItem);
                        continue;
                    }

                    // get card's json data from web

                    var webclient = new WebClient();
                    webclient.Encoding = Encoding.UTF8;

                    JObject jsondata = new JObject();
                    try
                    {
                        jsondata = (JObject)JsonConvert.DeserializeObject(webclient.DownloadString("https://api.scryfall.com/cards/" + Id));
                    }
                    catch
                    {
                        if (files.Count() > 0)
                            workerItem.local = new Uri(files.First());
                        backgroundWorker.ReportProgress(i, workerItem);
                        MessageBox.Show(String.Format("Cannot find image for card {0} with multiverseId {1}.", card.Name, Id));
                        continue;
                    }

                    if (!replace && !jsondata.Value<bool>("highres_image") && files.Length > 0 && (bool)e.Argument)
                    {
                        workerItem.local = new Uri(files.First());
                        backgroundWorker.ReportProgress(i, workerItem);
                        continue;
                    }

                    var imageDownloadUrl = "";
                    var flipCard = false;

                    switch (jsondata.Value<string>("layout"))
                    {
                        case "transform":
                            {
                                if (alt.Key == "transform")
                                    imageDownloadUrl = jsondata["card_faces"][1]["image_uris"][xl ? "large" : "normal"].ToString();
                                else
                                    imageDownloadUrl = jsondata["card_faces"][0]["image_uris"][xl ? "large" : "normal"].ToString();
                                break;
                            }
                        case "split":
                            {
                                if (alt.Key == "")
                                    imageDownloadUrl = jsondata["image_uris"][xl ? "large" : "normal"].ToString();
                                break;
                            }
                        case "flip":
                            {
                                if (alt.Key == "flip")
                                    flipCard = true;
                                imageDownloadUrl = jsondata["image_uris"][xl ? "large" : "normal"].ToString();
                                break;
                            }
                        default:
                            {
                                imageDownloadUrl = jsondata["image_uris"][xl ? "large" : "normal"].ToString();
                                break;
                            }
                    }

                    if (string.IsNullOrEmpty(imageDownloadUrl))
                    {
                        backgroundWorker.ReportProgress(i, workerItem);
                        continue;
                    }

                    if (!(bool)e.Argument)
                    {
                        workerItem.local = (files.Length == 0) ? null : new Uri(files.First());
                        workerItem.web = new Uri(imageDownloadUrl);
                        backgroundWorker.ReportProgress(i, workerItem);
                        continue;
                    }

                    // download image

                    var garbage = Config.Instance.Paths.GraveyardPath;
                    if (!Directory.Exists(garbage)) Directory.CreateDirectory(garbage);

                    foreach (var f in files.Select(x => new FileInfo(x)))
                    {
                        f.MoveTo(Path.Combine(garbage, f.Name));
                        if (workerItem.local == null)
                        {
                            workerItem.local = new Uri(f.FullName);
                        }
                    }

                    var newPath = Path.Combine(selectedSet.ImagePackUri, imageUri + ".jpg");

                    webclient.DownloadFile(new Uri(imageDownloadUrl), newPath);

                    if (flipCard)
                    {
                        using (var newimg = System.Drawing.Image.FromFile(newPath))
                        {
                            newimg.RotateFlip(System.Drawing.RotateFlipType.Rotate180FlipNone);
                            newimg.Save(newPath);
                        }
                    }
                    else if (card.Size.Name == "Plane")
                    {
                        using (var newimg = System.Drawing.Image.FromFile(newPath))
                        {
                            newimg.RotateFlip(System.Drawing.RotateFlipType.Rotate90FlipNone);
                            newimg.Save(newPath);
                        }
                    }

                    workerItem.web = new Uri(newPath);

                    backgroundWorker.ReportProgress(i, workerItem);
                }
            }
        }

        private void ProgressChanged(object sender, ProgressChangedEventArgs e)
        {
            ProgressBar.Value = e.ProgressPercentage;
            WorkerItem workerItem = e.UserState as WorkerItem;
            CurrentCard.Text = workerItem.card.Name;
            LocalImage.Source = null;
            if (workerItem.local != null)
            {
                BitmapImage local = LoadImage(workerItem.local);
                LocalImage.Source = local;
                LocalDimensions.Text = local.PixelWidth.ToString() + " x " + local.PixelHeight.ToString();
            }
            WebImage.Source = null;
            if (workerItem.web != null)
            {
                BitmapImage web = LoadImage(workerItem.web);
                WebImage.Source = web;
            }
        }

        private BitmapImage LoadImage(Uri uri)
        {
            var ret = new BitmapImage();
            ret.BeginInit();
            ret.CacheOption = BitmapCacheOption.OnLoad;
            ret.UriSource = uri;
            ret.EndInit();
            return ret;
        }

        private void BackgroundWorker_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {
            CurrentCard.Text = "DONE";
            ReplaceImages.IsEnabled = true;
            XLImages.IsEnabled = true;
            SetList.IsEnabled = true;
            DownloadButton.Visibility = Visibility.Visible;
            CancelButton.Visibility = Visibility.Collapsed;
        }

        private void CancelWorkers(object sender, EventArgs e)
        {
            if (backgroundWorker.IsBusy)
            {
                CurrentCard.Text = "Cancel";
                backgroundWorker.CancelAsync();
            }
        }

        private void SetList_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (e.AddedItems.Count == 0)
            {
                selectedSet = null;
            }
            else
            {
                Set set = e.AddedItems[0] as Set;
                selectedSet = set;
                ProgressBar.Maximum = 1;
                ReplaceImages.IsEnabled = false;
                XLImages.IsEnabled = false;
                SetList.IsEnabled = false;
                DownloadButton.Visibility = Visibility.Collapsed;
                CancelButton.Visibility = Visibility.Visible;
                backgroundWorker.RunWorkerAsync(false);
            }
        }

        private class WorkerItem
        {
            public Card card;
            public Uri local;
            public Uri web;
        }

        private void XLImages_Checked(object sender, RoutedEventArgs e)
        {
            xl = XLImages.IsChecked ?? false;
        }

        private void ReplaceImages_Checked(object sender, RoutedEventArgs e)
        {
            replace = ReplaceImages.IsChecked ?? false;
        }
        
    }
}
