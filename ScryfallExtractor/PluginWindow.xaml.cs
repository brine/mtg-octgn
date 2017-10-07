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
        public Set tokenSet;

        private BackgroundWorker backgroundWorker = new BackgroundWorker();

        public MainWindow()
        {
            this.InitializeComponent();
            if (game == null)
            {
                game = DbContext.Get().GameById(Guid.Parse("A6C8D2E8-7CD8-11DD-8F94-E62B56D89593")) ?? throw new Exception("MTG is not installed!");
            }
            
            JArray scryfallSetData;
            JArray OctgnSetData;

            using (var webclient = new WebClient() { Encoding = Encoding.UTF8 })
            {
                OctgnSetData = (JArray)JsonConvert.DeserializeObject(webclient.DownloadString("http://www.octgngames.com/forum/json.php"));
                scryfallSetData = (JsonConvert.DeserializeObject(webclient.DownloadString("https://api.scryfall.com/sets")) as JObject)["data"] as JArray;
            }

            tokenSet = game.GetSetById(new Guid("a584b75b-266f-4378-bed5-9ffa96cd3961"));

            SetList.ItemsSource = game.Sets().Where(x => !x.Hidden && x.Cards.Count() > 0 && x != tokenSet).OrderBy(x => x.Name);

            sets = new List<SetInfo>();


            foreach (var jsonset in scryfallSetData)
            {
                var setInfo = new SetInfo();
                
                setInfo.Code = jsonset.Value<string>("code");
                setInfo.ParentCode = jsonset.Value<string>("parent_set_code");
                setInfo.BlockCode = jsonset.Value<string>("block_code");

                var OctgnId = OctgnSetData.FirstOrDefault(x => x.Value<string>("octgn_code").ToLower() == setInfo.Code);
                if (OctgnId != null)
                    setInfo.Id = OctgnId.Value<string>("guid");

                setInfo.Type = jsonset.Value<string>("set_type");
                setInfo.SearchUri = jsonset.Value<string>("search_uri");
                
                sets.Add(setInfo);
            }
            
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
            XLImages.IsEnabled = false;
            SetList.IsEnabled = false;
            DownloadButton.Visibility = Visibility.Collapsed;
            CancelButton.Visibility = Visibility.Visible;
            ProgressBar.Maximum = selectedSet.Cards.Count();

            backgroundWorker.RunWorkerAsync(tokenSet);
        }
        
        private void ClickSet(object sender, SelectionChangedEventArgs e)
        {
            if (e.AddedItems.Count == 0)
            {
                selectedSet = null;
            }
            else
            {
                ProgressBar.Value = 0;
                selectedSet = e.AddedItems[0] as Set;
                var card = selectedSet.Cards.FirstOrDefault();
                var cardInfo = GetCardInfo(selectedSet, card);
                var cardImageUrl = FindLocalCardImages(selectedSet, card).FirstOrDefault();
                
                BitmapImage local = cardImageUrl == null ? null : StreamToBitmapImage(UriToStream(cardImageUrl));
                LocalImage.Source = local;
                LocalDimensions.Text = local == null ? null : local.PixelWidth.ToString() + " x " + local.PixelHeight.ToString();

                BitmapImage web = StreamToBitmapImage(UriToStream(cardInfo.NormalUrl));
                WebImage.Source = web;
            }
        }


        public CardInfo GetCardInfo(Set set, Card card)
        {
            CardInfo ret = null;

            var mainSet = sets.FirstOrDefault(x => x.Id == selectedSet.Id.ToString());
            if (mainSet == null) return null;

            ret = mainSet.FindCard(card);
            if (ret != null) return ret;

            if (set == tokenSet)
            {
                var tokenSet = sets.FirstOrDefault(x => x.ParentCode == mainSet.Code && x.Type == "token");
                if (tokenSet == null) return null;

                return tokenSet.FindCard(card);

            }

            var extraSets = sets.Where(x => x.ParentCode == mainSet.Code);
            foreach (var ex in extraSets)
            {
                ret = ex.FindCard(card);
                if (ret != null) return ret;
            }

            var baseSet = sets.FirstOrDefault(x => x.Code == mainSet.BlockCode);
            if (baseSet == null) return null;

            ret = baseSet.FindCard(card);
            if (ret != null) return ret;

            var extraBaseSets = sets.Where(x => x.ParentCode == baseSet.Code);
            foreach (var ex in extraBaseSets)
            {
                ret = ex.FindCard(card);
                if (ret != null) return ret;
            }
            
            return null;
        }

        private void DownloadSet(object sender, DoWorkEventArgs e)
        {
            var i = 0;
            var set = (e.Argument as Set);
            
            foreach (var c in set.Cards)
            {
                i++;
                foreach (var alt in c.Properties)
                {
                    var card = c.Clone();
                    card.Alternate = alt.Key;
                    if (backgroundWorker.CancellationPending) break;

                    var cardInfo = GetCardInfo(set, card);

                    var workerItem = new WorkerItem();
                    workerItem.card = card;

                    // get local image info

                    var files = FindLocalCardImages(set, card);

                    if (cardInfo == null)
                    {
                        if (set != tokenSet)
                            MessageBox.Show(String.Format("Cannot find scryfall data for card {0}.", card.Name));
                        backgroundWorker.ReportProgress(i, workerItem);
                        continue;
                    }
                    workerItem.local = files.Length > 0 ? UriToStream(files.First()) : null;

                    var imageDownloadUrl = "";
                    var flipCard = false;

                    switch (cardInfo.Layout)
                    {
                        case "transform":
                            {
                                if (card.Alternate == "transform")
                                    imageDownloadUrl = xl ? cardInfo.LargeBackUrl : cardInfo.NormalBackUrl;
                                else
                                    imageDownloadUrl = xl ? cardInfo.LargeUrl : cardInfo.NormalUrl;
                                break;
                            }
                        case "split":
                            {
                                if (card.Alternate == "")
                                    imageDownloadUrl = xl ? cardInfo.LargeUrl : cardInfo.NormalUrl;
                                break;
                            }
                        case "flip":
                            {
                                if (card.Alternate == "flip")
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
                        backgroundWorker.ReportProgress(i, workerItem);
                        continue;
                    }

                    // check if the web image has a newer timestamp
                    var webTimestamp = Convert.ToInt32(imageDownloadUrl.Split('?')[1]);

                    if (workerItem.local != null)
                    {
                        int localTimestamp;
                        using (var image = Image.FromStream(workerItem.local))
                        {
                            if (image.PropertyIdList.FirstOrDefault(x => x == 40092) == 0)
                            {
                                localTimestamp = 0;
                            }
                            else
                            {
                                localTimestamp = Convert.ToInt32(Encoding.Unicode.GetString(image.GetPropertyItem(40092).Value));
                            }
                            if (localTimestamp > 0 && ((image.Width == 672 && xl) || (image.Width == 488 && !xl)))
                            {
                                if (webTimestamp <= localTimestamp)
                                {
                                    backgroundWorker.ReportProgress(i, workerItem);
                                    continue;
                                }
                            }
                        }
                    }

                    // download image

                    var garbage = Config.Instance.Paths.GraveyardPath;
                    if (!Directory.Exists(garbage)) Directory.CreateDirectory(garbage);

                    foreach (var f in files.Select(x => new FileInfo(x)))
                    {
                        f.MoveTo(Path.Combine(garbage, f.Name));
                    }

                    var newPath = Path.Combine(set.ImagePackUri, card.GetImageUri() + ".jpg");


                    workerItem.web = UriToStream(imageDownloadUrl);

                    using (var newimg = Image.FromStream(workerItem.web))
                    {
                        if (flipCard)
                        {
                            newimg.RotateFlip(System.Drawing.RotateFlipType.Rotate180FlipNone);
                        }
                        else if (cardInfo.Layout == "Planar")
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

        public string[] FindLocalCardImages(Set set, Card card)
        {

            var imageUri = card.GetImageUri();
            var files =
                Directory.GetFiles(set.ImagePackUri, imageUri + ".*")
                    .Where(x => System.IO.Path.GetFileNameWithoutExtension(x).Equals(imageUri, StringComparison.InvariantCultureIgnoreCase))
                    .OrderBy(x => x.Length)
                    .ToArray();
            return files;
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
        

        private class WorkerItem
        {
            public Card card;
            public MemoryStream local;
            public MemoryStream web;
        }
        public class SetInfo
        {
            public string SearchUri;
            public bool? IsHiRes;
            public string Id;
            public string Type;
            public string Code;
            public string ParentCode;
            public string BlockCode;

            public List<CardInfo> Cards;

            public CardInfo FindCard(Card card)
            {
                if (Cards == null)
                    Cards = new List<CardInfo>();

                CardInfo ret = null;
                
                while (ret == null)
                {
                    if (Type == "token")
                    {
                        var props = card.Properties[card.Alternate].Properties;
                        if (props.First(x => x.Key.Name == "Flags").Value.ToString().ToLower() != Code)
                            return null;

                        ret = Cards.FirstOrDefault(x => x.Number == props.First(y => y.Key.Name == "Number").Value.ToString());
                    }
                    else
                        ret = Cards.FirstOrDefault(x => x.Id == card.Id.ToString() || x.MultiverseId == card.Properties[""].Properties.First(y => y.Key.Name == "MultiverseId").Value.ToString());
                    if (ret == null)
                    {
                        if (SearchUri == null) break;

                        using (var webclient = new WebClient() { Encoding = Encoding.UTF8 })
                        {
                            var jsonsetdata = (JObject)JsonConvert.DeserializeObject(webclient.DownloadString(SearchUri));
                            foreach (var jsoncarddata in jsonsetdata["data"])
                            {
                                CardInfo cardInfo = new CardInfo();
                                cardInfo.Layout = jsoncarddata.Value<string>("layout");
                                if (jsoncarddata["card_faces"] == null)
                                {
                                    cardInfo.NormalUrl = jsoncarddata["image_uris"].Value<string>("normal");
                                    cardInfo.LargeUrl = jsoncarddata["image_uris"].Value<string>("large");
                                }
                                else
                                {
                                    cardInfo.NormalUrl = jsoncarddata["card_faces"][0]["image_uris"].Value<string>("normal");
                                    cardInfo.LargeUrl = jsoncarddata["card_faces"][0]["image_uris"].Value<string>("large");
                                    cardInfo.NormalBackUrl = jsoncarddata["card_faces"][1]["image_uris"].Value<string>("normal");
                                    cardInfo.LargeBackUrl = jsoncarddata["card_faces"][1]["image_uris"].Value<string>("large");
                                }
                                cardInfo.Id = jsoncarddata.Value<string>("id");
                                cardInfo.MultiverseId = jsoncarddata.Value<string>("multiverse_id");
                                cardInfo.Number = jsoncarddata.Value<string>("collector_number");
                                Cards.Add(cardInfo);
                            }
                            SearchUri = (jsonsetdata.Value<bool>("has_more") == true) ? jsonsetdata.Value<string>("next_page") : null;
                        }
                    }
                }
                
                return ret;
            }
        }

        public class CardInfo
        {
            public string NormalUrl;
            public string LargeUrl;
            public string NormalBackUrl;
            public string LargeBackUrl;
            public string Layout;
            public string Id;
            public string MultiverseId;
            public string Number;
            public string Alt;
            public string Name;
        }
        
    }
}
