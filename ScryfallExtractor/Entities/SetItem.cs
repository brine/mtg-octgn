using Octgn.DataNew.Entities;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MTGImageFetcher.Entities
{
    public partial class SetItem : INotifyPropertyChanged
    {
        public Set set;
        public DateTime releaseDate;
        public int imageCount;
        public int cardCount;

        public SetInfo setData;
        public List<SetInfo> extraSets;

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
                return cardCount;
            }
            set
            {
                if (cardCount == value) return;
                cardCount = value;
                OnPropertyChanged("CardCount");
            }
        }

        public int ImageCount
        {
            get
            {
                return imageCount;
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
