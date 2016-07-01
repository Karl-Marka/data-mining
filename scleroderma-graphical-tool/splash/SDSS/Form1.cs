using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace SDSS
{
    using System.Diagnostics;
    using System;
    using System.IO;
    public partial class Splash : Form
    {
        public Splash()
        {
            InitializeComponent();
        }

        //Use timer class

        Timer tmr;

        private void Splash_Shown(object sender, EventArgs e)

        {
            var path = @".\bin\SDSS_GUI.exe";
            Process.Start(path);

            tmr = new Timer();
            //set time interval 10 sec
            tmr.Interval = 10000;
            //starts the timer
            tmr.Start();
            tmr.Tick += tmr_Tick;

        }

        void tmr_Tick(object sender, EventArgs e)

        {

            //after 10 sec stop the timer
            tmr.Stop();
            //exit
            Application.Exit();

        }

    }
}
