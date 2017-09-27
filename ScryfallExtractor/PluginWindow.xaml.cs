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
        public SetInfo selectedSet;

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
            backgroundWorker.DoWork += DownloadSet;
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
            ProgressBar.Maximum = selectedSet.Set.Cards.Count();

            backgroundWorker.RunWorkerAsync(selectedSet);
        }

        private void ClickSet(object sender, SelectionChangedEventArgs e)
        {
            if (e.AddedItems.Count == 0)
            {
                selectedSet = null;
            }
            else
            {
                selectedSet = e.AddedItems[0] as SetInfo;
                var card = selectedSet.Set.Cards.FirstOrDefault();
                var cardInfo = getCardInfo(selectedSet, card);
                var cardImageUrl = FindLocalCardImages(card).FirstOrDefault();
                
                BitmapImage local = cardImageUrl == null ? null : StreamToBitmapImage(UriToStream(cardImageUrl));
                LocalImage.Source = local;
                LocalDimensions.Text = local == null ? null : local.PixelWidth.ToString() + " x " + local.PixelHeight.ToString();

                BitmapImage web = StreamToBitmapImage(UriToStream(cardInfo.normalUrl));
                WebImage.Source = web;
            }
        }
        
        public string[] FindLocalCardImages(Card card)
        {

            var imageUri = card.GetImageUri();
            var files =
                Directory.GetFiles(card.GetSet().ImagePackUri, imageUri + ".*")
                    .Where(x => System.IO.Path.GetFileNameWithoutExtension(x).Equals(imageUri, StringComparison.InvariantCultureIgnoreCase))
                    .OrderBy(x => x.Length)
                    .ToArray();
            return files;
        }

        public CardInfo getCardInfo(SetInfo set, Card card)
        {
            if (set.Cards == null) // cards have not yet been initialized
                set.Cards = new List<CardInfo>();

            var ret = set.Cards.FirstOrDefault(x => x.id == card.Id.ToString() || x.multiverseId == card.Properties[""].Properties.FirstOrDefault(y => y.Key.Name == "MultiverseId").Value.ToString());

            if (ret == null)
            {
                using (var webclient = new WebClient() { Encoding = Encoding.UTF8 })
                {
                    while (set.SearchUri != null && ret == null)
                    {
                        var jsonsetdata = (JObject)JsonConvert.DeserializeObject(webclient.DownloadString(set.SearchUri));
                        foreach (var jsoncarddata in jsonsetdata["data"])
                        {
                            CardInfo cardInfo = new CardInfo();
                            cardInfo.layout = jsoncarddata.Value<string>("layout");
                            if (jsoncarddata["card_faces"] == null)
                            {
                                cardInfo.normalUrl = jsoncarddata["image_uris"].Value<string>("normal");
                                cardInfo.largeUrl = jsoncarddata["image_uris"].Value<string>("large");
                            }
                            else
                            {

                                cardInfo.normalUrl = jsoncarddata["card_faces"][0]["image_uris"].Value<string>("normal");
                                cardInfo.largeUrl = jsoncarddata["card_faces"][0]["image_uris"].Value<string>("large");
                                cardInfo.normalBackUrl = jsoncarddata["card_faces"][1]["image_uris"].Value<string>("normal");
                                cardInfo.largeBackUrl = jsoncarddata["card_faces"][1]["image_uris"].Value<string>("large");
                            }
                            cardInfo.isHiRes = jsoncarddata.Value<bool>("highres_image");
                            cardInfo.id = jsoncarddata.Value<string>("id");
                            cardInfo.multiverseId = jsoncarddata.Value<string>("multiverse_id");
                            set.Cards.Add(cardInfo);
                        }

                        set.SearchUri = (jsonsetdata.Value<bool>("has_more") == true) ? jsonsetdata.Value<string>("next_page") : null;

                        ret = set.Cards.FirstOrDefault(x => x.id == card.Id.ToString() || x.multiverseId == card.Properties[""].Properties.FirstOrDefault(y => y.Key.Name == "MultiverseId").Value.ToString());
                    }
                }
            }

            return ret;
        }


        private void DownloadSet(object sender, DoWorkEventArgs e)
        {
            var i = 0;
            var set = (e.Argument as SetInfo);
            
            foreach (var card in set.Set.Cards)
            {
                i++;
                foreach (var alt in card.Properties)
                {
                    if (backgroundWorker.CancellationPending) break;

                    card.Alternate = alt.Key;
                    
                    var workerItem = new WorkerItem();
                    workerItem.card = card;

                    // get local image info
                    
                    var files = FindLocalCardImages(card);

                    var cardInfo = getCardInfo(set, card);
                    if (cardInfo == null)
                    {
                        MessageBox.Show(String.Format("Cannot find scryfall data for card {0}.", card.Name));
                        backgroundWorker.ReportProgress(i, workerItem);
                        continue;
                    }

                    workerItem.local = files.Length > 0 ? UriToStream(files.First()) : null;
                    
                    // don't overwrite with low res images unless replace is selected
                    if (replace == false && cardInfo.isHiRes == false && workerItem.local != null)
                    {
                        backgroundWorker.ReportProgress(i, workerItem);
                        continue;
                    }

                    var imageDownloadUrl = "";
                    var flipCard = false;

                    switch (cardInfo.layout)
                    {
                        case "transform":
                            {
                                if (card.Alternate == "transform")
                                    imageDownloadUrl = xl ? cardInfo.largeBackUrl : cardInfo.normalBackUrl;
                                else
                                    imageDownloadUrl = xl ? cardInfo.largeUrl : cardInfo.normalUrl;
                                break;
                            }
                        case "split":
                            {
                                if (card.Alternate == "")
                                    imageDownloadUrl = xl ? cardInfo.largeUrl : cardInfo.normalUrl;
                                break;
                            }
                        case "flip":
                            {
                                if (card.Alternate == "flip")
                                    flipCard = true;
                                imageDownloadUrl = xl ? cardInfo.largeUrl : cardInfo.normalUrl; ;
                                break;
                            }
                        default:
                            {
                                imageDownloadUrl = xl ? cardInfo.largeUrl : cardInfo.normalUrl;
                                break;
                            }
                    }

                    // if the card has no web image 

                    if (string.IsNullOrEmpty(imageDownloadUrl))
                    {
                        backgroundWorker.ReportProgress(i, workerItem);
                        continue;
                    }

                    // check if the web image has been updated

                    var webTimestamp = Convert.ToInt32(imageDownloadUrl.Split('?')[1]);

                    if (files.Length > 0)
                    {
                        int localTimestamp;
                        using (System.Drawing.Image image = System.Drawing.Image.FromFile(files.First()))
                            if (image.PropertyIdList.FirstOrDefault(x => x == 40092) == 0)
                            {
                                localTimestamp = 0;
                            }
                            else
                            {
                                localTimestamp = Convert.ToInt32(Encoding.Unicode.GetString(image.GetPropertyItem(40092).Value));
                            }

                        if (webTimestamp <= localTimestamp)
                        {
                            backgroundWorker.ReportProgress(i, workerItem);
                            continue;
                        }
                    }

                    // download image

                    var garbage = Config.Instance.Paths.GraveyardPath;
                    if (!Directory.Exists(garbage)) Directory.CreateDirectory(garbage);

                    foreach (var f in files.Select(x => new FileInfo(x)))
                    {
                        f.MoveTo(Path.Combine(garbage, f.Name));
                    }

                    var newPath = Path.Combine(set.Set.ImagePackUri, card.GetImageUri() + ".jpg");

                    MemoryStream imagestream = UriToStream(imageDownloadUrl);
                    
                    workerItem.web = imagestream;

                    using (var newimg = StreamToImage(imagestream))
                    {
                        if (flipCard)
                        {
                            newimg.RotateFlip(System.Drawing.RotateFlipType.Rotate180FlipNone);
                        }
                        else if (card.Size.Name == "Plane")
                        {
                            newimg.RotateFlip(System.Drawing.RotateFlipType.Rotate90FlipNone);
                        }

                        var commentMetadata = (PropertyItem)FormatterServices.GetUninitializedObject(typeof(PropertyItem));
                        
                        commentMetadata.Id = 40092; // this is the comments field
                        commentMetadata.Value = Encoding.Unicode.GetBytes(webTimestamp.ToString());
                        commentMetadata.Len = commentMetadata.Value.Length;
                        commentMetadata.Type = 1;

                        newimg.SetPropertyItem(commentMetadata);
                        newimg.Save(newPath, ImageFormat.Jpeg);
                    }

                    backgroundWorker.ReportProgress(i, workerItem);
                }
            }
        }

        private MemoryStream UriToStream(string uri)
        {
            MemoryStream ms;
            using (WebClient wc = new WebClient())
            {
                byte[] bytes = wc.DownloadData(uri);
                ms = new MemoryStream(bytes);
            }
            return ms;
        }

        private System.Drawing.Image StreamToImage(MemoryStream ms)
        {
            return System.Drawing.Image.FromStream(ms);
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

        private void ProgressChanged(object sender, ProgressChangedEventArgs e)
        {
            ProgressBar.Value = e.ProgressPercentage;
            WorkerItem workerItem = e.UserState as WorkerItem;
            CurrentCard.Text = workerItem.card.Name;
            LocalImage.Source = null;
            if (workerItem.local != null)
            {
                BitmapImage local = StreamToBitmapImage(workerItem.local);
                LocalImage.Source = local;
                LocalDimensions.Text = local.PixelWidth.ToString() + " x " + local.PixelHeight.ToString();
            }
            WebImage.Source = null;
            if (workerItem.web != null)
            {
                BitmapImage web = StreamToBitmapImage(workerItem.web);
                WebImage.Source = web;
            }
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

        private void XLImages_Checked(object sender, RoutedEventArgs e)
        {
            xl = XLImages.IsChecked ?? false;
        }

        private void ReplaceImages_Checked(object sender, RoutedEventArgs e)
        {
            replace = ReplaceImages.IsChecked ?? false;
        }

        private class WorkerItem
        {
            public Card card;
            public MemoryStream local;
            public MemoryStream web;
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

            public string Name => Set.Name;
        }

        public class CardInfo
        {
            public string normalUrl;
            public string largeUrl;
            public string normalBackUrl;
            public string largeBackUrl;
            public string layout;
            public string id;
            public string multiverseId;
            public bool isHiRes;
        }
        
    }
}
