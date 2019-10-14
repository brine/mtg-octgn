using System;
using System.Collections.Generic;
using System.Configuration;
using System.Data;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Windows;
using Octgn.Library;

namespace MTGImageDownloaderPluginConsole
{
    /// <summary>
    /// Interaction logic for App.xaml
    /// </summary>
    public partial class App : Application
    {

        protected override void OnStartup(StartupEventArgs e)
        {
            try
            {
                Config.Instance = new Config();
                Config.Instance.ImageDirectory = Path.Combine(Config.Instance.DataDirectory, "ImageDatabase");
            }
            catch (Exception ex)
            {

            }
            base.OnStartup(e);
        }
    }
}
