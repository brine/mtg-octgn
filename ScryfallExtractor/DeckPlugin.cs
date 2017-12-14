
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

        public void OnLoad(GameManager games)
        {
            // I'm showing a message box, but don't do this, unless it's for updates or something...but don't do it every time as it pisses people off.
        }

        public Guid Id
        {
            get
            {
                // All plugins are required to have a unique GUID
                // http://www.guidgenerator.com/online-guid-generator.aspx
                return Guid.Parse("89cd022c-69b2-411d-bd6a-63fc8465ad7f");
            }
        }

        public string Name
        {
            get
            {
                // Display name of the plugin.
                return "MTG Plugin";
            }
        }

        public Version Version
        {
            get
            {
                // Version of the plugin.
                // This code will pull the version from the assembly.
                return Assembly.GetCallingAssembly().GetName().Version;
            }
        }

        public Version RequiredByOctgnVersion
        {
            get
            {
                // Don't allow this plugin to be used in any version less than 3.0.12.58
                return Version.Parse("3.1.0.0");
            }
        }
    }

    public class PluginMenuItem : IPluginMenuItem
    {
        public string Name
        {
            get
            {
                return "MTG Image Downloader";
            }
        }

        /// <summary>
        /// This happens when the menu item is clicked.
        /// </summary>
        /// <param name="con"></param>
        /// 

        public void OnClick(IDeckBuilderPluginController con)
        {

            if (con.GetLoadedGame() == null || con.GetLoadedGame().Id.ToString() != "a6c8d2e8-7cd8-11dd-8f94-e62b56d89593")
            {
                MessageBox.Show("Can only use this plugin for Magic the Gathering");
                return;
            }

            MainWindow window = new MainWindow()
            {
                game = con.GetLoadedGame()
            };
            window.ShowDialog();
        }
    }
}
