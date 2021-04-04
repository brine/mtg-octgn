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
using log4net;
using System.Reflection;

namespace MTGImageDownloaderPluginConsole
{
    /// <summary>
    /// Interaction logic for App.xaml
    /// </summary>
    public partial class App : Application
    {
        private static ILog Log = LogManager.GetLogger(MethodBase.GetCurrentMethod().DeclaringType);
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
            var game = DbContext.Get().GameById(Guid.Parse("A6C8D2E8-7CD8-11DD-8F94-E62B56D89593")) ?? throw new Exception("MTG is not installed!");
            var window = new PluginWindow(game);
            window.ShowDialog();
        }
    }
}
