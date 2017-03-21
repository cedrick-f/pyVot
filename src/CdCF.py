#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##This file is part of PyVot
#############################################################################
#############################################################################
##                                                                         ##
##                                  CdCF                                   ##
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

import Const
import pickle
import Images,Montage
import wx
import xml.etree.ElementTree as ET
import FenPrincipale as FP
import Icones
##import gui
##import ConfigParser


################################################################################
#     Constantes     #
################################################################################
lstLubrif = [u"huile", u"graisse", u"aucune"]

pression = {-1 : u"(extérieur)",
             0 : u"",
             1 : u"(interieur)"}

## Structure de l'arbre
##---------------------
#_treeStruct = {'Charges'   : [5, {'ChargeAx'   : [50,{'G' : [500,],
#                                                      'D' : [501,]}],
#                                  'ChargeRa'   : [51,{'G' : [510,],
#                                                      'D' : [511,]}],
#                                  'BagueTourn' : [52,]}],
#
#              'Etancheite' : [6, {'Pression'  : [60,],
#                                  'Vitesse'   : [61,],
#                                  'Lubrif'    : [62,]}],
#        
#              'Cout'       : [7, {'CoutMax'   : [70,]}]
#              }

## Contenu de l'arbre
##-------------------
#_treeImageList = {5   : None,
#                  50  : None,
#                  500 : None,
#                  501 : None,
#                  51  : None,
#                  510 : None,
#                  511 : None,
#                  52  : None,
#                  
#                  6   : None,
#                  60  : None,
#                  61  : None,
#                  62  : None,
#                  
#                  7   : None,
#                  70  : None,
#                  }
## Images de l'arbre
##-------------------
#_treeLabelList = {5   : u"Efforts dans la liaison",
#                  50  : u"Charge Axiale",
#                  500 : u"gauche",
#                  501 : u"droite",
#                  51  : u"Charge Radiale",
#                  510 : u"gauche",
#                  511 : u"droite",
#                  52  : u"Bague tournante par rapport à la Charge Radiale",
#                  
#                  6   : u"Etanchéité / Lubrification",
#                  60  : u"Pression",
#                  61  : u"Vitesse",
#                  62  : u"Lubrifiant",
#                  
#                  7   : u"Coût",
#                  70  : u"Coût maximum",
#                  }

class nbCdCF(wx.Notebook):
    def __init__(self, parent, mtgComplet, app):
        wx.Notebook.__init__(self, parent, -1, style = wx.CLIP_CHILDREN)
        imgList = wx.ImageList(16, 16)
        self.AssignImageList(imgList)
        self.MaxSize = None
        
        # Première page du NoteBook
        #--------------------------
        self.CdCF_Charges = SchemaCdCF(self, mtgComplet.CdCF, app)
        self.CdCF_Cout    = ZoneCdCFCout(self, mtgComplet.CdCF, app)
        self.CdCF_Etancheite    = ZoneCdCFEtancheite(self, mtgComplet.CdCF, app)
        
#        self.ovr = wx.html.HtmlWindow(panel, -1, size=(400, 400))

        self.AddPage(self.CdCF_Charges, u"Efforts sur l'arbre", imageId=0)
        self.AddPage(self.CdCF_Cout, u"Coût admissible", imageId=1)
        self.AddPage(self.CdCF_Etancheite, u"Lubrification - Etanchéité", imageId=2)
        
        # Set up a wx.html.HtmlWindow on the Overview Notebook page
        # we put it in a panel first because there seems to be a
        # refresh bug of some sort (wxGTK) when it is directly in
        # the notebook...
#        def OnOvrSize(evt, ovr=self.ovr):
#            ovr.SetSize(evt.GetSize())
#        panel.Bind(wx.EVT_SIZE, OnOvrSize)
#        CdCF_Charges.Bind(wx.EVT_ERASE_BACKGROUND, EmptyHandler)
        self.SetSelection(0)
#        if "gtk2" in wx.PlatformInfo:
#            self.ovr.SetStandardFonts()
        self.Layout()
        
    def miseAJourTousCriteres(self):
        self.CdCF_Charges.miseAJourTousCriteres()
        self.CdCF_Cout.miseAJourTousCriteres()
        self.CdCF_Etancheite.miseAJourTousCriteres()
        
    def GetMaxSize(self):
        w,h = 0,0
        for p in range(self.GetPageCount()-1):
            w = max(w,self.GetPage(p).GetSize()[0])
            h = max(h,self.GetPage(p).GetSize()[1])
        return (w,h)
        

#############################################################################
#    CdCF    #
#############################################################################           
class CdCF:
    "Classe définissant un CdCF"
    
    
    
    def __init__(self,num):
        lstCdCF = ((0,0,            #effort axial (sens 0 , sens 1)
                    0,0,            #effort radial (rlt G , rlt D)
                    "I",            #bague tournante
                    100,            #coût maximum
                    0,))            #sens de montage
        
        self.effortAxial  = { 0  : Indice(),
                              1  : Indice()}
        
        self.effortRadial = {"G" : Indice(),
                             "D" : Indice()}
        
        self.coutMax = IntVar()

        if num == 1:
            self.effortAxial[0].__init__(lstCdCF[0])
            self.effortAxial[1].__init__(lstCdCF[1])
            self.effortRadial["G"].__init__(lstCdCF[2])
            self.effortRadial["D"].__init__(lstCdCF[3])
            self.bagueTournante = lstCdCF[4]
            self.coutMax.__init__(lstCdCF[5])

        self.pression = IntVar()
        
#        self.cotePression = ""

        self.lubrifiant = IntVar(2, lstLubrif)
                
        self.vitesse = IntVar()

        self.echelleEffort = 8
        self.echelleCout = 110
        self.echellePression = 10
        self.echelleVitesse = 10
        self.echellePV = 10

        self.pressionAdmChapeau = 1
        
        self.radialeIntensite = IntVar(0)
        self.radialePourCent  = IntVar(0)

        self.zone = None
    
        self._tree = FP.StructureArbre(
        # Structure de l'arbre
        #---------------------
        _treeStruct = {'Charges'   : [5, {'ChargeAx'   : [50,{'G' : [500,],
                                                              'D' : [501,]}],
                                          'ChargeRa'   : [51,{'G' : [510,],
                                                              'D' : [511,]}],
                                          'BagueTourn' : [52,]}],

                      'Etancheite' : [6, {'Pression'  : [60,],
                                          'Vitesse'   : [61,],
                                          'Lubrif'    : [62,]}],
        
                      'Cout'       : [7, {'CoutMax'   : [70,]}]
                      },
    
        # Images de l'arbre
        #-------------------
        _treeImageList = {5   : None,
                          50  : None,
                          500 : None,
                          501 : None,
                          51  : None,
                          510 : None,
                          511 : None,
                          52  : None,
                  
                          6   : None,
                          60  : None,
                          61  : None,
                          62  : None,
                  
                          7   : None,
                          70  : None,
                          },
        # Labels de l'arbre
        #-------------------
        _treeLabelList = {5   : u"Efforts dans la liaison",
                          50  : u"Charge Axiale",
                          500 : u"gauche",
                          501 : u"droite",
                          51  : u"Charge Radiale",
                          510 : u"gauche",
                          511 : u"droite",
                          512 : u"intensité",
                          513 : u"répartition",
                          52  : u"Bague tournante par rapport à la Charge Radiale",
                  
                          6   : u"Etanchéité / Lubrification",
                          60  : u"Pression",
                          61  : u"Vitesse",
                          62  : u"Lubrifiant",
                  
                          7   : u"Coût",
                          70  : u"Coût maximum",
                          },
                            
        # Répartition des données dans l'arbre
        #--------------------------------------
        _treeData  = {5   : None,
                      50  : None,
                      500 : self.effortAxial[0],
                      501 : self.effortAxial[1],
                      51  : None,
                      510 : self.effortRadial["G"],
                      511 : self.effortRadial["D"],
                      512 : self.radialeIntensite,
                      513 : self.radialePourCent,
                      52  : self.bagueTournante,
                  
                      6   : None,
                      60  : self.pression,
                      61  : self.vitesse,
                      62  : self.lubrifiant,
                  
                      7   : None,
                      70  : self.coutMax,
                      })
    
#    def creerBranche(self, branche):
#        """ Crée une branche ElementTree
#            --> Pour sauvegarde
#        """
#        
#        def strval(d):
#            if type(d) == int : return str(d)
#            elif type(d) == str : return d 
#            else: return str(d.val)
#        
#        def creerSub(b):
#            elem = ET.SubElement(branche,b[0])
#            if _treeData[b[1][0]] is not None:
#                elem.attrib["val"] = strval(_treeData[b[1][0]])
#            if len(b[1]) > 0:
#                for c in b[1][1].items():
#                    creerSub(c)
#        
#        for b in _treeStruct.items():
#            creerSub(b)
#            
#
#
#    def actualiserDepuisBranche(self, branche):
#        """ Actualise le CdCF depuis une branche ElementTree
#            --> après ouverture fichier
#        """
#        
#        def valstr(d, num):
#            if type(_treeData[num]) == int : return evalr(d)
#            elif type(_treeData[num]) == str : return d 
#            else: return Indice(eval(d))
#        
#        def actualiseSub(b,elem):       
#            if _treeData[b[1][0]] is not None:
#                _treeData[b[1][0]] = valstr(elem.get("val"),b[1][0])
#            for subb,subelem in b[1][1].items(),elem.getchildren():
#                actualiseSub(subb,subelem)
#        
#        for b in _treeStruct.items():
#            actualiseSub(b, branche)
        
#        ChargeAx = branche.getiterator("ChargeAx")[0]
#        G = ChargeAx.getiterator("gauche")[0]
#        self.effortAxial[0].val = eval(G.attrib["val"])
#        D = ChargeAx.getiterator("droite")[0]
#        self.effortAxial[1].val = eval(D.attrib["val"])
#        
#        ChargeRa = branche.getiterator("ChargeRa")[0]
#        G = ChargeRa.getiterator("gauche")[0]
#        self.effortRadial["G"].val = eval(G.attrib["val"])
#        D = ChargeRa.getiterator("droite")[0]
#        self.effortRadial["D"].val = eval(D.attrib["val"])
#        
#        etanch = branche.getiterator("Etancheite")[0]
#        P = etanch.getiterator("pression")[0]
#        self.pression = eval(P.attrib["val"])
#        P = etanch.getiterator("lubrif")[0]
#        self.lubrifiant = P.attrib["val"]
#        P = etanch.getiterator("vitesse")[0]
#        self.vitesse = eval(P.attrib["val"])
        
    def MaJ(self):
#        print "Mise à jour CdCF"
        self.effortAxial[0] = self._tree._treeData[500]
        self.effortAxial[1] = self._tree._treeData[501]
        self.effortRadial["G"] = self._tree._treeData[510]
        self.effortRadial["D"] = self._tree._treeData[511]
        self.radialeIntensite = self._tree._treeData[512]
        self.radialePourCent = self._tree._treeData[513]
#        print "BT :", self._tree._treeData[52]
        self.bagueTournante = self._tree._treeData[52]
        self.pression = self._tree._treeData[60]
        self.vitesse = self._tree._treeData[61]
        self.lubrifiant = self._tree._treeData[62]
        self.lubrifiant.list = lstLubrif
        self.coutMax = self._tree._treeData[70]
        self.tradGD_PI()
        self.effortAxial[0].conv()
        self.effortAxial[1].conv()
#        print self
        
#    def DataChanged(self):
#        evt = Montage.MyEvent(Montage.myEVT_DATA_CHANGED,0)
#        evt.SetMyVal(0)
#        #print id(evt), sys.getrefcount(evt)
#        self.GetEventHandler().ProcessEvent(evt)
#        #print id(evt), sys.getrefcount(evt)
#        event.Skip()

#    ############################################################################
#    def afficherTousLesCriteres(self):
#        self.zone

    ############################################################################
    def codeBagueTournante(self, num):
        if num == 0:
            return "I"
        else:
            return "E"

    

    ############################################################################
    def nomBagueTournante(self, cod):
        if cod == "I" : return u"Intérieure"
        else : return u"Extérieure"

    #############################################################################
    def __repr__(self):
        t = u"CdCF :\n"
        t += u"Charges Axiales  : " + unicode(str(self.effortAxial[0].val)) + unicode(str(self.effortAxial[1].val)) + u"\n"
        t += u"Charges Radiales : " + unicode(str(self.effortRadial["G"].val)) + unicode(str(self.effortRadial["D"].val)) + u"\n"
        t += u"Bague tournante  : " + unicode(self.bagueTournante) + u"\n"
        t += u"Cout  : " + unicode(self.coutMax.val) + u"\n"
        t += u"Pression  : " + unicode(self.pression.val) + u"\n"
        return t
        

    ##########################################################################
    def code2critere(self,code):
        if code[1:] == "EffortAxial":
            return self.effortAxial[eval(code[0])].val
        elif code[1:] == "EffortRadial":
            return self.effortRadial[code[0]].val
        elif code == "BagueTournante":
            return self.bagueTournante
        elif code == "EffortRadialP":
            return self.radialePourCent
        elif code == "EffortRadialI":
            return self.radialeIntensite



    ##########################################################################
    def tradPI_GD(self):
        self.effortRadial["D"].val = (self.radialeIntensite.val * (10 + self.radialePourCent.val) * self.echelleEffort + 500)/1000
        self.effortRadial["G"].val = (self.radialeIntensite.val * (10 - self.radialePourCent.val) * self.echelleEffort + 500)/1000 
        for k,c in self.effortRadial.items():
            if c.val > self.echelleEffort:
                c.val = self.echelleEffort
        self.effortRadial["D"].conv()
        self.effortRadial["G"].conv()
#        print "  P  I  -->  G  D  "
#        print self.radialePourCent.val,self.radialeIntensite.val,self.effortRadial["G"].val,self.effortRadial["D"].val



    ##########################################################################
    def tradGD_PI(self):
        p = 10 * ( self.effortRadial["D"].val - self.effortRadial["G"].val)
        som = self.effortRadial["D"].val + self.effortRadial["G"].val
        if som <> 0 :
            p = p / som
        self.radialePourCent.val = (p)
        self.radialeIntensite.val = som * 100 / ( 2 * self.echelleEffort )

        self.effortRadial["D"].conv()
        self.effortRadial["G"].conv()
#        print "  G  D  -->  P  I  "
#        print self.effortRadial["G"].val,self.effortRadial["D"].val,self.radialePourCent.val,self.radialeIntensite.val




#    ############################################################################
#    def copie(self,cdcf):
#        for s in [0,1]:
#            self.effortAxial[s].copie(cdcf.effortAxial[s])
#        for c in ["G","D"]:
#            self.effortRadial[c].copie(cdcf.effortRadial[c])
#
#        self.bagueTournante.set(cdcf.bagueTournante.get())
#        self.coutMax.set(cdcf.coutMax.get())
#
#        self.radialeIntensite.set(cdcf.radialeIntensite.get())
#        self.radialePourCent.set(cdcf.radialePourCent.get())


##    #############################################################################
##    def sensMax(self):
##        "Renvoie le sens pour lequel l'effort axial est le plus important"
##        if self.effortAxial[0].get() > self.effortAxial[1].get():
##            return 0
##        else:
##            return 1



    ##########################################################################
    def ouvrir02(self,fichier):
        "Ouvrir un CdCF"
        self.effortAxial[0].val.set(pickle.load(fichier))
        self.effortAxial[1].val.set(pickle.load(fichier))
        self.effortAxial[0].conv()
        self.effortAxial[1].conv()
        
        self.effortRadial["G"].val.set(pickle.load(fichier))
        self.effortRadial["D"].val.set(pickle.load(fichier))
        self.effortRadial["G"].conv()
        self.effortRadial["D"].conv()
        
        self.bagueTournante=pickle.load(fichier)
        self.coutMax.set(pickle.load(fichier))

        self.miseAjour()
        
        
    ##########################################################################
    def ouvrir(self, fichier):
        """ Ouvrir un CdCF depuis un fichier ConfigParser
            - version 0.3 -
        """
#        print "ouverture CdCF"
        self.effortAxial[0].val = fichier.getint('CdCF', 'effortAxial0')
        self.effortAxial[1].val = fichier.getint('CdCF', 'effortAxial1')
        self.effortAxial[0].conv()
        self.effortAxial[1].conv()
        
        self.effortRadial["G"].val = fichier.getint('CdCF', 'effortRadialG')
        self.effortRadial["D"].val = fichier.getint('CdCF', 'effortRadialD')
        self.effortRadial["G"].conv()
        self.effortRadial["D"].conv()
        
        self.bagueTournante = fichier.get('CdCF', 'bagueTournante')

        self.coutMax.val = fichier.getint('CdCF', 'coutMax')

        try :
            self.pression.val = fichier.getint('CdCF', 'Pression')
            self.vitesse.val = fichier.getint('CdCF', 'Vitesse')
        except:
            pass

#        self.miseAjour()


    ##########################################################################
#    def enregistrer(self,fichPyv):
#        "Enregistrer le CdCF dans un fichier ConfigParser"
#        
#        fichPyv.add_section('CdCF')
#        fichPyv.set('CdCF', 'effortAxial0', self.effortAxial[0].val.get())
#        fichPyv.set('CdCF', 'effortAxial1', self.effortAxial[1].val.get())
#        fichPyv.set('CdCF', 'effortRadialG', self.effortRadial["G"].val.get())
#        fichPyv.set('CdCF', 'effortRadialD', self.effortRadial["D"].val.get())
#        fichPyv.set('CdCF', 'bagueTournante', self.bagueTournante.get()[0])
#        fichPyv.set('CdCF', 'Pression', self.pression.get())
#        fichPyv.set('CdCF', 'Vitesse', self.vitesse.get())
#        fichPyv.set('CdCF', 'coutMax', self.coutMax.get())

#    ##########################################################################
#    def miseAjour(self):
##        self.zone.afficherTousLesCriteres()
##        self.tradGD_PI()
#        print "Fin ouverture cdcf :"
#        print self

    def RAZ(self):
        self.__init__(0)
        

#############################################################################
#    Indice de critère    #
#############################################################################           
class Indice:
    def __init__(self, val = 0):
        self.val = val
        self.ch = u""
        self.conv()
    
    def __repr__(self):
        return self.val
#        return unicode(self.val)+"("+self.ch#.encode('cp1252','replace')+")"

    def conv(self):
        ch = {0 : u'très faible',
              1 : u'assez faible',
              2 : u'faible',
              3 : u'moyenne',
              4 : u'assez élevée',
              5 : u'élevée',
              6 : u'forte',
              7 : u'très forte',
              8 : u'très forte',
              }
        self.ch = ch[self.val]
        

    def convAdm(self):
        ch = {0 : u'inadapté',
              1 : u'peu adapté',
              2 : u'satisfaisant',
              3 : u'bon',
              4 : u'excellent'
              }
        self.ch = ch[self.val]

    def copie(self,indice):
         self.val.set(indice.val.get())
         self.conv()

    def copy(self):
        return Indice(self.val)

    def AfficheDansArbre(self):
        return self.val
    
    def set(self,val):
        self.val = val
        self.conv()
    
    def get(self):
        return self.val
    

#############################################################################
#    Variable  Int  #
#############################################################################           
class IntVar:
    def __init__(self, val = 0, list = None):
        self.val = val
        self.list = list
        self.set(val)
        self.ch = ""
        
    def __repr__(self):
        return str(self.val)+ self.ch.encode('cp1252','replace')

    def get(self):
        return self.val
    
    def getCh(self):
        return self.list[self.val]
    
    def set(self,val):
        self.val = val
        if self.list is not None:
            self.ch = self.list[val]
            
    def copy(self):
        return IntVar(self.val)




###############################################################################
# Evenement indiquant que des données ont été modifiées dans le CdCF
###############################################################################
class CdCFModifiedEvent(wx.PyCommandEvent):
    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self,evtType,id)
        self.tag = 0
        self.critId = 0
        
    def SetCritId(self, id):
        self.critId = id
        
    def GetCritId(self):
        return self.critId
        
        
myEVT_CDCF_MODIFIED = wx.NewEventType()
EVT_CDCF_MODIFIED = wx.PyEventBinder(myEVT_CDCF_MODIFIED,1)


   
##############################################################################
#     Canvas Schéma CdCF     #
##############################################################################
class SchemaCdCF(wx.Panel):

    def __init__(self, master, cdcf, app):
        wx.Panel.__init__(self, master, -1,style = wx.CLIP_CHILDREN)
        self.evt = None
        
        # Chargement des images Schema CdCF
        Images.charger_imagesSchema()
        
        # Image du schema
        imgSchema = self.BitmapSchema(0)
        
        #Longueur par défaut des slider
        self.lgSlider = 60
        
        # Dimension du schema avec les fleches
#        self.x_Schema = 342
#        self.y_Schema = 164
        self.x_Schema = imgSchema.GetWidth() + 2 * self.lgSlider + 8
        self.y_Schema = imgSchema.GetHeight()+ self.lgSlider + 20
        
        self.master = master
        self.app = app
        self.cdcf = cdcf
        
        self.SetBackgroundColour('white')
        
        # Slider et Fleche 
        self.flecheCritere = {}
        self.sliderCritere = {}
        self.sliderVisibles = False
        
        # Sizer principal
        border = wx.GridBagSizer(1,0)
        
        # Création de la boite contenant le schema et les sliders
        #=========================================================
        self.boxSchema = wx.StaticBox(self, -1, u"Intensité et répartition",
                                 size = (self.x_Schema, self.y_Schema) )
        self.bsizer1 = wx.StaticBoxSizer(self.boxSchema, wx.VERTICAL)
        
        # Slider des charges
        #--------------------
        ali = {0 : wx.ALIGN_RIGHT,
               1 : wx.ALIGN_LEFT}
        
        for s in [0,1]:
            id = 500+s         # Efforts Axiaux
            dec = 4
            self.sliderCritere[id] = ScaleCdcf(self, deb = (1-s) * self.cdcf.echelleEffort,
                                               fin = s * self.cdcf.echelleEffort,
                                               orient = "H",
                                               numCrit = id,
                                               pos = (dec+s*(self.x_Schema-2*dec),30),
                                               ancre = s,
                                               align = ali[s])
            id = 510+s        # Efforts Radiaux
            self.sliderCritere[id] = ScaleCdcf(self,
                                               deb = 0,
                                               fin = self.cdcf.echelleEffort,
                                               orient = "V", 
                                               numCrit = 510+abs(s+1)/2,
                                               pos = (self.x_Schema/2+(2*s-1)*44, imgSchema.GetHeight()+16),
                                               ancre = s,
                                               maj = "GD",
                                               align = ali[s])
        # Intensité
        self.sliderCritere[512] = ScaleCdcf(self, deb = 0,
                                            fin = 100,
                                            orient = "V",
                                            numCrit = 512,
                                            pos = (self.x_Schema/2, 90),
                                            ancre = -1,
                                            maj = "PI",lg = 54)
        # Répartition
        self.sliderCritere[513] = ScaleCdcf(self, deb = -10,
                                            fin = 10,
                                            orient = "H",
                                            numCrit = 513,
                                            pos = (self.x_Schema/2, 140),
                                            ancre = -1,
                                            maj = "PI",lg = 54)
        
        
        # Création de la boite "Bague tournante" ##################################
        #=========================================================================
        sb = wx.StaticBox(self, -1, u"Mobilité bagues/charge radiale")
        rsb = wx.StaticBoxSizer(sb, wx.VERTICAL)
        st = wx.StaticText(self, -1, u"Bague tournante par rapport à la charge Radiale")
        
        rsb.Add(st)
        gbs = wx.GridBagSizer()
        radio1 = wx.RadioButton( self, 0, u'Intérieure', style = wx.RB_GROUP )
        radio2 = wx.RadioButton( self, 1, u'Extérieure' )
        radio1.SetToolTip(wx.ToolTip(u"à choisir si la bague intérieure est tournante\npar rapport à la charge radiale"))
        radio2.SetToolTip(wx.ToolTip(u"à choisir si la bague extérieure est tournante\npar rapport à la charge radiale"))
        gbs.Add(radio1, (0,0), flag = wx.ALIGN_CENTER_VERTICAL)
        gbs.Add(radio2, (1,0), flag = wx.ALIGN_CENTER_VERTICAL)
        im1 = wx.StaticBitmap(self, -1, Icones.BagueTournInt.GetBitmap())
        im2 = wx.StaticBitmap(self, -1, Icones.BagueTournExt.GetBitmap())
        
        self.radioBT = {"I" : radio1, "E" : radio2}
        
        gbs.Add(im1, (0,1))
        gbs.Add(im2, (1,1))
        rsb.Add(gbs, 0, wx.ALL, 5)
        
        self.Bind(wx.EVT_RADIOBUTTON, self.miseAJourSchema, radio1 )
        self.Bind(wx.EVT_RADIOBUTTON, self.miseAJourSchema, radio2 )
        
        
        # Initialisation affichage
        self.afficherTousCriteres()

        border.Add(self.boxSchema, (0,0))
        border.Add(rsb, (0,1))
        
        self.montrerSliders()
        self.SetSizerAndFit(border)
        self.cacherSliders()
        
#        self.Bind(EVT_CDCF_MODIFIED, self.miseAJourTousCriteres)
        
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        self.Bind(wx.EVT_MOTION,self.OnMove)
        
#        self.Bind(wx.EVT_KILL_FOCUS, self.OnLeave)
#        self.Bind(wx.EVT_SET_FOCUS, self.OnEnter)
        
        self.Bind(wx.EVT_SIZE, self.OnSize)
#        self.Bind(wx.EVT_BUTTON, self.miseAJourSchema)
#        self.Bind(wx.EVT_PAINT, self.OnPaint)
    
    
    #############################################################################            
    def OnSize(self, event):    
        self.montrerSliders()
#        self.Fit()
        self.cacherSliders()

    #############################################################################            
    def OnEnter(self, event):
        # le pointeur entre dans la zone du schéma
        if self.app.nbGauche.GetSelection() <> 2:
            self.montrerSliders()

    #############################################################################            
    def OnLeave(self, event):
        obj = event.GetEventObject()
        pos = event.GetPosition()
#        print pos,
        if obj in self.GetChildren():
#            print obj.GetPosition(),
            pos += obj.GetPosition()
#        else:
#            print obj,
#        pos = (event.m_x,event.m_y)
#        pos = (event.GetX(),event.GetX())
        basp = pos[1]
#        rec = event.GetEventObject().GetRect()
        rec = self.boxSchema.GetRect()
        basr = rec[3]
#        print rec.Contains(pos)
#        print basp, basr, basp > basr 
        if not rec.Contains(pos) \
           or basp > basr :
            self.cacherSliders()

    def OnMove(self, event):
        pos = event.GetPosition()
        rec = self.boxSchema.GetRect()
        if not rec.Contains(pos):
            self.cacherSliders()
        else:
            self.montrerSliders()
        

    ###########################################################################
    def miseAJourSchema(self, event = None):
        """ Modification de l'image du schéma
            et envoi évenement EVT_CDCF_MODIFIED
        """
        self.bmpSchema.SetBitmap(self.BitmapSchema(event.GetId()))
        self.cdcf._tree._treeData[52] = self.cdcf.codeBagueTournante(event.GetId())
        self.evt = CdCFModifiedEvent(myEVT_CDCF_MODIFIED, event.GetId())
        self.evt.SetCritId(52)
        self.GetEventHandler().ProcessEvent(self.evt)
        
            
    ###########################################################################
    def miseAJourTousCriteres(self,  event = None, fit = False):
        """ Met à jour les flêches du schéma et les positions des sliders.
            <event> permet de ne mettre à jour que le slider concerné
            <fit> assure un affichage correct de toutes les flèches (après ouverture)
        """
        
        if event is not None:
            id = event.GetId()
        else: id = None
        
#        print "  ",self.cdcf._tree._treeData[500].val, self.cdcf._tree._treeData[501].val
#        if id is not None:
#            self.sliderCritere[id].SetValueCrit(self.cdcf._tree._treeData[id])
            
        if id is None or self.sliderCritere[id].maj <> '':
            for id, item in self.sliderCritere.items():
                item.SetValueCrit(self.cdcf._tree._treeData[id])
            for id, item in self.flecheCritere.items():
                item.MaJ(self.cdcf._tree._treeData[id])
                if fit:
                    item.Fit()
        else:
            self.flecheCritere[id].MaJ(self.cdcf._tree._treeData[id])
            
#        print "Maj BT", self.cdcf._tree._treeData[52]
        self.radioBT[self.cdcf._tree._treeData[52]].SetValue(True)
        if  self.cdcf._tree._treeData[52] == "I":
            n = 0
        else:
            n = 1
        self.bmpSchema.SetBitmap(self.BitmapSchema(n))
        
        # Rafraichissement de l'affichage ???
        self.Fit()
        self.Refresh()
        self.Layout()
        
   
   
            
    ###########################################################################
    def afficherTousCriteres(self, event = None):
        ali = {0 : wx.ALIGN_RIGHT,
               1 : wx.ALIGN_LEFT}
        
        # Flèches 
        #========
        for s in [0,1]:
            style = ali[s]|wx.ST_NO_AUTORESIZE
            flag = ali[s]
            size = (45,-1)
            id = 500+s
            self.flecheCritere[id] = FlecheCdcfLegend(self, self.cdcf._tree._treeData[id], 
                                                      id,
                                                      orient = "H", sens = 1-s*2)
            id = 510+s
            self.flecheCritere[id] = FlecheCdcfLegend(self, self.cdcf._tree._treeData[id],
                                                      id,
                                                      orient = "V", sens = s*2-1)

        
        # Image du schéma
        #=================
        imgSchema = self.BitmapSchema(0)
        self.bmpSchema = wx.StaticBitmap(self, -1, imgSchema, 
                                         pos = ((self.x_Schema-imgSchema.GetWidth())/2, 14)
                                         )
        self.bsizer1.Add(self.bmpSchema)
        self.bmpSchema.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.bmpSchema.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        
        self.miseAJourTousCriteres()
            
            
    ##########################################################################
    def montrerSliders(self):
        if self.sliderVisibles:
            return
        for s in self.sliderCritere.values():
            s.Show()
        self.sliderVisibles = True

    ##########################################################################
    def cacherSliders(self):
        if not self.sliderVisibles:
            return
        for s in self.sliderCritere.values():
            s.Hide()
        self.sliderVisibles = False

    ##########################################################################
    def BitmapSchema(self, bagueTournante):
        imageSchema = Images.imageSchema ["Sch"]
        l,h = imageSchema.GetSize()
        if bagueTournante == 0:
            imageFleche = Images.imageSchema ["Fle"]
        else:
            imageFleche = Images.imageSchema ["Fba"]
 
        dx, dy = imageFleche.GetSize()
        x,y = (l-dx)/2 , (h-dy)/2
        
        bmp = wx.EmptyBitmap(l, h)
        dc = wx.MemoryDC(bmp)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        dc.DrawBitmap(imageSchema, 0, 0, True)
        dc.DrawBitmap(imageFleche,x,y, True)
        dc.SelectObject(wx.NullBitmap)
        
        return bmp

    def BitmapSchemaAvecFleches(self, bagueTournante):
        l,h = self.boxSchema.GetSize()
        bmp = wx.EmptyBitmap(l, h)
        dc = wx.MemoryDC(bmp)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        
        sch = self.BitmapSchema(bagueTournante)
        ls, hs = sch.GetWidth(), sch.GetHeight()
        x, y = l/2 - ls/2, 0
        dc.DrawBitmap(sch, x, y, True)
   
        dc.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT , wx.FONTSTYLE_ITALIC, wx.NORMAL))
        for id in [500, 501]:
            bmpf = self.flecheCritere[id].bmp.GetBitmap()
            lf = bmpf.GetWidth()
            x, y = l/2 + (2 * (id-500) - 1)*ls/2 - (501-id)* lf,  34
            dc.DrawBitmap(bmpf, x, y, True)
            txtf = self.flecheCritere[id].txt.GetLabel()
            lt, ht = dc.GetTextExtent(txtf)
            dc.DrawText(txtf, l/2 + (2 * (id-500) - 1)*ls/2 - (501-id)*lt, y+15)
            
        for id in [510, 511]:
            bmpf = self.flecheCritere[id].bmp.GetBitmap()
            lf = bmpf.GetWidth()
            x, y = l/2 + (2 * (id-510) - 1)*46 - (511-id)* lf,  hs
            dc.DrawBitmap(bmpf, x, y, True)
            txtf = self.flecheCritere[id].txt.GetLabel()
            lt, ht = dc.GetTextExtent(txtf)
            dc.DrawText(txtf, x-(511-id)*lt+(id-510)*lf, y+5)
            
        dc.SelectObject(wx.NullBitmap)

        return bmp

##############################################################################
#     Flèche CdCF     #
##############################################################################
class FlecheCdcfLegend(wx.Panel):
    def __init__(self, parent, indice, id, orient = "H", sens = 1):
        
        # Bit d'orientation
        if orient == "H": 
            v = 0
            o = wx.VERTICAL
        else: 
            v = 1
            o = wx.HORIZONTAL
        
        # Bit de sens
        s = (-sens+1)/2
        
        # Calcul de la dimension
        lg = parent.lgSlider #- 4
        if orient == "H":
            dim = (lg,30)
        else:
            dim = (lg+15,lg)
        
        
        # Calcul de la position
        posSlider = parent.sliderCritere[id].GetPosition()
        dimSlider = parent.sliderCritere[id].GetSizeTuple()
        if orient == "H":
            pos = (posSlider[0], posSlider[1] + dimSlider[1] -2)
        else:
            pos = (posSlider[0] + sens*((1-s)*dimSlider[0]+s*dim[0]), posSlider[1])
        
        wx.Panel.__init__(self, parent, id, pos, dim)#, style = wx.BORDER_SIMPLE)
        
        self.SetMinSize(dim)
        self.SetToolTip(wx.ToolTip(parent.sliderCritere[id].GetToolTip().GetTip()))
        
        sizer = wx.BoxSizer(o)
        
        self.indice = indice
        self.parent = parent
        self.orient = orient
        self.sens = sens
        
        # Flag de positionnement du texte
        if s: flagtxt = wx.ALIGN_LEFT
        else: flagtxt = wx.ALIGN_RIGHT
        if v:
            if flagtxt == wx.ALIGN_LEFT:
                flagtxt = wx.ALIGN_RIGHT
            else: 
                flagtxt = wx.ALIGN_LEFT
        
        # Flag de positionnement de la fleche
        if s: flagbmp = wx.ALIGN_LEFT
        else: flagbmp = wx.ALIGN_RIGHT
        
        if not v:
            flagbmp = flagbmp|wx.ALIGN_CENTER_VERTICAL
            
        self.bmp = wx.StaticBitmap(self, -1, self.FlecheCdcf(self.indice.val, orient, sens))
        self.bmp.SetToolTip(wx.ToolTip(parent.sliderCritere[id].GetToolTip().GetTip()))
        self.txt = wx.StaticText(self, -1, self.indice.ch, size = (lg, 14), style = flagtxt)
        self.txt.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT , wx.FONTSTYLE_ITALIC, wx.NORMAL))
        self.txt.SetForegroundColour('gray')
        self.txt.SetToolTip(wx.ToolTip(parent.sliderCritere[id].GetToolTip().GetTip()))
        # Mise en place dans le sizer
        sizer.Add(self.bmp,  flag = flagbmp)
        if v and s:
            sizer.Prepend(self.txt,  flag = flagtxt)
        else:
            sizer.Add(self.txt,  flag = flagtxt)
        
        self.SetSizer(sizer)
        
        parent.bsizer1.Add(self)
        
        self.Bind(wx.EVT_LEAVE_WINDOW, self.parent.OnLeave)
        self.Bind(wx.EVT_ENTER_WINDOW, self.parent.OnEnter)
        
        
    def MaJ(self, indice = None):
        if indice is not None:
            self.indice = indice
        self.bmp.SetBitmap(self.FlecheCdcf(self.indice.val, self.orient, self.sens))
#        self.val.SetLabel(str(self.indice.val))
        self.txt.SetLabel(self.indice.ch)
        self.Layout()
        self.SetSize(self.GetMinSize())
#        self.RecalcSizes()

    def FlecheCdcf(self, long, orient, sens):
        dc = wx.MemoryDC()
        # largeur totale
        e = 13
        # Pas
        p = 4
        # Bit de sens
        s = (-sens+1)/2 # vers la droite : 0 ; vers la gauche : 1
        # Bit d'orientation
        if orient == "V": 
            v = 1
        else: 
            v = 0
        # Bout de la Fleche
        lb, eb = 8, 3
        
        # longueur de la flèche seule
        lf = long*p+2
        
        # Position du texte    
        lt, ht = dc.GetTextExtent(str(long))
        xt,yt = s*(lf+5)*(1-v) + v*lt/2, v*(lf+2)
        
        # Dimension totale
        l,h = lf + lt + 2 + v*ht, e
        
        # Points extrémités de la Fleche
        x1,y1 = 1 + (1-v)*(1-s)*lt, e/2
        x2,y2 = x1 + lf, e/2
        
        if orient == "V":
            l,h = h,l
            x1,y1,x2,y2 = y1,x1,y2,x2

        if orient == "V":
            poly = [(x1,y1),(x1+eb, y1+lb), (x1-eb, y1+lb)]
            y1 = y1 + 4
        else:
            if sens == -1:
                xb,yb = x1,y1
                x1 = x1 + 3
            else:
                xb,yb = x2,y2
                x2 = x2 - 3
            poly = [(xb,yb),(xb-sens*lb, yb+eb), (xb-sens*lb, yb-eb)]
        
        bmp = wx.EmptyBitmap(l , h)
        dc.SelectObject(bmp)
        dc.SetBackground(wx.Brush(self.parent.GetBackgroundColour()))
        dc.Clear()
        
        dc.SetPen(wx.Pen("red", 3))
        dc.DrawLine(x1,y1,x2,y2)
        
        dc.SetPen(wx.Pen("red", 1))
        dc.SetBrush(wx.RED_BRUSH)
        if long > 0:
            dc.DrawPolygon(poly, fillStyle = wx.WINDING_RULE)
        
        dc.SetTextForeground("red")
        dc.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT , wx.FONTSTYLE_NORMAL, wx.NORMAL))
        dc.DrawText(str(long), xt, yt)
        
        return bmp
        
##############################################################################
#     Scale CdCF     #
##############################################################################
class ScaleCdcf(wx.Slider):
    """ Slider de CdCF
        <pos> = position en pixel
        <ancre> = point d'ancrage : -1 = Centre ; 0 = Gauche ; 1 = Droite
    """
    def __init__(self, parent, deb, fin, orient, numCrit, pos, ancre, 
                 maj = '', lg = -1, align = wx.ALIGN_CENTER ):
        self.maj = maj
        self.numCrit = numCrit
        self.critere = parent.cdcf._tree._treeData[numCrit]
        self.parent = parent
        self.buttonUp = False
        
        if lg == -1 : lg = parent.lgSlider
        
        if orient == "H":
            orient = wx.SL_HORIZONTAL 
            dim = (lg,lg/3)
            w = lg
        else:
            orient = wx.SL_VERTICAL
            dim = (lg/3,lg)
            w = 20
            if align == wx.ALIGN_LEFT:
                orient = orient|wx.SL_RIGHT
            else:
                orient = orient|wx.SL_LEFT
            
        if deb>fin:
            orient = orient|wx.SL_INVERSE
            de = fin
            fin = deb
            deb = de
        
        
        if ancre == 0:
            posit = pos
        elif ancre == 1:
            posit = (pos[0] - w ,pos[1])
        elif ancre == -1:
            posit = (pos[0] - w/2 ,pos[1])
        
#        print self.numCrit, type(self.critere)
    
        wx.Slider.__init__( self, parent, numCrit, self.critere.val, deb, fin,
                            point = posit, size = dim,
                            style = orient)
        self.MiseAJour(self.critere.val)
        
        parent.bsizer1.Add(self)
#        parent.sizer.Add(self,
#                         pos, span,
#                         flag = align 
#                         )
#        print (parent.master.GetBackgroundColour())
        self.SetOwnBackgroundColour('white')
        
        
        # Info bulle ###
        self.InfoBulle = wx.ToolTip(parent.cdcf._tree._treeLabelList[numCrit/10] + " : " + parent.cdcf._tree._treeLabelList[numCrit])
        self.SetToolTip(self.InfoBulle)
        
        # Evenements ##
        self.Bind(wx.EVT_LEAVE_WINDOW, self.parent.OnLeave)
        self.Bind(wx.EVT_ENTER_WINDOW, self.parent.OnEnter)
        self.parent.Bind(wx.EVT_SCROLL_CHANGED, self.OnChange, self)
#        self.parent.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.OnRelease, self)
        self.parent.Bind(wx.EVT_SCROLL_THUMBTRACK, self.OnScrollThumb, self)
#        self.parent.Bind(wx.EVT_SCROLL, self.OnScroll, self)
#        self.parent.Bind(wx.EVT_LEFT_UP, self.OnButtonUp, self)
#        self.parent.Bind(wx.EVT_LEFT_DOWN, self.OnButtonDown, self)

    ###############################################################################
    def OnScrollThumb(self,event):
#        print "EVT_SCROLL_THUMBTRACK",
#        print "Disable ToolTip"
        self.GetToolTip().Enable(False)
        val = event.GetInt()
        self.MiseAJour(val)
        self.parent.miseAJourTousCriteres(event)
        self.parent.Refresh()
#        event.Skip()
        
    ###############################################################################
    def SetValueCrit(self, critere = None):
        if critere is not None:
            self.critere = critere
        self.critere.set(self.critere.get())
#        print self.critere
        if isinstance(self.critere, Indice) or isinstance(self.critere, IntVar):
            self.SetValue(self.critere.get())
        else:
            if self.maj == "GD":
                self.parent.cdcf.tradGD_PI()
            elif self.maj == "PI":
                self.parent.cdcf.tradPI_GD()
            self.SetValue(self.critere)
        
        
    
    ###############################################################################
    def MiseAJour(self, val):
#        print "Mise a jour"
        if isinstance(self.critere, Indice) or isinstance(self.critere, IntVar):
            self.critere.set(val)
        else:
            self.critere = val
        
        if self.maj == "GD":
            self.parent.cdcf.tradGD_PI()
        elif self.maj == "PI":
            self.parent.cdcf.tradPI_GD()

        
    def OnChange(self, event):
#        print "CHANGE"
        self.OnRelease(event)

    ###############################################################################
    def OnRelease(self,event):
#        print "OnRelease"
        event.Skip(False)
        val = event.GetInt()
        self.MiseAJour(val)
        
        self.parent.evt = CdCFModifiedEvent(myEVT_CDCF_MODIFIED, self.GetId())
        self.parent.evt.SetCritId(self.numCrit)
        self.parent.GetEventHandler().ProcessEvent(self.parent.evt)
        
        self.GetToolTip().Enable(True)
#        print "Enable ToolTip"
#        event.Skip()
        


##############################################################################
#     Zone du CdCF Cout    #
##############################################################################
class ZoneCdCFCout(wx.Panel):
    def __init__(self, master, cdcf, app):
        wx.Panel.__init__(self, master, -1, style = wx.CLIP_CHILDREN)
        self.evt = None
        self.master = master
        self.cdcf = cdcf
        self.critere = self.cdcf._tree._treeData[70]
        
        border = wx.GridBagSizer(1,0)

        self.controls = {}
#        self.scalesAffichees = False
#        self.scales = []
        

        # Création de la boite contenant le slider "coüt"
        #=================================================
        self.controls[70] = Slider_Spin(self, u"Coût indicatif maximum", self.critere, 70,
                           (0, self.cdcf.echelleCout), 2, 5)
        self.controls[70].SetToolTip(u"Réglage du coût indicatif maximum du montage")
        
#        self.boxSchema = wx.StaticBox(self, -1, u"Coût indicatif maximum")
#        self.boxSchema.SetToolTip(wx.ToolTip(u"Réglage du coût indicatif maximum du montage"))
#        self.bsizer = wx.StaticBoxSizer(self.boxSchema, wx.VERTICAL)
#                           
##        self.st = wx.StaticText(self, -1, str(self.critere))
##        self.bsizer.Add(self.st)
#
#        self.sp = wx.SpinCtrl(self, -1, str(self.critere.val),
#                              style = wx.SP_ARROW_KEYS | wx.SP_WRAP)
#        self.sp.SetRange(0, self.cdcf.echelleCout)
#        self.bsizer.Add(self.sp, flag = wx.ALIGN_CENTRE)
#        
#        self.sl = wx.Slider(self, -1, self.critere.val, 0, self.cdcf.echelleCout,
#                            size = (self.cdcf.echelleCout*2+28, -1),
#                            style = wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS | wx.SL_TOP)
#        self.sl.SetTickFreq(5)
#        self.sl.SetThumbLength(self.cdcf.echelleCout*2)
#        self.sl.SetToolTip(wx.ToolTip(u"Faire glisser pour modifier le coût indicatif maximum"))
#        self.bsizer.Add(self.sl)
        
        border.Add(self.controls[70], (0,0))
        self.SetSizerAndFit(border)
        
#        self.bsizer.FitInside(self)
#        self.SetSizer(self.bsizer)
#        self.Bind(EVT_CDCF_MODIFIED, self.miseAJourTousCriteres)
#        self.Bind(wx.EVT_SCROLL_CHANGED, self.OnRelease, self.sl)
#        self.Bind(wx.EVT_SCROLL_THUMBTRACK, self.OnScrollThumb, self.sl)
#        self.Bind(wx.EVT_SPINCTRL, self.OnRelease, self.sp)
        
        
#        self.Bind(EVT_CDCF_MODIFIED, self.MiseAJour)

    ###########################################################################
    def miseAJourTousCriteres(self,  event = None, fit = False):
        """ Met à jour les flêches du schéma et les positions des sliders.
            <event> permet de ne mettre à jour que le slider concerné
            <fit> assure un affichage correct de toutes les flèches (après ouverture)
        """
        
        if event is not None:
            id = event.GetId()
        else: id = None
        
#        print "  ",self.cdcf._tree._treeData[500].val, self.cdcf._tree._treeData[501].val
#        if id is not None:
#            self.sliderCritere[id].SetValueCrit(self.cdcf._tree._treeData[id])
        for id, item in self.controls.items():
            if isinstance(item, Slider_Spin):
                item.critere = self.cdcf._tree._treeData[id]
                item.SetValue(self.cdcf._tree._treeData[id].val)
            elif isinstance(item, wx.Choice):
                item.SetSelection(self.cdcf._tree._treeData[id].val)
        
        
#        if id is None or self.sliderCritere[id].maj <> '':
#            for id, item in self.sliderCritere.items():
#                item.SetValueCrit(self.cdcf._tree._treeData[id])
#            for id, item in self.flecheCritere.items():
#                item.MaJ(self.cdcf._tree._treeData[id])
#                if fit:
#                    item.Fit()
#        else:
#            self.flecheCritere[id].MaJ(self.cdcf._tree._treeData[id])
            
            
        # Rafraichissement de l'affichage ???
        self.Fit()
        self.Refresh()
        self.Layout()
    ###############################################################################
#    def OnScrollThumb(self,event):
#        val = event.GetInt()
#        self.MiseAJour(val)
#        self.sp.SetValue(val)
#        self.sl.SetValue(val)
#        self.master.Refresh()
#        
#        
#    ###############################################################################
#    def OnRelease(self,event):
##        print "OnRelease"
#        self.OnScrollThumb(event)
#        event.Skip(False)
#        val = event.GetInt()
#        
#        self.evt = CdCFModifiedEvent(myEVT_CDCF_MODIFIED, self.GetId())
#        self.evt.SetCritId(70)
#        self.GetEventHandler().ProcessEvent(self.evt)
#        
#        
#    ###############################################################################
#    def MiseAJour(self, val):
#        self.critere.set(val)
##        print "Mise à jour coût :", val, self.cdcf.coutMax  
##        self.st.SetLabel(str(self.cdcf.coutMax))
#        
#        
#    ##########################################################################
#    def modifier(self, event = None, temps = 1000):
#        if (not self.scalesAffichees) and (not self.root.modeAnalyse):
#            print "Modif CdCF"
#            self.action = self.root.after(temps,self.afficherScales)
#            self.root.zoneMessage.afficher('ModifCdCF',True)
#            self.scalesAffichees = True
#
# 
#    ##########################################################################
#    def afficher(self, event = None):
#        if not self.root.modeAnalyse:
#            self.root.after_cancel(self.action)
#            self.effacerScales()
#            self.root.zoneMessage.restaurer()
#            self.scalesAffichees = False
#
#            
#    ##########################################################################
#    def afficherScales(self):
#        for s in self.scales.values():
#            s.grid()
#
#    ##########################################################################
#    def effacerScales(self):
#        for s in self.scales.values():
#            s.grid_remove()
#            
#    ##########################################################################
#    def afficherCriteres(self):
#        pass

##############################################################################
#     Zone du CdCF Cout    #
##############################################################################
class ZoneCdCFEtancheite(wx.Panel):
    def __init__(self, master, cdcf, app):
        wx.Panel.__init__(self, master, -1, style = wx.CLIP_CHILDREN)
        self.evt = None
        self.master = master
        self.cdcf = cdcf
        
        self.critere = {60 : self.cdcf._tree._treeData[60],
                        61 : self.cdcf._tree._treeData[61],
                        62 : self.cdcf._tree._treeData[62]}
        
        border = wx.GridBagSizer(1,1)

        self.controls = {}
#        self.scalesAffichees = False
#        self.scales = []
        
        # Pression relative
        #-------------------
        self.controls[60] = Slider_Spin(self, u"Pression relative", self.critere[60], 60,
                           (0, self.cdcf.echellePression),
                           10, 1)
        self.controls[60].SetToolTip(u"Réglage de la pression relative intérieur/extérieur")

        
#       # Lubrification
        #---------------
        box = wx.StaticBox(self, -1, u"Type de lubrification", size = self.controls[60].box.GetSize())
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        pnl = wx.Panel(self, -1)
        self.controls[62] = wx.Choice(pnl, 62, choices = lstLubrif, size = (100,-1) )
        self.controls[62].SetSelection(self.critere[62].val)
        self.controls[62].SetToolTip(wx.ToolTip(u"Choix du type de lubrification"))
        self.Bind(wx.EVT_CHOICE, self.EvtChoice, self.controls[62])
        
        self.img = wx.StaticBitmap(self, -1, wx.NullBitmap)
        self.MaJImage()
        
#        pnl.SetMinSize((110, self.controls[60].box.GetSize()[1]-22))
        bsizer.Add(pnl, flag = wx.ALIGN_CENTRE)
        bsizer.Add(self.img, flag = wx.ALIGN_CENTRE)
#        print "taille box", pnl.GetMinSize()
        
        # Vitesse de rotation
        #---------------------
        self.controls[61] = Slider_Spin(self, u"Vitesse de rotation", self.critere[61], 61,
                           (0, self.cdcf.echelleVitesse),
                           10, 1)
        self.controls[61].SetToolTip(u"Réglage de la vitesse de rotation")
        
        border.Add(self.controls[60], (0,0))
        border.Add(bsizer, (0,1))
        border.Add(self.controls[61], (0,2))
        self.SetSizerAndFit(border)
        
#        self.bsizer.FitInside(self)
#        self.SetSizer(self.bsizer)
#        self.Bind(EVT_CDCF_MODIFIED, self.miseAJourTousCriteres)
#        self.Bind(wx.EVT_SCROLL_CHANGED, self.OnRelease, self.sl)
#        self.Bind(wx.EVT_SCROLL_THUMBTRACK, self.OnScrollThumb, self.sl)
#        self.Bind(wx.EVT_SPINCTRL, self.OnRelease, self.sp)
        
        
#        self.Bind(EVT_CDCF_MODIFIED, self.MiseAJour)


#    ###############################################################################
#    def OnScrollThumb(self, event):
#        
#        val = event.GetInt()
##        print val
#        self.MiseAJour(val)
#        self.sp.SetValue(val)
#        self.sl.SetValue(val)
#        self.master.Refresh()
#        
#        
#    ###############################################################################
#    def OnRelease(self, event):
##        print "OnRelease"
#        self.OnScrollThumb(event)
#        event.Skip(False)
#        val = event.GetInt()
#        
#        self.evt = CdCFModifiedEvent(myEVT_CDCF_MODIFIED, self.GetId())
#        self.evt.SetCritId(60)
#        self.GetEventHandler().ProcessEvent(self.evt)
#
#        
    ###############################################################################
    def EvtChoice(self, event):
        event.Skip(False)
        val = event.GetInt()
        idCrit = event.GetId()
        self.critere[idCrit].set(val)
        self.MaJImage()
        self.evt = CdCFModifiedEvent(myEVT_CDCF_MODIFIED, self.GetId())
        self.evt.SetCritId(idCrit)
        self.GetEventHandler().ProcessEvent(self.evt)
        
    def MaJImage(self):
        if self.critere[62].val == 0:
            self.img.SetBitmap(Icones.LubrifHuile.GetBitmap())
        elif self.critere[62].val == 1:
            self.img.SetBitmap(Icones.LubrifGraisse.GetBitmap())
        else :
            x,y = Icones.LubrifGraisse.GetBitmap().GetSize()
            imgVide = wx.EmptyBitmap(x,y)
            imgVide.SetMask(wx.Mask(imgVide))
            self.img.SetBitmap(imgVide)
#        self.Fit()
#        self.Refresh()
#        self.Layout()
        
    ###########################################################################
    def miseAJourTousCriteres(self,  event = None, fit = False):
        """ Met à jour les flêches du schéma et les positions des sliders.
            <event> permet de ne mettre à jour que le slider concerné
            <fit> assure un affichage correct de toutes les flèches (après ouverture)
        """
#        print "Mise a jour CdCFEtancheite"
        
        if event is not None:
            id = event.GetId()
        else: id = None
        
        self.critere = {60 : self.cdcf._tree._treeData[60],
                        61 : self.cdcf._tree._treeData[61],
                        62 : self.cdcf._tree._treeData[62]}
#        print "  ",self.cdcf._tree._treeData[500].val, self.cdcf._tree._treeData[501].val
#        if id is not None:
#            self.sliderCritere[id].SetValueCrit(self.cdcf._tree._treeData[id])
        for id, item in self.controls.items():
            if isinstance(item, Slider_Spin):
                item.critere = self.cdcf._tree._treeData[id]
                item.SetValue(self.cdcf._tree._treeData[id].val)
            elif isinstance(item, wx.Choice):
                if self.cdcf._tree._treeData[id].val is None:
                    self.cdcf._tree._treeData[id].set(0)
                item.SetSelection(self.cdcf._tree._treeData[id].val)
        
        self.MaJImage()
        
#        if id is None or self.sliderCritere[id].maj <> '':
#            for id, item in self.sliderCritere.items():
#                item.SetValueCrit(self.cdcf._tree._treeData[id])
#            for id, item in self.flecheCritere.items():
#                item.MaJ(self.cdcf._tree._treeData[id])
#                if fit:
#                    item.Fit()
#        else:
#            self.flecheCritere[id].MaJ(self.cdcf._tree._treeData[id])
            
            
        # Rafraichissement de l'affichage ???
        self.Fit()
        self.Refresh()
        self.Layout()

##############################################################################
#     Zone du CdCF Etancheité    #
##############################################################################
#class ZoneCdCFEtanch(Frame):
#    """La Zone affichant CdCF à l'écran"""
#    def __init__(self, master, root, cdcf = None):
#        
#        Frame.__init__(self, master)
#        
#        self.cdcf = cdcf
#        
#        self.root = root
#
#        self.scalesAffichees = False
#
#        #  Zone Etancheité   ##################                     
#        self.zoneEtanch = Frame(self)
#        self.zoneEtanch.grid(row = 1, column = 1, sticky = SW)
#
#        #  Pression ###########################
#        t = Label(self.zoneEtanch, text = u"Pression relative", \
#              font = Const.Font_CdCFTitre[0],
#              fg = Const.Font_CdCFTitre[1],
#              justify = LEFT, 
#              anchor = NE) 
#        t.grid(row = 0, column = 0, padx = 5,  sticky = NE)
#        Const.InfoBulleSimple(t, 'CdCFPress')
#        
#        
#        Label(self.zoneEtanch, textvariable = self.cdcf.pression, \
#              font = Const.Font_CdCFValeur[0],
#              fg = Const.Font_CdCFValeur[1],
#              justify = LEFT,
#              anchor = NW,
#              height = 1,
#              width = 2) \
#              .grid(row = 0,column = 1,  sticky = NW)
#
#        Label(self.zoneEtanch, textvariable = self.cdcf.cotePression, \
#              font = Const.Font_CdCFMoy[0],
#              fg = Const.Font_CdCFMoy[1],
#              justify = LEFT,
#              anchor = NW,
#              height = 1,
#              width = 9) \
#              .grid(row = 0,column = 2,  sticky = NW)
#
#        #  Vitesse ###########################
#        t = Label(self.zoneEtanch, text = u"Vitesse angulaire", \
#              font = Const.Font_CdCFTitre[0],
#              fg = Const.Font_CdCFTitre[1],
#              justify = LEFT, 
#              anchor = NE) 
#        t.grid(row = 2, column = 0, padx = 5,  sticky = NE)
#        Const.InfoBulleSimple(t, 'CdCFVitt')
#
#        Label(self.zoneEtanch, textvariable = self.cdcf.vitesse, \
#              font = Const.Font_CdCFValeur[0],
#              fg = Const.Font_CdCFValeur[1],
#              justify = LEFT,
#              anchor = NW,
#              height = 1,
#              width = 2) \
#              .grid(row = 2,column = 1,  sticky = NW)
#
#        #  Lubrifiant  ###########################
#        t = Label(self.zoneEtanch, text = u"Type de lubrifiant", \
#              font = Const.Font_CdCFTitre[0],
#              fg = Const.Font_CdCFTitre[1],
#              justify = LEFT, 
#              anchor = NE) 
#        t.grid(row = 10, column = 0, padx = 5,  sticky = NE)
#        Const.InfoBulleSimple(t, 'CdCFPress')
#
#        t = Label(self.zoneEtanch, textvariable = self.cdcf.lubrifiant, \
#              font = Const.Font_CdCFValeur[0],
#              fg = Const.Font_CdCFValeur[1],
#              justify = LEFT,
#                  width = 8,
#              anchor = NW) 
#        t.grid(row = 10, column = 1, padx = 5, rowspan = 2, sticky = NW)
#        Const.InfoBulleSimple(t, 'CdCFPress')
#
#        # Scales ############################################
#        self.scales = {}
#        self.scales["press"] = Scale(self.zoneEtanch,
#                                 from_ = -self.cdcf.echellePression,
#                                 to = self.cdcf.echellePression,
#                                 orient = HORIZONTAL, 
#                                 variable = self.cdcf.pression,
#                                 length = 100,
#                                 width = 10,
#                                 relief = SOLID, bd = 0,
#                                 showvalue = 0,
#                                 command = self.modifCote)
#        self.scales["press"].grid(column = 0, row = 0, columnspan = 3)
#        Const.InfoBulleSimple(self.scales["press"], 'CdCFCurs')
#
#        self.scales["vitt"] = Scale(self.zoneEtanch,
#                                 from_ = 0,
#                                 to = self.cdcf.echelleVitesse,
#                                 orient = HORIZONTAL, 
#                                 variable = self.cdcf.vitesse,
#                                 length = 100,
#                                 width = 10,
#                                 relief = SOLID, bd = 0,
#                                 showvalue = 0)
#        self.scales["vitt"].grid(column = 0, row = 2, columnspan = 3)
#        Const.InfoBulleSimple(self.scales["vitt"], 'CdCFCurs')
#
#        self.scales["lubrif"] = Tix.ComboBox(self.zoneEtanch,
#                                        editable=1, dropdown=1,
#                                        variable = self.cdcf.lubrifiant)
#        self.scales["lubrif"].subwidget_list["entry"].configure(width = 8)
#        self.scales["lubrif"].subwidget_list["slistbox"].subwidget_list["listbox"].configure(height = 2,
#                                        width = 1)
#
#        self.scales["lubrif"].grid(row = 10,column = 1, columnspan = 2, sticky = W)
#        for item in lstLubrif.values():
#            self.scales["lubrif"].insert(END, item)
#        Const.InfoBulleSimple(self.scales["lubrif"], 'CdCFPress')
#
#        
#        self.zoneEtanch.rowconfigure(0,minsize = 50)
#
#        self.zoneEtanch.rowconfigure(2,minsize = 50)
#
#
#        self.effacerScales()
#
#        master.bind('<Enter>',self.modifier)
#        master.bind('<Leave>',self.afficher)
#
#
#    ##########################################################################
#    def modifier(self, event = None, temps = 1000):
#        if (not self.scalesAffichees) and (not self.root.modeAnalyse):
#            print "Modif CdCF"
#            self.action = self.root.after(temps,self.afficherScales)
#            self.root.zoneMessage.afficher('ModifCdCF',True)
#            self.scalesAffichees = True
#
# 
#    ##########################################################################
#    def afficher(self, event = None):
#        if not self.root.modeAnalyse \
#           and not self.scales["lubrif"].subwidget_list["slistbox"].winfo_ismapped():
#            self.root.after_cancel(self.action)
#            self.effacerScales()
#            self.root.zoneMessage.restaurer()
#            self.scalesAffichees = False
#
#            
#    ##########################################################################
#    def afficherScales(self):
#        for s in self.scales.values():
#            s.grid()
#
#
#    ###########################################################################
#    def modifLubrif(self, event = None, ):
#        i=listbox.curselection()  ## Récupération de l'index de l'élément sélectionné
#        return listbox.get(i)  ## On retourne l'élément (un string) sélectionné
#
#
#        
#    ##########################################################################
#    def modifCote(self, event = None):
#        if self.cdcf.pression.get() != 0:
#            sg = abs(self.cdcf.pression.get())/self.cdcf.pression.get()
#        else:
#            sg = 0
#        self.cdcf.cotePression.set(pression[sg])
#
#    ##########################################################################
#    def effacerScales(self):
###        print "Suppression Scales ..."
#        for s in self.scales.values():
#            s.grid_remove()
#            
#    ##########################################################################
#    def afficherCriteres(self):
#        pass
#        

class Slider_Spin(wx.Panel):
    def __init__(self, parent, label, critere, idCrit, range, coef, tickfreq):
        wx.Panel.__init__(self, parent, -1)
        self.critere = critere
        self.parent = parent
        self.idCrit = idCrit
        
        self.box = wx.StaticBox(self, -1, label)
        self.bsizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
                           
        self.spin = wx.SpinCtrl(self, -1, str(critere.val),
                                style = wx.SP_ARROW_KEYS | wx.SP_WRAP)
        self.spin.SetRange(range[0], range[1])
        self.bsizer.Add(self.spin, flag = wx.ALIGN_CENTRE)
        
        self.slider = wx.Slider(self, -1, critere.val, range[0], range[1],
                                size = ((range[1]-range[0])*coef+28, -1),
                                style = wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS | wx.SL_TOP)
        self.slider.SetTickFreq(tickfreq)
        self.slider.SetThumbLength(range[1]-range[0])
        self.bsizer.Add(self.slider, flag = wx.ALIGN_CENTRE)
        
        self.SetSizerAndFit(self.bsizer)
        
        self.parent.Bind(wx.EVT_SCROLL_CHANGED, self.OnRelease, self.slider)
        self.parent.Bind(wx.EVT_SCROLL_THUMBTRACK, self.OnScrollThumb, self.slider)
        self.parent.Bind(wx.EVT_SPINCTRL, self.OnRelease, self.spin)

    ###############################################################################
    def SetToolTip(self, tip):
        self.box.SetToolTip(wx.ToolTip(tip))
        self.slider.SetToolTip(wx.ToolTip(tip))
        self.spin.SetToolTip(wx.ToolTip(tip))
        
    ###############################################################################
    def OnScrollThumb(self, event):
        val = event.GetInt()
        self.MiseAJour(val)
        self.SetValue(val)

        
    ###############################################################################
    def OnRelease(self, event):
        self.OnScrollThumb(event)
        event.Skip(False)
#        val = event.GetInt()
        self.parent.evt = CdCFModifiedEvent(myEVT_CDCF_MODIFIED, self.GetId())
        self.parent.evt.SetCritId(self.idCrit)
        self.parent.GetEventHandler().ProcessEvent(self.parent.evt)

    ###############################################################################
    def MiseAJour(self, val):
        self.critere.set(val)
        
        
    def SetValue(self, val):
        self.spin.SetValue(val)
        self.slider.SetValue(val)
        self.parent.master.Refresh()
        
