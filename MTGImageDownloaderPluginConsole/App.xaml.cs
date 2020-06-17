using System;
using System.Collections.Generic;
using System.Configuration;
using System.Data;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Windows;
using Octgn.DataNew;
using Octgn.Library;
using MTGImageFetcher;

namespace MTGImageDownloaderPluginConsole
{
    /// <summary>
    /// Interaction logic for App.xaml
    /// </summary>
    public partial class App : Application
    {
        private void Application_Startup(object sender, StartupEventArgs e)
        {
            try
            {
                Config.Instance = new Config();
            }
            catch (Exception ex)
            {
                Shutdown();
            }
            var window = new PluginWindow();
            window.ShowDialog();
        }
    }
}
