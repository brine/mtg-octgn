using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Documents;
using System.Xml;
using System.Xml.Linq;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace Jumpstart_Compiler
{
    class Program
    {
        static void Main(string[] args)
        {
            var decksPath = new DirectoryInfo(args[0]);

            var decks = new Dictionary<string, List<Card>>();


            foreach (var file in decksPath.GetFiles())
            {
                if (file.Extension == ".o8d")
                {
                    var name = Path.GetFileNameWithoutExtension(file.FullName);
                    var cards = new List<Card>();

                    XDocument doc = XDocument.Load(file.FullName);
                    foreach (XElement xmlCard in doc.Element("deck").Element("section").Elements("card"))
                    {
                        var card = new Card()
                        {
                            count = int.Parse(xmlCard.Attribute("qty").Value),
                            id = xmlCard.Attribute("id").Value,
                        };
                        cards.Add(card);
                    }
                    decks.Add(name, cards);
                }
            }

            var jsonData = JsonConvert.SerializeObject(decks, Newtonsoft.Json.Formatting.Indented);
            File.WriteAllText(Path.Combine(decksPath.FullName, "jumpstart.py"), jsonData);

        }
    }

    public class Deck
    {
        public string Name;
        public List<Card> Cards;

        public Deck()
        {
            Cards = new List<Card>();
        }
    }

    public class Card
    {
        public string id;
        public int count;
    }
}
