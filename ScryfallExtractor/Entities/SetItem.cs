using Octgn.DataNew.Entities;
using System;
using System.ComponentModel;
using System.Linq;

namespace MTGImageFetcher.Entities
{
    public class SetItem : INotifyPropertyChanged
    {
        public Set set;
        public int? imageCount;
        public int? cardCount;

        public string Code
        {
            get
            {
                return set.ShortName;
            }
        }

        public DateTime ReleaseDate
        {
            get
            {
                return set.ReleaseDate;
            }
        }
        public string Name
        {
            get
            {
                return set.Name;
            }
        }

        public int CardCount
        {
            get
            {
                if (cardCount == null)
                {
                    cardCount = set.Cards.SelectMany(x => x.PropertySets).Count(x => !x.Key.Contains("split") && !x.Key.Contains("adventure"));
                }
                return (int)cardCount;
            }
        }

        public int ImageCount
        {
            get
            {
                if (imageCount == null)
                {
                    var ret = 0;
                    foreach (var card in set.Cards)
                    {
                        ret += card.PropertySets
                            .Where(x => !x.Key.Contains("split") && !x.Key.Contains("adventure"))
                            .Count(x => PluginWindow.FindLocalCardImages(set, card, x.Key).Any());
                    }
                    imageCount = ret;
                }
                return (int)imageCount;
            }
            set
            {
                if (imageCount == value) return;
                imageCount = value;
                OnPropertyChanged("ImageCount");
            }
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
    }
}
