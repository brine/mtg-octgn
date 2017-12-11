using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using Octgn.DataNew.Entities;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using System.Windows;

namespace ScryfallExtractor.Entities
{
    public class SetInfo
    {
        public string SearchUri;
        public bool? IsHiRes;
        public string Type;
        public string Code;
        public string ParentCode;
        public string BlockCode;

        public List<CardInfo> Cards;

        public CardInfo FindCard(Card card, string alt)
        {
            if (Cards == null)
                Cards = new List<CardInfo>();

            CardInfo ret = null;

            while (ret == null)
            {

                if (card.SetId.ToString() == "a584b75b-266f-4378-bed5-9ffa96cd3961")
                {
                    var props = card.Properties[alt].Properties;
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
                            if (cardInfo.Layout == "transform")
                            {
                                cardInfo.NormalUrl = jsoncarddata["card_faces"][0]["image_uris"].Value<string>("normal");
                                cardInfo.LargeUrl = jsoncarddata["card_faces"][0]["image_uris"].Value<string>("large");
                                cardInfo.NormalBackUrl = jsoncarddata["card_faces"][1]["image_uris"].Value<string>("normal");
                                cardInfo.LargeBackUrl = jsoncarddata["card_faces"][1]["image_uris"].Value<string>("large");
                            }
                            else
                            {
                                if (jsoncarddata["image_uris"] != null)
                                {
                                    cardInfo.NormalUrl = jsoncarddata["image_uris"].Value<string>("normal");
                                    cardInfo.LargeUrl = jsoncarddata["image_uris"].Value<string>("large");
                                }
                            }
                            cardInfo.HiRes = jsoncarddata.Value<string>("highres_image");
                            cardInfo.Id = jsoncarddata.Value<string>("id");
                            var multiverseIds = (jsoncarddata["multiverse_ids"] == null) ? new List<string>() : jsoncarddata["multiverse_ids"].Select(x => x.ToString());
                            cardInfo.MultiverseId = (jsoncarddata["multiverse_ids"].FirstOrDefault() == null) ? null : jsoncarddata["multiverse_ids"].First().ToString();
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
}
