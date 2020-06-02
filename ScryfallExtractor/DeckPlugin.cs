
using System;
using System.Collections.Generic;
using System.Reflection;
using System.Windows;
using Octgn.Core.DataExtensionMethods;
using Octgn.Core.DataManagers;
using Octgn.Core.Plugin;
using System.Net;
using System.Linq;

namespace MTGImageFetcher
{

    public class MTGImageDownloader : IDeckBuilderPlugin
    {
        public IEnumerable<IPluginMenuItem> MenuItems
        {
            get
            {
                // Add your menu items here.
                return new List<IPluginMenuItem> { new PluginMenuItem() };
            }
        }

        public void OnLoad(GameManager games) { }

        public Guid Id => Guid.Parse("89cd022c-69b2-411d-bd6a-63fc8465ad7f");

        public string Name => "Magic: The Gathering Image Downloader Plugin";

        public Version Version => Version.Parse("5.0.0.0");

        public Version RequiredByOctgnVersion => Version.Parse("3.1.0.0");
    }

    public class PluginMenuItem : IPluginMenuItem
    {
        public string Name => "Magic: The Gathering Image Downloader";

        public void OnClick(IDeckBuilderPluginController con)
        {
            PluginWindow window = new PluginWindow();
            if (window.game != null)
                window.ShowDialog();
        }
    }
}
