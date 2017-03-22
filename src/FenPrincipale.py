#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##This file is part of PyVot
#############################################################################
#############################################################################
##                                                                         ##
##                          FenPrincipale                                  ##
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

import wx                  # This module uses the new wx namespace
import wx.aui
import wx.html
import wx.richtext as rt
import wx.lib.buttons as buttons
import wx.lib.hyperlink as hl
import wx.lib.scrolledpanel as scrolled

from wx.lib.mixins.treemixin import ExpansionState
from wx.lib.wordwrap import wordwrap

import webbrowser

import Icones, Images, Imprime

import sys, os, traceback, xml

import Montage, Elements, Affichage, CdCF, Options, Analyse
import ConfigParser
import globdef
import xml.etree.ElementTree as ET
import xml.parsers
import ElementTable

ALLOW_AUI_FLOATING = False
DEFAULT_PERSPECTIVE = "Default Perspective"

#---------------------------------------------------------------------------
#def opj(path):
#    """Convert paths to the platform-specific separator"""
#    st = apply(os.path.join, tuple(path.split('/')))
#    # HACK: on Linux, a leading / gets lost...
#    if path.startswith('/'):
#        st = '/' + st
#    return st

def val2str(d):
#    print d
    if type(d) == int : return str(d)
    elif type(d) == unicode : return d
    elif type(d) == str : return unicode(d,'cp1252')
    elif isinstance(d,CdCF.Indice) \
        or isinstance(d,CdCF.IntVar): 
        if hasattr(d, 'ch'):
            return d.ch+" ("+unicode(d.val)+")"
        else:
            return unicode(d.val)
    elif isinstance(d,Elements.Element) :
#        print d.num
        s = unicode(d.num)
        if d.num is not None and d.type == "R" :
            s = d.taille+s
            if d.estOblique():
                s += d.orientation
        return s
    else: return u""

def val2strn(d):
    if type(d) == int : return str(d)
    elif type(d) == str or type(d) == unicode : return d 
    elif isinstance(d,CdCF.Indice) \
        or isinstance(d,CdCF.IntVar): 
            return unicode(d.val)
    elif isinstance(d,Elements.Element) :
        s = unicode(d.num)
        if d.num is not None and d.type == "R" :
            s = d.taille+s
            if d.estOblique():
                s += d.orientation
        return s
    else: return ""

def val2val(d):
    if type(d) == int : return d
    elif type(d) == str or type(d) == unicode: return eval(d)
    elif isinstance(d,CdCF.Indice)  \
        or isinstance(d,CdCF.IntVar) : return d.val
    elif isinstance(d,Elements.Element) : return d.num
    else: return d

def str2val(s, d):
    if s is None:
        ss = ''
    else:
        ss =  s.strip('\n').strip()
    
    def evalN(s):
        if s == '' :
            return None
        else:
            return eval(s)
          
    if type(d) == int : 
        d = evalN(ss)
    elif type(d) == str or type(d) == unicode: 
        d = ss
    elif isinstance(d, CdCF.Indice)  \
        or isinstance(d, CdCF.IntVar) : 
        d.val = evalN(ss)
    elif isinstance(d, Elements.Element) :
#        print d.num, s
        
        if ss == 'None':
            n = None
            o = ''
            t = "P"
        else:
            t = ss[0]
            if t in ["G","P"]:
                ss = ss[1:]
            else:
                t = "P"
                
            o = ss[-1:]
            if o in ["G","D"]:
                ss = ss[:-1]
            else:
                o = ""
            
            try:
                n = evalN(ss)
            except:
                print "ERREUR :",s,ss,t,o

        d.__init__(n,t,o)
    else:
        d = ss
    return ss,d
    
#---------------------------------------------------------------------------
# Show how to derive a custom wxLog class
#class MyLog(wx.PyLog):
#    def __init__(self, textCtrl, logTime=0):
#        wx.PyLog.__init__(self)
#        self.tc = textCtrl
#        self.logTime = logTime
#
#    def DoLogString(self, message, timeStamp):
#        #print message, timeStamp
#        #if self.logTime:
#        #    message = time.strftime("%X", time.localtime(timeStamp)) + \
#        #              ": " + message
#        if self.tc:
#            self.tc.AppendText(message + '\n')


#class MyTP(wx.PyTipProvider):
#    def GetTip(self):
#        return "This is my tip"



#---------------------------------------------------------------------------
# A class to be used to simply display a message in the demo pane
# rather than running the sample itself.
class MessagePanel(wx.Panel):
    def __init__(self, parent, message, caption='', flags=0):
        wx.Panel.__init__(self, parent)

        # Make widgets
        if flags:
            artid = None
            if flags & wx.ICON_EXCLAMATION:
                artid = wx.ART_WARNING            
            elif flags & wx.ICON_ERROR:
                artid = wx.ART_ERROR
            elif flags & wx.ICON_QUESTION:
                artid = wx.ART_QUESTION
            elif flags & wx.ICON_INFORMATION:
                artid = wx.ART_INFORMATION

            if artid is not None:
                bmp = wx.ArtProvider.GetBitmap(artid, wx.ART_MESSAGE_BOX, (32,32))
                icon = wx.StaticBitmap(self, -1, bmp)
            else:
                icon = (32,32) # make a spacer instead

        if caption:
            caption = wx.StaticText(self, -1, caption)
            caption.SetFont(wx.Font(28, wx.SWISS, wx.NORMAL, wx.BOLD))

        message = wx.StaticText(self, -1, message)

        # add to sizers for layout
        tbox = wx.BoxSizer(wx.VERTICAL)
        if caption:
            tbox.Add(caption)
            tbox.Add((10,10))
        tbox.Add(message)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add((10,10), 1)
        hbox.Add(icon)
        hbox.Add((10,10))
        hbox.Add(tbox)
        hbox.Add((10,10), 1)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add((10,10), 1)
        box.Add(hbox, 0, wx.EXPAND)
        box.Add((10,10), 2)

        self.SetSizer(box)
        self.Fit()
        


#---------------------------------------------------------------------------
# Constants for module versions

modOriginal = 0
modModified = 1
modDefault = modOriginal

def GetModifiedDirectory():
    """
    Returns the directory where modified versions of the demo files
    are stored
    """
    return os.path.join(GetDataDir(), "modified")

def GetDataDir():
    """
    Return the standard location on this platform for application data
    """
    sp = wx.StandardPaths.Get()
    return sp.GetUserDataDir()


def GetConfig():
    if not os.path.exists(GetDataDir()):
        os.makedirs(GetDataDir())

    config = wx.FileConfig(
        localFilename=os.path.join(GetDataDir(), "options"))
    return config



#---------------------------------------------------------------------------

class ModuleDictWrapper:
    """Emulates a module with a dynamically compiled __dict__"""
    def __init__(self, dict):
        self.dict = dict
        
    def __getattr__(self, name):
        if name in self.dict:
            return self.dict[name]
        else:
            raise AttributeError



##---------------------------------------------------------------------------
#


#---------------------------------------------------------------------------
class wxPyVot(wx.Frame):
    
    overviewText = "PyVot *test*"

    def __init__(self, parent, title, nomFichier = None):
        wx.Frame.__init__(self, parent, -1, title, size = (1024, 738),
                          style=wx.DEFAULT_FRAME_STYLE)# | wx.NO_FULL_REPAINT_ON_RESIZE)
        
        self.version = globdef.VERSION
        
        self.SetMinSize((1024,738)) # Taille mini d'écran : 1024x768

        # Use a panel under the AUI panes in order to work around a
        # bug on PPC Macs
        pnl = wx.Panel(self)
        self.pnl = pnl
        
        self.mgr = wx.aui.AuiManager()
        self.mgr.SetManagedWindow(pnl)

        # On applique l'icone
        self.SetIcon(Icones.getIconeFenetreIcon())

        # On centre la fenêtre dans l'écran ...
        self.Centre(wx.BOTH)
        
        #
        # On ajoute une barre de status ...
        #
        self.statusBar = PyVotStatusBar(self)
        self.SetStatusBar(self.statusBar)
#        self.statusBar = self.CreateStatusBar(1, wx.ST_SIZEGRIP)
#        self.statusBar.SetFieldsCount(2)
#        self.statusBar.SetStatusWidths([-1,100])
#        self.statusBar.SetStatusStyles(1, wx.SB_RAISED)
        
        
        def EmptyHandler(evt): pass

        #
        # Chargement des constantes diverses ...
        #
        
        #  qu'on ne peut pas faire tant que wx.App n'existe pas !!!
        Analyse.charger_styleText()

        # Instanciation d'un montage complet (Montage + CdCF) (on passe wxPyVot pour avoir GetEventHandler)
        self.mtgComplet = MontageComplet(self)
        
        # Instanciation d'une analyse du montage
        self.analyse = Analyse.Analyse()
        
        # On fait un copie des propriétés des éléments
        self.CopieListeElements = Elements.dictCopy(Elements.listeElements)
        
        # Taille des roulements à inserer
        self.taillelem = "P"
        
        #
        # Instanciation et chargement des options
        #
        options = Options.Options()
        if options.fichierExiste():
            try :
                options.ouvrir()
            except:
                print "Fichier d'options corrompus ou inexistant !! Initialisation ..."
                options.defaut()
        
        # On applique les options ...
        self.AppliquerOptions(options)
        
        # On garde un copie des options d'impression
        self.optionsImprProv = self.options.optImpression.copy()
        

        ###############################################################################################
        # Notebook du CdCF
        #################################################################################################
        self.nbCdCF = CdCF.nbCdCF(pnl, self.mtgComplet, self)
#        self.nbCdCF.SetSize((-1,self.nbCdCF.))
        self.nbCdCF.CdCF_Charges.Bind(CdCF.EVT_CDCF_MODIFIED, self.OnCdCFModified)
        self.nbCdCF.CdCF_Cout.Bind(CdCF.EVT_CDCF_MODIFIED, self.OnCdCFModified)
        self.nbCdCF.CdCF_Etancheite.Bind(CdCF.EVT_CDCF_MODIFIED, self.OnCdCFModified)
        self.Bind(Montage.EVT_MTG_MODIFIED, self.OnMtgModified)
#         self.nbCdCF.MaxSize = self.nbCdCF.GetMaxSize()
#        print "Size nbCdCF",self.nbCdCF.GetSize()
        
        
        ###############################################################################################
        # Menu
        #################################################################################################
        self.mainmenu = MenuPrincipal(self)
        self.SetMenuBar(self.mainmenu)
        
        ###############################################################################################
        # Fenetre de montage
        ###############################################################################################
        self.panelCentral = wx.ScrolledWindow(pnl, -1, style=wx.HSCROLL | wx.VSCROLL | wx.RETAINED|wx.BORDER_SUNKEN)
        sizerCentral = wx.GridSizer(1,1)
        self.zMont = Affichage.ZoneMontage(self.panelCentral, self, self.mtgComplet.mtg)
        
        self.panelCentral.SetVirtualSize(self.zMont.GetSize())
#        self.panelCentral.SetMaxSize(self.zMont.GetSize())
        self.panelCentral.SetScrollRate(5,5)
        self.panelCentral.Bind(wx.EVT_CHILD_FOCUS, self.OnFocus)
        
        sizerCentral.Add(self.zMont, flag = wx.ALIGN_CENTER|wx.ALL)
        self.panelCentral.SetSizerAndFit(sizerCentral)
        
        ################################################################################################
        # NoteBook de gauche
        #################################################################################################
        self.nbGauche = NbGauche(pnl, self.mtgComplet, self.zMont, self.analyse, self, self.nbCdCF,
                                 afficherArbre = self.options.optGenerales["OngletMontage"])
        self.tree = self.nbGauche.tree

        ###############################################
        ###############################################
        # Evenements ...
        ###############################################
        ###############################################

        self.Bind(wx.EVT_ACTIVATE, self.OnActivate)
        wx.GetApp().Bind(wx.EVT_ACTIVATE_APP, self.OnAppActivate)
        
        # Interception de la demande de fermeture
        self.Bind(wx.EVT_CLOSE, self.quitterPyVot )

#        # select some other initial module?
#        if len(sys.argv) > 1:
#            arg = sys.argv[1]
#            if arg.endswith('.py'):
#                arg = arg[:-3]
#            selectedDemo = self.treeMap.get(arg, None)
#            if selectedDemo:
#                self.tree.SelectItem(selectedDemo)
#                self.tree.EnsureVisible(selectedDemo)
        
        #############################################################################################
        # Mise en place des morceaux
        #############################################################################################
#        print "MaxSize zMont", self.zMont.GetMaxSize()
        self.mgr.AddPane(self.panelCentral, 
                         wx.aui.AuiPaneInfo().
                         CenterPane().
                         Caption(u"Montage")
#                          PaneBorder(False).
#                          Floatable(ALLOW_AUI_FLOATING).
#                          CloseButton(False).
#                          Name("Montage").
#                          Layer(2).BestSize(self.zMont.GetMaxSize()).
#                          MaxSize(self.zMont.GetMaxSize()))
                        )
        
        self.mgr.AddPane(self.nbGauche,
                         wx.aui.AuiPaneInfo().
                         Left().Layer(2).BestSize((264, -1)).
                         MinSize((262, -1)).
                         CaptionVisible(False).
#                          Floatable(ALLOW_AUI_FLOATING).FloatingSize((264, 700)).
                         CloseButton(False).
                         PaneBorder(False).
                         Name("Action")
                         )
        
        self.mgr.AddPane(self.nbCdCF,
                         wx.aui.AuiPaneInfo().
                         Bottom().
                         Layer(1).
#                         Floatable(False).
                        BestSize((-1, 200)).
                        MinSize((-1, 200)).
                         MinimizeButton(True).
                         Resizable(True).

#                         DockFixed().
#                         Gripper(True).
#                         Movable(False).
#                         Maximize().
                         CaptionVisible(False).
#                         PaneBorder(False).
                         CloseButton(False).
#                          Bottom().BestSize((-1, -1)).
#                          Fixed().
#                          MinSize((self.nbCdCF.MaxSize[0],self.nbCdCF.MaxSize[1]+28)).
#                          Floatable(ALLOW_AUI_FLOATING).FloatingSize((500, 160)).
#                          Dockable(True).
# #                         Dock().
                        Caption(u"Cahier des Charges Fonctionnel").
#                          CloseButton(False).
#                          PaneBorder(False).
                         Name("CdCF"))
        
        self.mgr.Update()
#         self.mgr.SetFlags(self.mgr.GetFlags() ^ wx.aui.AUI_MGR_TRANSPARENT_DRAG)
        
        
        
        #############################################################################################
        # Barre d'outils
        #############################################################################################
        tb = BarreOutils(self)
        self.SetToolBar(tb)
        
        
        #############################################################################################
        # Control affichant le cout du montage
        #############################################################################################
#        self.ctrlCout = BarreCout(self)
#        self.SetToolBar(self.ctrlCout)
#        SetFieldsCount
        
        
        #
        # On ouvre le fichier .pyv passé en argument
        #
        if nomFichier is not None:
            self.ouvrir(nomFichier)
        else :
            nomFichier = ''
        self.definirNomFichierCourant(nomFichier)
        
        #
        # On met à jour le cout
        #
        self.MiseAJourCout()
       
    def OnFocus(self, event):
        pass
    
    def Propriete(self, num):
        useMetal = False
        if 'wxMac' in wx.PlatformInfo:
            useMetal = self.cb.IsChecked()
            
        dlg = Elements.Propriete(self, -1, u"Propriétés", size=(350, 200),
                         #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME,
                         style=wx.DEFAULT_DIALOG_STYLE, # & ~wx.CLOSE_BOX,
                         num = num, useMetal=useMetal,
                         )
        dlg.CenterOnScreen()

        # this does not return until the dialog is closed.
        val = dlg.ShowModal()      
    
    #############################################################################
    def definirNomFichierCourant(self, nomFichier = '', modif = False):
#        if modif : print "Fichier courant modifié !"
        self.fichierCourant = nomFichier
        self.fichierCourantModifie = modif
        if self.fichierCourant == '':
            t = ''
        else:
            t = ' - ' + self.fichierCourant
        if modif : 
            t += " **"
        self.SetTitle("PyVot " + self.version + t )

    def MarquerFichierCourantModifie(self):
        self.analyse.estPerimee = True
        self.definirNomFichierCourant(self.fichierCourant, True)
        
#    def WriteText(self, text):
#        if text[-1:] == '\n':
#            text = text[:-1]
#        wx.LogMessage(text)
#
#    def write(self, txt):
#        self.WriteText(txt)

     #############################################################################            
    def Escape(self, event):
        "Op. à effectuer quand la touche <Echap> est pressée"
#        print "Escape"
        if not self.suppression:
            if self.elemProv.num is not None:
                self.elemProv.num = None
                self.mtg.effacerElem(self.elemProv)
##                self.mtg.frame.afficherIconeElem(self.elemProv)
##                self.mtg.frame.delete("Icone")
##        else:
##            self.desactiverModeSuppr()
        
        self.elemProv.num = None

        # Remise à la normale du curseur
        self.mtg.frame.effaceCurseur()
##        self.master["cursor"] = 'arrow'
##        self.mtg.frame["cursor"] = 'arrow'

        # Remise à la normale des boutons
        if not self.mtg.deuxrlt():
            self.barreElements.activer_desactiverBoutonPG(1)
        if self.elemProv.num is not None:
            self.barreElements.deverouille(self.elemProv.num)
##            self.barreElements.listeBouton[self.elemProv.num].configure(relief = RAISED)
            
##        for c in self.barreElements.listeBouton.keys():
##            self.barreElements.listeBouton[c].configure(relief = RAISED)

        self.zoneMessage.afficher('SelectElem')
        #self.elemProv.num = None

    
    
#    def initPageAnalyse(self, page):
#        self.nbGauche.GetParent().Freeze()
#        self.tbAnalys.DeletePage(page)
#        
#        self.nbGauche.GetParent().Thaw()
        
        
    def OnCdCFModified(self, event = None):
#        print "Modification du CdCF"
        self.MarquerFichierCourantModifie()
        self.mtgComplet.CdCF.MaJ()
        
        # Recréation de l'arbre de montage
        if self.nbGauche.GetSelectionId() == 1:
            self.nbGauche.tree.RecreateTree()
            
        # On refait l'analyse ...
        elif self.nbGauche.GetSelectionId() == 2:
            self.nbGauche.InitTBAnalyse()
#        print self.mtgComplet.CdCF
        self.MiseAJourCout()
        
    def MiseAJourCout(self):
        self.mtgComplet.mtg.majCout()
        if self.mtgComplet.CdCF.coutMax.get() < self.mtgComplet.mtg.cout:
            depass = True
        else:
            depass = False
        self.statusBar.MiseAJourCout(self.mtgComplet.mtg.cout, depass)
#        self.statusBar.SetStatusText("Coût : "+str(self.mtgComplet.mtg.cout),1)
            
    def OnMtgModified(self, event = None):
        self.MarquerFichierCourantModifie()
        
        # Recréation de l'arbre de montage
        if self.nbGauche.GetSelectionId() == 1:
            self.tree.RecreateTree()
    
        self.MiseAJourCout()



    def OnElemClick(self, event):
#        print "Bouton elem n°",event.GetId()
        self.nbGauche.tbElem.desactiverBouton(self.zMont.numElemProv)
        self.zMont.numElemProv = event.GetId()
        self.changerCurseur(elem = self.zMont.numElemProv)
#        self.statusBar.PushStatusText(u"Choisir un emplacement pour cet élément sur le montage ...",0) 
        
    def OnElemDeclick(self, event = None):
        if self.zMont.numElemProv != None:
            self.nbGauche.tbElem.desactiverBouton(self.zMont.numElemProv)
            self.zMont.numElemProv = None
            self.changerCurseur(globdef.CURSEUR_DEFAUT)
#            self.statusBar.PopStatusText()
                                      
    def OnOpenClick(self, event):    
        self.dialogOuvrir()
    
    def OnSaveClick(self, event):
        id = event.GetId()
        if id == 1030:
            self.commandeEnregistrer()
        elif id == 1035:
            self.dialogEnregistrer()  
        
    def OnNewClick(self, event):
        if not self.mtgComplet.mtg.estNonVide():
            return
        dlg = DialogInitProjet(self)
        raz = dlg.ShowModal()
        dlg.Destroy()
        
        if raz == wx.ID_OK:
            self.mtgComplet.RAZ()
            self.tree.init(self.mtgComplet)
            self.mtgComplet.mtg.rafraichirAffichage(self.zMont)
            self.definirNomFichierCourant()
            self.nbGauche.SetSelection(0)
            self.nbCdCF.miseAJourTousCriteres()
    
    def OnAnalysClick(self, event):
        self.nbGauche.SetSelection(self.nbGauche.IdPages[2])
#        self.nbGauche.SetSelectionId(2)
    
    def OnPrintClick(self, event):
        """ Impression d'un rapport d'analyse
        """
        self.Freeze()
        
        # On lance l'analyse si ce n'est pas déja fait ...
        if self.analyse.estPerimee:
            self.analyse.lancerAnalyse(self.mtgComplet, self.zMont)
            self.nbGauche.InitTBAnalyse()
#            self.nbGauche.tbAnalys = Analyse.TBAnalyse(self.nbGauche, self.mtgComplet, self.zMont, self.analyse, self.nbCdCF)
        
        if self.options.optImpression["DemanderImpr"]:
            optionImpr = self.optionsImprProv.copy()
            dlg = Options.FenOptionsImpression(self, optionImpr)
            dlg.CenterOnScreen()
            val = dlg.ShowModal()
            if val == wx.ID_OK:
                self.optionsImprProv = optionImpr
                afficherRapport = True
            else:
                afficherRapport = False
            dlg.Destroy()
            optImpr = self.optionsImprProv
        else:
            afficherRapport = True
            optImpr = self.options.optImpression
        
        # Frame contenant le rapport   
        if afficherRapport:   
            win = Imprime.FrameRapport(self, optImpr, 
                                       self.fichierCourant,
                                       self.analyse, 
                                       self.zMont,
                                       self.mtgComplet.CdCF,
                                       self.nbCdCF.CdCF_Charges, 
                                       self.nbGauche.tbAnalys.GetPage(3),
                                       self.nbGauche.tbAnalys.GetPage(4), 
                                       self.nbGauche.tbAnalys.GetPage(1))
            
#            self.analyse.reinitialiserAffichage(self.zMont)
            win.Show(True)
        
        self.Thaw()
        
        
   
    def OnRetourneClick(self,event):
        wx.BeginBusyCursor(wx.HOURGLASS_CURSOR)
#        self.zMont.analyse.initTraceResultats()
        if self.analyse is not None:
            self.analyse.reinitialiserAffichage(self.zMont)
        self.analyse == None
#        self.mtgComplet.mtg.rafraichirAffichage(self.zMont)
        
        self.mtgComplet.mtg.retourner()
#        self.tree._tree._treeStruct['Composants'] = [2,self.mtgComplet.mtg._tree]
        self.tree.RecreateTree()
        self.mtgComplet.mtg.rafraichirAffichage(self.zMont)
        self.OnCdCFModified()
        wx.EndBusyCursor()
        
    def OnAboutClick(self, event):
        win = A_propos(self)
        win.Show()
  
    def OnHelpClick(self, event):
        lienAide = {"index"   : "index.html",
                    "cdcf"    : "cdcf.html",
                    "analyse" : "analyse.html"}
        
        fichierAideChm = os.path.join(globdef.HELPPATH,'PyvotAide.chm')
        fichierAideHtml = os.path.join(globdef.HELPPATH,"html","index.html")
        
        def aideAbsente():
            dlg = wx.MessageDialog(self, u"Le fichier d'aide est absent !",
                                       'Fichier absent',
                                       wx.OK | wx.ICON_ERROR
                                       #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                       )
            dlg.ShowModal()
            dlg.Destroy()
##    webbrowser.open(lienAide[clef])
##    print "Affichage de l'aide :",lienAide[clef]
        if self.options.optGenerales["TypeAide"] == 0 and sys.platform == 'win32':
            if os.path.isfile(fichierAideChm):
                os.startfile(fichierAideChm)
            else:
                aideAbsente()                
        else:
            if os.path.isfile(fichierAideHtml):
                os.chdir(os.path.join(globdef.HELPPATH,"html"))
                webbrowser.open('index.html')
                os.chdir(globdef.PATH)
            else:
                aideAbsente()

        
#        dlg = wx.MessageDialog(self, u"Cette fonctionnalité n'est pas encore disponible ...",
#                               'Aide de PyVot',
#                               wx.OK | wx.ICON_INFORMATION
#                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
#                               )
#        dlg.ShowModal()
#        dlg.Destroy()
  
    def AppliquerOptions(self, options):
        self.options = options.copie()
        
        # Affichage de l'onglet "Projet"
        self.AfficherArbre = self.options.optGenerales["OngletMontage"]
        
        # Dossier d'enregistrement
        self.DossierSauvegarde = self.options.optGenerales["RepCourant"]
  
        # Propriétés des éléments
            # Propriétés personnalisées
        if options.optElements["ProprietesDefaut"] != 0: 
            ElementTable.Exporter(options.optElements["FichierProprietes"], 
                                  Elements.listeElements)
            
            # Propriétés par défaut
        else:                                        
            Elements.listeElements = Elements.dictCopy(self.CopieListeElements)
        
#        print Elements.listeElements
            
    def OnOptionClick(self, event):
        options = self.options.copie()
        dlg = Options.FenOptions(self, options)
        dlg.CenterOnScreen()

        # this does not return until the dialog is closed.
        val = dlg.ShowModal()
    
        if val == wx.ID_OK:
#            print options
            self.AppliquerOptions(options)
        else:
            pass
#            print "You pressed Cancel"

        dlg.Destroy()
        
    def OnCdCFClick(self,event):
        panCdCF = self.mgr.GetPane(self.nbCdCF)
        if not event.GetInt():
            mess = u"Afficher le CdCF"
            size = (self.nbCdCF.MaxSize[0],0)
            state = False
        else:
            mess = "Masquer le CdCF"
            size = (self.nbCdCF.MaxSize[0],self.nbCdCF.MaxSize[1]+28)
            state = True
            
        panCdCF.Show(state)
#        panCdCF.MinSize(size)
#        panCdCF.MaxSize(size)
#        panCdCF.BestSize(size)
        self.GetToolBar().defToolCdCFHelp(event.GetInt())
        self.mgr.Update()
            
    def OnClick(self, event):
        id = event.GetId()
        if id == 10: self.OnNewClick(event)
        elif id == 20: self.OnOpenClick(event)
        elif id == 30 or id == 35 : self.OnSaveClick(event)  
        elif id == 40: self.OnPrintClick(event)
        elif id == 50: self.OnCdCFClick(event)
         
#            self.ToggleTool(50, True)
    def OnRClick(self,event):
        pass
#        print "RClick :",event.GetId()

#    #---------------------------------------------
#    def OnItemExpanded(self, event):
#        item = event.GetItem()
#        wx.LogMessage("OnItemExpanded: %s" % self.tree.GetItemText(item))
#        event.Skip()
#
#    #---------------------------------------------
#    def OnItemCollapsed(self, event):
#        item = event.GetItem()
#        wx.LogMessage("OnItemCollapsed: %s" % self.tree.GetItemText(item))
#        event.Skip()

#    #---------------------------------------------
#    def OnTreeLeftDown(self, event):
#        # reset the overview text if the tree item is clicked on again
#        pt = event.GetPosition();
#        item, flags = self.tree.HitTest(pt)
#        if item == self.tree.GetSelection():
#            self.SetOverview(self.tree.GetItemText(item)+" Overview", self.curOverview)
#        event.Skip()

    #---------------------------------------------
    def OnSelChanged(self, event):
        item = event.GetItem()
        itemText = self.tree.GetItemText(item)
#        self.LoadDemo(itemText)


    #---------------------------------------------
    # Menu methods
    def OnFileExit(self, *event):
        self.quitterPyVot()

    def OnToggleRedirect(self, event):
        app = wx.GetApp()
        if event.Checked():
            app.RedirectStdio()
#            print "Print statements and other standard output will now be directed to this window."
        else:
            app.RestoreStdio()
#            print "Print statements and other standard output will now be sent to the usual location."


#    def OnAUIPerspectives(self, event):
#        perspective = self.perspectives_menu.GetLabel(event.GetId())
#        self.mgr.LoadPerspective(self.auiConfigurations[perspective])
#        self.mgr.Update()
#
#
#    def OnSavePerspective(self, event):
#        dlg = wx.TextEntryDialog(self, "Enter a name for the new perspective:", "AUI Configuration")
#        
#        dlg.SetValue(("Perspective %d")%(len(self.auiConfigurations)+1))
#        if dlg.ShowModal() != wx.ID_OK:
#            return
#
#        perspectiveName = dlg.GetValue()
#        menuItems = self.perspectives_menu.GetMenuItems()
#        for item in menuItems:
#            if item.GetLabel() == perspectiveName:
#                wx.MessageBox("The selected perspective name:\n\n%s\n\nAlready exists."%perspectiveName,
#                              "Error", style=wx.ICON_ERROR)
#                return
#                
#        item = wx.MenuItem(self.perspectives_menu, -1, dlg.GetValue(),
#                           "Load user perspective %d"%(len(self.auiConfigurations)+1),
#                           wx.ITEM_RADIO)
#        self.Bind(wx.EVT_MENU, self.OnAUIPerspectives, item)                
#        self.perspectives_menu.AppendItem(item)
#        item.Check(True)
#        self.auiConfigurations.update({dlg.GetValue(): self.mgr.SavePerspective()})
#
#
#    def OnDeletePerspective(self, event):
#        menuItems = self.perspectives_menu.GetMenuItems()[1:]
#        lst = []
#        loadDefault = False
#        
#        for item in menuItems:
#            lst.append(item.GetLabel())
#            
#        dlg = wx.MultiChoiceDialog(self, 
#                                   "Please select the perspectives\nyou would like to delete:",
#                                   "Delete AUI Perspectives", lst)
#
#        if dlg.ShowModal() == wx.ID_OK:
#            selections = dlg.GetSelections()
#            strings = [lst[x] for x in selections]
#            for sel in strings:
#                self.auiConfigurations.pop(sel)
#                item = menuItems[lst.index(sel)]
#                if item.IsChecked():
#                    loadDefault = True
#                    self.perspectives_menu.GetMenuItems()[0].Check(True)
#                self.perspectives_menu.DeleteItem(item)
#                lst.remove(sel)
#
#        if loadDefault:
#            self.mgr.LoadPerspective(self.auiConfigurations[DEFAULT_PERSPECTIVE])
#            self.mgr.Update()


    def OnTreeExpansion(self, event):
        self.tree.SetExpansionState(self.expansionState)
        



    #---------------------------------------------
    def OnMaximize(self, evt):
#        wx.LogMessage("OnMaximize")
        evt.Skip()

    #---------------------------------------------
    def OnActivate(self, evt):
#        wx.LogMessage("OnActivate: %s" % evt.GetActive())
        evt.Skip()

    #---------------------------------------------
    def OnAppActivate(self, evt):
#        wx.LogMessage("OnAppActivate: %s" % evt.GetActive())
        evt.Skip()

    #---------------------------------------------------------------------------             
    def dialogOuvrir(self,nomFichier=None):
        mesFormats = "Projet PyVot (.pyv)|*.pyv|" \
                     "Tous les fichiers|*.*'"
                    
#        defautDir = self.options.repertoireCourant.get()
        defautDir = self.DossierSauvegarde #os.getcwd()
        if nomFichier == None:
            dlg = wx.FileDialog(
                                self, message="Ouvrir un projet",
                                defaultDir=defautDir, 
                                defaultFile="",
                                wildcard = mesFormats,
                                style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
                                )
                
            # Show the dialog and retrieve the user response. If it is the OK response, 
            # process the data.
            if dlg.ShowModal() == wx.ID_OK:
                # This returns a Python list of files that were selected.
                paths = dlg.GetPaths()
                nomFichier = paths[0]
            else:
                nomFichier = ''
                
                
        if nomFichier != '':
#            print "Ouverture de",nomFichier
#            self.options.extraireRepertoire(nomFichier)
##            print self.options.repertoireCourant.get()
            if self.mtgComplet.mtg.estNonVide() and self.fichierCourantModifie:
                raz = False
#                self.fenR = FenReinitialiser(self,self,self.raz)
                dlg = DialogInitProjet(self)
                raz = dlg.ShowModal()
                dlg.Destroy()
            else:
                raz = True
            if raz:
                wx.BeginBusyCursor(wx.HOURGLASS_CURSOR)
                self.ouvrir(nomFichier)
                wx.EndBusyCursor()
                         
    def ouvrir(self, nomFichier):
        """ Ouvre un fichier .pyv """
        
        def ouvrir03():
#            try:
            fichier = ConfigParser.ConfigParser()
            fichier.read(nomFichier)    
            self.mtgComplet.mtg.ouvrir(fichier)
            self.mtgComplet.CdCF.ouvrir(fichier)
            self.mtgComplet.__init__(self, self.mtgComplet.mtg, self.mtgComplet.CdCF)
            return 0
#            except:
#                return sys.exc_info()[2]
        
        def ouvrir06():
            # Version 0.6
            
            try:
                Etree = ET.parse(fichier).getroot()
#                print Etree
#                try:
#                    print self._treeData[52]
#                except:
#                    pass
                self.tree._tree.ActualiserDepuisET(Etree)
                self.tree._tree.ConfirmerActualisation()
                self.mtgComplet.mtg.MaJ()
#                print self.mtgComplet.mtg
                self.mtgComplet.CdCF.MaJ()
                return 0
            except xml.parsers.expat.ExpatError:
                return 1
            except : 
                return sys.exc_info()[2]
        
        def MaJ():
#            print "Ouverture réussie !"
            self.tree.RecreateTree(mtgComplet = self.mtgComplet)
            self.mtgComplet.mtg.rafraichirAffichage(self.zMont)
            self.analyse.estPerimee = True
#            print "Fichier Courant =",self.fichierCourant, nomFichier
            self.definirNomFichierCourant(nomFichier)#self.fichierCourant)
            self.nbGauche.SetSelection(0)
            self.nbCdCF.miseAJourTousCriteres()
            self.MiseAJourCout()
        
        def AfficheErreur(Erreur):
            mess = u'Impossible de lire le fichier %s!\n\n' %nomFichier
            for m in traceback.format_tb(Erreur):
                mess += "\n" + m
            dlg = wx.MessageDialog(self, mess,
                                   u'Erreur ouverture',
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            
        fichier = open(nomFichier,'r')

        Erreur06 = ouvrir06()
        if Erreur06 == 0:
            MaJ()
        elif Erreur06 == 1:
            Erreur03 = ouvrir03()
            if Erreur03 == 0:
                mess = u'Le fichier %s a été enregistré\n\
par la version 0.3 de PyVot.\n\n\
Attention! il sera enregistré par défaut\n\
au format de la version 0.6 !!' %nomFichier
                dlg = wx.MessageDialog(self, mess  ,
                                       u'Version ancienne',
                                       wx.OK | wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
                MaJ()
                # On marque "modifié" car version 0.3
                self.MarquerFichierCourantModifie()
                
            else:
                AfficheErreur(Erreur03)
        else:
            AfficheErreur(Erreur06)

        fichier.close()
            
    #----------------------------------------------------------------------------------------------
    def dialogEnregistrer(self):
        mesFormats = "Projet PyVot (.pyv)|*.pyv|" \
                     "Tous les fichiers|*.*'"
#        mesFormats = [
#                    ('Projet PyVot','*.pyv'),
#                    ('CompuServer GIF','*.gif'),
#                    ('Tous les fichiers','*.*'),
#                    ]
#        mesFormats = "Projet PyVot (*.pyv)|*.pyv;Tous les fichiers|*.*"
        dlg = wx.FileDialog(
            self, message="Enregistrer le projet sous ...", defaultDir=self.DossierSauvegarde , 
            defaultFile="", wildcard=mesFormats, style=wx.SAVE|wx.OVERWRITE_PROMPT|wx.CHANGE_DIR
            )
        dlg.SetFilterIndex(0)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.enregistrer(path)
            self.DossierSauvegarde = os.path.split(path)[0]
            print "Nouveau dossier de sauvegarde", self.DossierSauvegarde
        dlg.Destroy()
            
    def commandeEnregistrer(self):
#        print "fichier courant :",self.fichierCourant
        if self.fichierCourant != '':
            self.enregistrer(self.fichierCourant)
        else:
            self.dialogEnregistrer()

    def enregistrer(self, nomFichier):
        fichier = file(nomFichier, 'w')
        self.tree.enregistrer(fichier)
        fichier.close()
        self.definirNomFichierCourant(nomFichier)


    def changerCurseur(self, curs = wx.CURSOR_ARROW, elem = None):    
        if elem is not None:
            image = Images.Img_Elem(elem).ConvertToImage()

            # since this image didn't come from a .cur file, tell it where the hotspot is
            image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_X, 1)
            image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, 1)

            # make the image into a cursor
            cursor = wx.CursorFromImage(image)
            texte = u"Choisir un emplacement pour cet élément sur le montage ..."
            
        else:
            cursor = wx.StockCursor(curs)
            if curs == globdef.CURSEUR_DEFAUT:
                texte = u""
            elif curs == globdef.CURSEUR_INTERDIT:
                texte = u"Impossible de placer l'élément sélectionné ici ..."
            elif curs == globdef.CURSEUR_ORIENTATION:
                texte = u"Déplacer la souris pour choisir l'orientation du roulement ... puis cliquer ..."
            elif curs == globdef.CURSEUR_OK:
                texte = u"Cliquer pour placer l'élément sélectionné ici ..."      
        
        self.SetCursor(cursor)
        self.statusBar.SetStatusText(texte, 0)
        

#############################################################################
    def quitterPyVot(self, event = None):
#        print "Quitter !!!!!!"
#        self.options.enregistrer()
#        event.Skip()
        if not self.fichierCourantModifie:
            self.fermerPyVot(event)
            return
        
        texte = u"Le projet à été modifié.\nVoulez vous enregistrer les changements ?"
        if self.fichierCourant != '':
            texte += "\n\n\t"+self.fichierCourant+"\n"
            
        dialog = wx.MessageDialog(self, texte, 
                                  "Confirmation", wx.YES_NO | wx.CANCEL | wx.ICON_WARNING)
        retCode = dialog.ShowModal()
        if retCode == wx.ID_YES:
            self.commandeEnregistrer()
            self.fermerPyVot(event)
        elif retCode == wx.ID_NO:
            self.fermerPyVot(event)
#        else:
#            print 'skipping quit'

    def fermerPyVot(self, evt):
        try:
            self.options.enregistrer()
        except:
            print "Erreur enregistrement options"
#        self.Destroy()
        evt.Skip()
        sys.exit()


#        self.Destroy()
#        self.Hide()
        
#        try:
#            sys.exit()
#        except:
###            print "Erreur !"
#            pass


######################################################################################################
# Arbre présentant les boutons de selection d'élément
######################################################################################################
#class ArbreElements(wx.Treebook):
#    def __init__(self, parent):
#        wx.Treebook.__init__(self, parent, -1, 
#                             style = wx.NB_TOP|wx.BORDER_NONE|wx.TR_HAS_BUTTONS#|wx.TR_HAS_VARIABLE_ROW_HEIGHT
#                            )
##        self.root = root
#        self.parent = parent
#        
#    def OnCompareItems(self, item1, item2):
#        t1 = self.GetItemText(item1)
#        t2 = self.GetItemText(item2)
#        if t1 < t2: return -1
#        if t1 == t2: return 0
#        return 1
#
#    def EvtRadioBox(self, event):
##        print "Taille de roulement :",event.GetInt()
#        val2taille = {1 : "G",
#                      0 : "P"}
#        self.parent.taillelem = val2taille[event.GetInt()]
#        
#    def OnClick(self, event):
#        self.parent.app.OnElemClick(event)

class NbGauche(wx.Notebook):
    def __init__(self, parent, mtgComplet, zMont, analyse, app, nbCdCF, 
                 afficherArbre = False):
        wx.Notebook.__init__(self, parent, -1, style=wx.CLIP_CHILDREN|wx.BORDER_NONE)
        
        self.zMont = zMont
        self.mtgComplet = mtgComplet
        self.analyse = analyse
        self.parent = parent
        self.nbCdCF = nbCdCF
        
        self.AfficherArbre = afficherArbre
        
        self.NomPages = {0 : u'Eléments',
                         1 : u'Projet',
                         2 : u'Analyse'}
        self.IdPages = {0 : 0,
                        1 : 1,
                        2 : 2}
        
        num = 0
        # TreeBook des éléments (boutons) (page 0)
        #-----------------------------------------
        self.tbElem = Panel_ArbreElements(self, app)
        self.AddPage(self.tbElem, self.NomPages[0], imageId=0)
        self.IdPages[0] = num
        num += 1
        
        # Arbre du montage (page 1)
        #---------------------------
        self.treeMap = {}
        self.tree = ArbreMontage(self, mtgComplet)
        self.tree.RecreateTree()
        if self.AfficherArbre:
            self.AddPage(self.tree, self.NomPages[1], imageId=1)
            self.IdPages[1] = num
            num += 1
        else:
            self.tree.Hide()
            self.IdPages[1] = None
        
        
        # TreeBook d'Analyse (page 2)
        #----------------------------
        self.tbAnalys = Analyse.TBAnalyse(self, self.mtgComplet, self.zMont, analyse, self.nbCdCF)
        self.AddPage(self.tbAnalys, self.NomPages[2], imageId=2)
        self.IdPages[2] = num
        num += 1
        
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        
    #        self.tree.SetExpansionState(self.expansionState)
    #        self.tree.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded)
    #        self.tree.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed)
    #        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
    #        self.tree.Bind(wx.EVT_LEFT_DOWN, self.OnTreeLeftDown)
        
        self.SetSelection(0)

    def GetSelectionId(self):
        for id, sel in self.IdPages.items():
            if sel == self.GetSelection():
                return id
        return False
    
    def SetSelectionId(self, id):
        self.ChangeSelection(self.IdPages[id])


    def OnPageChanged(self, event = None, page = 0):
#        old = event.GetOldSelection()
        if event == None:
            new = page
        else:
            new = event.GetSelection()
#        sel = self.nbGauche.GetSelection()
#        print "PAGE CHANGED",  new, self.IdPages

#        if self.analyse is not None:
#            self.analyse.reinitialiserAffichage(self.zMont)
            
        if new == self.IdPages[1]:
            self.tree.RecreateTree()
            self.mtgComplet.mtg.rafraichirAffichage(self.zMont)
            self.analyse.estPerimee = True
            self.zMont.modeAnalyse = False
            
        elif new == self.IdPages[2]:
#            print "Page Analyse..."
#            self.tbAnalys.__init__(self, self.nbGauche, self.mtgComplet)
            
            
            self.InitTBAnalyse()
#            self.nbGauche.GetParent().Freeze()
#            self.nbGauche.DeletePage(2)
#            
#            self.tbAnalys = Analyse.TBAnalyse(self.nbGauche, self.mtgComplet, self.zMont)
#            self.zMont.analyse = self.tbAnalys.analyse
#            self.nbGauche.AddPage(self.tbAnalys,u'Analyse', imageId=2)
#            self.nbGauche.GetParent().Thaw()
#            self.tbAnalys.Initialiser(self.mtgComplet)
        elif new == self.IdPages[0]:
            
            self.zMont.modeAnalyse = False
            self.mtgComplet.mtg.rafraichirAffichage(self.zMont)
            self.analyse.estPerimee = True
            
#        if old == 2:
#            self.tbAnalys.OnPageChanged()

        # Si on veut qu'il change vraiment de page :
        if event is not None:
            event.Skip()

    def InitTBAnalyse(self):
        self.parent.Freeze()
        
        progBarr = Imprime.Progression(self.parent, "Analyse en cours ...")
        
#        print "Init TB Analyse", self.zMont.modeAnalyse
        # On sauvegarde la page d'analyse en cours...
        p = self.tbAnalys.GetSelection()
        progBarr.Avancer(10)
        
        # On supprime le TreeBook Analyse
        self.DeletePage(self.IdPages[2])
        progBarr.Avancer(5)
        
        # On en refait un ...
        self.tbAnalys = Analyse.TBAnalyse(self, self.mtgComplet, self.zMont, self.analyse, self.nbCdCF)
        progBarr.Avancer(40)
        
        self.AddPage(self.tbAnalys, self.NomPages[2], imageId=2)
        progBarr.Avancer(20)
        
        self.zMont.modeAnalyse = True
        # On revient à la page "Analyse"
        self.SetSelectionId(2)
        progBarr.Avancer(5)
        
        # On revient à la page d'analyse sauvegardée
        self.tbAnalys.ChangeSelection(p)
        progBarr.Avancer(100)
        
        self.parent.Thaw()



###########################################################################################################
class panelRoulement(wx.Panel):
    def __init__(self, parent, master, fam):
        wx.Panel.__init__(self, parent, -1)
        bg_color = parent.GetBackgroundColour()
        self.SetBackgroundColour(bg_color)
        
        bs = wx.BoxSizer(wx.VERTICAL)
        self.master = master
        sampleList = ['petit', 'grand']
        rb = wx.RadioBox(
            self, -1, "Taille de roulement", wx.DefaultPosition, wx.DefaultSize,
            sampleList, 2, wx.RA_SPECIFY_COLS
            )        
        self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, rb)
        rb.SetToolTip(wx.ToolTip(u"Selectionne la taille du roulement à placer"))
        bs.Add(rb, flag = wx.EXPAND)
        
        nb = wx.Notebook(self, -1, style = wx.BORDER_NONE )
        
        self.listPnlBoutons = []
        for ssfam in fam[1]:
            pnl = pnlBoutonsElem(nb, master, ssfam[1])
            self.listPnlBoutons.append(pnl)
            nb.AddPage(pnl , ssfam[0])
            
        bs.Add(nb, flag = wx.EXPAND)
        
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        
        self.SetSizerAndFit(bs)
        
    def OnPageChanged(self, event):
        pass
    
    def EvtRadioBox(self, event):
        event.Skip()
        self.master.EvtRadioBox(event)
        

class ListBookElements(wx.Listbook):
    def __init__(self, parent):
        wx.Listbook.__init__(self, parent, -1, style=
                            wx.BK_TOP
                            #wx.BK_TOP
                            #wx.BK_BOTTOM
                            #wx.BK_LEFT
                            #wx.BK_RIGHT
                            )
#        self.Bind(wx.EVT_SIZE, self.OnSize)
#        self.Bind(wx.EVT_LISTBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.lv = self.GetListView()
        sz = self.lv.GetSize()
        self.lastHPage = self.GetSizeTuple()[1]-self.lv.GetSize()[1]
#        lv.__init__(parent, -1, style = wx.LC_REPORT 
#                                 #| wx.BORDER_SUNKEN
#                                 | wx.BORDER_NONE
#                                 | wx.LC_NO_HEADER
#                                 #| wx.LC_VRULES
#                                 #| wx.LC_HRULES
#                                 #| wx.LC_SINGLE_SEL
#                                 )
#        self.SetListView(lv)
        self.lv.SetWindowStyle(wx.LC_ICON|wx.VSCROLL)
        self.lv.SetMaxSize((-1,150))
        self.parent = parent
        
    def OnCompareItems(self, item1, item2):
        t1 = self.GetItemText(item1)
        t2 = self.GetItemText(item2)
        if t1 < t2: return -1
        if t1 == t2: return 0
        return 1

    def OnSize(self, event):
        event.Skip()
        self.lv.SetSize((-1,150))
        return
        w,h = self.GetClientSizeTuple()
        hPage = self.GetSizeTuple()[1]-self.lv.GetSize()[1]
#        print "Resize",self.lastHPage,"-->",hPage," (",hPage-self.lastHPage,")"
        sz = self.lv.GetSize()
        self.lv.SetSize((sz[0],sz[1]-hPage+self.lastHPage))
#        print "   --> lv :",self.lv.GetSize()[1]
        self.lastHPage = hPage
        
    def OnPageChanged(self, event):
#        print "desactiver tout"
        self.parent.desactiverTousBoutons()


class Panel_ArbreElements(wx.Panel):
    def __init__(self, parent, app):
        # Use the WANTS_CHARS style so the panel doesn't eat the Return key.
        wx.Panel.__init__(self, parent, -1, 
                          style=wx.CLIP_CHILDREN|wx.BORDER_NONE )
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
        self.DClick = False
        
        self.app = app
        tID = wx.NewId()

        self.tree = ListBookElements(self)

        isz = (90,40)
        imgBout = {}
        il = wx.ImageList(isz[0], isz[1])
        self.il = il
#        listFctGet = {}
#        for i in Images.Img_Elem.keys():
#            listFctGet[i] = il.Add(Images.Img_Elem[i])
                      
#        for idImg in ImagesPV.listFctGet.keys():
#            imgBout[idImg] = il.Add(ImagesPV.listFctGet[idImg])
            
#        imgFamRlt     = il.Add(Icones.get0Bitmap())
#        fldridx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz))
#        fldropenidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, isz))
#        fileidx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
#        smileidx    = il.Add(images.getSmilesBitmap())

#        self.tree.SetImageList(il)
        
        # NOTE:  For some reason tree items have to have a data object in
        #        order to be sorted.  Since our compare just uses the labels
        #        we don't need any real data, so we'll just use None below for
        #        the item data.

#        self.root = self.tree.AddPage("Elements")
#        self.tree.SetPyData(self.root, None)
#        self.tree.SetItemImage(self.root, imgFamRlt, wx.TreeItemIcon_Normal)
#        self.tree.SetItemImage(self.root, imgFamRlt, wx.TreeItemIcon_Expanded)
                    
#        def construireFamille(root, lstfam):
#            self.tree.SetPyData(Tfam, None)
#            self.tree.SetItemImage(Tfam, imgFamRlt, wx.TreeItemIcon_Normal)
#            self.tree.SetItemImage(Tfam, imgFamRlt, wx.TreeItemIcon_Expanded)
#            print fam
#            print type(fam[1][0])  
        
        nn = 1
        for fam in Elements.listeFamilles:
            il.Add(Images.Img_IconesEns(nn))
            nn += 1
        self.tree.AssignImageList(il)
        
        nn = 0
        self.listPnlBoutons = []
        for fam in Elements.listeFamilles:
            if type(fam[1][0]) == list: # S'il y a des sous familles ...
                pnl = panelRoulement(self.tree, self, fam)
                self.listPnlBoutons.extend(pnl.listPnlBoutons)
            else:
                pnl = pnlBoutonsElem(self.tree, self, fam[1])
                self.listPnlBoutons.append(pnl)
            
            self.tree.AddPage(pnl, fam[0], imageId = nn)
            nn += 1

#        self.root = self.tree.AddRoot("Roulements")
#        self.tree.SetPyData(self.root, None)
#        self.tree.SetItemImage(self.root, fldridx, wx.TreeItemIcon_Normal)
#        self.tree.SetItemImage(self.root, fldropenidx, wx.TreeItemIcon_Expanded)
#
#
#        for x in range(15):
#            child = self.tree.AppendItem
#            self.tree.SetPyData(child, None)
#            self.tree.SetItemImage(child, fldridx, wx.TreeItemIcon_Normal)
#            self.tree.SetItemImage(child, fldropenidx, wx.TreeItemIcon_Expanded)
#
#            for y in range(5):
#                last = self.tree.AppendItem(child, "item %d-%s" % (x, chr(ord("a")+y)))
#                self.tree.SetPyData(last, None)
#                self.tree.SetItemImage(last, fldridx, wx.TreeItemIcon_Normal)
#                self.tree.SetItemImage(last, fldropenidx, wx.TreeItemIcon_Expanded)
#
#                for z in range(5):
#                    item = self.tree.AppendItem(last,  "item %d-%s-%d" % (x, chr(ord("a")+y), z))
#                    self.tree.SetPyData(item, None)
#                    self.tree.SetItemImage(item, fileidx, wx.TreeItemIcon_Normal)
#                    self.tree.SetItemImage(item, smileidx, wx.TreeItemIcon_Selected)

#        self.tree.Expand(self.root)

        self.tree.Bind(wx.EVT_LISTBOOK_PAGE_CHANGED, self.OnPageChanged)

#        self.tree.ExpandNode(0)

    def OnClick(self, event):
        click = event.GetEventObject().GetValue()
        if click:
            self.app.OnElemClick(event)
        else:
            self.app.OnElemDeclick(event)

    def EvtRadioBox(self, event):
#        print "Taille de roulement :",event.GetInt()
        val2taille = {1 : "G",
                      0 : "P"}
        self.app.taillelem = val2taille[event.GetInt()]


    def OnSize(self, event):
        w,h = self.GetClientSizeTuple()
        self.tree.SetDimensions(0, 0, w, h)
        

    def OnPageChanged(self, event):
        self.desactiverTousBoutons()
        self.item = event.GetSelection()


    def desactiverBouton(self, nb):
        if nb is None: return
        for pnl in self.listPnlBoutons:
            pnl.desactiver(nb)


    def desactiverTousBoutons(self):
        for pnl in self.listPnlBoutons:
            pnl.desactiverTout()
        self.app.OnElemDeclick()


        
        
#####################################################################################################
#####################################################################################################
class BarreOutils(wx.ToolBar):
    def __init__(self, parent):
        wx.ToolBar.__init__(self, parent, -1, wx.DefaultPosition, wx.DefaultSize,
                       wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)
        self.timer = None
        self.parent = parent
#        self.ctrlCout = CtrlCout(self)
        
        tsize = (32,32)
        lstImg = {}
        lstImg['BOuvrir'] = Icones.getBout_OuvrirBitmap()
        lstImg['BEnregi'] = Icones.getBout_EnregistrerBitmap()
        lstImg['BRAZ']    = Icones.getBout_RAZBitmap()
        lstImg['BAnalys'] = Icones.getBout_AnalyserBitmap()
        lstImg['BCdCF']   = Icones.getBout_CdCFBitmap()
        lstImg['BImprim'] = Icones.getBout_ImprimerBitmap()
        lstImg['BRet']    = Icones.getBout_RetournerBitmap()
        lstImg['BRapport']= Icones.getBout_RapportBitmap()
        for key in lstImg.keys():
            lstImg[key] = lstImg[key].ConvertToImage().Rescale(32,32,wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()


        self.SetToolBitmapSize(tsize)
        
        self.AddLabelTool(1010, "Nouveau", lstImg['BRAZ'], shortHelp="Nouveau montage",
                          longHelp="Efface tout !!")
        self.Bind(wx.EVT_TOOL, self.parent.OnNewClick, id=1010)

        self.AddLabelTool(1020, "Ouvrir", lstImg['BOuvrir'], shortHelp="Ouvrir un fichier .pyv",
                          longHelp="Ouvrir un projet depuis un fichier .pyv")
        self.Bind(wx.EVT_TOOL, self.parent.OnOpenClick, id=1020)
        
        self.AddLabelTool(1030, "Enregistrer", lstImg['BEnregi'], shortHelp="Enregistrer dans un fichier .pyv",
                          longHelp="Enregistrer le projet dans un fichier .pyv")
        self.Bind(wx.EVT_TOOL, self.parent.OnSaveClick, id=1030)
        
        self.AddSeparator()
        
        self.AddLabelTool(1032, "Imprimer", lstImg['BRapport'], shortHelp="Afficher un rapport",
                          longHelp="Afficher un rapport")
        self.Bind(wx.EVT_TOOL, self.parent.OnPrintClick, id=1032)
        
        self.AddSeparator()
        
        self.AddLabelTool(1040, "Analyser", lstImg['BAnalys'], shortHelp="Analyser le montage",
                          longHelp="Analyser le montage")
        self.Bind(wx.EVT_TOOL, self.parent.OnAnalysClick, id=1040)
        
        self.AddLabelTool(1041, "Retourner", lstImg['BRet'], shortHelp=u"Retourner le montage droite<>gauche",
                          longHelp=u"Retourner le montage droite<>gauche")
        self.Bind(wx.EVT_TOOL, self.parent.OnRetourneClick, id=1041)
        
        self.AddSeparator()
        
        self.AddCheckLabelTool(1050, "CdCF", lstImg['BCdCF'])
        self.ToggleTool(1050,True)
#        self.defToolCdCFHelp()
        self.Bind(wx.EVT_TOOL, self.parent.OnCdCFClick, id=1050)
        
        
        # Final thing to do for a toolbar is call the Realize() method. This
        # causes it to render (more or less, that is).
        self.Realize()

    def defToolCdCFHelp(self, state = None):
        if state is None:
            state = self.GetToolState(1050)
        else:
            self.ToggleTool(1050, state == 1)
            
        if state:
            self.SetToolShortHelp(1050,"Masquer le CdCF")
            self.SetToolLongHelp(1050,"Masquer le Cahier des Charges Fonctionnel")
        else:
            self.SetToolShortHelp(1050,"Afficher le CdCF")
            self.SetToolLongHelp(1050,"Afficher le Cahier des Charges Fonctionnel")
            

    def OnToolClick(self, event):
        self.parent.OnClick(event)
        if event.GetId() == 1050:
            self.defToolCdCFHelp()
        
    def OnToolRClick(self, event):
        self.parent.OnRClick(event)





        # Gestion des boutons ...
#        self.definirNomFichierCourant(nomFichier)
#        self.menu.activerMenuEnregistrer(True)
##        self.barreElements.activer_desactiverBoutons(self.mtg.deuxrlt())
##        self.mtg.frame["cursor"] = 'arrow'


class pnlBoutonsElem(scrolled.ScrolledPanel):
    def __init__(self, parent, master, lstNumElem):
        scrolled.ScrolledPanel.__init__(self, parent, -1,
                         style=wx.NO_FULL_REPAINT_ON_RESIZE)
        self.master = master
        
        self.dicBoutons = {}
        ls = 0
#        n = len(lstNumElem)/2
        n=2
        gbs = self.gbs = wx.GridBagSizer(2, 2)
        
        cnt = 0
        for nb in lstNumElem:
            img = Images.Img_Elem(nb)
            self.dicBoutons[nb] = buttons.GenBitmapToggleButton(self, nb, None)
            self.dicBoutons[nb].SetBitmapLabel(img)
#            b = wx.ToggleBitmapButton(self, nb, img)
            self.Bind(wx.EVT_BUTTON, self.OnClick, self.dicBoutons[nb])
            self.dicBoutons[nb].Bind(wx.EVT_LEFT_DCLICK, self.OnDClick)
            self.dicBoutons[nb].Bind(wx.EVT_RIGHT_UP, self.OnRClick)
#            self.Bind(EVT_BUTTON_DCLICK, self.OnDClick, self.dicBoutons[nb])
            c = cnt / n
            l = cnt % n
            gbs.Add(self.dicBoutons[nb],(c+ls, l))
            self.dicBoutons[nb].SetDefault()
            self.dicBoutons[nb].SetInitialSize()
#             self.dicBoutons[nb].SetSize(self.dicBoutons[nb].GetBestSize())
            self.dicBoutons[nb].SetToolTipString(Elements.listeElements[nb]['nom'])
            
            cnt += 1
            
        self.SetSizerAndFit(gbs)
    
    def desactiver(self, nb):
        if not self.master.DClick:
            if nb in self.dicBoutons:
                self.dicBoutons[nb].SetValue(False)
        
    
#        for child in self.GetChildren():
#            if child.GetId() == nb:
##                print "...",nb
#                child.SetValue(False)

    def desactiverTout(self):
        for b in self.dicBoutons.values():
            b.SetValue(False)

    def OnDClick(self, event):
        self.master.DClick = True
        print "DClick"
#        event.Skip()

    def OnClick(self, event):
        self.master.DClick = False
        self.master.OnClick(event)
        
    def OnRClick(self, event):
        self.master.app.Propriete(event.GetId())
        
class MenuPrincipal(wx.MenuBar):
    def __init__(self, parent):
        self.parent = parent
        wx.MenuBar.__init__(self)
        
        lstImg = {}
        lstImg['BOuvrir'] = Icones.getBout_OuvrirBitmap() 
        lstImg['BEnregi'] = Icones.getBout_EnregistrerBitmap()
        lstImg['BRAZ']    = Icones.getBout_RAZBitmap()
        lstImg['BAnalys'] = Icones.getBout_AnalyserBitmap()
        lstImg['BCdCF']   = Icones.getBout_CdCFBitmap()
        lstImg['BImprim'] = Icones.getBout_ImprimerBitmap()
        lstImg['BRet']    = Icones.getBout_RetournerBitmap()
        lstImg['BRapport']= Icones.getBout_RapportBitmap()
        for key in lstImg.keys():
            lstImg[key] = lstImg[key].ConvertToImage().Rescale(15,15,wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        
        # Menu "Fichier"
        #---------------
        menu = wx.Menu()
        
        item = wx.MenuItem(menu, 1010, '&Nouveau projet',
                           'Créer un nouveau montage')
        item.SetBitmap(lstImg['BRAZ'])
        menu.AppendItem(item)
        self.parent.Bind(wx.EVT_MENU, self.parent.OnNewClick, item)
        
        item = wx.MenuItem(menu, 1020, '&Ouvrir un projet',
                           'Ouvrir un montage depuis un fichier .pyv')
        item.SetBitmap(lstImg['BOuvrir'])
        menu.AppendItem(item)
        self.parent.Bind(wx.EVT_MENU, self.parent.OnOpenClick, item)
 
        item = wx.MenuItem(menu,1030, '&Enregistrer',
                           'Enregistre le projet dans le fichier courant')
        item.SetBitmap(lstImg['BEnregi'])
        menu.AppendItem(item)
        self.parent.Bind(wx.EVT_MENU, self.parent.OnSaveClick, item)
        
        item = wx.MenuItem(menu,1035, '&Enregistrer sous ...',
                           'Enregistre le projet dans un fichier .pyv')
        menu.AppendItem(item)
        self.parent.Bind(wx.EVT_MENU, self.parent.OnSaveClick, item)
        
        menu.AppendSeparator()
        
        optItem = wx.MenuItem(menu, 1095, 'Options ...', u"Options de PyVot")
#        imprItem.SetBitmap(Icones.getexitBitmap())
        menu.AppendItem(optItem)
        self.parent.Bind(wx.EVT_MENU, self.parent.OnOptionClick, optItem)
        
        menu.AppendSeparator()
        
        exitItem = wx.MenuItem(menu, 1100, '&Quitter\tCtrl-Q', u"Quitter l'application")
#         exitItem.SetBitmap(Icones.getexitBitmap())
        menu.AppendItem(exitItem)
        # à faire ...
        self.parent.Bind(wx.EVT_MENU, self.parent.OnFileExit, exitItem)
        
        wx.App.SetMacExitMenuItemId(exitItem.GetId())
        
        self.Append(menu, '&Fichier')

        # Menu "Affichage"
        #---------------
        menu = wx.Menu()
        
        item = wx.MenuItem(menu, 50, '&Afficher le CdCF',
                           'Afficher le CdCF', wx.ITEM_CHECK)
#        item.SetBitmap(lstImg['BCdCF'])
        menu.AppendItem(item)
        menu.Check(50, True)
        self.parent.Bind(wx.EVT_MENU, self.parent.OnCdCFClick, item)

        self.Append(menu, '&Affichage')
        
        
        
        
        # Menu "Insertion"
        #-----------------
        menu = wx.Menu()
        
        def ajoutFamElem(menu, famille):
            sub = wx.Menu()
            for e in famille[1]:
                if famille[0][0] == u"à":
                    ch = u""
                    lch = Elements.listeElements[e]['nom']
                    if lch.split()[2] == u"rotule":
                        lch = lch.split()[2:]
                    elif lch.split()[0] == u"Butée":
                        lch = lch.split()[0::3]
                    else:
                        lch = lch.split()[3:]
                    for c in lch:
                        ch += " "+c
                else:
                    ch = Elements.listeElements[e]['nom']
                item = wx.MenuItem(sub, e, ch,
                                  u"Insérer un "+Elements.listeElements[e]['nom'])
                img = Images.Img_Elem(e).ConvertToImage()
                item.SetBitmap(img.Rescale(30,30,wx.IMAGE_QUALITY_HIGH).ConvertToBitmap())
                sub.AppendItem(item)
                self.parent.Bind(wx.EVT_MENU, self.parent.OnElemClick, item)
            menu.AppendMenu(-1,famille[0],sub)
            
        
        def ajoutMenu(menu, famille):
#            print "Ajout menu :",famille[0].encode('cp437','replace')
#            sMenu = menu.Append(-1, famille[0], famille[0])
            if type(famille[1][0]) == list:
                sub = wx.Menu()
                for m in famille[1]:
#                    print "  ",
                    ajoutMenu(sub, m)
                menu.AppendMenu(-1,famille[0],sub)
            else:
                ajoutFamElem(menu, famille)
            
        
        nn = 1
        for fam in Elements.listeFamilles:
            ajoutMenu(menu, fam)
            
        
#        for indx, item in enumerate(Montage._treeList[:-1]):
#            menuItem = wx.MenuItem(menu, -1, item[0])
#            submenu = wx.Menu()
#            for childItem in item[1]:
#                mi = submenu.Append(-1, childItem)
#                self.Bind(wx.EVT_MENU, self.OnDemoMenu, mi)
#            menuItem.SetBitmap(Images.Img_Icones(Montage._Pngs[indx]))
#            menuItem.SetSubMenu(submenu)
#            menu.AppendItem(menuItem)
        self.Append(menu, '&Insertion')

        # Menu "Options"
        #---------------
        # If we've turned off floatable panels then this menu is not needed
#        if ALLOW_AUI_FLOATING:
#            menu = wx.Menu()
#            auiPerspectives = self.auiConfigurations.keys()
#            auiPerspectives.sort()
#            perspectivesMenu = wx.Menu()
#            item = wx.MenuItem(perspectivesMenu, -1, DEFAULT_PERSPECTIVE, "Load startup default perspective", wx.ITEM_RADIO)
#            self.parent.Bind(wx.EVT_MENU, self.OnAUIPerspectives, item)
#            perspectivesMenu.AppendItem(item)
#            for indx, key in enumerate(auiPerspectives):
#                if key == DEFAULT_PERSPECTIVE:
#                    continue
#                item = wx.MenuItem(perspectivesMenu, -1, key, "Load user perspective %d"%indx, wx.ITEM_RADIO)
#                perspectivesMenu.AppendItem(item)
#                self.Bind(wx.EVT_MENU, self.OnAUIPerspectives, item)
#
#            menu.AppendMenu(wx.ID_ANY, "&AUI Perspectives", perspectivesMenu)
#            self.perspectives_menu = perspectivesMenu
#
#            item = wx.MenuItem(menu, -1, 'Save Perspective', 'Save AUI perspective')
#            item.SetBitmap(images.catalog['saveperspective'].getBitmap())
#            menu.AppendItem(item)
#            self.parent.Bind(wx.EVT_MENU, self.OnSavePerspective, item)
#
#            item = wx.MenuItem(menu, -1, 'Delete Perspective', 'Delete AUI perspective')
#            item.SetBitmap(images.catalog['deleteperspective'].getBitmap())
#            menu.AppendItem(item)
#            self.parent.Bind(wx.EVT_MENU, self.OnDeletePerspective, item)
#
#            menu.AppendSeparator()
#
#            item = wx.MenuItem(menu, -1, 'Restore Tree Expansion', 'Restore the initial tree expansion state')
#            item.SetBitmap(images.catalog['expansion'].getBitmap())
#            menu.AppendItem(item)
#            self.parent.Bind(wx.EVT_MENU, self.OnTreeExpansion, item)
#
#            self.Append(menu, '&Options')
        
        # Menu "Action"
        #--------------
        menu = wx.Menu()
        retItem = wx.MenuItem(menu, 1041, 'Re&tourner le montage', u"Retourne le montage droite<>gauche")
        retItem.SetBitmap(lstImg['BRet'])
        menu.AppendItem(retItem)
        self.parent.Bind(wx.EVT_MENU, self.parent.OnRetourneClick, retItem)
        
        retItem = wx.MenuItem(menu, 1042, '&Analyser montage', u"Execute l'analyse complète du montage")
        retItem.SetBitmap(lstImg['BAnalys'])
        menu.AppendItem(retItem)
        self.parent.Bind(wx.EVT_MENU, self.parent.OnAnalysClick, retItem)
        
        imprItem = wx.MenuItem(menu, 1090, 'Afficher un &rapport', u"Afficher un rapport d'analyse")
        imprItem.SetBitmap(lstImg['BRapport'])
        menu.AppendItem(imprItem)
        self.parent.Bind(wx.EVT_MENU, self.parent.OnPrintClick, imprItem)
#        self.parent.Bind(wx.EVT_MENU, self.parent.OnHelpAbout, aproposItem)
        
#        self.Bind(wx.EVT_FIND, self.OnFind)
#        self.Bind(wx.EVT_FIND_NEXT, self.OnFind)
#        self.Bind(wx.EVT_FIND_CLOSE, self.OnFindClose)
#        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateFindItems, findItem)
#        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateFindItems, findNextItem)
        self.Append(menu, 'A&ction')
        
        # Menu "Aide"
        #------------
        menu = wx.Menu()
        aideItem = wx.MenuItem(menu, -1, '&Aide', u"Ouvre l'aide de PyVot")
        menu.AppendItem(aideItem)
        self.parent.Bind(wx.EVT_MENU, self.parent.OnHelpClick, aideItem)
        
        menu.AppendSeparator()

        aproposItem = wx.MenuItem(menu, -1, 'A propos de PyVot',
                                'Information sur Pyvot : version, licence, auteurs, lien web, ...')
        wx.App.SetMacAboutMenuItemId(aproposItem.GetId())
        menu.AppendItem(aproposItem)
        
        # à faire ...
        self.parent.Bind(wx.EVT_MENU, self.parent.OnAboutClick, aproposItem)
#        self.parent.Bind(wx.EVT_MENU, self.parent.OnHelpAbout, aproposItem)
        
#        self.Bind(wx.EVT_FIND, self.OnFind)
#        self.Bind(wx.EVT_FIND_NEXT, self.OnFind)
#        self.Bind(wx.EVT_FIND_CLOSE, self.OnFindClose)
#        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateFindItems, findItem)
#        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateFindItems, findNextItem)
        self.Append(menu, '&Aide')


#    def OnMenuClick(self, event):
#        self.parent.OnClick(event)
        
    def OnMenuRClick(self, event):
        self.parent.OnRClick(event)

        
class MontageComplet(object):
    def __init__(self, parent, mtg = None, cdcf = None):
        
        #Instanciation d'un Montage
        if mtg == None:
            self.mtg = Montage.Montage(parent)
        else:
            self.mtg = mtg
            
        #Instanciation d'un CdCF    
        if cdcf == None:
            self.CdCF = CdCF.CdCF(1)
        else:
            self.CdCF = cdcf
            
        self.estModifie = False
    
        
        
    def RAZ(self):
        self.mtg.RAZ()
        self.CdCF.RAZ()
        

    


class ArbreMontage(ExpansionState, wx.TreeCtrl):
    
    def __init__(self, parent, mtgComplet):
        wx.TreeCtrl.__init__(self, parent, style=wx.TR_DEFAULT_STYLE|
                               wx.BORDER_NONE|wx.TR_HAS_VARIABLE_ROW_HEIGHT)
#        self.BuildTreeImageList()
        self.root = self.AddRoot(u"Projet")
        self.SetItemBold(self.root, True)
        self.init(mtgComplet)
        
        
    def init(self, mtgComplet):
        self.mtgComplet = mtgComplet
        self._tree = StructureArbre(
        # Structure de l'arbre
        #---------------------
        _treeStruct = {'Proprietes'     : [1, {'Version' : [10,],
                                               'Auteur'  : [11,]}],
                       'Composants'     : [2,self.mtgComplet.mtg._tree],
                       'CdCF'           : [3,self.mtgComplet.CdCF._tree],
                       'Specifications' : [4,]},
                                  
        # Contenu de l'arbre
        #-------------------
        _treeImageList = {1  : None,
                          10 : None,
                          11 : None,
                          2  : None,
                          3  : None,
                          4  : None,
                          },
        # Images de l'arbre
        #-------------------
        _treeLabelList = {1  : u"Propriétés",
                          10 : u"Version",
                          11 : u"Auteur",
                          2  : u"Montage",
                          3  : u"CdCF",
                          4  : u"Spécifications",
                         },
        _treeData = {1  : None,
                     10 : wx.GetApp().version,
                     11 : wx.GetApp().auteur,
                     2  : None,
                     3  : None,
                     4  : None,
                     })
        
#        self.listItem = {}
        
        self._tree.construitArbre(self, self.root)

#        self.Bind(EVT_DATA_CHANGED, self.RecreateTree)
    
#    def BuildTreeImageList(self):
#        imgList = wx.ImageList(16, 16)
#        for png in _Pngs:
#            imgList.Add(Images.Img_Icones(png))
#        self.AssignImageList(imgList)
#        

    def GetItemIdentity(self, item):
        return self.GetPyData(item)



    #------------------------------------------------------------------------------------------    
    def RecreateTree(self, event = None, mtgComplet = None):
        if mtgComplet is not None:
            self.mtgComplet = mtgComplet
#        print "Recréation arbre montage :\n", self.mtgComplet.mtg
#        print self.mtgComplet.CdCF
        
        if event is not None:
            event.Skip()
        
        self.Freeze()
        self.DeleteChildren(self.root)
        self._tree.construitArbre(self, self.root)
#        critId = evt.critId
#        self.SetItemText(arbre.listItem[critId], "")
        self.ExpandAll()  
        self.Thaw()
        
        
    def enregistrer(self, fichier):
        self.RecreateTree()
        Etree = self._tree.ConvertirEnET("M")
        ET.ElementTree(Etree).write(fichier)
        




#####################################################################################################
#####################################################################################################
class StructureArbre(object):
    def __init__(self, _treeStruct, _treeImageList, _treeLabelList, _treeData):
        self._treeStruct = _treeStruct
        self._treeImageList = _treeImageList
        self._treeLabelList = _treeLabelList
        self._treeData = _treeData
        
    def __repr__(self, lvl = 0):
        s = ''
        def recurs(s, nom, lst, lvl = 0):
            s += "\n"+lvl*" " + nom + " : "
            d = self._treeData[lst[0]]
            if d is not None:
                s += val2str(d)
            if len(lst) > 1:
                if isinstance(lst[1], StructureArbre):
                    s += lst[1].__repr__(lvl+1) 
                else:
                    sub_s = ''
                    for sub_nom, sub_lst in lst[1].items():
                        s += recurs(sub_s, sub_nom, sub_lst, lvl+1) 
            return s
        
        
        for nom, lst in self._treeStruct.items():
#            print " ",nom,
            s = recurs(s, nom, lst, lvl)
#            print s
        
        return s
    
    #################################################################################################
    def TreeDataCopy(self):
        copie = {}
        for key,dat in self._treeData.items():
            if dat is None:
                d = dat
            elif type(dat) == str or type(dat) == int or type(dat) == unicode or type(dat) == float:
                d = dat
            else:
                d = dat.copy()
            copie[key] = d
        return copie
    
    
    #################################################################################################
    def copie(self):
        
        struct = {}
        
        def recurs(struct, nom, lst):
            struct[nom] = []
            struct[nom].append(lst[0])
            if len(lst) > 1:
                if isinstance(lst[1], StructureArbre):
                    struct[nom].append(lst[1].copie())
                else:
                    sub_struct = {}
                    for sub_nom, sub_lst in lst[1].items():
                        sub_struct = recurs(sub_struct, sub_nom, sub_lst)
                    struct[nom].append(sub_struct)
            return struct
        
        for nom, lst in self._treeStruct.items():
            struct = recurs(struct, nom, lst)
            
        return StructureArbre(struct,
                              self._treeImageList.copy(),
                              self._treeLabelList.copy(),
                              self._treeData.copy())
        
        
        
    #################################################################################################
    def construitArbre(self, arbre, item):
        """ Construit un arbre wx.TreeCtrl
            à partir de la structure <item>
        """
        
        def recurs(parent, e):
            id = e[1][0]
            text = self._treeLabelList[id]
            d = self._treeData[id]
            if d is not None:
                dat = u" : " + val2str(d)
            else:
                dat = u''
            
            if len(e[1]) > 1:
                item = arbre.AppendItem(parent, text+dat, data = None)
                if type(e[1][1]) is dict:
                    for sube in e[1][1].items():
                        recurs(item, sube)
                else:
                    e[1][1].construitArbre(arbre, item)
            else:
                item = arbre.AppendItem(parent, text+dat, data = None)
            
            # On affiche en GRAS les informations présentes dans le CdCF
            if   (isinstance(d,Elements.Element) and (d.num is not None)) \
                or (isinstance(d,CdCF.Indice)) or (isinstance(d,CdCF.IntVar)) \
                or type(d) == unicode :                                     
                arbre.SetItemBold(item, True)
            # On n'affiche pas les informations absentes
            elif (isinstance(d,Elements.Element) and (d.num is None)):
                arbre.Delete(item)
        
        for e in self._treeStruct.items():
            recurs(item, e)
    
    
    ##########################################################################################
    def ConvertirEnET(self, nom):
        """ Converti l'arbre  
            en un item ElementTree
            (pour sauvegarde)
        """
            
        def ajoutBranche(parent, nom, lstVal):
        
            if len(lstVal) > 1 :
                if isinstance(lstVal[1], StructureArbre):
                    branche = lstVal[1].ConvertirEnET(nom)
                    parent.append(branche)
                else:
                    branche = ET.SubElement(parent,nom)
                    for subNom, subLstVal in lstVal[1].items():
                        ajoutBranche(branche, subNom, subLstVal)
            else:
                branche = ET.SubElement(parent,nom)
            branche.text = val2strn(self._treeData[lstVal[0]])
#            print "ajout :",nom , branche.text
            
        root = ET.Element(nom)
        
        for nom, lstVal in self._treeStruct.items():
            ajoutBranche(root, nom, lstVal)

        # Indentation pour lecture plus facile
        def indent(elem, level=0):
            i = "\n" + level*"  "
            if len(elem):
                if not elem.text or not elem.text.strip():
                    elem.text = i + "  "
                for e in elem:
                    indent(e, level+1)
                    if not e.tail or not e.tail.strip():
                        e.tail = i + "  "
                if not e.tail or not e.tail.strip():
                    e.tail = i
            else:
                if level and (not elem.tail or not elem.tail.strip()):
                    elem.tail = i        
        
        indent(root)

        return root
    
    #----------------------------------------------------------------------------------------    
    def Ouvrir(self, fichier):
#        try: # Version 0.6
        Etree = ET.parse(fichier).getroot()
#        try:
        self.ActualiserDepuisET(Etree)
        self._treeData = self._treeDataProv
        return True
#        except : 
#            return False

    ####################################""
    def ActualiserDepuisET(self, branche):
        """ Actualise les données de l'arbre
            depuis une branche ElementTree
            (après ouverture fichier)
        """
#        print "Debut Actualisation ..."
        
        # Données provisoires ...
        self._treeDataProv = self.TreeDataCopy()
        
        def actualiseSub(elem, struct):
            for nom, lstVal in struct.items():
                id = lstVal[0]
                subelem = elem.getiterator(nom)[0]
#                print nom,"(",id,") : ",subelem.tag, subelem.text
                if self._treeDataProv[id] is not None: 
                    txt, self._treeDataProv[id] = str2val(subelem.text,self._treeDataProv[id])
#                    if isinstance(self._treeDataProv[id], Elements.Element):
#                        print self._treeDataProv[id]
#                    print "\t-->",txt
                
                if len(lstVal) > 1 :
                    if isinstance(lstVal[1], StructureArbre):
#                        print "   ",subelem.tag
                        lstVal[1].ActualiserDepuisET(subelem)
                    else:
                        actualiseSub(subelem, lstVal[1])

        actualiseSub(branche, self._treeStruct)    
        
#        print "Fin Actualisation ..."
    
    
    #################################################################################################
    def ConfirmerActualisation(self):
        
        def confirmeSub(struct):
#            try:
#                print self._treeDataProv[52]
#            except:
#                pass
            self._treeData = self._treeDataProv.copy()
            for nom, lstVal in struct._treeStruct.items():
                if len(lstVal) > 1 :
                    if isinstance(lstVal[1], StructureArbre):
                        lstVal[1].ConfirmerActualisation()

        confirmeSub(self) 


class FenChoixElemPopup(wx.PopupTransientWindow):
    """Adds a bit of text and mouse movement to the wx.PopupWindow"""
    def __init__(self, parent, elem, mtg):
        wx.PopupTransientWindow.__init__(self, parent, wx.SIMPLE_BORDER)
        
        self.parent = parent
        self.mtg = mtg
        self.elem = elem
        
        if elem.type == "R":
            for f in Elements.listeFamilles[0][1]:
                if elem.num in f[1]:
                    fam = f[1]
        elif elem.type == "A":
            fam = Elements.listeFamilles[1][1]
        elif elem.type == "J":
            fam = Elements.listeFamilles[2][1]
            
        self.panel = pnlBoutonsElem(self, self, fam)
        
        sz = self.panel.GetBestSize()
        self.SetSize( (sz.width+20, sz.height+20) )
        
    def disableInterdits(self, pos):
        for n,b in self.panel.dicBoutons.items():
            if not self.mtg.placeCompatible(pos, n):
                b.Enable(False)
                
                
    
    def OnClick(self, event):
        id = event.GetId()
        self.mtg.testerChangerTypeElem(self.parent, self.elem, id)
        self.mtg.rafraichirAffichage(self.parent)
        self.Destroy()
#        self.SetBackgroundColour("#FFB6C1")
#        st = wx.StaticText(self, -1,
#                          "wx.PopupTransientWindow is a\n"
#                          "wx.PopupWindow which disappears\n"
#                          "automatically when the user\n"
#                          "clicks the mouse outside it or if it\n"
#                          "(or its first child) loses focus in \n"
#                          "any other way."
#                          ,
#                          pos=(10,10))
        

    def ProcessLeftDown(self, evt):
        return False

    def OnDismiss(self):
        pass

########################################################################################################
class ZoneCout(wx.Panel):
    def __init__(self, parent, cout = 0):
        wx.Panel.__init__(self, parent, -1)
        
        sz = wx.BoxSizer(wx.HORIZONTAL)
        
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetWeight(wx.BOLD)
        self.SetFont(font)
        self.SetForegroundColour(wx.BLACK)
        
        label = wx.StaticText(self,-1, u" Coût indicatif : ")
        sz.Add(label)
        
        
#        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
#         
#        font.SetWeight(wx.BOLD)
#        self.SetFont(font)
#        self.SetForegroundColour(wx.GREEN)
        
        self.labelCout = wx.StaticText(self, -1, str(cout))
        self.MiseAJour(cout)
        
        sz.Add(self.labelCout)
        
        self.SetSizerAndFit(sz)

    def MiseAJour(self, cout, depass = False):
#        print cout, depass
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        if depass:
            font.SetWeight(wx.BOLD)
#            self.SetForegroundColour(wx.RED)
            self.labelCout.SetForegroundColour(wx.RED)
        else:
#            self.SetForegroundColour(wx.GREEN)
            self.labelCout.SetForegroundColour(wx.GREEN)
            
#        self.SetFont(font)
        self.labelCout.SetFont(font)
        
        self.labelCout.SetLabel(str(cout))

########################################################################################################
class PyVotStatusBar(wx.StatusBar):
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent, -1)

        # This status bar has three fields
        self.SetFieldsCount(2)
        # Sets the three fields to be relative widths to each other.
        self.SetStatusWidths([-2, -1])
        self.sizeChanged = False
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_IDLE, self.OnIdle)

        # Field 0 ... just text
        self.SetStatusText("", 0)

        # This will fall into field 1 (the second field)
        self.zoneCout = ZoneCout(self)
        self.Reposition()
        
    def MiseAJourCout(self, cout, depass):
        self.zoneCout.MiseAJour(cout, depass)

    def OnSize(self, evt):
        self.Reposition()  # for normal size events

        # Set a flag so the idle time handler will also do the repositioning.
        # It is done this way to get around a buglet where GetFieldRect is not
        # accurate during the EVT_SIZE resulting from a frame maximize.
        self.sizeChanged = True


    def OnIdle(self, evt):
        if self.sizeChanged:
            self.Reposition()


    # reposition the checkbox
    def Reposition(self):
        rect = self.GetFieldRect(1)
        self.zoneCout.SetPosition((rect.x+2, rect.y+2))
        self.zoneCout.SetSize((rect.width-4, rect.height-4))
        self.sizeChanged = False


class DialogInitProjet(wx.MessageDialog):
    def __init__(self, parent):
        wx.MessageDialog.__init__(self, parent, u'Voulez-vous vraiment initialiser le projet ?',
                                       u'Confirmation effacement',
                                       wx.OK | wx.ICON_QUESTION  | wx.CANCEL
                                       #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                       )

########################################################################################################
class A_propos(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, u"A propos de PyVot")
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        titre = wx.StaticText(self, -1, "PyVot")
        titre.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD, False))
        titre.SetForegroundColour(wx.NamedColour("BROWN"))
        sizer.Add(titre, border = 10)
        sizer.Add(wx.StaticText(self, -1, "Version : "+str(wx.GetApp().version)), 
                  flag=wx.ALIGN_RIGHT)
        sizer.Add(wx.StaticBitmap(self, -1, Icones.getLogoSplashBitmap()),
                  flag=wx.ALIGN_CENTER)
        
        sizer.Add(wx.StaticText(self, -1, u"CopyLeft 2006-2008 Cédrick FAURY"), 
                  border = 10)
#        sizer.Add(20)
        nb = wx.Notebook(self, -1, style=
                             wx.BK_DEFAULT
                             #wx.BK_TOP 
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             # | wx.NB_MULTILINE
                             )
        
        
        # Auteurs
        #---------
        auteurs = wx.Panel(nb, -1)
        fgs1 = wx.FlexGridSizer(cols=2, vgap=4, hgap=4)
        
        lstActeurs = ((u"Développement :",(u"Cédrick FAURY",)),
                     (u"Soutien, Tests, ... :",(u"Thomas PAVIOT", u"Franck VITTE", u"Arnaud DUBOIS")), 
                     (u"Site Web :" ,(u"Franck VITTE",)),
                     (u"Version LINUX :",(u"Arnaud DUBOIS",)))

        
        for ac in lstActeurs:
            t = wx.StaticText(auteurs, -1, ac[0])
            fgs1.Add(t, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=5)
            for l in ac[1]:
                t = wx.StaticText(auteurs, -1, l)
                fgs1.Add(t , flag=wx.RIGHT, border=10)
                t = wx.StaticText(auteurs, -1, "")
                fgs1.Add(t, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=10)
            t = wx.StaticText(auteurs, -1, "")
            fgs1.Add(t, flag=wx.RIGHT, border=5)
            
        auteurs.SetSizer(fgs1)
        
        # licence
        #---------
        licence = wx.Panel(nb, -1)
        
        txt = open("gpl.txt")
        lab = wx.TextCtrl(licence, -1, txt.read(), size = (400, -1), 
                          style = wx.TE_READONLY|wx.TE_MULTILINE|wx.BORDER_NONE )
        txt.close()

        
        # Description
        #-------------
        descrip = wx.Panel(nb, -1)
        wx.StaticText(descrip, -1, wordwrap(u"""PyVot est un logiciel éducatif de construction et d'analyse de liaisons PIVOT réalisées avec des roulements""",
            500, wx.ClientDC(self))) 
        
        nb.AddPage(descrip, "Description")
        nb.AddPage(auteurs, "Auteurs")
        nb.AddPage(licence, "Licence")
        
        sizer.Add(hl.HyperLinkCtrl(self, wx.ID_ANY, "Site web de PyVot",
                                   URL="http://www.pyvot.fr/"),  
                  flag=wx.ALIGN_RIGHT)
        sizer.Add(nb)
        
        self.SetSizerAndFit(sizer)
