using System;
using System.Collections.Generic;
using System.Configuration;
using System.Data;
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
            }
            catch (OctgnNotInstalledException ex)
            {

            }
            base.OnStartup(e);
        }
    }
}
