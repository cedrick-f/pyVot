#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##This file is part of PyVot
#############################################################################
#############################################################################
##                                                                         ##
##                                  PyVot                                  ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2006-2009 Cédrick FAURY

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
    
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


import wx
import Icones
import sys, os, getpass

##import psyco
##psyco.log()
##psyco.full()
import globdef
from globdef import *


#import sys, os, time, traceback, types


import FenPrincipale
#import wx.aui
#import wx.html

#import images

# For debugging
##wx.Trap();
##print "wx.VERSION_STRING = %s (%s)" % (wx.VERSION_STRING, wx.USE_UNICODE and 'unicode' or 'ansi')
##print "pid:", os.getpid()
##raw_input("Press Enter...")


#---------------------------------------------------------------------------
#---------------------------------------------------------------------------
class MySplashScreen(wx.SplashScreen):
    def __init__(self):
        bmp = Icones.getLogoSplashBitmap()
        wx.SplashScreen.__init__(self, bmp,
                                 wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT,
                                 5000, None, -1,
                                 style = wx.BORDER_NONE|wx.FRAME_NO_TASKBAR)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.fc = wx.FutureCall(2000, self.ShowMain)

    def OnClose(self, evt):
        # Make sure the default handler runs too so this window gets
        # destroyed
        evt.Skip()
        self.Hide()
        
        # if the timer is still running then go ahead and show the
        # main frame now
        if self.fc.IsRunning():
            self.fc.Stop()
            self.ShowMain()

    def ShowMain(self):
        NomFichier = None
        if len(sys.argv)>1: #un paramètre a été passé
            parametre=sys.argv[1]
            # on verifie que le fichier passé en paramètre existe
            if os.path.isfile(parametre):
                NomFichier = parametre
        frame = FenPrincipale.wxPyVot(None, "PyVot", NomFichier)
        frame.Show()
        if self.fc.IsRunning():
            self.Raise()
#        wx.CallAfter(frame.ShowTip)


#---------------------------------------------------------------------------

class PyVotApp(wx.App):
    def OnInit(self):
        """
        Create and show the splash screen.  It will then create and show
        the main frame when it is time to do so.
        """
        self.version = VERSION
#        try:
        self.auteur = unicode(getpass.getuser(),'cp1252')
#        except:
#            self.auteur = ""
        
        wx.SystemOptions.SetOptionInt("mac.window-plain-transition", 1)
        self.SetAppName("PyVot")
        
        # For debugging
        #self.SetAssertMode(wx.PYAPP_ASSERT_DIALOG)

        # Normally when using a SplashScreen you would create it, show
        # it and then continue on with the applicaiton's
        # initialization, finally creating and showing the main
        # application window(s).  In this case we have nothing else to
        # do so we'll delay showing the main frame until later (see
        # ShowMain above) so the users can see the SplashScreen effect.        
        splash = MySplashScreen()
        splash.Show()

        return True



#---------------------------------------------------------------------------

def main():
##    try:
#    demoPath = os.path.dirname(__file__)
#    os.chdir(demoPath)
#    print demoPath
#    except:
#        pass
    
    app = PyVotApp(False)
#     wx.Log.SetActiveTarget( LogPrintStackStderr() )
    app.MainLoop()


def PyVotRunning():
    #
    # Cette fonction teste si PyVot.exe est déjà lancé, auquel cas on arrete tout.
    #
    if not HAVE_WMI:
        return False
    else:
        nb_instances=0
        try:
            controler=wmi.WMI()
            for elem in controler.Win32_Process():
                if "PyVot.exe"==elem.Caption:
                    nb_instances=nb_instances+1
            if nb_instances>=2:
                sys.exit(0)
        except:
            pass
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
# from customLogTarget import *
if __name__ == '__main__':
    __name__ = 'Main'
    #
    # On teste si PyVot est déjà lancé
    #
#    PyVotRunning()
    #
    # Amélioration de la vitesse de traitement en utilisant psyco
    #
#     if USE_PSYCO:
#         try:
#             import psyco
#             HAVE_PSYCO=True
#         except ImportError:
#             HAVE_PSYCO=False
#         if HAVE_PSYCO:
#             print "Psyco !!!!!"
#             psyco.full()
            
    
    
    
    main()

#----------------------------------------------------------------------------
