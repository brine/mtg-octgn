using Octgn.DataNew.Entities;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MTGImageFetcher.Entities
{
    public class WorkerItem
    {
        public Card card;
        public string alt;
        public SetItem set;
        public MemoryStream local;
        public MemoryStream web;
        public double progress;
    }
}
