#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##This file is part of PyVot
#############################################################################
#############################################################################
##                                                                         ##
##                                  Analyse                                ##
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
import wx.lib.buttons as buttons
import wx.lib.stattext as st
import  wx.grid as gridlib
#from wx.lib.wordwrap import wordwrap
#from textwrap import fill
import Const

import globdef
from globdef import *

import Montage
import Images, Icones
import time
from math import sin,pi,cos
from Affichage import DCPlus

    
StyleText = {}
Couleur = {}
def charger_styleText():
    Couleur["rouge"] = wx.RED
    Couleur["vert"]  = wx.ColourDatabase().Find("FOREST GREEN")
    Couleur["bleu"]  = wx.BLUE
    StyleText["Titre1"] = Const.StyleDeTexte(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD, True),wx.BLUE)
    StyleText["Titre2"] = Const.StyleDeTexte(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False),wx.BLACK)
    StyleText["Messag"] = Const.StyleDeTexte(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD, False),wx.RED) 
    StyleText["Normal"] = Const.StyleDeTexte(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False),wx.BLACK)
    StyleText["Message"] = Const.StyleDeTexte(wx.Font(8, wx.DEFAULT, wx.ITALIC, wx.NORMAL, False),wx.BLACK)
    StyleText["Gras"] = Const.StyleDeTexte(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, False),wx.BLACK)



#####################################################
# Zone de résultats   ###############################
#####################################################
class ZoneResultats(wx.Panel):
    def __init__(self, parent, analyse, liaison = True):
        wx.Panel.__init__(self, parent, -1)
#                          style=wx.NO_FULL_REPAINT_ON_RESIZE)
        
        self.parent = parent
        self.analyse = analyse
#        print self.analyse
        # Structure principale
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.boutons = {}
        self.statBox = {}
        self.statBoxSizer = {}
        self.boutonSizer = {}
        
        if liaison and analyse.montageVide:
            self.MessagePasDeRoulement()
            
        self.Bind(wx.EVT_BUTTON, self.OnClick)
        

    ############################################################
    def MessagePasDeRoulement(self):
        StyleText["Message"].applique(self, wx.BLACK)
        txt = StaticTextWrapped(self, -1, u"Il faut au moins un roulement pour faire une liaison pivot !",
                                style = wx.ALIGN_CENTRE)
        self.sizer.Add(txt) #, (0,0), (1,1), wx.ALIGN_CENTRE|wx.ALIGN_BOTTOM)
        self.SetSizerAndFit(self.sizer)
       
    ############################################################# 
    def OnClick(self, event):
        return
    
    ############################################################# 
    def MakeStaticBox(self, id, titre, style = wx.VERTICAL):
        StyleText["Titre1"].applique(self)
        self.statBox[id] = wx.StaticBox(self, -1, titre)
        self.statBoxSizer[id] = wx.StaticBoxSizer(self.statBox[id], style)
        self.sizer.Add(self.statBoxSizer[id], flag = wx.ALIGN_CENTRE|wx.EXPAND)
        
    def MakeBoutonSizer(self, id, h = 1, v = 1):
        self.boutonSizer[id] = wx.GridBagSizer(h,v)
        self.statBoxSizer[id].Add(self.boutonSizer[id], flag = wx.ALIGN_CENTRE)
#        self.Add(id, self.boutonSizer[id])
        
    def StaticTextMessage(self, message, style = "Messag", wrapFact = None):
        StyleText[style].applique(self, Couleur[message.coul])
        stw = StaticTextWrapped(self, -1, message.mess)
        if wrapFact != None:
            stw.SetWrapFact(wrapFact)
        return stw
        
    def Add(self, id, objet, flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALIGN_LEFT|wx.TOP|wx.BOTTOM, border = 10):
        self.statBoxSizer[id].Add(objet, flag = flag, border = border)
        
    def AddBouton(self, id, objet, pos, span = (1,1), flag = wx.ALIGN_CENTRE):
        self.boutonSizer[id].Add(objet, pos, span, flag = flag)


#####################################################
# Immobilisation axiale #############################
#####################################################
class ZoneImmobAx(ZoneResultats):
    def __init__(self, parent, analyse):
#        print "Zone ImmobAx"
        ZoneResultats.__init__(self, parent, analyse),
#                          style=wx.NO_FULL_REPAINT_ON_RESIZE)
#        print analyse.chaineAct[0]
        
        if analyse.montageVide:
            return
        
        self.Freeze()
        
        self.labels = {}
        
        self.MakeStaticBox("1", u"Mise en position axiale")
        
        # Resultat principal
        #####################
        
        self.Add("1", self.StaticTextMessage(analyse.messageImmobilisation))
        
        # Boutons
        #####################
        self.MakeBoutonSizer("1", 4,10)        
        c = 0
        for s in [1,0]: # différents sens ...
            sizerResult = wx.BoxSizer(wx.VERTICAL)
            for mess in analyse.resultatImmobilisation[s]:
                sizerResult.Add(self.StaticTextMessage(mess, style = "Normal", wrapFact = 2))
            self.AddBouton("1", sizerResult,
                           (0,c), (1,1), wx.ALIGN_CENTRE|wx.EXPAND)
            
            # Bouton "Animer"
            #----------------
#            if True:#parent.master.options.proposerAnimArret.get() == 1 \
            if analyse.resultatImmobilisation[s][0].clef == 'ArretArbreSens':
                tag = "Arret"+ str(s)
                self.boutons[tag] = buttons.ThemedGenBitmapButton(self, 10+s , 
                                                                  Images.Img_BoutonMont(tag), 
                                                                  style = wx.BORDER_NONE)
                self.boutons[tag].SetToolTipString(Const.bulles['AnalyAnim'])

            # Bouton "Chaine"
            #----------------
#            elif True:#parent.master.options.proposerChaines.get() == 1 \
            elif analyse.resultatImmobilisation[s][0].clef == 'ImmobCorrect':
                tag = "Chaine"+ str(s)
                self.boutons[tag] = buttons.ThemedGenBitmapToggleButton(self, 20+s, 
                                                                        None, 
                                                                        style = wx.BORDER_NONE)
                
                self.boutons[tag].SetBitmapLabel(Images.Img_BoutonMont(tag))
                self.boutons[tag].SetInitialSize()
                self.boutons[tag].SetToolTipString(Const.bulles['AnalyChai'])


            # On place les widgets ...
            #-------------------------
            if self.boutons.has_key(tag):
                self.AddBouton("1", self.boutons[tag], (1,c), (1,2))
#                sizerBoutons.Add(self.boutons[tag], (1,c), (1,2), flag = wx.ALIGN_CENTRE)
            
       
#            # Label "Hyperstatique"
#            #----------------------
##            if parent.master.options.proposerChaines.get() == 1 \
#            if len(analyse.resultatImmobilisation[s])>1:
#                StyleText["Messag"].applique(self, analyse.resultatImmobilisation[s][1].coul)#"bleu")
#                self.labels["Hyper"] = wx.StaticText(self, -1, 
#                                                     analyse.resultatImmobilisation[s][1].mess)
#                self.AddBouton("1", self.labels["Hyper"], (3,c), (1,2))
##                sizerBoutons.Add(self.labels["Hyper"], (3,c), (1,2), flag = wx.ALIGN_CENTRE)
#                self.labels["Hyper"].SetToolTipString(Const.bulles['AnalyHypr'])

            tag = None

            c += 2

        # Schéma de structure
        #--------------------
        self.MakeStaticBox("2", u"Schéma de structure")
        self.Add("2", wx.StaticBitmap(self, -1, analyse.imageSchema),
                 flag = wx.ALIGN_CENTRE, border = 0)
        
        self.SetSizerAndFit(self.sizer)
        
        self.Thaw()
        
        self.Refresh()
        
    
    def initAffichage(self, zmont = None):
        for b in self.boutons.values():
            if isinstance(b, buttons.ThemedGenBitmapToggleButton):
                self.OnClick(id = b.GetId(), act = False)
                b.SetToggle(False)
    
#    def OnSize(self, event = None):
##        print self.GetClientSizeTuple()[0]
#        self.txt.SetLabel(self.txt.GetLabel().replace('\n',' '))
##        self.txt.SetLabel(self.mess)
#        self.txt.Wrap(self.GetClientSizeTuple()[0])
##        self.txt.Wrap(-1)
#        self.Fit()
#        event.Skip()
       
    def OnClick(self, event = None, id = None, act = None):
        if id is None: id = event.GetId()
#        print "Click",id, act
        if id in [10,11]:
            self.parent.animerElemNonArretes(id-10)
        elif id in [20,21]:
            if act is None: act = event.GetIsDown()
            self.parent.gererAffichageChaines(id-20, act )




#####################################################
# Résistance aux Charges ############################
#####################################################
class ZoneResistance(ZoneResultats):
    def __init__(self, parent, analyse):
        ZoneResultats.__init__(self, parent, analyse)

        if analyse.montageVide:
            return
        
        self.Freeze()

        # Résistance axiale du montage
        #####################################################
        self.MakeStaticBox("1", u"Résistance axiale du montage")

        # Resultat principal
        self.Add("1", self.StaticTextMessage(analyse.messageResistanceAxiale))
        
        # Boutons
        self.MakeBoutonSizer("1", 4,10) 
        
        self.listeActive = {}

        for s in [1,0]:
            c = 1-s # Colonne du sizerMtg
            sizerResult = wx.BoxSizer(wx.VERTICAL)
            for mess in analyse.resultatEffortAxialMtg[s]:
                sizerResult.Add(self.StaticTextMessage(mess, style = "Normal", wrapFact = 2))
            self.AddBouton("1", sizerResult,
                           (0,c), (1,1), wx.ALIGN_CENTRE|wx.EXPAND)
            # Bouton "Détail"
            #----------------
#            if parent.master.options.proposerChaines.get() == 1 \
            if analyse.resultatEffortAxialMtg[s][0].clef == 'ElemResistPas':
                tag = "_Chaine"+ str(s)
                if True:#master.master.options.proposerChaines.get() <> 0 :
                    self.boutons["_"+tag] = buttons.ThemedGenBitmapToggleButton(self, 30+s, 
                                                                                Images.Img_BoutonMont(tag), 
                                                                                style = wx.BORDER_NONE)
                    self.boutons["_"+tag].SetInitialSize()
                    self.boutons["_"+tag].SetToolTipString(Const.bulles['AnalyChai'])
#                    self.listeActive[s] = ListeActive(self, self.lstNom(s), self.boutons["_"+tag])
#                    self.listeActive[s].SetToolTipString(Const.bulles['SelectRoul'])
#                    self.AddBouton("1", self.listeActive[s].symboleDevelop, (1,c),(1,1), 
#                              wx.ALIGN_CENTRE|wx.ALIGN_BOTTOM)
#                    self.AddBouton("1", self.listeActive[s], (2+c,0), (1,2), 
#                              wx.ALIGN_CENTRE|wx.ALIGN_TOP)

                    rr = 2
                        
            # Bouton "Chaine"
            #----------------
#            elif parent.master.options.proposerChaines.get() == 1 \
            elif analyse.resultatEffortAxialMtg[s][0].clef in ['ChargeAxOk']:
                tag = "Chaine"+ str(s)
                if True:#parent.master.options.proposerChaines.get() <> 0 :
                    self.boutons["_"+tag] = buttons.ThemedGenBitmapToggleButton(self, 20+s, 
                                                                                None, 
                                                                                style = wx.BORDER_NONE)
                    self.boutons["_"+tag].SetBitmapLabel(Images.Img_BoutonMont(tag))
                    self.boutons["_"+tag].SetInitialSize()
                    self.boutons["_"+tag].SetToolTipString(Const.bulles['AnalyChai'])


            # Bouton "Animer"
            #----------------
#            elif parent.master.options.proposerAnimArret.get() == 1 \
            elif analyse.resultatEffortAxialMtg[s][0].clef == 'ArretArbreSens':
                tag = "Arret"+ str(s)
                self.boutons["_"+tag] = buttons.ThemedGenBitmapButton(self, 10+s, 
                                                                      Images.Img_BoutonMont(tag), 
                                                                      style = wx.BORDER_NONE)
                self.boutons["_"+tag].SetInitialSize()
                self.boutons["_"+tag].SetToolTipString(Const.bulles['AnalyAnim'])

            # On place les widgets ...
            #-------------------------
            if self.boutons.has_key("_"+tag):
                self.AddBouton("1", self.boutons["_"+tag], (1,c), (1,1), wx.ALIGN_CENTRE)

            tag = None
        
        # Résistance des roulements
        ########################################################################
        self.MakeStaticBox("2", u"Résistance des roulements")

        # Message général
        self.Add("2", self.StaticTextMessage(analyse.messageResistanceRlt), border = 10)
        
        # Schéma de structure
        self.Add("2", wx.StaticBitmap(self, -1, analyse.imageSchemaCharges), 
                 flag = wx.ALIGN_CENTRE, border = 0)
        
        # Messages par roulement
#        self.MakeBoutonSizer("2",1,20) 
        
        table = Tableau(self)
        table.SetColLabelValue(0, u"Roulement gauche")
        table.SetColLabelValue(1, u"Roulement droit")
        table.SetRowLabelSize(1)
        table.SetRowLabelAlignment(wx.ALIGN_RIGHT, wx.ALIGN_CENTRE)
#        table.SetRowLabelValue(0, u"Type\nde charge")
#        table.SetRowLabelValue(1, u"Résistance\ndu roulement")
        
        c = 0
        for p in ["G","D"]:
            l = 0
            if analyse.resultatResistanceRlt[p] is not None:
                table.SetCellValue(1,c, Const.typeCharge[analyse.typeCharge[p]])
                table.SetCellTextColour(1,c, wx.BLACK)
                if analyse.typeCharge[p] <> 0:
                    table.SetCellValue(0,c, analyse.resultatResistanceRlt[p].mess)
                table.SetCellTextColour(0,c, Couleur[analyse.resultatResistanceRlt[p].coul])
            c += 1
        
        table.Fit()
        table.ForceRefresh()
        
        size = 0
        for c in range(table.GetNumberCols()):
            if size < table.GetColSize(c):
                size = table.GetColSize(c)
                colmax = c
                
#        print colmax, table.GetColSize(colmax)
        
        table.SetColSize(1-colmax, table.GetColSize(colmax))
        
#        table.SetColSize(table)
        table.Fit()
        table.ForceRefresh()
        
#        flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALIGN_LEFT|wx.TOP|wx.BOTTOM
        
        self.Add("2", table, flag = wx.ALIGN_CENTRE, border = 0)
        
        self.tableResist = table
#        c = 0
#        for p in ["G","D"]:
#            if analyse.resultatResistanceRlt[p] is not None:
#
#                # Type de charge
#                #---------------
#                StyleText["Titre2"].applique(self)
#                txt = wx.StaticText(self, -1, Const.typeCharge[analyse.typeCharge[p]],
#                                    style = wx.ALIGN_CENTRE)
#                self.AddBouton("2", txt, (0,c), (1,1), wx.ALIGN_CENTRE|wx.EXPAND)
#
#                # Label "Résultat"
#                #----------------
#                if analyse.typeCharge[p] <> 0:
#                    StyleText["Messag"].applique(self, Couleur[analyse.resultatResistanceRlt[p].coul])
#                    txt = wx.StaticText(self, -1, analyse.resultatResistanceRlt[p].mess,
#                                        style = wx.ALIGN_CENTRE)
#                    self.AddBouton("2", txt, (1,c), (1,1), wx.ALIGN_CENTRE|wx.EXPAND)
#                c += 1
#    
        self.SetSizerAndFit(self.sizer)
        self.Thaw()


    def initAffichage(self, zmont = None):
#        print "initAffichage Resistance"
        for b in self.boutons.values():
            if isinstance(b, buttons.ThemedGenBitmapToggleButton):
                self.OnClick(id = b.GetId(), act = False)
                b.SetToggle(False)
               


    #############################################################################                
    def lstNom(self, sens):
        message = self.parent.analyse.resultatEffortAxialMtg[sens][1].mess

        lst = []
        pos = Montage.PositionDansPivot()
        for res in self.parent.analyse.lstElemResistePas[sens]:
            lst.append(pos.traduireEnTexte(res))
        
        return {'mess' : message, 'lst' : lst}
       
    
    
    
    def OnClick(self, event = None, id = None, act = None):
        if id is None: id = event.GetId()
        if id in [10,11]:
            idOpp = "__Chaine"+ str(11-id)
            if self.boutons.has_key(idOpp):
                self.boutons[idOpp].SetToggle(False)
                self.OnClick(id = 41-id, act = False)
            self.parent.animerElemNonArretes(id-10)
        elif id in [20,21]:
            if act is None: act = event.GetIsDown()
            self.parent.gererAffichageChaines(id-20, act)
        elif id in [30,31]:
            if act is None: act = event.GetIsDown()
            self.parent.gererSurBrillanceArrets(id-30, act)
#            self.listeActive[id-30].Montrer(act)
        self.Layout()
        self.Update()




#####################################################
# Montage ###########################################
#####################################################
class ZoneMontabilite(ZoneResultats):
    def __init__(self, parent, analyse):
        ZoneResultats.__init__(self, parent, analyse)

        self.analyse = analyse
        
        if analyse.montageVide:
            return
        
        self.Freeze()
        
        #####################################################
        # Message principal (montabilité globale)
        #####################################################
        self.txt = self.StaticTextMessage(analyse.resultatMontabilite)
        self.sizer.Add(self.txt, flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALIGN_LEFT|wx.TOP|wx.BOTTOM, border = 10)
        
        #####################################################
        # Montabilité de l'ensemble monté "libre"
        #####################################################
        if analyse.cdcf.bagueTournante == "I": ens = u"""arbre"""
        else: ens = u"""alésage"""
        self.MakeStaticBox("1", u"Montabilité de l'ensemble " + ens)
        self.MakeBoutonSizer("1",0,0)
        StyleText["Titre2"].applique(self)
        cbs = wx.BoxSizer(wx.HORIZONTAL)
        cb = wx.CheckBox(self, -1, " ")
        cb.SetValue(analyse.demonterRltSerres)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb)
        cbs.Add(cb)
        txt = StaticTextWrapped(self, -1, u"Ne pas tenir compte des roulements montés serrés")
        txt.marge = 40
        cbs.Add(txt)
        self.Add("1", cbs)
        
        #####################################################
        # Montabilité des roulements sur l'ensemble monté "serré
        #####################################################
        self.MakeStaticBox("2", u"Montabilité des roulements")
        self.MakeBoutonSizer("2",0,0)
        StyleText["Titre2"].applique(self)
        if self.analyse.mtg.palier["G"].rlt.num is not None:
            txt = wx.StaticText(self, -1, u"gauche", style = wx.ALIGN_CENTRE)
            self.AddBouton("2", txt, (0,0), (1,2), wx.ALIGN_CENTRE|wx.ALIGN_BOTTOM)
        if self.analyse.mtg.palier["D"].rlt.num is not None:
            txt = wx.StaticText(self, -1, u"droite", style = wx.ALIGN_CENTRE)
            self.AddBouton("2", txt, (0,2), (1,2), wx.ALIGN_CENTRE|wx.ALIGN_BOTTOM)

        #####################################################
        # Options
        #####################################################
#        self.MakeStaticBox("3", u"Options", wx.HORIZONTAL)
#        self.MakeBoutonSizer("3",0,0)
#        StyleText["Titre2"].applique(self)
#        cb = wx.CheckBox(self, -1, " ")
#        cb.SetValue(analyse.demonterRltSerres)
#        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, cb)
#        self.Add("3", cb)
#        txt = StaticTextWrapped(self, -1, u"Ne pas tenir compte des roulements montés sérrés")
#        txt.marge = 40
#        self.Add("3", txt)#, flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALIGN_LEFT|wx.TOP|wx.BOTTOM|wx.LEFT)

        #####################################################
        # Tous les boutons ...
        #####################################################
        
        # Ensemble
        dl = 2
        for tag, pos in [["AnimEnsb1", (0,0)],
                         ["AnimEnsb0", (0,2)]]:
            
            lstObs = analyse.obstacleEnsble[eval(tag[8])]
#            if analyse.obstacleEnsble[eval(tag[8])] <> []:
#                lstObs.append(analyse.obstacleEnsble[eval(tag[8])])
#            for p in ["G","D"]:
#                if analyse.obstacleEnsble[eval(tag[8])][p] <> ():
#                    lstObs.append(analyse.obstacleEnsble[eval(tag[8])][p])
            if lstObs <> []: typeAction = 'obstacle'
            else: typeAction = 'demonte'
            
            # Le bouton ...
            self.boutons[tag] = BoutonMontage(self,
                                              tag = tag,
                                              typeAction = typeAction,
                                              analyse = analyse,
                                              lstObs = lstObs)
            self.AddBouton("1", self.boutons[tag], pos, flag = wx.ALIGN_CENTRE)
            
#            # La zone "liste active" ...
#            if typeAction == 'obstacle':
#                self.AddBouton("1", self.boutons[tag].listeActive.symboleDevelop, (pos[0]+1,pos[1]), (1,2), 
#                                  wx.ALIGN_CENTRE|wx.ALIGN_BOTTOM)
#                self.AddBouton("1", self.boutons[tag].listeActive, (pos[0]+dl, 0), (1,4), 
#                                  wx.ALIGN_CENTRE|wx.ALIGN_TOP|wx.EXPAND)
#                dl += 1
                
        # Roulements
        dl = 2
        for tag, pos in [["AnimRltG0",(1,1)], \
                         ["AnimRltG1",(1,0)], \
                         ["AnimRltD0",(1,3)], \
                         ["AnimRltD1",(1,2)]] :
            
            lstObs = analyse.obstacleRoults[tag[7]][eval(tag[8])]
            if lstObs <> []: typeAction = 'obstacle'
            else: typeAction = 'demonte'
            
            # Le bouton ...
            if self.analyse.mtg.palier[tag[7]].rlt.num is not None:
                self.boutons[tag] = BoutonMontage(self,
                                                  tag = tag,
                                                  typeAction = typeAction,
                                                  analyse = analyse,
                                                  lstObs = lstObs)
                self.AddBouton("2", self.boutons[tag], pos, flag = wx.ALIGN_CENTRE)
                
#            # La zone "liste active" ...
#            if typeAction == 'obstacle':
#                self.AddBouton("2", self.boutons[tag].listeActive.symboleDevelop, (pos[0]+1,pos[1]), (1,1), 
#                                wx.ALIGN_CENTRE|wx.ALIGN_BOTTOM)
#                self.AddBouton("2", self.boutons[tag].listeActive, (pos[0]+dl, 0), (1,4), 
#                                wx.ALIGN_CENTRE_VERTICAL|wx.ALIGN_TOP|wx.EXPAND)
#                dl += 1
        
        c = 0
        for p in ["G", "D"]:
            if p in analyse.obstacleBagueIsolee.keys() > 0:
                tag = "BagueIsolee"+p
                self.boutons[tag] = buttons.ThemedGenBitmapToggleButton(self, 100+c,
                                                                        Images.Img_BoutonMont('BagueIsolee'),
                                                                        style = wx.BORDER_NONE)
                self.boutons[tag].SetInitialSize()
    #                self.SetBitmapLabel(Images.Img_BoutonMont(tag+self.rad))
                self.AddBouton("2", self.boutons[tag], (2,c), (1,2), flag = wx.ALIGN_CENTRE)
                self.boutons[tag].SetToolTipString(u"Cliquer pour visualiser la bague de roulement qui ne peut pas être démontée.")
                self.Bind(wx.EVT_BUTTON, self.montrerBaguesIsolee, self.boutons[tag])
            c += 2
        self.gererActivationBoutons()
        
        self.SetSizerAndFit(self.sizer)
        self.Thaw()
        


#    ############################################################################
#    def OnClick(self, event):
#        id = event.GetId()
#        if id in [10,11]:
#            idOpp = "__Chaine"+ str(11-id)
#            if self.boutons.has_key(idOpp):
#                self.boutons[idOpp].SetToggle(False)
#            self.parent.animerElemNonArretes(id-10)
#        elif id in [20,21]:
#            self.parent.gererAffichageChaines(event)
#        elif id in [30,31]:
#            self.parent.gererSurBrillanceArrets(event, id-30)

    def EvtCheckBox(self, event):
#        print self.analyse.demonterRltSerres, "-->", event.IsChecked()
        self.analyse.analyserMontabilite(event.IsChecked(), self.parent.zoneMtg)
        self.parent.ReplacePage(2)
        
        

    def initAffichage(self, zoneMtg):
#        print "Init affichage ZoneMont"
        self.initAffichageSurbrillance()
        self.analyse.elemDemonte = []
        # On remonte tout instantanément
        for i in zoneMtg.lstItemMtg:
            if hasattr(i,"x"):
                i.pos = (i.x,i.pos[1])
            i.normale()
        self.initEtatBoutons()
        self.gererActivationBoutons()
        zoneMtg.Redessiner(self.analyse)

    def initEtatBoutons(self):
        for b in self.boutons.values():
            b.SetToggle(False)
        
    def initAffichageSurbrillance(self):
        for b in self.boutons.values():
            if isinstance(b, BoutonMontage) and b.typeAction == 'obstacle':
                b.Actionner(False)
        self.Refresh()
        self.Update()

        

    #############################################################################
    def gererActivationBoutons(self):
        """ Change l'état normal des boutons d'animation de la montabilité """
#        print
#        print "Gestion Activation Boutons", self.analyse.elemDemonte,self.boutons["AnimEnsb1"].GetValue()

#        if self.parent.master.options.proposerAnimMont.get() == 0:
#            return


        ### Boutons "Ensemble"
        if  "AnimEnsb0" in self.analyse.elemDemonte or self.boutons["AnimEnsb0"].GetValue():
            self.boutons["AnimEnsb1"].Active(False)
        elif  "AnimEnsb1" in self.analyse.elemDemonte or self.boutons["AnimEnsb1"].GetValue():
            self.boutons["AnimEnsb0"].Active(False)
        else:
            self.boutons["AnimEnsb0"].Active(True)
            self.boutons["AnimEnsb1"].Active(True)

      
        ### Boutons "Roulements"
        if     "AnimEnsb0" in self.analyse.elemDemonte \
            or "AnimEnsb1" in self.analyse.elemDemonte:
            etat = True
        else:
            etat = False
        for t in self.boutons.keys():#["AnimRltG0","AnimRltG1","AnimRltD0","AnimRltD1"]:
            if t[:7] == "AnimRlt":
                self.boutons[t].Active(etat)
            elif t[:-1] == "BagueIsolee":
                self.boutons[t].Enable(not etat)
       
        ### 
        for p in ["G","D"]:
            if "AnimRlt"+p+"0" in self.analyse.elemDemonte:
                self.boutons["AnimRlt"+p+"1"].Active(False)
            if "AnimRlt"+p+"1" in self.analyse.elemDemonte:
                self.boutons["AnimRlt"+p+"0"].Active(False)

        self.Layout()
        self.Refresh()
        self.Update()
#        self.UpdateWindowUI()


#    #############################################################################
#    def activerDesactiverBoutons_Montage(self):
#        """ Activation ou Désactivation des boutons lors d'un démontage """
#
#        if self.master.analyse.elemDemonte == []:
#            state = 'normal'
#        else:
#            state = 'disabled'
#        
#        for b in self.boutons.keys():
#            if b[:4] <> "Anim":
#                if state == 'normal':
#                    e = state
#                else:
#                    e = state
#                self.boutons[b].activerDesactiver(state)
#                self.boutons[b].changerBulle()
#                
#        self.appliquerActivationDesactivation()
#
#    #############################################################################
#    def appliquerActivationDesactivation(self):
#        for clef in self.boutons:
#            if self.boutons[clef].type == 'demonte':
#                self.boutons[clef]["state"] = self.etatBoutons[clef]

#    ###########################################################################
#    def montrerCollision(self, num):
#        self.analyse.montrerCollision(n)      
                

    ###########################################################################
    def montrerBaguesIsolee(self, event):
        if event.GetId() == 100:
            p = "G"
        else:
            p = "D"
#        print "Bagues isolées", self.analyse.obstacleBagueIsolee[p]
        self.parent.montrerBagueIsolee(self.analyse.obstacleBagueIsolee[p], 
                                       self.boutons["BagueIsolee"+p].GetValue())



#####################################################
# Etanchéité ########################################
#####################################################
class ZoneEtancheite(ZoneResultats):
    def __init__(self, parent, analyse):
        ZoneResultats.__init__(self, parent, analyse, liaison = False)
        
        self.Freeze()

        # Etancheité statique
        #####################################################
        self.MakeStaticBox("1", u"Etanchéité statique")

        # Resultat principal
        message = analyse.resultatEtancheite["SB"]
        self.Add("1", self.StaticTextMessage(message))
        if "SB+" in analyse.resultatEtancheite.keys():
            for mess in analyse.resultatEtancheite["SB+"]:
                self.Add("1", self.StaticTextMessage(mess, style = 'Message'))
        
        # Resultats par joint
        self.MakeBoutonSizer("1",5,5) 
        StyleText["Titre2"].applique(self)
        
        table = Tableau(self)
        table.SetColLabelValue(0, u"Coté\ngauche")
        table.SetColLabelValue(1, u"Coté\ndroit")
        table.SetRowLabelValue(0, u"Sur Arbre")
        table.SetRowLabelValue(1, u"Sur Alésage")
        
        l, c = 0, 0
        for p in ["G","D"]:
            l = 0
            for r in ["Ar","Al"]:
                if analyse.resultatEtancheite["S"][p][r]:
                    table.SetCellValue(l,c, "X")
                    table.SetCellTextColour(l,c, Couleur["rouge"])
                else:
                    table.SetCellValue(l,c, "Ok")
                    table.SetCellTextColour(l,c, Couleur["vert"])
                l += 1
            c += 1
        
        table.Fit()
        table.ForceRefresh()
        self.AddBouton("1", table, (0,0), (1,1), wx.ALIGN_CENTRE|wx.EXPAND)
        
        self.tableStat = table
        
        
        # Etanchéité Dynamique
        ########################################################################
        self.MakeStaticBox("2", u"Etanchéité dynamique")

        if "DB" in analyse.resultatEtancheite:
            
            # Résultat principal
            message = analyse.resultatEtancheite["DB"]
            self.Add("2", self.StaticTextMessage(message))
            if "DB+" in analyse.resultatEtancheite.keys():
                for mess in analyse.resultatEtancheite["DB+"]:
                    self.Add("2", self.StaticTextMessage(mess, style = 'Message'))
            
            table = Tableau(self)
            table.SetColLabelValue(0, u"Coté\ngauche")
            table.SetColLabelValue(1, u"Coté\ndroit")
            table.SetRowLabelValue(0, u"Vitesse")
            table.SetRowLabelValue(1, u"Facteur PV")
        
            # Resultat par joint
            self.MakeBoutonSizer("2",5,5)
            l, c = 0, 0
            for p in ["G","D"]:
                l = 0
                for r in ["P","PV"]:
                    if analyse.resultatEtancheite["D"][p][r]:
                        table.SetCellValue(l,c, "X")
                        table.SetCellTextColour(l,c, Couleur["rouge"])
                    else:
                        table.SetCellValue(l,c, "Ok")
                        table.SetCellTextColour(l,c, Couleur["vert"])
                    l += 1
                c += 1
            
            table.Fit()
            table.ForceRefresh()
            self.AddBouton("2", table, (0,0), (1,1), wx.ALIGN_CENTRE|wx.EXPAND)
            
            self.tableDyn = table
#            self.MakeBoutonSizer("2",5,5) 
#            StyleText["Titre2"].applique(self)
#            self.AddBouton("2", wx.StaticText(self, -1,u"Coté",style = wx.ALIGN_CENTRE), (0,1), (1,2), wx.ALIGN_CENTRE|wx.EXPAND)
#            if not analyse.resultatEtancheite["J"]["G"]["Ar"]:
#                self.AddBouton("2", wx.StaticText(self, -1,"gauche",style = wx.ALIGN_CENTRE), (1,1), (1,1), wx.ALIGN_CENTRE|wx.EXPAND)
#            if not analyse.resultatEtancheite["J"]["D"]["Ar"]:
#                self.AddBouton("2", wx.StaticText(self, -1,"droit",style = wx.ALIGN_CENTRE), (1,2), (1,1), wx.ALIGN_CENTRE|wx.EXPAND)
#            if not (analyse.resultatEtancheite["J"]["D"]["Ar"] and analyse.resultatEtancheite["J"]["G"]["Ar"]):
#                self.AddBouton("2", wx.StaticText(self, -1,"vitesse",style = wx.ALIGN_RIGHT), (2,0), (1,1), wx.ALIGN_CENTRE|wx.EXPAND)
#                self.AddBouton("2", wx.StaticText(self, -1,"facteur PV",style = wx.ALIGN_RIGHT), (3,0), (1,1), wx.ALIGN_CENTRE|wx.EXPAND)
#            
#            c = 1
#            l = 2
#            for p in ["G","D"]:
#                if not analyse.resultatEtancheite["J"][p]["Ar"]:
#                    for r in ["P","PV"]:
#                        if analyse.resultatEtancheite["D"][p][r]:
#                            StyleText["Messag"].applique(self, Couleur["rouge"])
#                            txt = wx.StaticText(self, -1, "X",
#                                                style = wx.ALIGN_CENTRE)
#                        else:
#                            StyleText["Messag"].applique(self, Couleur["vert"])
#                            txt = wx.StaticText(self, -1, "Ok",
#                                                style = wx.ALIGN_CENTRE)
#                        self.AddBouton("2", txt, (l,c), (1,1), wx.ALIGN_CENTRE|wx.EXPAND)
#                        l += 1
#                    c += 1
#                    l = 2
        else:
            pass
        # Compatibilité lubrifiant
        ########################################################################
        self.MakeStaticBox("3", u"Compatibilité lubrifiant")

        message = analyse.resultatEtancheite["C"]
        self.Add("3", self.StaticTextMessage(message))
        
        self.SetSizerAndFit(self.sizer)
        
        self.Thaw()


    def initAffichage(self, zmont = None):
        for b in self.boutons.values():
            if isinstance(b, buttons.ThemedGenBitmapToggleButton):
                self.OnClick(id = b.GetId(), act = False)
                b.SetToggle(False)
               


    #############################################################################                
    def lstNom(self,sens):
        message = self.parent.analyse.resultatEffortAxialMtg[sens][1].mess

        lst = []
        pos = Montage.PositionDansPivot()
        for res in self.parent.analyse.lstElemResistePas[sens]:
            lst.append(pos.traduireEnTexte(res))
        
        return {'mess' : message, 'lst' : lst}

#    def OnSize(self, event = None):
#        print "Resize ZoneResistance",
#        print self.GetClientSizeTuple(),
#        print self.GetSize()
##        print self.GetClientSizeTuple()[0]
##        for txt in [self.txt1,self.txt2]:
##            txt.SetLabel(txt.GetLabel().replace('\n',' '))
##            txt.Wrap(self.GetClientSizeTuple()[0])
#        self.Fit()
#        event.Skip()
       
    
    def OnClick(self, event = None, id = None, act = None):
        if id is None: id = event.GetId()
        if id in [10,11]:
            idOpp = "__Chaine"+ str(11-id)
            if self.boutons.has_key(idOpp):
                self.boutons[idOpp].SetToggle(False)
                self.OnClick(id = 41-id, act = False)
            self.parent.animerElemNonArretes(id-10)
        elif id in [20,21]:
            if act is None: act = event.GetIsDown()
            self.parent.gererAffichageChaines(id-20, act)
        elif id in [30,31]:
            if act is None: act = event.GetIsDown()
            self.parent.gererSurBrillanceArrets(id-30, act)
            self.listeActive[id-30].Montrer(act)
        self.Layout()
        self.Update()


#####################################################
# Devis #############################
#####################################################
class ZoneDevis(ZoneResultats):
    def __init__(self, parent, analyse):
#        print "Zone ImmobAx"
        ZoneResultats.__init__(self, parent, analyse, liaison = False),
#                          style=wx.NO_FULL_REPAINT_ON_RESIZE)
#        print analyse.chaineAct[0]
        
        if analyse.montageVide:
            return
        
        self.Freeze()
        
        self.labels = {}
        
        self.MakeStaticBox("1", u"Devis du montage")
        
        # Resultat principal
        #####################
#        p = wx.Panel(self, -1)
        self.lstElem = {}
        self.devis = gridlib.Grid(self, -1, style = wx.NO_BORDER)
        self.devis.CreateGrid(0, 2)
        devisMtg = self.parent.mtgComplet.mtg.devis
#        print devisMtg
        self.devis.SetColLabelValue(0,u'Element')
        self.devis.SetColLabelValue(1,u'Coût')
        self.devis.SetLabelFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, False))
#        self.devis.SetLabelBackgroundColour(wx.WHITE)
        self.devis.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTRE)
        self.devis.SetRowLabelAlignment(wx.ALIGN_RIGHT, wx.ALIGN_CENTRE)
        self.devis.SetRowLabelSize(1)
        
        self.devis.SetDefaultCellFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False))
        self.devis.SetDefaultCellTextColour(wx.BLACK)

        attrS = gridlib.GridCellAttr()
        attrS.SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD, True))
        attrS.SetTextColour(wx.BLUE)
        attrS.SetReadOnly(True)
        
        attrN = gridlib.GridCellAttr()
        attrN.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False))
        attrN.SetTextColour(wx.BLACK)
        attrN.SetAlignment(wx.ALIGN_RIGHT, wx.ALIGN_CENTRE)
        attrN.SetReadOnly(True)
        
        attrC = gridlib.GridCellAttr()
        attrC.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, False))
        attrC.SetTextColour(wx.BLACK)
        attrC.SetAlignment(wx.ALIGN_RIGHT, wx.ALIGN_CENTER)
        attrC.SetReadOnly(True)
        
        self.devis.AppendRows()
        self.devis.SetRowAttr(0, attrS)
        self.devis.SetCellValue(0, 0, u"Roulements")
        self.devis.SetCellValue(0, 1, u" ")
        
        i = 1
        for l in devisMtg[0:2]:
            if l[1] <>0:
                self.devis.AppendRows()
                self.devis.SetRowAttr(i, attrN)
                self.devis.SetCellValue(i, 0, l[0].nom)
                self.devis.SetCellValue(i, 1, str(l[1]))
                self.lstElem[i] = l[0].pos
                i += 1
            
        self.devis.AppendRows()
        self.devis.SetRowAttr(i, attrS)
        self.devis.SetCellValue(i, 0, u"Arrets axiaux")
        self.devis.SetCellValue(i, 1, u" ")
        i += 1
        
        for l in devisMtg[2:10]:
            if l[1] <>0:
                self.devis.AppendRows()
                self.devis.SetRowAttr(i, attrN)
                self.devis.SetCellValue(i, 0, l[0].nom)
                self.devis.SetCellValue(i, 1, str(l[1]))
                self.lstElem[i] = l[0].pos
                i += 1
        
        self.devis.AppendRows()
        self.devis.SetRowAttr(i, attrS)
        self.devis.SetCellValue(i, 0, u"Etanchéité")
        self.devis.SetCellValue(i, 1, u" ")
        i += 1
        
        for l in devisMtg[10:14]:
            if l[1] <>0:
                self.devis.AppendRows()
                self.devis.SetRowAttr(i, attrN)
                self.devis.SetCellValue(i, 0, l[0].nom)
                self.devis.SetCellValue(i, 1, str(l[1]))
                self.lstElem[i] = l[0].pos
                i += 1
        
        for l in devisMtg[14:]:
            if l[1] <>0:
                self.devis.AppendRows()
                self.devis.SetRowAttr(i, attrN)
                self.devis.SetCellValue(i, 0, u"Chapeau support "+Const.cote2text[l[0]])
                self.devis.SetCellValue(i, 1, str(l[1]))
                i += 1
        
        attrS.SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD, False))
        attrS.SetTextColour(wx.BLUE)
        
        self.devis.SetColAttr(1, attrC)
        
        self.devis.AppendRows()
        self.devis.SetCellValue(i, 0, u"TOTAL")
        self.devis.SetCellFont(i, 1, wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD, False))
        self.devis.SetCellFont(i, 0, wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD, False))
        self.devis.SetCellValue(i, 1, str(self.parent.mtgComplet.mtg.cout))
        if self.parent.mtgComplet.CdCF.coutMax.get() < self.parent.mtgComplet.mtg.cout:
            col = wx.RED
        else:
            col = wx.GREEN
        self.devis.SetCellBackgroundColour(i, 1, col)
        
        for r in range(self.devis.GetNumberRows()):
            self.devis.SetRowLabelValue(r, " ")
        
        self.devis.AutoSizeColumns()
        self.devis.AutoSizeRows()
        
        self.devis.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.Add("1", self.devis, flag = wx.ALIGN_CENTRE)
        
#        print self.devis.GetSize()
        self.devis.Fit()
        self.devis.ForceRefresh()
        self.SetSizerAndFit(self.sizer)
#        p.SetSize(self.devis.GetSize())
#        self.statBox[id].SetClientSize(p.GetSize())
        
        self.Thaw()
        
        self.Refresh()
    
    def OnCellLeftClick(self, event):
        r = event.GetRow()
        if r in self.lstElem.keys():
            self.parent.zoneMtg.surImage(self.lstElem[r])
        else:
            self.parent.zoneMtg.surImage()
        event.Skip()
    
    def initAffichage(self, zmont = None):
        self.parent.zoneMtg.surImage()
        
#########################################################
# Remarques générales ###################################
#########################################################
#class ZoneRemarques(wx.Panel):
#    def __init__(self, parent):
#        ZoneResultats.__init__(self, parent, analyse)
#        
#    
#    
#    
#    def init(self, parent):
#        self.DestroyChildren()
#        self.boutons = {}
#        
#        sizer = wx.GridBagSizer()
#        
#        if len(master.analyse.resultatRemarques)>0:
#        
#            for i in range(len(master.analyse.resultatRemarques)):
#                txt = wx.StaticText(self, -1, master.analyse.resultatRemarques[i].mess)
#                sizer.Add(txt, (i+1,0), (1,7))
##                Label(self, text = master.analyse.resultatRemarques[i].mess, \
##                      font = Const.Font_CdCFValeur[0],
##                      fg = master.analyse.resultatRemarques[i].coul, bg = "white", \
##                      anchor = W, justify = LEFT , wraplength = wl*2) \
##                      .grid(row = i+1, column = 0, columnspan = 7,
##                            padx = 5, pady = 2, sticky = W)



#####################################################
# Etancheite ###########################################
#####################################################
#class ZoneEtancheite(Frame):
#    def __init__(self, master = None):
#        Frame.__init__(self)
#
#        self.boutons = {}
#        self.etatBoutons = {}
#        
#        self.master = master
#
#        wl = 130
#
#        Label(self, text = master.analyse.resultatEtancheite["M"].mess, \
#                font = Const.Font_CdCFValeur[0],
#                fg = master.analyse.resultatEtancheite["M"].coul, bg = "white", \
#                anchor = W, justify = LEFT , wraplength = wl*2) \
#            .grid(row = 0, column = 0, columnspan = 7,
#                 padx = 5, pady = 2, sticky = W)
#
#        c = 0
#        for p in ["G","D"]:
#            Label(self, text = Const.cote2text[p], \
#                        font = Const.Font_CdCFTitre[0],
#                        fg = Const.Font_CdCFTitre[1],
#                        bg = "white", justify = CENTER, anchor = CENTER ) \
#                      .grid(row = 1, column = c, columnspan = 2,
#                            padx = 5)
#
#            
#            if master.analyse.resultatEtancheite[p]['pres'] is not None:
#                Label(self, text = master.analyse.resultatEtancheite[p]['pres'].mess, \
#                        font = Const.Font_CdCFValeur[0],
#                        fg = master.analyse.resultatEtancheite[p]['pres'].coul, bg = "white", \
#                        anchor = W, justify = LEFT , wraplength = wl) \
#                    .grid(row = 2, column = c, columnspan = 2,
#                         padx = 5, pady = 2, sticky = W)
#
#            if master.analyse.resultatEtancheite[p]['vitt'] is not None:
#                Label(self, text = master.analyse.resultatEtancheite[p]['vitt'].mess, \
#                        font = Const.Font_CdCFValeur[0],
#                        fg = master.analyse.resultatEtancheite[p]['pres'].coul, bg = "white", \
#                        anchor = W, justify = LEFT , wraplength = wl) \
#                    .grid(row = 3, column = c, columnspan = 2,
#                         padx = 5, pady = 2, sticky = W)
#
#            c += 2

class Tableau(gridlib.Grid):
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, -1, style = wx.NO_BORDER)
        self.CreateGrid(2,2)
        attrS = gridlib.GridCellAttr()
        attrS.SetReadOnly(True)
        self.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.SetLabelBackgroundColour(wx.WHITE)
        self.SetLabelFont(StyleText["Normal"].font)
        self.SetDefaultCellFont(StyleText["Messag"].font)
        self.SetRowAttr(0, attrS)
        self.SetRowAttr(1, attrS)
        self.AutoSizeRows()


##############################################################################                
##############################################################################
#
#     Fenêtre d'Analyse     #
#
##############################################################################
##############################################################################
class TBAnalyse(wx.Treebook):
    def __init__(self, parent, mtgComplet, zMont, analyse, nbCdCF):
#        print "INSTANCIATION TBAnalyse"
        wx.BeginBusyCursor(wx.HOURGLASS_CURSOR)
        wx.Treebook.__init__(self, parent, -1, 
                             style = wx.NB_TOP|wx.BORDER_NONE|wx.TR_HAS_BUTTONS)
        
        self.dicTypeAnalyse = ([u"Structure du Montage",    ZoneImmobAx,         Icones.Icon_AnalysArret.GetBitmap()],
                               [u"Résistance aux Charges",              ZoneResistance,      Icones.Icon_AnalysEffort.GetBitmap()],
                               [u"Montabilité des Eléments",            ZoneMontabilite,     Icones.Icon_AnalysMonta.GetBitmap()],
                               [u"Etanchéité du montage",               ZoneEtancheite,      Icones.Icon_AnalysEtanch.GetBitmap()],
                               [u"Devis : coût indicatif",              ZoneDevis,           Icones.Icon_AnalysDevis.GetBitmap()])
        
        self.parent = parent
        self.nbCdCF = nbCdCF
        
        self.Freeze()
        
        self.InitialiserAnalyse(mtgComplet, zMont, analyse)

#        print self.analyse

        self.img = []
        il = wx.ImageList(30, 30)
        for p in self.dicTypeAnalyse:
            self.img.append(il.Add(p[2]))
        self.AssignImageList(il)
        
        for p in range(len(self.dicTypeAnalyse)):
            self.InitPage(p)
            
        self.ExpandNode(0)

#        # This is a workaround for a sizing bug on Mac...
#        wx.FutureCall(100, self.AdjustSize)
        
        self.Bind(wx.EVT_TREEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_TREEBOOK_PAGE_CHANGING, self.OnPageChanging)
        
        self.Thaw()
        wx.EndBusyCursor()
#        print "FIN INSTANCIATION TBAnalyse"

    def InitialiserAnalyse(self, mtgComplet, zoneMtg, analyse):
        self.zoneMtg = zoneMtg
        self.mtgComplet = mtgComplet
        self.analyse = analyse
        self.analyse.elemDemonte = []
        if self.analyse.estPerimee:
            self.analyse.lancerAnalyse(mtgComplet, zoneMtg)

    def InitPage(self, num):
        fam = self.dicTypeAnalyse[num]
        page = fam[1](self, self.analyse)
        self.InsertPage(num, page, fam[0], imageId = self.img[num])
#        page.Layout()
        
#    def ReplaceAllPages(self):
#        self.Freeze()
#        self.InitialiserAnalyse(self.mtgComplet)
#        sel = self.GetSelection()
#        
#        self.DeleteAllPages()
#        for p in range(len(self.dicTypeAnalyse)):
#            self.InitPage(p)
#        
#        self.Layout()
##        self.ChangeSelection(sel)
#        self.Thaw() 
        
        
    def ReplacePage(self, num):
        self.Freeze()
        
        sel = self.GetSelection()
        self.GetPage(num).initAffichage(self.zoneMtg)
        self.InitPage(num)
        self.DeletePage(num+1)
        self.Layout()
        self.ChangeSelection(sel)
        
        self.Thaw()
    
    def OnPageChanging(self, event):
        self.analyse.initTraceResultats(self.zoneMtg)
        try:
#        self.GetPage(self.GetSelection()).initAffichage()
            self.GetCurrentPage().initAffichage(self.zoneMtg)
        except: pass
#        self.mtgComplet.mtg.rafraichirAffichage(self.zoneMtg)
        self.zoneMtg.Redessiner(self.analyse)
        event.Skip()
        

    def OnPageChanged(self, event = None):
#        print "Page changed"
        if self.GetSelection() == 3:
            self.nbCdCF.nb.ChangeSelection(2)
        elif self.GetSelection() == 1:
            self.nbCdCF.nb.ChangeSelection(0)
        
        
#        for p in self.GetAllPages():
#            p.initAffichage()
        
        
        
    
        
        
#    def InitialiserPages(self):
#        for id in ["ImmAx","ResCh","Monta"]:
#            fam = self.dicTypeAnalyse[id]
#            self.page[id] = self.makePanel(fam[1]) #fam[1](parent)
#            self.AddPage(self.page[id], fam[0])
        
                
#    def InitialiserPages(self):
#        for p in self.page.values():
#            if not p.IsBeingDeleted():
#                try:
#                    p.init(self.analyse)
#                except AttributeError:
#                    p.Destroy()
#                    p.__init__(self, self.analyse)
#                p.Layout()
    
    def AdjustSize(self):
        self.GetTreeCtrl().InvalidateBestSize()
        self.SendSizeEvent()
        
        
#    def makePanel(self, PanelZone):
##        p = wx.Panel(self, -1)
#        p = PanelZone(self, self.analyse)
##        p.win = win
##        def OnCPSize(evt, win=p):
##            win.SetPosition((0,0))
##            win.SetSize(evt.GetSize())
##        p.Bind(wx.EVT_SIZE, OnCPSize)
#        return p
        
    #############################################################################                
    def animerElemNonArretes(self, sens):
        # On efface la chaine opposée si besoin ...
        sensOpp = 1-sens
        chopp = self.analyse.chaineTracee[sensOpp]
        if chopp is not None:
#            print "On efface la chaine"
            effchopp = True
            self.analyse.chaineTracee[sensOpp] = None
            self.zoneMtg.Redessiner(self.analyse)
        else:
            effchopp = False
            
        # On effectue l'animation
        self.analyse.animerManqueArret(self.zoneMtg, sens)
        
        # On raffiche la chaine opposée si besoin ...
        if effchopp:
            self.analyse.chaineTracee[sensOpp] = True #self.analyse.chaineAct[sensOpp].lstLignes
            self.zoneMtg.Redessiner(self.analyse)
        
    def surbrillanceMobiles(self, sens, active):
        self.GetCurrentPage().gererActivationBoutons()
        self.analyse.tracerSurBrillanceMobiles(self.zoneMtg, sens ,active)
#        for b in self.page["Monta"].boutons.values():
#            print "Bouton :",b.tag
#            if b.tag == tag:
#                self.analyse.gererSurBrillanceMobiles(self.zoneMtg, tag ,active)
#            else:
##                self.analyse.gererSurBrillanceMobiles(self.zoneMtg, b.tag , False)
#                b.Actionner(False)
#            self.analyse.gererSurBrillanceMobiles(self.zoneMtg, b.tag ,False)
        
#        self.zoneMtg.Redessiner()
    
    #############################################################################
    def montrerCollision(self, lstObs, palier = None, action = True, surBrill = False):
        self.analyse.montrerCollision(self.zoneMtg, lstObs, palier, action, surBrill)

    def montrerBagueIsolee(self, lstCode, active):
        self.analyse.montrerCollision(self.zoneMtg, lstCode,
                                      active = active)

    #############################################################################                
    def animerMontage(self, tag, remonter):
        # On efface la chaine opposée si besoin ...
#        sensOpp = 1-sens
#        chopp = self.zoneMtg.chaineTracee[sensOpp]
#        if chopp is not None:
#            print "On efface la chaine"
#            effchopp = True
#            self.zoneMtg.chaineTracee[sensOpp] = None
#            self.zoneMtg.InitBuffer()
#        else:
#            effchopp = False

#        if remonter:
#            print "Remontage",
#        else:
#            print "Démontage",
#        print tag
        
        
        
        def collision(tag, tagOpp, remonter):
            # Cas ou l'opération de montage/démontage sur le palier opposée est déja faite ...
            if remonter != (tagOpp in self.analyse.elemDemonte):
                return False
            
            # Etude des collisions
            if remonter:
                if (tag[8] == "0" and tag[7] == "D") \
                   or  (tag[8] == "1" and tag[7] == "G"):
                    return True
            else:
                if (tag[8] == "0" and tag[7] == "G") \
                   or   (tag[8] == "1" and tag[7] == "D"):
                    return True
                
            return False

        self.operationMontage = True
        
        lstBoutons = self.GetPage(2).boutons

        if tag[4] == "R":
            if self.mtgComplet.mtg.palier[tag[7]].rlt.num is None:
                return
            if tag[7] == "G":
                tagOpp = tag[0:7] + "D" + tag[8]
            elif tag[7] == "D":
                tagOpp = tag[0:7] + "G" + tag[8]
            if tagOpp in lstBoutons and collision(tag, tagOpp, remonter):
                lstBoutons[tagOpp].Actionner(not remonter)


        if tag[4] == "E" and remonter:
##            print " ... déja démontés = ",self.analyse.elemDemonte
            while len(self.analyse.elemDemonte) > 1:
                t = self.analyse.elemDemonte[1]
                if t[4] == "R":
##                    self.master.boutons[t].animerMontage(t,remonter)
                    lstBoutons[t].Actionner(not remonter)

        if  remonter:
            self.analyse.animerMontageDemontage(self.zoneMtg, tag ,remonter)
            if tag in self.analyse.elemDemonte:
                self.analyse.elemDemonte.remove(tag)
#            self.bulle.changer(self.listeBulle(not remonter))

        else:
            self.analyse.elemDemonte.append(tag)
#            self.bulle.changer(self.listeBulle(not remonter))
            self.analyse.animerMontageDemontage(self.zoneMtg, tag ,remonter)

        self.GetCurrentPage().gererActivationBoutons()
        
        
#        # On raffiche la chaine opposée si besoin ...
#        if effchopp:
#            self.zoneMtg.chaineTracee[sensOpp] = self.analyse.chaineAct[sensOpp].lstLignes
#            self.zoneMtg.InitBuffer()
        
    #############################################################################
    def gererAffichageChaines(self, sens, afficher):
#        id = event.GetId()
#        print "Gestion affichage chaine",sens,":",afficher
        if afficher:
            self.analyse.SetTracerChaine(sens, True) #self.analyse.chaineAct[id-20].lstLignes
        else:
            self.analyse.SetTracerChaine(sens, None)
#        print self.analyse.chaineTracee
        self.zoneMtg.Redessiner(self.analyse)
        
        
    ###############################################################################
    def gererSurBrillanceArrets(self, sens, action):
##        print "SurBrillance arrets: sens",sens
###        print self.lstElemResistePas[sens]

        if self.analyse.elemDemonte <> []:
            return
        
        self.analyse.tracerSurbrillanceArrets(self.zoneMtg, sens, action)
        
        self.gererAffichageChaines(sens, action)
#        self.zoneMtg.InitBuffer()


################################################################################        
################################################################################
class BoutonMontage(buttons.ThemedGenBitmapToggleButton):
    def __init__(self, parent, tag,
                 typeAction, analyse,
                 lstObs):

        if tag[:4] == "Anim":
            if analyse.cdcf.bagueTournante == "I":
                self.rad = "Ar"
            else:
                self.rad = "Al"
##            sens = eval(img[8])
        else:
            self.rad = ""

        self.typeAction = typeAction
        self.parent = parent
        self.analyse = analyse
        self.lstObs = lstObs
        self.tag = tag
        
        if typeAction == 'demonte':
            buttons.ThemedGenBitmapToggleButton.__init__(self, parent, -1,None, style = wx.BORDER_NONE)
            self.SetBitmapLabel(Images.Img_BoutonMont(tag+self.rad))
            self.SetBitmapSelected(Images.Img_BoutonMont(tag+self.rad+"R"))
            self.SetInitialSize()
#             self.SetSize(self.GetBestSize())
        else:
            buttons.ThemedGenBitmapToggleButton.__init__(self, parent, -1, 
                                                   Images.Img_BoutonMont(tag+self.rad, True),
                                                   style = wx.BORDER_NONE)
#            self.listeActive = ListeActive(self.parent, self.lstNom(lstObs), self)
#            self.bulle = Const.InfoBulleDetails(self.w, self.lstNom(lstObs),
#                                          commandEntrer = self.montrerCacherElem,
#                                          commandQuitter = self.montrerCacherElem)
        self.appliquerBulle(False)
        self.SetAutoLayout(True)
        self.parent.Bind(wx.EVT_BUTTON, self.OnClick, self)
        
    ############################################################################    
    def Actionner(self, state):
        """ Simule l'action d'un Click
            ... avec evenement ... """
#        print self.tag,self.GetValue(), state
        if self.GetValue() <> state:
            self.SetToggle(state)
            self.OnClick(state = state)
                    
    ############################################################################    
    def OnClick(self, event = None, state = None):
        wx.BeginBusyCursor(wx.HOURGLASS_CURSOR)

        if state is None: state = event.GetIsDown() 
        if self.typeAction == 'demonte':
            self.parent.initAffichageSurbrillance()
            self.parent.parent.animerMontage(self.tag, not state)
            self.appliquerBulle(state)
        elif self.tag[4] <> "R":# and self.GetValue():
#            self.listeActive.Montrer(state)
            self.parent.parent.surbrillanceMobiles(eval(self.tag[8]), state)
#            if hasattr(self, "typeAction"):
#                if self.tag[4] <> "R":
#                    surBrill = False
#                else:
#                    surBrill = True
            self.parent.parent.montrerCollision(self.lstObs, 
                                                palier = self.tag[7],
                                                action = state, surBrill = False)
            self.parent.Layout()
        elif self.tag[4] == "R":# and self.GetValue():   
#            print "Obstacle Ensemble :",n, action
            self.parent.parent.montrerCollision(self.lstObs, 
                                                palier = self.tag[7],
                                                action = state, surBrill = True)
#            print "surbrill", state
#            self.listeActive.Montrer(state)
            self.parent.Layout()
            
        wx.EndBusyCursor()
#        self.Refresh()
#        self.Update()
#            self.UpdateWindowUI()
#        self.parent.Layout()
#        self.parent.Update()
        
    ############################################################################    
    def appliquerBulle(self, state):
        def listeBulle(remonter = False):
            b = []
            if self.tag[4] == "R" \
                and self.analyse.elemDemonte == []:
                b.append('EnsPasDemont')
            else:
                b.append('vide')
            if remonter:
                b.append("Rem")
            else:
                b.append("Dem")
            b.append(self.tag[4:7])
            if self.tag[4] == "R":
                b.append(self.tag[7])
            else:
                b.append(self.rad)
            if remonter:
                b.append("depuis")
            else:
                b.append("vers")
            b.append("sens"+self.tag[8])
            return b

        if self.typeAction == 'demonte':
            txt = ''
            for c in listeBulle(state):
                txt += Const.bulles[c]+" "
            self.SetToolTipString(txt)
        else:
            self.SetToolTipString(Const.bulles['AnalyMtgObs'])

    ############################################################################    
    def lstNom(self,lstObstacles):
        
        if type(lstObstacles) == list:
            if type(lstObstacles[0]) == str:
                self.label = 'simple'
                message = Const.MessageAnalyse('CollisionRlt').mess
            else:
                self.label = 'double'
                message = Const.MessageAnalyse('Collision').mess
        else:
            self.label = 'bague'
            if len(lstObstacles.keys()) == 1:
                message = Const.MessageAnalyse('BagueIsolee').mess
            else:
                message = Const.MessageAnalyse('BaguesIsolees').mess
        pos = Montage.PositionDansPivot()
        lst = []
        for i in lstObstacles:
            strObstacles = ''
            if self.label == 'double':
                strObstacles += pos.traduireEnTexte(i[0]) + "\n" + pos.traduireEnTexte(i[1])
            elif self.label == 'simple':
                strObstacles += pos.traduireEnTexte(i)
            elif self.label == 'bague':
                strObstacles += Const.cote2text[i]
            lst.append(strObstacles)
#        print lst[0].encode('cp437','replace')
        return {'mess' : message, 'lst' : lst}


    

    

#    ############################################################################       
#    def gererSurBrillanceMobiles(self, tag = None, active = True):
#        apply(Pmw.busycallback(lambda _tag = tag, _active = active :\
#                               self.analyse.gererSurBrillanceMobiles(tag = _tag, active = _active)))


    ##########################################################################################
    def montrerCacherElem(self, num, act = True):
        
        deuxCoul = True
        if self.label == 'double':
            lstElem = self.lstObs[num]
        elif self.label == 'simple':
            lstElem = [self.lstObs[num]]
        elif self.label == 'bague':
            deuxCoul = False
            lstElem = self.lstObs[num]
        
        self.analyse.montrerArrets(lstCode = lstElem, palier = self.tag[7], active = act,
                                                        deuxCouleurs = deuxCoul)


    ############################################################################
    def Active(self, etat):
        """ Active (ou désactive) le bouton
        """
#        if state == 'normal':
#            etat = self.type
#        else:
#            etat = state
        if etat : self.Enable()
        else: self.Disable()
        
#        if self.type == 'normal':
#            if etat == 'normal':
#                self.SetToggle(True)
##                self.w.activer()
#            else:
#                self.SetToggle(False)
#                self.w.desactiver()
##            self.etat = self.master.etatBoutons[self.img]
##        self.changerBulle()



##################################################################################        
##################################################################################
##class BoutonAction(BoutonBistable):
##    def __init__(self, master, text = None, img = None, clefBulle = None,
##                 lstObs = None, messBulle = None, sens = None, relief = 'raised',
##                 command = None, type = 'disabled', typeBulle = None):
##        
##        BoutonBistable.__init__(self, master, text = text,relief = relief,
##                        command = command)
##        self.master = master
##        self.remonter = False
##        self.typeBulle = typeBulle
##        self.clefBulle = clefBulle
##        self.img = img
##        
##        if img is not None and img[:4] == "Anim":
##            if master.master.analyse.cdcf.bagueTournante == u"Intérieure":
##                self.rad = "Ar"
##            else:
##                self.rad = "Al"
##            sens = eval(img[8])
##        else:
##            self.rad = ""
##        
####        print "Création boutonAction : type", typeBulle," tag",img
####        if typeBulle == 'normal':
####            self.bulle = Const.infoBulle(self, lstClef = [clefBulle], temps = 0)
##            
##        if typeBulle == 'mont':
##            self.bulle = InfoBulle(self, Const.InfoBulleMulti,
##                                   lstClefBulle = self.listeBulle(), temps = 0)
##            
##        elif typeBulle == 'detail':
##            self.bulle = FrameDetails(self, lstObs, eval(img[8]), img[7])
####            if img[4] == "E":
####                self.bind('<Enter>', lambda evt = None , arg = img : \
####                                        self.gererSurBrillanceMobiles(evt,arg) , "+")
####                self.bind('<Leave>', lambda evt = None , arg = img : \
####                                        self.gererSurBrillanceMobiles(evt,arg,False) , "+")
##    
####        elif typeBulle == 'spec':
####            self.bulle = Const.infoBulle(self, lstMess = messBulle, side = TOP, temps = 0)
####            self.bind('<Enter>', lambda evt = None , arg = sens : self.gererSurBrillanceArrets(evt,arg) , "+")
####            self.bind('<Leave>', lambda evt = None , arg = sens : self.gererSurBrillanceArrets(evt,arg,False) , "+")
##        
##        elif typeBulle == 'bagueIsolee':
##            self.bulle = FrameDetails(self, lstObs, 0, "G")
##            
##        
##        self.changerEtatDefaut(etatDefaut)
##        
##        if text is not None:
##            self['height'] = 1
##            self['width'] = 10
##
##        if img is not None:
##            self.afficheImage()
##
##    ############################################################################
##    def faireUneCroix(self):
##        self['text'] = "X"
##        self['relief'] = 'flat'
##
##
####    ############################################################################       
####    def gererSurBrillanceMobiles(self, event = None, tag = None, active = True):
####        apply(Pmw.busycallback(lambda _tag = tag, _active = active :\
####                               self.master.master.analyse.gererSurBrillanceMobiles(tag = _tag, active = _active)))
##
##
####    ############################################################################       
####    def gererSurBrillanceArrets(self, event = None, sens = None, active = True):
####        self.master.master.analyse.gererSurBrillanceArrets(sens = sens, active = active)
####        
##        
##    ############################################################################
##    def activerDesactiver(self, state):
##        print "Activation bouton",self.img,state
##        if state == 'normal':
##            self.master.etatBoutons[self.img] = self.etatDefaut
##        else:
##            self.master.etatBoutons[self.img] = state
##
##        self.etat = self.master.etatBoutons[self.img]
##        self.changerBulle()
##        
##
##    ############################################################################
##    def afficheImage(self,  remonter = False):
##        self.remonter = remonter
##        if remonter:
##            tagImg = self.img+self.rad+"R"
##        else:
##            tagImg = self.img+self.rad
##        self.image = ImageTk.PhotoImage(Images.BoutonMont[tagImg])
##        self['image'] = self.image
##        self.changerBulle()
##
##        
##    ############################################################################
##    def changerEtatDefaut(self,  etatDefaut):
##        self['state'] = etatDefaut
##        self.etatDefaut = etatDefaut
##        self.etat = self['state']
##        if etatDefaut == 'disabled':
##            self['cursor'] = "question_arrow"
##            self.faireUneCroix()
##        else:
##            self['cursor'] = "arrow"
##
##
##    ############################################################################
##    def changerBulle(self):
##        
##        if self.typeBulle <> 'mont':
##            return
##        if self.etat == 'disabled':
##            return
####        print "changer bulle :",self.typeBulle
####        if self.typeBulle == 'normal':
######            print "   ",self.clefBulle
####            self.bulle.__init__(self,clefMess = self.clefBulle)
##        if self.typeBulle == 'mont':
####            print "   .."
##            self.bulle = InfoBulle(self, Const.InfoBulleMulti,
##                                   lstClefBulle = self.listeBulle(), temps = 0)
##            
##
##
##        
##    ############################################################################    
##    def listeBulle(self):
##        b = []
##        if self.typeBulle == 'mont':
##            if self.etatDefaut == "normal" and self.img[4] == "R" \
##               and self.master.master.analyse.elemDemonte == []:
##                b.append('EnsPasDemont')
##            else:
##                b.append('vide')
##            if self.remonter:
##                b.append("Rem")
##            else:
##                b.append("Dem")
##            b.append(self.img[4:7])
##            if self.img[4] == "R":
##                b.append(self.img[7])
##            else:
##                b.append(self.rad)
##            if self.remonter:
##                b.append("depuis")
##            else:
##                b.append("vers")
##            b.append("sens"+self.img[8])
##
##
##        return b



#####################################################################################################
##              
#####################################################################################################
##class FrameDetails(Toplevel):
##    def __init__(self, master = None, lstObstacles = None, sens = None, palier = None):
##        Toplevel.__init__(self, master, bd = 2, bg = 'lightyellow', relief = RIDGE)
####        print "Détails pour palier",palier,"obs =",lstObstacles,"sens ",sens
##        self.parent = master
##        self.withdraw()
##        self.overrideredirect(1)
##        self.transient()
##
##        self.tipwidth = 0
##        self.tipheight = 0
##        
##        self.lstObstacles = lstObstacles
##        self.sens = sens
##        self.palier = palier
##
####        print lstObstacles
##        if type(lstObstacles) == ListType:
##            if type(lstObstacles[0]) is StringType:
##                self.label = 'simple'
##                message = Const.MessageAnalyse('CollisionRlt')
##            else:
##                self.label = 'double'
##                message = Const.MessageAnalyse('Collision')
##        else:
##            self.label = 'bague'
##            if len(lstObstacles.keys()) == 1:
##                message = Const.MessageAnalyse('BagueIsolee')
##            else:
##                message = Const.MessageAnalyse('BaguesIsolees')
##
####        print "double = ",self.double
##        
##        Label(self, text = message.mess,
##                font = Const.Font_MessBulleS[0],
##                fg = Const.Font_MessBulleS[1],
##                bg = 'lightyellow',
##                anchor = W, justify = LEFT) \
##            .grid(row = 0, column = 0, sticky = W)
##
##        
##        pos = Montage.PositionDansPivot()
##        r = 1
##        self.lab = {}
##        for i in lstObstacles:
##            strObstacles = ''
##            if self.label == 'double':
##                strObstacles += "  - " + pos.traduireEnTexte(i[0]) + "\n\tet " + pos.traduireEnTexte(i[1])
##            elif self.label == 'simple':
##                strObstacles += "  - " + pos.traduireEnTexte(i)
##            elif self.label == 'bague':
##                strObstacles += "  - " + Const.cote2text[i]
##
##            if self.label == 'bague':
##                nn = i
##            else:
##                nn = r-1
##                
##            self.lab[nn] = Label(self, text = strObstacles,
##                                  font = Const.Font_MessBulle[0],
##                                  fg = Const.Font_MessBulle[1],
##                                  bg = 'lightyellow',
##                                  anchor = W, justify = LEFT)
##
##            self.lab[nn].grid(row = r, column = 0, sticky = W)
##            r +=1
##            
##            self.lab[nn].bind('<Enter>',lambda evt = None, num = nn, act = True  : \
##                              self.montrerCacherElem(evt,num,act))
##            self.lab[nn].bind('<Leave>',lambda evt = None, num = nn, act = False : \
##                              self.montrerCacherElem(evt,num,act))
##
##        
##        self.bind('<Button-1>',self.efface,"+")
####        self.bind('<Leave>',self.efface,"+")
##        self.bind_all("<Escape>", self.efface, "+")
##        self.parent.bind('<Leave>',self.delai,"+")
##        self.bind('<Enter>',self.affiche,"+")
##        self.parent.bind('<Enter>',self.affiche,"+")
##        self.parent.master.bind('<Enter>',self.delai,"+")
##        self.parent.master.master.bind('<Enter>',self.delai,"+")
##        
##
##
##    ##########################################################################################
##    def montrerCacherElem(self, event, num, act):
##        
##        if act:
##            coul = "blue"
##        else:
##            coul = "black"
##        self.lab[num].config(fg = coul)
##        
##        deuxCoul = True
##        if self.label == 'double':
##            lstElem = self.lstObstacles[num]
##        elif self.label == 'simple':
##            lstElem = [self.lstObstacles[num]]
##        elif self.label == 'bague':
##            deuxCoul = False
##            lstElem = self.lstObstacles[num]
##        
##        self.parent.master.master.analyse.montrerArrets(lstCode = lstElem, sens = self.sens,
##                                                        palier = self.palier, active = act,
##                                                        deuxCouleurs = deuxCoul)
##
##    ####################################################################################################
##    def delai(self,event = None):
##        self.action = self.parent.after(200,self.efface)
##        
##    ####################################################################################################
##    def affiche(self, event = None):
##        self.update_idletasks()
##        
##        posX = self.parent.winfo_rootx()+self.parent.winfo_width()/2
##        posY = self.parent.winfo_rooty()+self.parent.winfo_height()
##        if posX + self.tipwidth > self.winfo_screenwidth():
##            posX = posX-self.winfo_width()-self.tipwidth/2
##        if posY + self.tipheight > self.winfo_screenheight():
##            posY = posY-self.winfo_height()-self.tipheight
####        else:
####            posX = self.parent.winfo_rootx() 
####            posY = self.parent.winfo_rooty() 
##
##        self.geometry('+%d+%d'%(posX,posY))
##        self.deiconify()
##        self.parent.after_cancel(self.action)
##
##    ####################################################################################################
##    def efface(self,event = None):
##        self.withdraw()
####        self.parent.after_cancel(self.action)
##                       
                

            









##############################################################################
##############################################################################
#
#     Chaines d'Action dans le sens <sens>   #
#
##############################################################################
##############################################################################
class ChainesAction:
    def __init__(self, sens):
##        self.chaine = ChaineActionSens(sens)
##        self.result = []
        self.sens = sens

        # liste des numéros des parcours valides
        self.valid = []

        # Liste des parcours
        self.parcoursElemEntr = [[]]

        # Une liste de lignes par sens ...
        self.lstLignes = []


    
    #############################################################################                
    def determiner(self, mtg, zoneMtg, serrage = False):
##        print "---------------------"
##        print
        
        self.__init__(self.sens)

##        # On teste s'il y a 2 roulements :
##        #---------------------------------
##        if mtg.deuxrlt == 0:
##            mtg.resultatRemarques.append(Const.MessageAnalyse('ManqueRlt'))
##            return
        
##        print "Sens = ",self.sens
        
        if self.sens == 0:
            cote = "G"
            coteOpp = "D"
        else:
            cote = "D"
            coteOpp = "G"

        
#        print ">>> Sens " ,self.sens  
#        print mtg                                  


        # Analyse depuis l'extrémité du montage :
        #----------------------------------------
        pos = Montage.PositionDansPivot(typelem = "A",
                                        radiale = "Ar",
                                        cotelem = cote,
                                        palier = cote)
        self.maillonElemEntraines(mtg,pos,0)
        


        # Analyse depuis le milieu du montage :
        #--------------------------------------
        pos = Montage.PositionDansPivot(typelem = "A",
                                        radiale = "Ar",
                                        cotelem = cote,
                                        palier = coteOpp)
        self.parcoursElemEntr.append([])
        self.maillonElemEntraines(mtg,pos,len(self.parcoursElemEntr)-1)

        # Analyse depuis le roulement extrémité :
        #----------------------------------------
        if serrage:
            pos = Montage.PositionDansPivot(typelem = "R",
                                        radiale = "Ar",
                                        cotelem = cote,
                                        palier = cote)
            self.parcoursElemEntr.append([])
            self.maillonElemEntraines(mtg,pos,len(self.parcoursElemEntr)-1)
            
        # Analyse depuis le roulement milieu :
        #-------------------------------------
        if serrage:
            pos = Montage.PositionDansPivot(typelem = "R",
                                        radiale = "Ar",
                                        cotelem = cote,
                                        palier = coteOpp)
            self.parcoursElemEntr.append([])
            self.maillonElemEntraines(mtg,pos,len(self.parcoursElemEntr)-1)

        # Analyse des parcours :
        #-----------------------
        for i in range(len(self.parcoursElemEntr)):
            par = self.parcoursElemEntr[i]
            if len(par) > 0:
                pos = par[len(par)-1]
##                print mtg.elemPos(pos)
                if pos.radiale == "Al" \
                   and mtg.elemPos(pos).supporteEffortAxial(self.sens,pos) \
                   and pos.typelem == "A":
                    self.valid.append(i)

        # Détermination des lignes :
        #---------------------------
        self.determinerLignes(mtg, zoneMtg, self.sens)     
        
#        print "Parcours :\n",self.parcoursElemEntr
#        print "Valides :\n",self.valid
        

            

#    ###########################################################################
#    def __repr__(self, num = 0):
##        print '< Parcours sens',self.sens,': '+str(num)+' >'
#        return self.parcoursElemEntr[num]

        
    ##########################################################################
    def ajouterMaillonElemEntre(self, pos, num):
        lp = Montage.PositionDansPivot()
        lp = pos.copie()
##        print "  > Ajout",num,pos
        self.parcoursElemEntr[num].append(lp)
##        print "-- Ajout",lp

        
    ##########################################################################
    def nouveauParcours(self, num, dernPos = None):
        "Crée un nouveau parcours à partir du parcour <num> et retourne son numéro"
        # On crée le nouveau parcours ...
        self.parcoursElemEntr.append([])
        numSuiv = len(self.parcoursElemEntr)-1
##        print "dernpos",dernPos
        # On copie le parcours dans le parcours suivant ...  
        for p in self.parcoursElemEntr[num]:
##            print "copie",p
            self.ajouterMaillonElemEntre(p, numSuiv)
            if p.egal(dernPos):
##                print "fin"
                return numSuiv

        return numSuiv


    #########################################################################
    def maillonElemEntraines(self,mtg,pos,num):
        """ Renvoie un maillon "actif" d'une chaine d'action
        """

##        if len(self.parcoursElemEntr)<num+1:
##            self.parcoursElemEntr.append([])
            
##        print
#         print "**** sens",self.sens,"*************"
#         print ">> Num",num
#         print ">> Position",pos
#         print ">> Eléments",self.parcoursElemEntr[num]
        
        if pos == None:
            return False
        else:
            maillon = mtg.elemPos(pos)
            maillonOpp = mtg.elemPos(pos.opposee())

        # Sortie si premier maillon est entretoise
        if  (    maillon.estEntretoise() \
             or (maillon.num is None and maillonOpp.estEntretoise())) \
           and len(self.parcoursElemEntr[num]) == 0:
#             print "prem maillon = entretoise"
            return False    
            
        ### si l'élément est une entretoise
        if maillon.estEntretoise() or maillonOpp.estEntretoise():
#             print "  > Entretoise"
            # Ajout de l'entretoise et séparation éventuelle des parcours
            if not maillon.estEntretoise() and pos.radiale == "Al":
                # Si double contact entretoise / épaulement
#                 print "  > Nouveau parcours : cas 3 = double contact entretoise/épaulement"
                numSuiv = self.nouveauParcours(num)
                self.ajouterMaillonElemEntre(pos.opposee(),numSuiv)
            else:
                numSuiv = num
                self.ajouterMaillonElemEntre(pos,numSuiv)

            # Ajout du roulement suivant si entretoise sur alésage
            if pos.radiale == "Al":
#                 print "  > Ajout rlt",pos.suivant("RoultSuiv",self.sens).code()
                self.ajouterMaillonElemEntre(pos.suivant("RoultSuiv",self.sens),numSuiv)

            # On continue par l'entretoise ...    
            if not self.maillonElemEntraines(mtg,pos.suivant("SauteEntre",self.sens),numSuiv):
#                 print "  > num",numSuiv," Echec après entretoise !"
                if num == numSuiv:
                    return False
            if num == numSuiv:
                return True

                
        ### si l'élément supporte
#        ss =  maillon.supporteEffortAxial(self.sens,pos)
#        print ss
        if (maillon.num is not None) and maillon.supporteEffortAxial(self.sens,pos):
##            print "  > num",num," Supporte"
            # On ajoute l'élément ...  
            self.ajouterMaillonElemEntre(pos,num)
##            print self.__repr__(num)
            if pos.radiale == "Al":
##                print "  > Fin ..."
                return True
                    
            else:
                # On continue ...
                if not self.maillonElemEntraines(mtg,pos.suivant("DansChaine",self.sens),num):
##                    print "  > num",num," Echec dans chaine !"
                    pass
##                    return False

                # 2ème parcours : cas 1 = traverse bague int rlt
                if pos.radiale == "Ar" and pos.typelem == "A":
##                    print "  > num",num," Nouveau parcours cas 1 = traverse bague int rlt"
##                    print "  >  reprise à",pos
                    numSuiv = self.nouveauParcours(num,pos)
                    # On ajoute le roulement sauté ...
                    self.ajouterMaillonElemEntre(pos.suivant("RoultSaute",self.sens),numSuiv)
                    if not self.maillonElemEntraines(mtg,pos.suivant("SauteRoult",self.sens),numSuiv):
##                        print "  > num",numSuiv," Echec après cas 1 !"
                        return False

        
        ### si l'élément NE supporte PAS
        else:
##            print "  > num",num," Supporte pas"
            # On ajoute le dernier maillon ...
            if maillon.num is not None:
                self.ajouterMaillonElemEntre(pos,num)
            

            # 2ème parcours : cas 2 = palier suivant
            if (self.sens == 0 and pos.palier == "G") \
               and (self.sens == 1 and pos.palier == "D"):
##                print "  > num",num,"Nouveau parcours : cas 2 = palier suivant"
                self.parcoursElemEntr.append([])
                numSuiv = len(self.parcoursElemEntr)-1
                if not self.maillonElemEntraines(mtg,pos.suivant("SautePalier",self.sens),numSuiv):
##                    print "  > num",numSuiv," Echec après cas 2 !"
                    return False
            
##            print "  > num",num," Echec supporte pas !"
##            return False

        return True



    #############################################################################                
    def determinerLignes(self, mtg, zoneMtg,  sens):
        """ Rempli une liste de points <self.lstLignes>
            pour le tracé des chaines d'action.
        """
            
        def ajouterPoints(x , y, ligne, sgnSens, ecartement = 5):
            """Ajoute 2 points autour de la position <x,y> """
            ligne.append(wx.Point(x - sgnSens*ecartement,
                                  zoneMtg.milieuY + y + sgnSens))
            ligne.append(wx.Point(x + sgnSens*ecartement,
                                  zoneMtg.milieuY + y + sgnSens))
        
        sgnsens = -sens * 2 + 1

        # Une ligne en haut ...
        lignes = []
        
##        print
##        print "Chaine d'action : sens =",sens

        # Préparation des parcours :
        #--------------------------
        lstParcours = []
        for nParcours in self.valid:
            
            # Nouveau parcours
            parcours = []
            lstParcours.append(parcours)
            
#            print "Parcours ",nParcours,":",self.parcoursElemEntr[nParcours]

            for i in range(len(self.parcoursElemEntr[nParcours])):
                
                posParcours = self.parcoursElemEntr[nParcours][i]

                # Cas des arrets ...
                if posParcours.typelem == "A" :
                    elemEntret = mtg.elemPos(posParcours).estEntretoise()
                    elemOppEntret = mtg.elemPos(posParcours.opposee()).estEntretoise()

                    #  Cas des entretoises
                    if elemEntret or elemOppEntret: # il y a une entretoise ...
#                        print "  .. entretoise ..",
                        if elemEntret: # and (elemOppEntret \
#                           or (posParcours.palier == "G" and sens == 0 \
#                               or  posParcours.palier == "D" and sens == 1)): # elle sert ...
#                            print "  .. qui sert. .."
                            pos = posParcours.copie()
                            pos.palier = None
                            pos.cotelem = None
                            parcours.append(pos)
                        else: # elle ne sert pas ...
#                            print
                            parcours.append(posParcours)
                    else: # il n'y a pas d'entretoise ...
                        parcours.append(posParcours)
                            
                # Cas des roulements
                elif posParcours.typelem == "R":
                    # On l'ajoute s'il est "traversé" radialement ...
                    if (self.parcoursElemEntr[nParcours][i-1].radiale \
                        <> self.parcoursElemEntr[nParcours][i+1].radiale):
                        parcours.append(posParcours)

#            print "  Parcours modifié :",parcours

        # Fabrication des lignes :
        #-------------------------
        lstLignes = []
        for parcours in lstParcours:
            
            # Nouvelle ligne
            ligne = []
            lstLignes.append(ligne)

            # Points de départ
            ajouterPoints(zoneMtg.milieuX - sgnsens * (zoneMtg.milieuX - 40) ,
                               0 ,
                               ligne, sgnsens, ecartement = 20)

            
            # Bords des elements #############################
            for posParcours in parcours:

                # Alignement en Y en face du premier bord
                if len(ligne) == 2:
                    x , y = zoneMtg.coordsBordElem(mtg, posParcours)
                    ajouterPoints(x - sgnsens*40, 0, ligne, sgnsens,
                                       ecartement = 20)

                # Cas des entretoises
                if posParcours.palier == None:
##                    print "  entretoise..."
                    pos = posParcours.copie()
                    cotesEntretoise = [{'p' : "G", 'c' : "D"},
                                       {'p' : "D", 'c' : "G"}]
                    if sens == 1:
                        cotesEntretoise.reverse()
                        
                    for d in cotesEntretoise:
                        pos.palier = d['p']
                        pos.cotelem = d['c']
                        x , y = zoneMtg.coordsBordElem(mtg, pos, entretoise = True)
                        ajouterPoints(x , y , ligne, sgnsens)
                    
                else:
                    x , y = zoneMtg.coordsBordElem(mtg, posParcours)
                    ajouterPoints(x , y , ligne, sgnsens)

            # Points d'arrivée
            ajouterPoints(x + sgnsens*40, -200, ligne, sgnsens,
                               ecartement = 20)
            ajouterPoints(zoneMtg.milieuX + sgnsens * (zoneMtg.milieuX - 40) ,
                               -200,
                               ligne, sgnsens, ecartement = 20)


        self.lstLignes = lstLignes
         





##############################################################################
##############################################################################
#                       #
#       Analyse         #
#                       #
##############################################################################
##############################################################################
class Analyse:
    def __init__(self):
        
        # Options :
        # ... ne pas tenir compte des ajustements sérrés des roulements
        self.demonterRltSerres = False
        
        # Etat de l'analyse
        self.estPerimee = True
        
        # Par défaut : pas de roulements
        self.montageVide = True
        
        # Liste des tags des éléments démontés
        self.elemDemonte = []

        # Flag pour annoncer si animation en cours
        self.animEnCours = False

        self.mobileTrace = None
        self.lstItemAles, self.lstItemArbre = [], []
        
        # Chaines d'actions à tracer lors d'un "DessineTout"
        self.chaineTracee = {0 : None, 
                             1 : None}

        self.obstacleTrace = None

    ##########################################################################
    def lancerAnalyse(self, mtgComplet, zoneMtg):
        """ Lance la procédure d'analyse du montage
           """
#            
#         print "Début analyse ..."
#         print mtgComplet.mtg
        
        tm = time.clock()
        
        self.cdcf = mtgComplet.CdCF
        self.mtg = mtgComplet.mtg
        
        # Toutes les analyses ...
        #-------------------------
        
        # Remarques diverses....
        self.analyserRemarques()
        
        # Immobilisation axiale
        self.analyserImmobilisationAxiale(zoneMtg)
        
        # Structure ....
        self.analyserStructure()
        
        # Résistance aux charges ( dans cet ordre !! )
        self.analyserResistanceRlt()
        self.analyserResistanceAxialeMtg()

        # Montabilité
        self.analyserMontabilite(self.demonterRltSerres, zoneMtg)
        
        if self.mtg.palier["G"].rlt.num is not None \
           or self.mtg.palier["D"].rlt.num is not None:
            self.montageVide = False
            
        else:
            self.montageVide = True
            
        # Etanchéité
        self.analyserEtancheite()
        
        self.estPerimee = False
#        print "Fin analyse", time.clock()- tm

    ##########################################################################
    #  Analyse : Structure du montage  #
    ##########################################################################
    def analyserStructure(self):
        """ Analyser la structure du montage :
            --> ddl supprimés
            --> Schéma de strucure
        """
        
        def definirddlSupprimes(palier):
            """ Détermination des ddl supprimés par le <palier>
                 0 : aucuns
                 1 : x+
                 2 : x-
                 4 : y
                 8 : n (rotation /z)
            """

#            print "Définition des ddl, palier",palier
            d = 0
            
            if self.mtg.palier[palier].rlt.num == None:
                return d
            
            for sens in [0,1]:
                for parcoursvalid in self.chaineAct[sens].valid :
                    parcours = self.chaineAct[sens].parcoursElemEntr[parcoursvalid]
    #                    print "  ", sens, parcours
                    for n in range(len(parcours)-2):
                        pos = parcours[1:-1][n]
                        av = parcours[:-2][n]
                        ap = parcours[2:][n]
    #                    for [av, pos, ap] in [parcours[:-2], parcours[1:-1], parcours[2:]]:
    #                    print av, pos, ap,
                        if pos.typelem == "R" and pos.palier == palier and av.radiale <> ap.radiale:
                            d = d|(2**sens)
    #                            print ddlSupprimes[cote]
                            if not self.mtg.elemPos(pos).estButee() and not self.mtg.elemPos(pos).estButeeDbl():
    #                            print palier,"pas butée_"
                                d = d|4
            if not self.mtg.palier[palier].rlt.estButee() and not self.mtg.palier[palier].rlt.estButeeDbl():
    #                print cote,"pas butée"
                d = d|4 
                
            if self.mtg.palier[palier].rlt.num == 10 or self.mtg.palier[palier].rlt.num == 11:
    #                print cote,"pas butée"
                d = d|8
#            print "  ddl suppr :",d
            
            return d
        
        self.ddlSupprimes = {}
        for i in ["G","D"]:
            self.ddlSupprimes[i] = definirddlSupprimes(i)
        self.schemaStructure = SchemaStructure()
        self.schemaStructure.determiner(self.mtg, self.ddlSupprimes)
        
        # Image du Schéma de Structure
        #------------------------------
        self.imageSchema = self.schemaStructure.bitmap()



    ##########################################################################
    #  Analyse : Remarques générales  #
    ##########################################################################
    def analyserRemarques(self):
        """ Analyser si les regles de montage axial des roulements est respectée
        """

        # Résultats
        self.resultatRemarques = []
        

        # Teste s'il y a deux roulements ###############################################
        if self.mtg.deuxrlt() == 0:
            self.resultatRemarques.append(Const.MessageAnalyse('ManqueRlt'))
            return
        

        # Teste si les  deux roulements  sont compatibles ##############################
        if self.mtg.palier["G"].rlt.estOblique() or self.mtg.palier["D"].rlt.estOblique():
            if (not self.mtg.palier["D"].rlt.estOblique()) or (not self.mtg.palier["G"].rlt.estOblique()):
                self.resultatRemarques.append(Const.MessageAnalyse('RltsImcomp'))

            else:
                if self.mtg.palier["G"].rlt.orientation == self.mtg.palier["D"].rlt.orientation:
                    self.resultatRemarques.append(Const.MessageAnalyse('OrientIncorr'))


        # Teste si les roulements à bague séparable sont maintenus #####################
        clefResultRem = ""
        for i in ["G","D"]:
            if self.mtg.palier[i].rlt.estSeparable() \
                and not self.mtg.palier[i].rlt.estOblique():
                if not self.mtg.palier[i].arr['Ar']['G'].estDefini() \
                    or not self.mtg.palier[i].arr['Ar']['D'].estDefini() \
                    or not self.mtg.palier[i].arr['Al']['G'].estDefini() \
                    or not self.mtg.palier[i].arr['Al']['D'].estDefini():
                    clefResultRem += i

            
        if clefResultRem <> "":
            self.resultatRemarques.append(Const.MessageAnalyse('RltPasMaintenu',[clefResultRem]))

            
        # Teste si les roulements sont arrétés sur la bague "tournante" ################
        clefResultRem = ""
        for i in ["G","D"]:
            if self.cdcf.bagueTournante == "I":
                codBag = "Ar"
                if not self.mtg.palier[i].rlt.estOblique() \
                    and (not self.mtg.palier[i].arr['Ar']['G'].estDefini() \
                    or not self.mtg.palier[i].arr['Ar']['D'].estDefini()):
                    clefResultRem += i 
            else:
                codBag = "Al"
                if not self.mtg.palier[i].rlt.estOblique() \
                    and (not self.mtg.palier[i].arr['Al']['G'].estDefini() \
                    or not self.mtg.palier[i].arr['Al']['D'].estDefini()):
                    clefResultRem += i

        if clefResultRem <> "":    
            self.resultatRemarques.append(Const.MessageAnalyse('RltPasArrete', (clefResultRem, codBag)))
         
         
         
    ##########################################################################
    #  Analyse : immobilisation axiale du montage  #
    ##########################################################################
    def analyserImmobilisationAxiale(self, zoneMtg):
        """ Analyse de l'immobilisation axiale du montage
            ==> résultats dans des chaines d'action
        """
        
        # Immobilisation axiale du montage ...
        #-------------------------------------
        # --> resultats : un  par sens ...
        self.resultatImmobilisation = [[],[]]
        # --> chaines d'action : une  par sens ...
        self.chaineAct = [ChainesAction(0), \
                          ChainesAction(1)]
        # --> Liste des éléments qui ne sont par arrétée : une par sens ...
        self.listeElementsNonArretes = [[],[]]
        # --> Image du Schéma de structure
        self.imageSchema = None
        # --> Message principal
        self.messageImmobilisation = None
            
#        print self.chaineAct[0]
        
        def listeElementsNonArretes(sens):
            """ Renvoie la liste des éléments non arrêtés dans le sens <sens>
            """
    
            lst = []
            
            if sens == 0:
                sensstr = "D"
            else:
                sensstr = "G"
    
            # S'il existe un parcours valide ... on sort 
            if len(self.chaineAct[sens].valid) > 0:
                return lst
    
            # On passe par tous les parcousrs
            for i in range(len(self.chaineAct[sens].parcoursElemEntr)):
#                print "  Parcours",i,":",self.chaineAct[sens].parcoursElemEntr[i]
    
                # Parcours du parcours i
                for po in self.chaineAct[sens].parcoursElemEntr[i]:
    
                    # Cas des roulements
                    if po.typelem == "R":
    
                        radialePreced = lst[len(lst)-1][3:]
                        # On ajoute les 2 bagues du roulement poussé
#                        print po, radialePreced, self.mtg.elemPos(po).supporteEffortAxial(sens)
                        if (radialePreced == "Ar" \
                               and self.mtg.elemPos(po).supporteEffortAxial(sens)) \
                           or (radialePreced == "Al" \
                               and self.mtg.elemPos(po).supporteEffortAxial(not sens)) \
                           or (self.mtg.elemPos(po).supporteEffortAxial(not sens) \
                               and self.mtg.elemPos(po).supporteEffortAxial(sens)):
                            lst.append(po.code()[0:3]+'--')
#                            print po.code()[0:3]+'--'
                            
                        # On ajoute la bague du roulement poussée
                        else:
                            po.palier = lst[len(lst)-1][1]
                            lst.append(po.code(radialePreced))
    ##                        if radialePreced == "Ar":
    ##                            lst.append("BI" + lst[len(lst)-1][1] + sensstr)
    ##                        else:
    ##                            lst.append("BE" + lst[len(lst)-1][1] + sensstr)
    
                    # Cas des arrets
                    else:        
                        lst.append(po.code())
                        
                        # Cas des entretoises
                        if self.mtg.elemPos(po).estEntretoise():
    ##                        print "Entretoise"
                            lst.append(po.opposee().code())
    
    
                          
            # On ajoute les arrets fixés à l'arbre
            for p in [Montage.PositionDansPivot("G","A","G","Ar"),
                        Montage.PositionDansPivot("G","A","D","Ar"),
                        Montage.PositionDansPivot("D","A","G","Ar"),
                        Montage.PositionDansPivot("D","A","D","Ar")]:
    ##                print self.elemPos(p).codeTag(p)
                el = self.mtg.elemPos(p)
                if el is not None \
                    and el.supporteEffortAxial() \
                    and not el.estEpaulement():
    ##                    lst.append(mtg.elemPos(p).codeTag(p))
                    lst.append(p.code())
                    # Ajout bague intérieure si entrainée
    #                if p.cotelem <> sensstr:
    #                    lst.append("BI"+p.palier+sensstr)
    
    
            # Nettoyage de la liste
            lst2 = []
            for i in range(len(lst)):
                if not lst[i] in lst2:
                    lst2.append(lst[i])
            
    ##        print "  Liste des éléments non arrétés :",lst2
            return lst2
        
        
        for s in [0,1]:
            
            # Analyse :
            self.chaineAct[s].determiner(self.mtg, zoneMtg)
            self.listeElementsNonArretes[s] = listeElementsNonArretes(s)
            print self.listeElementsNonArretes[s]
            # Résultats :
            
                # Arbre pas arrêté !
            if len(self.chaineAct[s].valid) == 0:
                self.resultatImmobilisation[s].append(Const.MessageAnalyse('ArretArbreSens', [s]))

                # Arbre arrêté !
            else:
                self.resultatImmobilisation[s].append(Const.MessageAnalyse('ImmobCorrect'))

                # hyperstatique !
            if len(self.chaineAct[s].valid) > 1:
                self.resultatImmobilisation[s].append(Const.MessageAnalyse('Hyperstatique'))


        # Message Principal
        #-------------------
        if    self.resultatImmobilisation[0][0].clef == 'ImmobCorrect' \
          and self.resultatImmobilisation[1][0].clef == 'ImmobCorrect':
            self.messageImmobilisation = Const.MessageAnalyse('ArbreArrete')
        else:
            self.messageImmobilisation = Const.MessageAnalyse('ArbrePasArrete')
            
        
    
    ##########################################################################
    #  Analyse : résistance axiale du montage #
    ##########################################################################
    def analyserResistanceAxialeMtg(self):
        """ Analyse la résistance axiale du montage complet 
        """
        
        #############################################################################                
        def nomsElem(sens):
            lst = []
            pos = Montage.PositionDansPivot()
            for res in self.lstElemResistePas[sens]:
                lst.append(Const.MessageAnalyse(mess = pos.traduireEnTexte(res), coul = "rouge"))
            return lst
        
        
        # Résistance axiale du montage ...
        # --> Résultats :
        self.resultatEffortAxialMtg = [[],[]]
        # --> Eléments ne résistant : par sens ...
        self.lstElemResistePas = [[],[]]
        # --> Image du Schéma de structure (avec charges)
        self.imageSchemaCharges = None
        # --> Message principal
        self.messageResistanceAxiale = None
        
        
        lstElemResistePas = [[],[]]
        for sens in [0,1]:
##            print "sens", sens
            chaine = self.chaineAct[sens]
            for nParcours in chaine.valid:
##                print chaine.parcoursElemEntr[nParcours]
                for n in range(len(chaine.parcoursElemEntr[nParcours])):
                    posParcours = chaine.parcoursElemEntr[nParcours][n]
                    elem = self.mtg.elemPos(posParcours)
##                    print n
                    if (elem.num is not None) and not (posParcours.typelem == "R" and \
                       chaine.parcoursElemEntr[nParcours][n-1].radiale == chaine.parcoursElemEntr[nParcours][n+1].radiale):
                        if elem.effortAxialSupporte() < self.cdcf.effortAxial[sens].val:
##                            print posParcours,self.resultatResistanceRlt[posParcours.palier].clef =='RltSupportePas'
                            if posParcours.typelem <> "R" \
                               or self.resultatResistanceRlt[posParcours.palier].clef == 'RltSupportePas':
                                lstElemResistePas[sens].append(posParcours.code())

            # On ote les doublons et on "regroupe" les bagues des roulements
            for e in lstElemResistePas[sens]:
                if e[0] == "R":
                    e = e[0:2]+"---"
                if not e in self.lstElemResistePas[sens]:
                    self.lstElemResistePas[sens].append(e)

            if lstElemResistePas[sens] <> []:
                self.resultatEffortAxialMtg[sens].append(Const.MessageAnalyse('ElemResistPas'))
                self.resultatEffortAxialMtg[sens].extend(nomsElem(sens))
                
            else:
                if chaine.valid == []:
                    self.resultatEffortAxialMtg[sens].append(Const.MessageAnalyse('ArretArbreSens', [sens]))
                else:
                    self.resultatEffortAxialMtg[sens].append(Const.MessageAnalyse('ChargeAxOk'))
        
        # Message principal
        #-------------------
        if    self.resultatEffortAxialMtg[0][0].clef == 'ChargeAxOk' \
          and self.resultatEffortAxialMtg[1][0].clef == 'ChargeAxOk':
            self.messageResistanceAxiale = Const.MessageAnalyse('ChargeAxOk')
        else:
            self.messageResistanceAxiale = Const.MessageAnalyse('ChargeAxNo')
             
        # Image du Schéma de Structure
        #------------------------------
        def charge(cote):
            return [self.typeCharge[cote], 
                    self.typeCharge[cote] == 0 \
                        or self.resultatResistanceRlt[cote] == None \
                        or self.resultatResistanceRlt[cote].clef == 'RltSupporte']
        charges = {"G" : charge("G"),
                   "D" : charge("D")} 
        self.imageSchemaCharges = self.schemaStructure.bitmap(charges)
    
    
    ##########################################################################
    #  Analyse : résistance aux charges des roulements #
    ##########################################################################
    def analyserResistanceRlt(self):
        """ Analyse la résistance aux charges des roulements
                * Type de charge subie par un roulement :
                    0 : aucune
                    1 : x+
                    2 : x-
                    4 : y
                * 
        """
        
        # Résistance des roulements ...
        # --> Résultats : un par palier ...
        self.resultatResistanceRlt = {"G" : None,
                                      "D" : None}
        
        # --> Un type de charge par palier ...
        self.typeCharge = {"G" : 0,
                           "D" : 0}
#        self.sensChargeAx = {"G" : [],
#                             "D" : []}

        
        def definirTypeChargeCdCF(palier):
            """ Type de charge que doit supporter le <palier> d'après le CdCF
            """
            
            t = 0
#            self.sensChargeAx[palier] = []
    ##        print
    #        print "Definition type de charge CdCF",palier, "-->",
            if self.cdcf.effortRadial[palier].get() <> 0:
                t += 4
                
            for sens in [0,1]:
#                print self.cdcf.effortAxial[sens].get(),"-->",
                if self.cdcf.effortAxial[sens].get() <> 0:
                    t = t|(1+sens)
    #        print t
            return t
        
    
        # Analyse des roulements ...
        for i in ["G","D"]:
            # Type de charge suportée par le palier
            typeChargeCdCF = definirTypeChargeCdCF(i)
            self.typeCharge[i] = (self.ddlSupprimes[i]|4) & typeChargeCdCF
            
            rlt = self.mtg.palier[i].rlt

            # Détermination de l'intensité de la charge axiale (s'il y en a une ...)
            chargeAxiale = 0
            ls = []
            if self.typeCharge[i]&1 :
                ls.append(0)
            if self.typeCharge[i]&2:
                ls.append(1)
            for sens in ls:
                chargeAxiale = max(chargeAxiale, self.cdcf.effortAxial[sens].get())

            # Détermination de l'intensité de la charge radiale (s'il y en a une ...)
            chargeRadiale = self.cdcf.effortRadial[i].get()

            # On teste si le roulement résiste ...
            if rlt.num is not None:
                if self.typeCharge[i]&4:
                    typeCharge = "radial"
                    intensite = chargeRadiale
                if self.typeCharge[i]&3:
                    typeCharge = "axial"
                    intensite = chargeAxiale
                if self.typeCharge[i]&3 and self.typeCharge[i]&4:
                    typeCharge = "combi"
                    intensite = max(chargeRadiale,chargeAxiale)
                if self.typeCharge[i] == 0:
                    typeCharge = ""
                    intensite = 0
                    
#                print self.typeCharge[i]
#                print "test rlt",i , typeCharge, intensite,
                if typeCharge <> "" and rlt.coefTaille(rlt.chargeAdm[typeCharge]) < intensite:
#                if    (self.typeCharge[i]&4 and (rlt.coefTaille(rlt.chargeAdm["radial"]) < chargeRadiale)) \
#                   or (self.typeCharge[i]&3 and (rlt.coefTaille(rlt.chargeAdm["axial"]) < chargeAxiale)) \
#                   or (self.typeCharge[i]&3 and self.typeCharge[i]&4 and (rlt.coefTaille(rlt.chargeAdm["combi"]) < max(chargeRadiale,chargeAxiale))):
                    self.resultatResistanceRlt[i] = Const.MessageAnalyse('RltSupportePas')
#                    print "No"
                else:
                    self.resultatResistanceRlt[i] = Const.MessageAnalyse('RltSupporte')
#                    print "Ok"

        # Message principal
        supp = []
        for p in ["G","D"]:
            if self.resultatResistanceRlt[p] is not None \
               and self.resultatResistanceRlt[p].clef == 'RltSupportePas':
                supp.append(p)
        if len(supp) == 2:
            self.messageResistanceRlt = Const.MessageAnalyse('TRltSupportePas')
        elif len(supp) == 1:
            self.messageResistanceRlt = Const.MessageAnalyse('1RltSupportePas', supp[0])
        else:
            self.messageResistanceRlt = Const.MessageAnalyse('TRltSupporte')
#        print "Charges CdCF :", self.typeCharge
        

    ##########################################################################
    #  Analyse : Etancheite #
    ##########################################################################
    def analyserEtancheite(self):
        """ Analyse l'étanchéité du montage
        """
#        print "Analyse etancheite"

        #
        # Etanchéité du montage
        #
        # --> Résultats :
        self.resultatEtancheite = {"M" : None,
                                   "G" : {'vitt' : None,
                                          'pres' : None},
                                   "D" : {'vitt' : None,
                                          'pres' : None}}
        
        pasEtanchStat = {"G" : {"Ar" : False,            # 
                                "Al" : False},           # Localisation 
                         "D" : {"Ar" : False,            #  du défaut 
                                "Al" : False},           #
                         "B" : []}                # 
        
        pasEtanchDyn = {"G" : {"P"  : False,
                               "PV" : False},
                        "D" : {"P"  : False,
                               "PV" : False},
                        "B" : []}
        
        pasDeJoint = {"G" : {"Ar" : False,
                             "Al" : False},
                      "D" : {"Ar" : False,
                             "Al" : False},
                      "B" : False}
        
        for p in ["G","D"]:
            # Etanchéité statique
            #--------------------
            for r in ["Ar","Al"]:
                if  self.mtg.palier[p].jnt[r].num is None:
#                    print "pas de joint", p,r, 
#                    pasEtanchStat[p][r] = True
                    pasDeJoint[p][r] = True
                    if r == "Ar":
                        pasDeJoint["B"] = True
                        pasEtanchStat["B"].append('ManqueJoint'+p)
                        pressAdm = -1
                    else:
                        if self.mtg.palier[p].jnt["Ar"].num is None:
                            pressAdm = -1
                        else:
                            pressAdm = self.cdcf.pressionAdmChapeau
                else:
                    pressAdm = self.mtg.palier[p].jnt[r].pressAdm[r]
                
#                print "Pr",self.cdcf.pression.get(), "PrAdm",pressAdm 
                if  pressAdm < self.cdcf.pression.get():
#                    print "pas étanche !", pressAdm, "<", self.cdcf.pression.get()
                    pasEtanchStat[p][r] = True
                    if not ('PressTrop'+p in pasEtanchStat["B"]):
                        pasEtanchStat["B"].append('PressTrop'+p)
#                else: print
                    
            
            # Etanchéité dynamique
            #---------------------
            # Calcul du facteur PV
            if self.mtg.palier[p].taille == "P" :
                coefVitt = 1
            else:
                coefVitt = 1.5
            facteurPV = self.cdcf.pression.get()*self.cdcf.vitesse.get()*coefVitt/ \
                        (self.cdcf.echellePression*self.cdcf.echelleVitesse*coefVitt) \
                        *10

#            print "PV", facteurPV,
            
            # Vitesse admissible par le joint
            if  self.mtg.palier[p].jnt["Ar"].num is None:
                vittAdm = 10
                facteurPVAdm = -1
            else:
                vittAdm = self.mtg.palier[p].jnt["Ar"].vittAdm
                facteurPVAdm = self.mtg.palier[p].jnt["Ar"].facteurPV
            
#            print "PVAdm", facteurPVAdm
            # Test à la vitesse
            if vittAdm < self.cdcf.vitesse.get():
                pasEtanchDyn[p]["P"] = True
                pasEtanchDyn["B"].append('VitesseTrop'+p)
            # Test au facteur PV
            if facteurPVAdm < facteurPV:
                pasEtanchDyn[p]["PV"] = True
                pasEtanchDyn["B"].append('FactPVTrop'+p)
        
        #
        # Compatibilité lubrifiant
        #
        compatible = True
        if self.cdcf.lubrifiant.get() == 0 :
            for p in ["G","D"]:
                if  self.mtg.palier[p].jnt["Ar"].num is 203:
                    compatible = False
                    continue
        
        
        #
        # Bilan
        #-------
        self.resultatEtancheite["S"] = pasEtanchStat
        self.resultatEtancheite["J"] = pasDeJoint
        
        if compatible:
            self.resultatEtancheite["C"] = Const.MessageAnalyse('LubrifComp')
        else:
            self.resultatEtancheite["C"] = Const.MessageAnalyse('LubrifPasComp')
        
        if pasEtanchStat["B"] <> []:
            self.resultatEtancheite["SB"] = Const.MessageAnalyse('PasEtanchStat')
            self.resultatEtancheite["SB+"] = []
            for m in pasEtanchStat["B"]:
                self.resultatEtancheite["SB+"].append(Const.MessageAnalyse(m[:-1],m[-1:]))
        else:
            self.resultatEtancheite["SB"] = Const.MessageAnalyse('EtanchStat')

            self.resultatEtancheite["D"] = pasEtanchDyn
            if pasEtanchDyn["B"] <> []:
                self.resultatEtancheite["DB"] = Const.MessageAnalyse('PasEtanchDyn')
                self.resultatEtancheite["DB+"] = []
                for m in pasEtanchDyn["B"]:
                    self.resultatEtancheite["DB+"].append(Const.MessageAnalyse(m[:-1],m[-1:]))
            else:
                self.resultatEtancheite["DB"] = Const.MessageAnalyse('EtanchDyn')



    ##########################################################################
    #  Analyse : type de charge   #
    ##########################################################################
    


                    






    
                
            

    
           

        
    ###########################################################################
    def montrerCollision(self, zoneMtg, lstCode, palier = None,
                         active = True, deuxCouleurs = True):
        """ Met en évidence les obstacles au démontage """
        
        
#        print "Montrer collision :",lstCode,
        obstaclesRoulements = len(lstCode) == 1
        
#        # On quitte si déja démonté ...
#        if not obstaclesRoulements and self.elemDemonte <> []:
#            return

#        # On quitte si déja démonté ...
#        if obstaclesRoulements and not ("AnimEnsb0" in self.elemDemonte \
#                                   or "AnimEnsb1" in self.elemDemonte):
#            return
        
        if    (self.cdcf.bagueTournante == "I" and not obstaclesRoulements) \
           or (self.cdcf.bagueTournante == "E" and obstaclesRoulements):
            rad = "Al"
        else:
            rad = "Ar"
#
        # Ajout roulement pour obstacles roulement
        if obstaclesRoulements:
            lstCode = [lstCode[0], "R"+palier+"---"]
#        else:
#            lstCode = lstCode
            
#        print lstCode
        # Liste des position pour la flêche
        lstPos = []
        
        # Couleurs d'affichage
        if deuxCouleurs:
            coul = "rouge"
        else:
            coul = "noir"
        
        lstCodeCoul = [[lstCode[0],"noir"],
                       [lstCode[1],coul]]
        
        

        for pcode in lstCodeCoul:
            elemClef = self.mtg.clefElemPosCode(pcode[0])
            elem = elemClef[0]
            lstClef = elemClef[1]
            
            lstPos.append(Montage.PositionDansPivot().posCode(pcode[0]))
            
#            for clef in lstClef:
#                if active:
#                    elem.item[clef].couleur(pcode[1])
#                else:
#                    elem.item[clef].normale()
        
#        print lstPos  
        
        if active:
            self.obstacleTrace = (lstPos,rad)
        else:
            self.obstacleTrace = None
            
        zoneMtg.Redessiner(self)


    ##########################################################################
    def animerManqueArret(self, zoneMtg, sens, position = None):
        "Animation des éléments non arrêtés axialement"
        
#        print "Animation des éléments non arrêtés axialement"
#        print "listeElementsNonArretes",self.listeElementsNonArretes[sens]

        wx.BeginBusyCursor()
        
        lstItemAnim = []

        # signe du sens de déplacement ##############################
        sgn = 1 - sens*2

        # Préparation des éléments non arêtés #####################
        for i in zoneMtg.lstItemMtg:     # On parcours tous les items affichés
            # On inclus tous les éléments d'arbres
            if TAG_ARBRE in i.tag:
                lstItemAnim.append(i)
                continue
            # On inclus les éléments de la liste (sans les éléments d'alésage)
            else:
#                print i.tag,
                for t in self.listeElementsNonArretes[sens]:
                    if t in i.tag and not TAG_ALESAGE in i.tag:
                        lstItemAnim.append(i)
                        continue

        s = set(lstItemAnim)
        lstItemAnim = list(s)

#        print "lstItemAnim",lstItemAnim

        # Lancement de l'animation
        #=========================
        # Durée (en seconde) & amplitude (en pixels)
        duree, amplitude  = 2, 4
        # Nombre de positions
        nbPos = duree * 25
        # Calcul du pas
        s = 0
        for n in range(nbPos):
            s += sin((1.0*n)/nbPos*pi)
#        pas = 2 * amplitude/s
        
#        def GroupeBmp(lstItem):
#            # Regroupement des images
#            bmp = wx.EmptyBitmap(zoneMtg.maxWidth, zoneMtg.maxHeight)
#            memdc = wx.MemoryDC(bmp)
#            memdc.SetBackground(wx.Brush(wx.Colour(255,255,254))) #wx.TRANSPARENT_BRUSH)
#            memdc.Clear()
#            for i in lstItemAnim:
#                memdc.DrawBitmap(i.bmp, i.pos[0], i.pos[1], True)
##            zoneMtg.hachurer(memdc, self.listeElementsNonArretes[sens])
#            memdc.SelectObject(wx.NullBitmap)
#            img = wx.ImageFromBitmap(bmp)
#            img.SetMaskColour(255,255,254)
#            img.SetMask(True)
#            bmp = wx.BitmapFromImage(img)
#            return bmp

        # Sauvegarde de la position en x de chaque item
        for i in lstItemAnim:
            i.x = i.pos[0]
        
        if position == None:
            # Mouvement
            oldx = 0
            for c in range(nbPos):
                tm = time.clock()
                x = int(round(-amplitude*cos(pi*2*c/nbPos)+amplitude))
                if x <> oldx:
                    for i in lstItemAnim:
                        i.pos = (i.x + sgn*x, i.pos[1])
                    oldx = x
                    zoneMtg.Redessiner()
                dt = 0.05 - time.clock() + tm
                if dt > 0:
                    time.sleep(dt)
        else:
            for i in lstItemAnim:
                i.pos = (i.x + sgn*amplitude*2*position, i.pos[1])
       
       
        wx.EndBusyCursor()
       
       
    ##########################################################################
    #  Analyse : montabilité  #
    ##########################################################################
    def analyserMontabilite(self, demonterRltSerres, zoneMtg):
        """ Analyse de la montabilité du montage
        """
    
        self.demonterRltSerres = demonterRltSerres
        
        # Montabilité du montage
        # --> Rélultat général :
        self.resultatMontabilite = None
        # --> Liste des éléments mobiles : une par sens ...
        self.listeElemArbre = [[],[]]
        # --> Liste des éléments fixes : une par sens ...
        self.listeElemAlesage = [[],[]]
        # --> Liste des éléments à démonter pour le démontage : une par sens ...
        self.lstArretsAEnleverEns = [[],[]]
        # --> Liste des éléments à démonter pour le démontage des roulements : une par sens et par palier...
        self.lstArretsAEnleverRlt = {"G" : [[],[]],
                                     "D" : [[],[]]}
        # --> Liste des obstacles au Montage/Démontage de l'ensemble: une par sens ...
        self.obstacleEnsble = [[],[]]

        # --> Liste des obstacles au Montage/Démontage des roulements: une par sens et par palier ...
        self.obstacleRoults = {"G" : [[],[]],
                               "D" : [[],[]]}
        # --> Liste des obstacles au Montage/Démontage des bagues isolées : une par sens et par palier ...
        self.obstacleBagueIsolee = {"G" : [[],[]],
                                    "D" : [[],[]]}
        
        

        def bagueIndemontable(rad):
            if rad == "Ar":
                if self.cdcf.bagueTournante == "I" and not self.demonterRltSerres:
                    return True
                else:
                    return False
            elif rad == "Al":
                if self.cdcf.bagueTournante == "E" and not self.demonterRltSerres:
                    return True
                else:
                    return False
            

        class groupeMontage():
            def __init__(self):
                self.lst = [[]] * 6
                self.min = [1] * 6
                
            def __repr__(self):
                t = []
                n = 1
                for p in self.lst:
                    n = max(n,len(p))
                
                c = ""
                for m in self.min:
                    c += "\t  "+str(m)
                t.append(c+"\n")
                
                for l in range(n):
                    c = ""
                    for p in self.lst:
                        try:
                            c += "\t"+p[l]
                        except:
                            c += "\t"
                    t.append(c+"\n")
                
                if self.lst[0][0][4] == "r":
                    t.reverse()
                texte = ''.join(t)
                return texte
            
            def agrandir(self, pos, groupeOppose):
                tranche = self.lst[pos]
                trancheOpp = groupeOppose.lst[pos]
                if len(tranche) > self.min[pos]:
                    trancheOpp.append(tranche.pop())
                    return True
                return False
            
            def enlever(self, pos, mtg, lstArretsAEnleverEns):
                tranche = self.lst[pos]
#                print tranche[-1:][0]
                if mtg.estEnlevable(tranche[-1:][0]):
                    lstArretsAEnleverEns.append(tranche.pop())
                    return True
                return False

        def listeElementsArbre(sens):
            """ Renvoie la liste des éléments liés à l'arbre 
                sur leur logement dans le sens <sens>
                PROVISOIRE !!
            """
            
#            print "Etabli la listedes éléments liés à l'arbre"
#            print ">>> Sens",sens
#            print ">>> Démonter Rlts serrés :",self.demonterRltSerres
          
            grp = groupeMontage()
                    
            # La liste la plus petite possible (seulement les logements)
            lst =  [["-G-Ar"],
                    ["-G-Ar"],
                    ["-G-Ar"],
                    ["-D-Ar"],
                    ["-D-Ar"],
                    ["-D-Ar"]]        
            
            # On met les arrêts d'arbre
            for pos in [0,2,3,5]:
                p = lst[pos][0][1]
                if pos == 0 or pos == 3:
                    c = "G"
                else:
                    c = "D"
                elem = self.mtg.palier[p].arr["Ar"][c]
                if elem.num is not None:
                    if not elem.estEntretoise():
                        lst[pos].append("A"+p+c+"Ar")
                            
            
            # On met les roulements (si sérrés sur l'arbre)
            for pos in [1,4]:
                p = lst[pos][0][1]
                elem = self.mtg.palier[p].rlt
                if elem.num is not None:
                    if bagueIndemontable("Ar"):
                        if elem.estSeparableSens(not sens, "Ar"):
                            lst[pos].append("R"+p+"-Ar")
                        else:
                            lst[pos].append("R"+p+"---")
                            
                    
            
            # On retourne pour mettre dans le sens du démontage
            if sens == 1:
                lst.reverse()
                
            grp.lst = lst
            
            # On défini les "niveaux" minimum ...
            for p in [0,1,4,5]:
                grp.min[p] = len(grp.lst[p])
                
            for p in [2,3]:
                grp.min[p] = len(grp.lst[p])
            
            return grp

        def listeElementsAlesage(lstAr, sens):
            """ Renvoie la liste des éléments "libres"
                 = complémentaire de <lMob> !
            """
            
            def ccote(pos):
                if (pos == 0 or pos == 3) and sens == 0 \
                    or (pos == 2 or pos == 5) and sens == 1:
                    return "G"
                else:
                    return "D"
                
            grp = groupeMontage()
            
            # La liste la plus grande possible
            lst =  [["-G-Al", "AGGAl", "AGGAr"],
                    ["-G-Al", "RG---", "RG-Al", "RG-Ar"],
                    ["-G-Al", "AGDAl", "ADGAl", "AGDAr", "ADGAr"],
                    ["-D-Al", "ADGAl", "AGDAl", "ADGAr", "AGDAr"],
                    ["-D-Al", "RD---", "RD-Al", "RD-Ar"],
                    ["-D-Al", "ADDAl", "ADDAr"]]
    
            # On retourne pour mettre dans le sens du démontage
            if sens == 1:
                lst.reverse()
    
            # On ote ceux qui sont déja dans lstAr
            for pos in range(6):
                for p in lstAr[pos]:
                    if p in lst[pos]:
                        lst[pos].remove(p)
                        if p[0] == "R":
                            if p[4] == "-":
                                lst[pos].remove(p[0:3]+"Ar")
                                lst[pos].remove(p[0:3]+"Al")
                            else:
                                lst[pos].remove(p[0:3]+"--")
                    
            # On ote les arrets absents
            for pos in [0,2,3,5]:
                for p in lst[pos][1:]:
                    palier = p[1]
                    cote = p[2]
                    rad = p[-2:]
                    elem = self.mtg.palier[palier].arr[rad][cote]
                    if elem.num is None:
                        lst[pos].remove(p)
                    
            # On ajoute les entretoises sur épaulement
            for r in ["Ar","Al"]:
                if sens == 0:
                    pG, pD = 2,3
                else:
                    pG, pD = 3,2
                elemG, elemD = self.mtg.palier["G"].arr[r]["D"], self.mtg.palier["D"].arr[r]["G"]
                if elemG.estEpaulement() and elemD.estEntretoise():
                    try:
                        lst[pD].remove("AGD"+r)
                    except: pass
                elif elemD.estEpaulement() and elemG.estEntretoise():
                    try:
                        lst[pG].remove("ADG"+r)
                    except: pass
                else:
                    try:
                        lst[pD].remove("AGD"+r)
                    except: pass
                    try:
                        lst[pG].remove("ADG"+r)
                    except: pass
            
                                    
            # On ote les morceaux de roulements inutiles
            for pos in [1,4]:
                if len(lst[pos]) > 3:
                    p = lst[pos][0][1]
                    elem = self.mtg.palier[p].rlt
                    if elem.num is None:
                        lst[pos].remove("R"+p+"---")
                        lst[pos].remove("R"+p+"-Ar")
                        lst[pos].remove("R"+p+"-Al")
                    elif elem.estSeparableSens(sens, "Al"):
                        lst[pos].remove("R"+p+"---")
                    else:
                        lst[pos].remove("R"+p+"-Ar")
                        lst[pos].remove("R"+p+"-Al")
            
            grp.lst = lst
            
            # On défini les "niveaux" minimum ...
                # On compte les arrêts d'alésage
            for pos in [0,2,3,5]:
                p = lst[pos][0][1]
                c = ccote(pos)
                elem = self.mtg.palier[p].arr["Al"][c]
#                print pos, elem.num
                if elem.num is not None:
                    if not elem.estEntretoise():
                        grp.min[pos] +=1
            
                # On met les roulements (si sérrés sur l'arbre)
            for pos in [1,4]:
                p = lst[pos][0][1]
                elem = self.mtg.palier[p].rlt
                if elem.num is not None:
                    if self.cdcf.bagueTournante == "E" and not self.demonterRltSerres:
                        grp.min[pos] +=1
                        
            return grp

        def listeElementsAEnleverRlt(sens, palier):
            "Etabli la liste des éléments à enlever pour le démontage des roulements"
            lst = []
    
            if (sens == 0 and palier == "G") \
               or (sens == 1 and palier == "D"):
                if self.mtg.deuxrlt():
                    return []
            
            if sens == 0:
                a = "D"
            else:
                a = "G"
                
            if self.cdcf.bagueTournante == "I":
                r = "Ar"
            else:
                r = "Al"
    
            if self.mtg.palier["G"].rlt.num is None:
                p = "D"
            elif self.mtg.palier["D"].rlt.num is None:
                p = "G"
            else:
                p = a
    
            code = "A"+p+a+r
            if self.mtg.clefElemPosCode(code)[0].num is not None:
                lst.append(code)
                
            # 
            # On s'occupe des joints
            #
            # Listes des éléments libres et fixes
#            if self.cdcf.bagueTournante == "I":
#                lstElemLibres = self.listeElemAlesage[sens]
#            else:
#                lstElemLibres = self.listeElemArbre[sens]
#            self.lstArretsAEnleverEns[sens]
            lstElemEnleve = self.lstArretsAEnleverEns[0] + self.lstArretsAEnleverEns[1]
#            print "Liste élem enlevés", lstElemEnleve
            code = "J"+p+"-Ar"
            if self.mtg.clefElemPosCode(code)[0].num is not None and not code in lstElemEnleve:
                lst.append(code)
                
            code = "J"+p+"-Al"
            if self.mtg.clefElemPosCode(code)[0].num is not None and not code in lstElemEnleve:
                lst.append(code)
    
#            print lst
            
    ##        print ">>> à enlever",palier , lst
            return lst

        def estDemontable(sens):
            "Teste si le montage est démontable dans le sens <sens>"
    
            def demontagePossible(sens, posAr, posAl):

                def dimension(int_ext, pcode, fix = False):
                    """Renvoie la dimension de l'élément à la position <pcode>
                        mesurée depuis l'<int_ext>
                        parmis les éléments <fix> ou pas"""
            ##        print "Dimension pcode =",pcode
                    if pcode[3:] == "--":
                        dicElem = {"Ar" : self.mtg.clefElemPosCode(pcode[0:3]+"Ar")[0],
                                   "Al" : self.mtg.clefElemPosCode(pcode[0:3]+"Al")[0]}
                        if   (int_ext == "E" and dicElem["Al"].num is not None) \
                          or (int_ext == "I" and dicElem["Ar"].num is None):
                            rad = "Al"
                        else:
                            rad = "Ar"
                        elem = dicElem[rad]
                    else:
                        elem = self.mtg.clefElemPosCode(pcode)[0]
            
                    radiale = pcode[3:]
                    if radiale == "--":
                        if self.cdcf.bagueTournante == "I":
                            radiale = "Al"
                        else:
                            radiale = "Ar"
            ##        print " --> élém =",elem,elem.pos,elem.taille
                    dim = elem.dimensions(radiale, int_ext, self.mtg.palier[pcode[1]].taille)
            ##        print " --> dimension =",dim
                    # Choix de la dimension appropriée :
                    #-----------------------------------
                    
                    # Cas roulements séparés
                    if pcode <> "" and pcode[0] == "R" and pcode[3] == "A":
                        return dim['demonte']
            
                    # Cas des arrêts démontables
                    if elem.num <> None \
                       and not elem.pasDemontable(not self.mtg.deuxrlt(),elem.pos) \
                       and fix:
            ##            print "Démontage élément",elem.num,pcode,elem.pos
                        return dim['demonte']
            
                    # Cas des Arrêts mobiles
                    if int_ext == "E" and pcode[0] == "A":
                        return dim['entier']
                        
                    return dim['entier']
     
#                print lAr[posAr][-1:][0],lAl[posAl][-1:][0],
                
                dimAr = dimension("E", lAr[posAr][-1:][0])
                dimAl = dimension("I", lAl[posAl][-1:][0])
#                print "\t",dimAr, dimAl,
                
                if dimAl >= dimAr: # Ca passe !
#                    print
                    if posAl > 0:
                        return demontagePossible(sens, posAr, posAl-1)
                    elif posAr > 1:
                        return demontagePossible(sens, posAr-1, posAr-2)
                    else:
                        return True
                    
                else: # Ca passe pas !
#                    print "^",
                    if not bagueIndemontable("Al") and grAl.enlever(posAl, self.mtg, self.lstArretsAEnleverEns[sens]):
#                        print "//",lAl[posAl][-1:][0]
                        return demontagePossible(sens, posAr, posAl)
                    elif not bagueIndemontable("Ar") and grAr.enlever(posAr, self.mtg, self.lstArretsAEnleverEns[sens]):
#                        print "//",lAr[posAr][-1:][0]
                        return demontagePossible(sens, posAr, posAl)
                    elif grAl.agrandir(posAl, grAr):
                        if posAl in [2,3]:
                            p = lAr[posAl][-1:][0][1]
                            c = lAr[posAl][-1:][0][2]
                            rad = lAr[posAl][-1:][0][3:]
                            elem = self.mtg.palier[p].arr[rad][c]
                            if elem.estEntretoise():
#                                print "^",
                                grAl.agrandir(posAl-1, grAr)
#                        print "Al"
                        return demontagePossible(sens, posAr, posAl)
                    
                    else:
#                        print "--"
                        return [posAr, posAl]
                
#            print "Test Montabilité Ensemble ...", sens
            
            self.lstArretsAEnleverEns[sens] = []
            
            grAr = listeElemArbre
            lAr = listeElemArbre.lst
            
            grAl = listeElemAlesage
            lAl = listeElemAlesage.lst
            
            obs = demontagePossible(sens, 5, 4)
            if obs is not True:
                self.obstacleEnsble[sens] = [lAr[obs[0]][-1:][0],lAl[obs[1]][-1:][0]]
            
            # Compilation et mise à jour des listes
            #--------------------------------------
#            print ">>> Arbre   :\n",listeElemArbre
#            print ">>> Alésage :\n",listeElemAlesage
            lst = []
            for l in listeElemArbre.lst:
                lst += l[1:]
            s = set(lst)
            lst = list(s)
            self.listeElemArbre[sens] = lst
        
            lst = []
            for l in listeElemAlesage.lst:
                lst += l[1:]
            s = set(lst)
            lst = list(s)
            self.listeElemAlesage[sens] = lst
            
            # Traitement des joints
            #-----------------------
            # On s'occupe de ceux qui sont associée à un arret alésage
            for p in ["G","D"]:
                for r in ["Ar","Al"]:
                    if self.mtg.palier[p].jnt[r].num is not None:
                        codeArrAssocie = "A"+p+p+"Al"
                        if codeArrAssocie in self.lstArretsAEnleverEns[sens]:
                            self.lstArretsAEnleverEns[sens].append("J"+p+"-"+r)
                        else:
                            self.listeElemAlesage[sens].append("J"+p+"-"+r)
            
            # On s'occupe de ceux qui gènent de toute façon ... si démontage possible !
            if self.obstacleEnsble[sens] == [] :
                
                # On déterminer le coté qui gène ...
#                if (sens == 0 and self.cdcf.bagueTournante == "I")\
#                    or (sens == 1 and self.cdcf.bagueTournante == "E"):
#                    p = "G"
#                else:
#                    p = "D"
                if sens == 0:
                    p = "G"
                else:
                    p = "D"
#                print "Coté qui gène :", p, sens, self.cdcf.bagueTournante
                # On enlève le(s) joint(s) qui gène(nt) ...
                enleveJnt = False
                for r in ["Ar","Al"]:
                    if self.mtg.palier[p].jnt[r].num is not None: 
                        self.lstArretsAEnleverEns[sens].append("J"+p+"-"+r)
                        enleveJnt = True
                
                # On enlève l'arrêt qui est sur le même chapeau ...
                if enleveJnt:
                    enleveJnt = False
                    codeArrAssocie = "A"+p+p+"Al"
                    if codeArrAssocie in self.listeElemAlesage[sens]:
                        self.lstArretsAEnleverEns[sens].append(codeArrAssocie)
                        
            
#            print ">>> Arbre   :",self.listeElemArbre[sens]
#            print ">>> Alésage :",self.listeElemAlesage[sens]
#            print ">>> Obstacles :", self.obstacleEnsble[sens]
#            print ">>> Eléments à enlever :", self.lstArretsAEnleverEns[sens]
#            print
            
            return
        
        
        def estDemontableRlt(sens, palier, bagueLibre):
            "Teste si le roulement <palier> est démontable dans le sens <sens>"
    
    #        print
#            print "Test Montabilité Roulements"
#            print ">>> Sens",sens
#            print ">>> Roulement",palier
#            print ">>> Bague libre",bagueLibre
    
            
            # Détermination des arrets concernés pour le démontage du roulement
            lstArrets = []
            if (self.cdcf.bagueTournante == "I" and bagueLibre) \
               or (self.cdcf.bagueTournante == "E" and not bagueLibre):
                radiale = "Ar"
            else:
                radiale = "Al"
    
            if sens == 0:
                if palier == "D":
                    lstArrets.append("ADD"+radiale)
                else:
                    lstArrets.append("AGD"+radiale)
                    lstArrets.append("ADG"+radiale)
                    lstArrets.append("ADD"+radiale)
            else:
                if palier == "G":
                    lstArrets.append("AGG"+radiale)
                else:
                    lstArrets.append("ADG"+radiale)
                    lstArrets.append("AGD"+radiale)
                    lstArrets.append("AGG"+radiale)
    
    ##        print ">>> Arrêts",lstArrets
    
            tailleRlt = self.mtg.palier[palier].rlt.taille
    
            passPas = []
            pos = Montage.PositionDansPivot()
            for pa in lstArrets:
                ar = self.mtg.elemPos(pos.posCode(pa))
                if ar.num is None:
                    tailleArret = self.mtg.palier[pa[1]].taille
                    pa = "-"+pa[1]+"-"+pa[3:5]
                else:
                    tailleArret = ar.taille
                if tailleRlt <> tailleArret \
                   and     ((radiale == "Ar" and tailleArret == "G") \
                        or (radiale == "Al" and tailleArret == "P")):
                    if ar.estEntretoise():
                        if pa[1] <> palier:
                            passPas.append("-"+pa[1]+"-"+pa[3:5])
                    else:
                        passPas.append(pa)
    
                if tailleRlt == tailleArret and ar.pasDemontable(not self.mtg.deuxrlt()):
                    passPas.append(pa)
    
    ##        print ">>> Obstacles",passPas
           
            if len(passPas)>0:
                posObs = []
                for i in passPas:
                    posObs.append(pos.posXCode(i))
                if palier == "G":
                    plusProche = passPas[posObs.index(min(posObs))]
                else:
                    plusProche = passPas[posObs.index(max(posObs))]
    
                
                passPas = [plusProche]
    
    #        print ">>> Obstacles",passPas
            
            return passPas
      
        def traiterBaguesIsolees():
            
            obsBagueIsolee = {"G" : [],
                              "D" : []}
            
            for palier in ["G","D"]:
                for sens in [0,1]:
                    if self.obstacleBagueIsolee[palier][sens] <> []:
                        obsBagueIsolee[palier].append(self.obstacleBagueIsolee[palier][sens][0])
                if len(obsBagueIsolee[palier]) >= 2:
                    self.obstacleBagueIsolee[palier] = obsBagueIsolee[palier]
                else:
                    del self.obstacleBagueIsolee[palier]
#            print "Obstacles Bagues isolées :",self.obstacleBagueIsolee
           
        #
        # On lance l'analyse ...
        #
        for sens in [0,1]:
            # Etabli les listes des éléments libres et des éléments sérrés
            
            listeElemArbre = listeElementsArbre(sens)
#            print ">>> Eléments Arbre   :\n", listeElemArbre
            listeElemAlesage = listeElementsAlesage(listeElemArbre.lst, sens)
#            print ">>> Eléments Alésage :\n", listeElemAlesage
            
#            self.listeElemArbre[sens] = listeElementsArbre(sens)
#            self.listeElemAlesage[sens] = listeElementsAlesage(self.listeElemArbre[sens],sens)
            
            # Teste si le montage est démontable
            estDemontable(sens)
        
            
            # Etabli la liste des éléments à enlever pour le démontage
#            self.lstArretsAEnleverEns[sens] = listeElementsAEnleverEns(sens)
            
        for sens in [0,1]:
            # Teste si les roulements sont démontables
            for p in ["G","D"]:
                self.obstacleRoults[p][sens] = estDemontableRlt(sens,p,True)

            # Teste si les bagues isolées sont démontables
            for p in ["G","D"]:
                self.obstacleBagueIsolee[p][sens] = estDemontableRlt(sens,p,False)
                

            # Etabli la liste des éléments à enlever pour le démontage des roulements
            for p in ["G","D"]:
                self.lstArretsAEnleverRlt[p][sens] = listeElementsAEnleverRlt(sens,p)

        # On inserse le sens de démontage si bague tournante extérieure
        if self.cdcf.bagueTournante == "E":
#            print "Retournement sens montage ..."
            self.listeElemArbre.reverse()
            self.listeElemAlesage.reverse()
            self.lstArretsAEnleverEns.reverse()
            self.obstacleEnsble.reverse()
            
        # Traitement des bagues isolées
        traiterBaguesIsolees()
##        print "Bagues isolées :",self.obstacleBagueIsolee

#        # On prépare les item pour les animations
#        for sens in [0,1]:
#            self.preparerMontageDemontageEns(sens)
#            for p in ["G","D"]:
#                self.preparerMontageDemontageRlt(sens,p)

##        print "Obsacles roulements 1 :",self.obstacleRoults
        
        # Montabilité Général :
        #----------------------
        montables = {}

        # roulements
        for p in self.obstacleRoults:
            obs = self.obstacleRoults[p]
            montables[p] = (obs[0] == []) or (obs[1] == [])

        # bagues isolées
        for p in self.obstacleBagueIsolee:
            obs = self.obstacleBagueIsolee[p]
            montables["I"+p] = obs == []

        # cas des roulements obstacle
        for p in ["G","D"]:
            if p == "G":
                o = "D"
                s = 0
            else:
                o = "G"
                s = 1
            obs = self.obstacleRoults[p]
            ropp = self.obstacleRoults[o]
            if ropp[0] <> [] and ropp[1] <> [] and obs[s] == []:
                obs[s].append("R"+o+"---")
##                print "Correction obstacle rlt",p,"sens",s," : ",obs[s]

        # ensemble
        for s in [0,1]:
##            print "MONTABILITE"
##            print self.obstacleEnsble[s]
            montables[s] = self.obstacleEnsble[s] == []
#            montables[s] = True
#            for p in ["G","D"]:    
#                montables[s] = montables[s] and (self.obstacleEnsble[s][p] == ())
##            print montables[s]

        
        montables["E"] = montables[0] or montables[1]
        del montables[0]
        del montables[1]
#        print montables
        montable = True
        for t in montables:
            montable = montable and montables[t]
        
        
        if montable:
            self.resultatMontabilite = Const.MessageAnalyse('MontPoss')
        else:
            self.resultatMontabilite = Const.MessageAnalyse('MontImposs')


        self.listeItemLibres = [self.GetListeItemLibres(zoneMtg, 0), self.GetListeItemLibres(zoneMtg, 1)]
        self.ListeItemRoult  = {"G" : [self.GetListeItemRoult(zoneMtg, 0, "G"),self.GetListeItemRoult(zoneMtg, 1, "G")],
                                "D" : [self.GetListeItemRoult(zoneMtg, 0, "D"),self.GetListeItemRoult(zoneMtg, 1, "D")]}
##        print "Obsacles roulements 2 :",self.obstacleRoults



    ##########################################################################
    def afficher_cacherArretsAEnleverEns(self, zoneMtg, sens, afficher = True, instant = False):
        self.afficher_cacherArretsAEnlever(zoneMtg, sens, "E", afficher, instant)

    ##########################################################################
    def afficher_cacherArretsAEnleverRlt(self, zoneMtg, sens, afficher = True, instant = False):
        self.afficher_cacherArretsAEnlever(zoneMtg, sens, False, afficher, instant)
    

    ##########################################################################
    def afficher_cacherArretsAEnlever(self, zoneMtg, sens, objet, afficher, instant):
        """ Affiche ou cache les éléments à enlever pour le montage/démontage
            sens du démontage : <sens>
            objet à enlever : <objet> = "E" ou "G" ou "D"
            instantanément : <instant>
        """
#        print "  Afficher/Cacher éléments à enlever :",tag

#        sens = eval(tag[8])
        ensemble = objet == "E"
        if self.cdcf.bagueTournante == "I" and ensemble \
           or self.cdcf.bagueTournante == "E" and not ensemble:
            radiale = "Al"
        else:
            radiale = "Ar"

        # Cas des "Ensembles"
        if objet == "E":
            lst = self.lstArretsAEnleverEns[sens]

        # Cas des roulements
        else:
##            if   (tag[7] == "G" and sens == 1) \
##              or (tag[7] == "D" and sens == 0):
            lst = self.lstArretsAEnleverRlt[objet][sens]
##            else:
##                lst = []
#        print "   ... élém à enlever :",sens, lst
        
        if len(lst) == 0:
            return
        
        
        
        # Préparation des paramètres de "fondu"
        if instant:
            rng = range(0,101, 100)
        else:
            rng = range(0,101,4)    # en %
        if afficher:
            n = 'imag'
            o = 'vide'
            
        else:
            n = 'vide'
            o = 'imag'
            rng.reverse()
        
#        # Préparation des éléments non arêtés #####################
#        for i in zoneMtg.lstItemMtg:     # On parcours tous les items affichés
#            # On inclus tous les éléments d'arbres
#            if TAG_ARBRE in i.tag:
#                lstItemAnim.append(i)
#                continue
#            # On inclus les éléments de la liste (sans les éléments d'alésage)
#            else:
#                print i.tag,
#                for t in self.listeElementsNonArretes[sens]:
#                    if t in i.tag and not TAG_ALESAGE in i.tag:
#                        lstItemAnim.append(i)
#                        continue
        
        lstItemEff = []
        for itemTag in lst:
            e = self.mtg.clefElemPosCode(itemTag)[0]
#            lstItemEff.append(e.item['imag'])
            for i in zoneMtg.lstItemMtg:     # On parcours tous les items affichés
                for t in e.item['imag'].tag:
                    if t in i.tag:
                        lstItemEff.append(i)  # On rajoute tous les item qui ont le même tag
        
#        print "   ... items effacés :",lstItemEff
        
        lstItemEch = []
        for i in lstItemEff:
            if hasattr(i, "vide"):
                lstItemEch.append(i)
            else:
                lstItemEch.append(None)    
        
#        print "   ... items échangés :",lstItemEch 
        
        # Le fondu ...
        for niv in rng[1:]:
            for i in range(len(lstItemEff)):
                lstItemEff[i].fondu(lstItemEch[i], niv)
            if not instant:
                zoneMtg.Redessiner()
            time.sleep(0.020)
            
        return    
    

    ############################################################
    def GetListeItemLibres(self, zoneMtg, sens):
        """ Préparation du Montage/Démontage de l'ensemble "Alésage"
            renvoie la liste des items qui vont se déplacer ...
        """
##        print
#        print "Préparation du Montage/Démontage ""Ensemble"""
#        print ">>> sens",sens
#        tag = "AnimEnsb" + str(sens)
##        print "   ... tag =",tag
        
        def lstElemAEnlever(rad):
            lst = []

            for c in self.lstArretsAEnleverEns[sens]:
                if rad == "Ar":
                    if c[0] != "J" and c[-2:] == rad:
                        lst.append(c)
                else:
                    if c[0] == "J" or c[-2:] == rad:
                        lst.append(c)
            return lst
        
        #
        # On selectionne les éléments libres
        #
        if self.cdcf.bagueTournante == "I":
            rad = TAG_ALESAGE
            lstElemLibres = self.listeElemAlesage[sens]
            lstElemLibres.extend(lstElemAEnlever("Al"))
        else:
            rad = TAG_ARBRE
            lstElemLibres = self.listeElemArbre[sens]
            lstElemLibres.extend(lstElemAEnlever("Ar"))

#        print ">>> Liste Elem Libres sens", sens, ":",lstElemLibres

        #
        # On selectionne les items libres
        #
        lstItemAnim = []
        for i in zoneMtg.lstItemMtg:
            #
            # On inclus les éléments d'arbres ou bien d'alésage
            #
            if rad in i.tag:
                lstItemAnim.append(i)
                continue
            
            #
            # On inclus les éléments de la liste 'lstElemLibres'
            #
            else:
#                print i.tag,
                for t in lstElemLibres:
#                    print t
                    if t in i.tag:
                        lstItemAnim.append(i)
#                        print
                        continue
        
#        print "1",lstItemAnim

        #
        # On ajoute les suppléments d'arrêts à enlever qui peuvent être démontés/montés
        #
#        for itemTag in self.lstArretsAEnleverEns[sens]:
#            e = self.mtg.clefElemPosCode(itemTag[0:])[0]
#            if e.item.has_key('supp'):
#                lstItemAnim.append(e.item['supp'])
                
#        print "2",lstItemAnim
        
        return lstItemAnim
                
                
                
    ############################################################
    def GetListeItemRoult(self, zoneMtg, sens, palier):
        """Préparation du Montage/Démontage des roulements"""
#        print 
#        print "Préparation du Montage/Démontage ""Roulement"""
#        print ">>> sens",sens
#        print ">>> palier",palier
#        tag = "AnimRlt" + palier + str(sens)
        lstItemAnim = []
##        print "   ... tag =",tag

        if self.cdcf.bagueTournante == "I":
            radiale = "Ar"
            radopp = "Al"
        else:
            radiale = "Al"
            radopp = "Ar"

        # Ensemble déja démonté
        if "AnimEnsb0" in self.elemDemonte:
            te = "AnimEnsb0"
        elif "AnimEnsb1" in self.elemDemonte:
            te = "AnimEnsb1"
        else:
            te = None

        # Listes des éléments libres et fixes
        if self.cdcf.bagueTournante == "I":
            lstElemLibres = self.listeElemAlesage[sens]
            lstElemFixes = self.listeElemArbre[sens]
        else:
            lstElemLibres = self.listeElemArbre[sens]
            lstElemFixes = self.listeElemAlesage[sens]
            
        # Liste des éléments à démonter ###########################
        lst = []
        
          # Le roulement ...
        
        for tr in ["R"+palier+"-Ar",
                   "R"+palier+"-Al",
                   "R"+palier+"---"]:
            if tr in lstElemFixes:
                lst.append(tr)
    
          # Autres éléments à démonter ...
        if   (palier == "G" and sens == 0) \
          or (palier == "D" and sens == 1):
            for tr in ["AGD"+radiale,
                       "ADG"+radiale,
                       "ADG"+radopp,
                       "AGD"+radopp]:
                if tr in lstElemFixes:
                    lst.append(tr)
        
#        print "   ... elem à démonter ? =",lst
        
#        for tr in ["J"+palier+"-Ar",
#                   "J"+palier+"-Al"]:
#            if tr in lstElemFixes:
#                lst.append(tr)
        
        
          # On finalise la liste des éléments à démonter
        lst2 = []
        for c in lst:
##            print "tag",c," : ",frameMtg.gettags(c)
            pasDejaDemonte = not c in lstElemLibres
##            print "pas deja demonte =",pasDejaDemonte,frameMtg.gettags(c)
            pasAEnlever = not (c in self.lstArretsAEnleverRlt[palier][sens])
##            print "pas à enlever =",pasAEnlever
            if (pasDejaDemonte or c == "R"+palier+"---" ) and (pasAEnlever or c[0] == "R"): #and frameMtg.gettags(c) <> () \
                lst2.append(c)


        # On met les tags ... sans les épaulements
        for i in zoneMtg.lstItemMtg:
            for t in lst2:
                if t in i.tag and not TAG_ARBRE in i.tag and not TAG_ALESAGE in i.tag:
                    lstItemAnim.append(i)


#        # On enlève les épaulements
#        frameMtg.dtag(TAG_ARBRE,tag)
#        frameMtg.dtag(TAG_ALESAGE,tag)
        
##        if self.cdcf.bagueTournante <> u"Extérieure":
##            for t in self.lstArretsAEnleverRlt[sens]:
##                frameMtg.addtag_withtag(tag,t)        

##        print "   ... elem à démonter =",lst2
#        print "Roulement",palier,"sens",sens
#        print "   ... elem à démonter =",lst2
#        print "   ... item à démonter =",lstItemAnim
        return lstItemAnim
                
           
                
    ############################################################
    def animerMontageDemontage(self, zoneMtg, tag, remonter, instant = False):
        """ Animation du Montage/Démontage
        
        """
        
        def animer():
            # Durée (en seconde)
            duree = globdef.DUREE_ANIMATION_MONTAGE
    
            # Calcul du nombre de positions (à 20 img/s)
            nbPos = duree * globdef.FRAME_RATE
            
            # Paramètre de la fonction x(t) = ax²
            a = 1.0*sensdep*dist/nbPos**2
            
            oldx = 0
            for c in range(nbPos):
                tm = time.clock()
                x = int(round(a*(c-n*nbPos)**2))
                if x <> oldx:
                    for i in lstItemAnim:
                        i.pos = (i.x + x, i.pos[1])
                    oldx = x
                    zoneMtg.Redessiner()
                dt = 1.0/globdef.FRAME_RATE - time.clock() + tm
                if dt > 0:
                    time.sleep(dt)

#        if remonter: t = "Démontage"
#        else : t = "Montage"
#        print 
#        print "  Animation ",tag
        
        wx.BeginBusyCursor()
        
#        def GroupeBmp(lstItem):
#            # Regroupement des images
#            bmp = wx.EmptyBitmap(zoneMtg.maxWidth, zoneMtg.maxHeight)
#            memdc = wx.MemoryDC(bmp)
#            memdc.SetBackground(wx.Brush(wx.Colour(255,255,254))) #wx.TRANSPARENT_BRUSH)
#            memdc.Clear()
#            for i in lstItemAnim:
#                memdc.DrawBitmap(i.bmp, i.pos[0], i.pos[1], True)
#            zoneMtg.hachurer(memdc, self.listeElementsNonArretes[sens])
#            memdc.SelectObject(wx.NullBitmap)
#            img = wx.ImageFromBitmap(bmp)
#            img.SetMaskColour(255,255,254)
#            img.SetMask(True)
#            bmp = wx.BitmapFromImage(img)
#            return bmp
        
        #
        # Réglage de la distance (en pixels)
        #
        if tag[4] == "E":
            dist = DISTANCE_DEMONTAGE_ENSEMBLE
        else:
            if tag[7] == "G" and tag[8] == "0" \
               or tag[7] == "D" and tag[8] == "1":
                dist = DISTANCE_DEMONTAGE_RLT_LONG
            else:
                dist = DISTANCE_DEMONTAGE_RLT_COURT
        #
        # On établi la liste des item à animer
        #
        sens = eval(tag[8])
        if tag[4] == "E":
            lstItemAnim = self.listeItemLibres[sens]
        else:
            lstItemAnim = self.ListeItemRoult[tag[7]][sens]
            
#        print "   ... elem à démonter =",self.listeElemAlesage[sens]
#        print "   ... item à démonter =",lstItemAnim
        
        #
        # Lancement de l'animation
        #=========================
        #
        # signe du sens de déplacement ##############################
        if not remonter:
            sgn = 1
        else:
            sgn = -1

        # sens du déplacement (demontage) ##############################
        # ( 1 = vers la droite
        #   -1 = vers la gauche )
        sensdep = 1 - eval(tag[8]) * 2
  
        if remonter:
            n = 1
        else:
            n = 0
        
        # On ote les arrêt à enlever
        if tag[4] == "E":
            objet = "E"
        else:
            objet = tag[7]
        if not remonter:
            self.afficher_cacherArretsAEnlever(zoneMtg, sens, objet, remonter, instant)
        
        # Sauvegarde de la position en x
        if not remonter:
            for i in lstItemAnim:
                i.x = i.pos[0]
        
        # Mouvement
        if instant:
#            print dist*sensdep*sgn
            for i in lstItemAnim:
                i.pos = (i.pos[0] + dist*sensdep*sgn, i.pos[1])
#            zoneMtg.Redessiner()
            
        else:
            animer()
            
        # On affiche les arrêt à enlever
        if remonter:
            self.afficher_cacherArretsAEnlever(zoneMtg, sens, objet, remonter, instant)
        
        wx.EndBusyCursor()
        
    
        
    #############################################################################
    def initTraceResultats(self, zoneMtg):
        self.mobileTrace = None
        self.chaineTracee = {0 : None, 
                             1 : None}
        self.obstacleTrace = None
        
#        for t in self.chaineTracee.values():
#            t = None        
#        self.mobileTrace = None
#        for t in self.obstacleTrace.values():
#            t = None

    def reinitialiserAffichage(self, zoneMtg):
#        print "Réinitialisation affichage analyse"
        if self.mobileTrace is not None:
            self.tracerSurBrillanceMobiles(zoneMtg, self.mobileTrace, False)
        self.initTraceResultats(zoneMtg)
#        print self.chaineTracee.values() 
        zoneMtg.Redessiner(self)

    def SetTracerChaine(self, sens, state):
        self.chaineTracee[sens] = state

    #############################################################################
    def tracerResultats(self, dc, zoneMtg):
#        print "Tracé résultats analyse",self.chaineTracee.items()
        for s,t in self.chaineTracee.items():
            if t is not None:
#                print "  Tracé chaine",s
                self.tracerChaineAct(dc, zoneMtg, s)
            
        if self.mobileTrace is not None:
            self.tracerFlechesObstacleEnsemble(dc, zoneMtg, self.mobileTrace)
        
#        for obs in self.obstacleTrace.values():
        self.tracerObstacle(dc, zoneMtg, self.obstacleTrace)
       
    ##############################################################################################
    def tracerSurbrillanceArrets(self, zoneMtg, sens, action = True, montrer = True): 
        """ Met les arrets ne résistant pas en surbrillance
        """
        for p in self.lstElemResistePas[sens]:
            elem = self.mtg.clefElemPosCode(p)[0]
            
            if action:
                elem.item['imag'].couleur("rouge")
                try:
                    elem.item['imagAr'].couleur("rouge")
                except:
                    pass
                zoneMtg.SurBrillanceActive = False
            else:
                elem.item['imag'].normale()
                zoneMtg.SurBrillanceActive = True
                try:
                    elem.item['imagAr'].normale()
                except:
                    pass
        
        if montrer :
            zoneMtg.Redessiner(self)
        
    ###############################################################################
    def tracerSurBrillanceMobiles(self, zoneMtg, sens, active = True):
        """ Met en surbrillance Bleu et Noir 
            les ensembles entrant en collision (indémontable) 
        """
#        print "Surbrillance collision"
#        sens = eval(tag[8])

        def mettreEnSurbrillance():
            for i in self.lstItemAles:
                i.couleur("bleu")
            for i in self.lstItemArbre:    
                i.couleur("noir")
        
        def oterSurbrillance():
            for i in zoneMtg.lstItemMtg:
                i.normale()

#        print "SurBrillance mobiles : sens",sens
#        print ">>> Eléments serrés :",self.listeElemArbre[sens]
#        print ">>> Eléments libres :",self.listeElemAlesage[sens]

        self.lstItemArbre = []
        self.lstItemAles = []

        if self.elemDemonte <> []:
            return

        listeSerres = self.listeElemArbre[sens]
        listeLibres = self.listeElemAlesage[sens]
        
        # Cas des éléments liés à l'alésage
        #-----------------------------------
        for pcode in self.listeElemAlesage[sens]:
            elem,lstclef = self.mtg.clefElemPosCode(pcode)
            for clef in lstclef:
                self.lstItemAles.append(elem.item[clef])

        # Cas des éléments liés à l'arbre
        #---------------------------------
        for pcode in self.listeElemArbre[sens]:
            elem,lstclef = self.mtg.clefElemPosCode(pcode)
            for clef in lstclef:
                self.lstItemArbre.append(elem.item[clef])
            
        # Cas des morceaux d'arbre ou d'alésage
        #--------------------------------------
        for i in zoneMtg.lstItemMtg:
            # On inclus les éléments d'arbres
            if TAG_ARBRE in i.tag:
                self.lstItemArbre.append(i)
            elif TAG_ALESAGE in i.tag:
                self.lstItemAles.append(i)
       
        # Cas des éléments à enlever
        #----------------------------
        for pcode in self.lstArretsAEnleverEns[sens]:
            elem,lstclef = self.mtg.clefElemPosCode(pcode)
            for clef in lstclef:
                if pcode[3:] == "Ar":
                    self.lstItemArbre.append(elem.item[clef])
                elif pcode[3:] == "Al":
                    self.lstItemAles.append(elem.item[clef])
                    
        # On ote les doublons
        #---------------------
#        def OterDoublons(liste):
#            i = 0
#            while i < len(liste):
#                if liste[i] in liste[i+1:]:
#                    liste.pop(i)
#                i += 1
#        OterDoublons(self.lstItemArbre)
#        OterDoublons(self.lstItemAles)   
                 
        self.lstItemArbre = list(set(self.lstItemArbre))
        self.lstItemAles = list(set(self.lstItemAles))
        
        
        #   On cache ou affiche les éléments à démonter (instantanément !)
        #-----------------------------------------------------------------
        self.afficher_cacherArretsAEnleverEns(zoneMtg, sens, not active, instant = True)
        
        if active:
            mettreEnSurbrillance()
        else:
            oterSurbrillance()

        if active:
            self.mobileTrace = sens
        else:
            self.mobileTrace = None
    
        zoneMtg.Redessiner(self)
            
    
            
    #############################################################################    
    def tracerFlechesObstacleEnsemble(self, dc, zoneMtg, sens):
        """ Trace des fleches illustrant le sens de collision des ensembles mobiles (indémontable) 
        """
        def Fleche(long, sens, texte):
            """ Fleche avec texte dedans ...
            """
            # épaisseur (en pixel)
            e = 41
            
            # décalage de l'ombre
            o = 4
            
            # Pen de la flèche
            pen = wx.Pen(wx.Colour(159,0,0), e)
#            pen = wx.Pen("red", e)
            pen.SetCap(wx.CAP_BUTT)
          
            # Points extrémités de la Fleche
            x1,y1,x2,y2 = 0, e/2, long, e/2
    
            bmp = wx.EmptyBitmap(long+o, e+o)
            dc = DCPlus(bmp)
            dc.SetBackground(wx.TRANSPARENT_BRUSH)
            dc.Clear()
            dc.SetBrush(wx.Brush(wx.BLACK))
            dc.SetTextForeground(wx.NamedColour('LIGHT GREY'))
            dc.SetPen(pen)
            dc.DrawLineArrow(x1,y1,x2,y2, 
                             style = 1+(sens+1)/2, tanF = 1)
            
            dc.SetFont(wx.Font(14, wx.DEFAULT, wx.ITALIC, wx.BOLD, False))
            lt, ht = dc.GetTextExtent(texte)
            if sens == -1:
                x1 = x2-lt
            dc.DrawText(texte, x1, y1 - ht/2)
            dc.SelectObject(wx.NullBitmap)
            bmp.SetMask(wx.Mask(bmp))
            bmp = Images.ombrer(bmp)
            return bmp

        if self.cdcf.bagueTournante == "I": s = 1
        else: s = -1
        dy = 210
        for i in [-1, 0, 1]:
            sg = (i*i*2-1)*s*(sens * 2 - 1)
            bmp = Fleche(160, -sg, " Impossible !! ")
            y = zoneMtg.milieuY + i * dy - bmp.GetHeight()/2
            x = zoneMtg.milieuX - sg * 150 
            dc.DrawBitmap(bmp, x, y, True)


    #############################################################################                
    def tracerObstacle(self, dc, zoneMtg, obsTrace):
        """ Met en évidence un obstacle au démontage
            par une double flèche les éméments en collision
        """
        if obsTrace is None:
            return
        
#        print u"trace des obstacles :", obsTrace
        obs, rad = obsTrace[0], obsTrace[1]
        lien = []

#        print "Tracé flèche entre :",obs, rad
#        print obs[0].posX(), obs[1].posX()
        # On met la liste dans l'ordre "D" "G"
        if obs[0].posX() > obs[1].posX():
            obs.reverse()
        
        lstPosX = [[obs[0],"D"],
                   [obs[1],"G"]]

#        print lstPosX, obs[0].posX(), obs[1].posX()

        # Calcul des coordonnées
        for posX in lstPosX:
            x , y = zoneMtg.coordsBordElem(self.mtg, posX[0], posX[1], rad)
#            print x
            lien.append((x,zoneMtg.milieuY + y))
        
        #On met tout à la même hauteur ...
        
        
        def fleche(sens, pt):
            # Bout de la Fleche
            s = sens*2-1
            lf, ef = 10, 5
            x,y = pt[0],pt[1]
            return [(x,y),(x + s*lf, y+lf), (x + s*lf, y-lf)]
        
        def tracerFleche():
            dc.SetPen(wx.Pen(coul, 5))
            dc.DrawLines(lien)
            dc.SetPen(wx.Pen(coul, 1))
            dc.DrawPolygon(fleche(1, lien[len(lien)-1]), fillStyle = wx.WINDING_RULE)
            dc.DrawPolygon(fleche(0, lien[0]), fillStyle = wx.WINDING_RULE)
        
        # Tracé de la flêche
        if len(lien)>1:
#                print lien
#                lien[0][1] = (lien[0][1] + lien[1][1]) / 2
#                lien[1][1] = lien[0][1]
#                if lien[0][0] == lien[1][0]:
#                    lien[0][0] -= 1 
                
##                if cote == "D":
##                    a = lien[2]
##                    lien[2] = lien[0]
##                    lien[0] = a
                coul = "red"
                tracerFleche()
                lien[0] = (lien[0][0], 2 * zoneMtg.milieuY - lien[0][1])
                lien[1] = (lien[1][0], 2 * zoneMtg.milieuY - lien[1][1])
                tracerFleche()
              

    #############################################################################                
    def tracerChaineAct(self, dc, zoneMtg, sens):
        """ Trace une chaine d'action dans <dc> """
        lstLignes = self.chaineAct[sens].lstLignes
        def fleche(sens, pt):
            # Bout de la Fleche
            s = sens*2-1
            lf, ef = 10, 5
            return [(pt.x - s*4, pt.y),(pt.x + s*lf, pt.y+lf), (pt.x + s*lf, pt.y-lf)]
        
        # Epaisseur en pixel
        epaisseur = 4
        
        # Une Couleur différente selon le sens
        if sens == 0: 
            coul = "red"
            dc.SetBrush(wx.RED_BRUSH)
        else: 
            coul = "blue"
            dc.SetBrush(wx.BLUE_BRUSH)

        
        dc.BeginDrawing()
        
        # Tracé des chaînes
        for ligne in lstLignes:
            ligneBas = []
#            impair = True
            # Chaine du bas ...
            for p in ligne:
                ligneBas.append(wx.Point(p[0],zoneMtg.milieuY - (p[1] - zoneMtg.milieuY)))
#                if impair:
#                    ligneBas .append(c)
#                else:
#                    ligneBas.append()
#                impair = not impair
                
            lignes = [ligne,ligneBas]
            for l in lignes:
                dc.SetPen(wx.Pen(coul, 5))
                dc.DrawSpline(l)
                dc.SetPen(wx.Pen(coul, 1))
                dc.DrawPolygon(fleche(sens, l[len(l)-1]), fillStyle = wx.WINDING_RULE)
        dc.EndDrawing()  



###################################################################################################################
###################################################################################################################
class ListeActive(wx.Panel):
    def __init__(self, parent, listeNom, bouton, actions = None, wrap = 20):
        self.coul = wx.NamedColour("PINK")
        wx.Panel.__init__(self, parent, -1 )
        self.SetBackgroundColour(self.coul)
        
#        box = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.GridBagSizer(0,0)
        
        self.parent = parent
        self.bouton = bouton
#        self.nbObs = len(listeNom['lst'])
        
        StyleText["Gras"].applique(self)
        txt = StaticTextWrapped(self, -1, listeNom['mess'])
#        txt.Wrap(wrap)
#        box.Add(txt, 0, wx.ALIGN_LEFT|wx.ALL, 10)
        sizer.Add(txt, (0,0), (1,2), flag = wx.ALIGN_LEFT|wx.TOP|wx.BOTTOM, border = 4)
        
        self.lBox = []
        StyleText["Normal"].applique(self)
        l = 1
        for choix in listeNom['lst']:
            box = wx.CheckBox(self, l-1, "")#size = (-1,-1), # 18*len(listeNom['lst'])), 
#                              choices = listChoix, 
#                              style = wx.LB_MULTIPLE|wx.LB_NEEDED_SB)
            self.lBox.append(box)
            txt = wx.StaticText(self, -1, choix)
#            box.Add(self.lb, 0, wx.ALIGN_LEFT|wx.EAST|wx.WEST|wx.SOUTH, 10)
            sizer.Add(box, (l,0), flag = wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, border = 2)
            sizer.Add(txt, (l,1), flag = wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, border = 2)
#        self.lb.Fit()
#        txt.SetLabel(wordwrap(txt.GetLabel(), lb.GetSize()[0],wx.ClientDC(self)))
#        lb.Check(wx.NOT_FOUND)
            self.Bind(wx.EVT_CHECKBOX, self.EvtListBox, box)
            l += 1
            
        parent.Bind(wx.EVT_SIZE, self.OnSize)
#        self.action = action
        
        self.SetSizerAndFit(sizer)
#        self.FitInside()

        def SymboleDevelop(taille):
            bmp = wx.EmptyBitmap(taille, 10)
            dc = wx.MemoryDC(bmp)
            dc.SetBackground(wx.Brush(wx.Colour(255,255,254))) #wx.TRANSPARENT_BRUSH)
            dc.Clear()
            dc.SetPen(wx.Pen("PINK", 0))
            dc.SetBrush(wx.Brush(self.coul))
            poly = ((taille/2, 0),(0,10),(taille,10))
            dc.DrawPolygon(poly, fillStyle = wx.WINDING_RULE)
            img = wx.ImageFromBitmap(bmp)
            img.SetMaskColour(255,255,254)
            img.SetMask(True)
            bmp = wx.BitmapFromImage(img)
            return bmp
        
        self.symboleDevelop = wx.StaticBitmap(parent, -1, SymboleDevelop(bouton.GetSize()[0]))
        self.Montrer(False)
        
        
    ###################################################
    def OnSize(self, event):
#        print "Resize Liste Active",# self.GetSize(), 
        self.SetSize(wx.Size(self.parent.GetClientSize().GetWidth(),-1))
#        print self.GetSize()
        event.Skip()
#        self.FitInside()
    
    ###################################################
    def EvtListBox(self, event = None, num = None):
        if num is not None: n = num
        else: #n = event.GetSelection()
            n = event.GetId()
#        print n    
        if hasattr(self.bouton, "typeAction"):
            action = self.lBox[n].IsChecked()
            if self.bouton.tag[4] <> "R":
                surBrill = False
            else:
                surBrill = True     
#            print "Obstacle Ensemble :",n, action
            self.parent.parent.montrerCollision(self.bouton.lstObs, n, 
                                                palier = self.bouton.tag[7],
                                                action = action, surBrill = surBrill)
        
#        print n
            
    ###################################################
    def Montrer(self, etat):
#        print "montrer", self.GetId(),"==>", etat,
        if etat: 
            self.Show()
            self.symboleDevelop.Show()
        else: 
            self.Hide()
            self.symboleDevelop.Hide()
            for lb in self.lBox:
                if lb.IsChecked():
                    lb.SetValue(False)
                    self.EvtListBox(lb.GetId())
#        self.parent.Layout()
        self.parent.Refresh()
#        self.Update()
#        self.parent.Fit()

class StaticTextWrapped(wx.StaticText):
    """ A StaticText-like widget which implements word wrapping. """
    
    def __init__(self, *args, **kwargs):
        wx.StaticText.__init__(self, *args, **kwargs)

        # store the initial label
        self.__label = super(StaticTextWrapped, self).GetLabel()

        self.marge = 8
         
        # listen for sizing events
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.GetParent().Bind(wx.EVT_SIZE, self.OnParentSize)

    def SetWrapFact(self, WrapFact):
        self.WrapFact = WrapFact

    def SetLabel(self, newLabel):
        """Store the new label and recalculate the wrapped version."""
        self.__label = newLabel
        self.__wrap()

    def GetLabel(self):
        """Returns the label (unwrapped)."""
        return self.__label
    
    def __wrap(self):
        """Wraps the words in label."""
        words = self.__label.split()
        lines = []

        # get the maximum width (that of our parent)
        max_width = self.GetParent().GetVirtualSizeTuple()[0]-self.marge
        # On applique un facteur pour le cas ou il y a plusieurs colonnes de texte
        if hasattr(self, "WrapFact"):
            max_width = max_width/self.WrapFact
        
        index = 0
        current = []

        for word in words:
            current.append(word)

            if self.GetTextExtent(" ".join(current))[0] > max_width:
                del current[-1]
                lines.append(" ".join(current))

                current = [word]

        # pick up the last line of text
        lines.append(" ".join(current))

        # set the actual label property to the wrapped version
        super(StaticTextWrapped, self).SetLabel("\n".join(lines))
        
        # refresh the widget
#        self.Update()
        self.Refresh()
        
    def OnSize(self, event):
        # dispatch to the wrap method which will 
        # determine if any changes are needed
        self.__wrap()

    def OnParentSize(self, event):
        txt = self.__label[:6]+"..."+self.__label[-6:]
#        print txt.encode('cp437','replace'),
        self.__wrap()
#        w,h = self.GetParent().GetClientSize()
#        w += -8
#        self.SetSize((w,h))#self.GetSize()[1]))
#        print self.GetSize()
        event.Skip()

#class StaticTextWrapped(wx.StaticText):
#    def __init__(self, *arg ,  **kwarg):
#        wx.StaticText.__init__(self, *arg , **kwarg)
##        self.parent = self.GetParent()
#        self.orgtxt = self.GetLabel()
#        self.orgSiz = self.GetSize()[0]
#        self.GetParent().Bind(wx.EVT_SIZE, self.OnSize)
#    
#    def OnSize(self, event = None):
##        print "Resize StaticTextWraped",self.GetId(), "\t"
#        sz = self.GetParent().GetClientSize()[0]-8
##        sz = event.GetEventObject().GetSize()[0]
#        self.SetLabel(self.orgtxt)
##        self.SetLabel(self.GetLabel().replace('\n',' '))
##        print "taille textwrapped", sz
#        if sz < self.GetSize()[0]:
#            self.Wrap(sz)
#            self.Update()
##            print self.GetLabel().encode('cp437','replace'), self.GetSize()
#        self.GetParent().Refresh()
#        self.GetParent().Update()
#        self.GetParent().Update()
#        self.GetParent().Refresh()
#        event.Skip()
            

class SchemaStructure():
    def __init__(self):
        self.liaisons = {"G" : None,
                         "D" : None}
        
        
    def determiner(self, mtg, ddlSupprimes):
        # Degrés de liberte supprimés par chacuns des paliers
        # 0 : aucuns
        # 1 : x+
        # 2 : x-
        # 4 : y
        # 8 : n (rotation /z)
        
#        print "Determination de la structure", ddlSupprimes
        
        #
        # Associe des laisons normalisées à chaque palier
        #
        for cote, ddlSuppr in ddlSupprimes.items():
            if ddlSuppr & 8 == 8:
                if ddlSuppr & 1 == 1 or ddlSuppr & 2 == 2:
                    self.liaisons[cote] = "Pivot"
                else:
                    self.liaisons[cote] = "PivotGliss"
            elif ddlSuppr & 4 == 4:
                if ddlSuppr & 1 == 1 and ddlSuppr & 2 == 2:
                    self.liaisons[cote] = "Rotule_"
                elif ddlSuppr & 1 == 1:
                    self.liaisons[cote] = "RotuleG"
                elif ddlSuppr & 2 == 2:
                    self.liaisons[cote] = "RotuleD"
                else:
                    self.liaisons[cote] = "LinAnn"
            else:
                if ddlSuppr & 1 == 1 and ddlSuppr & 2 == 2:
                    self.liaisons[cote] = "AppPlan_"
                elif ddlSuppr & 1 == 1:
                    self.liaisons[cote] = "AppPlanG"
                elif ddlSuppr & 2 == 2:
                    self.liaisons[cote] = "AppPlanD"
                else:
                    self.liaisons[cote] = "Aucune"
        
#        print "  ",self.liaisons
        
        
    def panel(self, parent):
        pnl = wx.Panel(parent, -1)
        
        return pnl

    def bitmap(self, charges = None):
#        print "Charges :", charges
        Ycentres = 30
        Xcentres = {"G" : 50,
                    "D" : 150}
        couleurBati = wx.NamedColour("GOLD")
        couleurArbr = wx.BLUE
        couleurOk = wx.NamedColour("FOREST GREEN")
        couleurNo = wx.RED
        epaiss = 3
        epaisCharg = 17
        penBati = wx.Pen(couleurBati, epaiss)
        penArbr = wx.Pen(couleurArbr, epaiss)
        penOk = wx.Pen(couleurOk, epaisCharg)
        penNo = wx.Pen(couleurNo, epaisCharg)
        penOk.SetCap(wx.CAP_BUTT)
        penNo.SetCap(wx.CAP_BUTT)
#        penOk = wx.Pen(couleurOk, 1)
#        penNo = wx.Pen(couleurNo, 1)
        
        DimLiaison = 10
        
        def dessinerBati(dc, cote, decaler = 0):
            dc.SetPen(penBati)
            if cote == "G":
                s = -1
            else:
                s = 1
            dc.DrawLine(Xcentres[cote]+s*decaler*DimLiaison*2, Ycentres+DimLiaison*2-decaler*DimLiaison*2, 
                        Xcentres[cote]+s*decaler*DimLiaison*2, Ycentres+DimLiaison*4)
            dc.DrawLine(Xcentres[cote]-DimLiaison*2+s*decaler*DimLiaison*2, Ycentres+DimLiaison*4, 
                        Xcentres[cote]+DimLiaison*2+s*decaler*DimLiaison*2, Ycentres+DimLiaison*4)
            if decaler <> 0:
                dc.DrawLine(Xcentres[cote]+s*decaler*DimLiaison*2, Ycentres, 
                            Xcentres[cote]+s*decaler*DimLiaison/2, Ycentres)
            for i in range(5):
                dc.DrawLine(Xcentres[cote]-DimLiaison*2+i*DimLiaison+s*decaler*DimLiaison*2, Ycentres+DimLiaison*4, 
                            Xcentres[cote]-DimLiaison*2+(i+1)*DimLiaison+s*decaler*DimLiaison*2, Ycentres+DimLiaison*5)
                 
        def dessinerArbr(dc, liaisons = None):
            dc.SetPen(penArbr)
            decal = [0,0]
            if liaisons is not None:
                for s in [0,1]:
                    if liaisons[s] == "AppPlan" or liaisons[s][:-1] == "AppPlan":
                        decal[s] = (1-2*s) * DimLiaison/2
                    elif liaisons[s] == "Pivot" or liaisons[s] == "PivotGliss":
                        decal[s] = (1-2*s) * DimLiaison*5
            dc.DrawLine(Xcentres["G"]+DimLiaison+decal[1], Ycentres, 
                        Xcentres["D"]-DimLiaison+decal[0], Ycentres)
            
        def dessinerLiaison(dc, liaison, cote):
            if liaison[:-1] == "AppPlan":
                if cote == "G":
                    penB, penA = penBati, penArbr
                else:
                    penA, penB = penBati, penArbr
                dc.SetPen(penB)
                dc.DrawLine(Xcentres[cote]-DimLiaison/2, Ycentres-DimLiaison*2, 
                            Xcentres[cote]-DimLiaison/2, Ycentres+DimLiaison*2)
                dc.SetPen(penA)
                dc.DrawLine(Xcentres[cote]+DimLiaison/2, Ycentres-DimLiaison*2, 
                            Xcentres[cote]+DimLiaison/2, Ycentres+DimLiaison*2)
            elif liaison[:-1] == "Rotule" or liaison == "LinAnn":
                dc.SetPen(penBati)
                dc.SetBrush(wx.TRANSPARENT_BRUSH)
                if liaison[-1:] == "G":
                    dc.DrawArc(Xcentres[cote], Ycentres+DimLiaison*2, 
                               Xcentres[cote], Ycentres-DimLiaison*2,
                               Xcentres[cote], Ycentres)
                elif liaison[-1:] == "D":
                    dc.DrawArc(Xcentres[cote], Ycentres-DimLiaison*2, 
                               Xcentres[cote], Ycentres+DimLiaison*2,
                               Xcentres[cote], Ycentres)
                elif liaison == "LinAnn":
                    dc.DrawRectangle(Xcentres[cote]-DimLiaison*2, Ycentres-DimLiaison/4, 
                                     DimLiaison*4, DimLiaison*2+DimLiaison/4)
                else:
                    if cote == "G":
                        s = -1
                    else:
                        s = 1
                    dc.DrawArc(Xcentres[cote]-s*DimLiaison, Ycentres+s*(DimLiaison*7/4), 
                               Xcentres[cote]-s*DimLiaison, Ycentres-s*(DimLiaison*7/4),
                               Xcentres[cote], Ycentres)
                dc.SetBrush(dc.GetBackground())
                dc.SetPen(penArbr)
                dc.DrawCircle(Xcentres[cote], Ycentres, DimLiaison)
            elif liaison == "Pivot" or liaison == "PivotGliss":
                dc.SetPen(penBati)
                dc.SetBrush(wx.TRANSPARENT_BRUSH)
                dc.DrawRectangle(Xcentres[cote]-DimLiaison*2, Ycentres-DimLiaison*3/2, 
                                 DimLiaison*4, DimLiaison*3)
                dc.DrawLine(Xcentres[cote], Ycentres+DimLiaison*3/2, 
                            Xcentres[cote], Ycentres+2*DimLiaison)
                dc.SetBrush(dc.GetBackground())
                dc.SetPen(penArbr)
                if liaison == "Pivot":
                    dc.DrawLine(Xcentres[cote]-DimLiaison*3, Ycentres-DimLiaison, 
                                Xcentres[cote]-DimLiaison*3, Ycentres+DimLiaison)
                    dc.DrawLine(Xcentres[cote]+DimLiaison*3, Ycentres-DimLiaison, 
                                Xcentres[cote]+DimLiaison*3, Ycentres+DimLiaison)
#                dc.SetBrush(wx.TRANSPARENT_BRUSH)
             
        def dessinerFlecheCharge(dc, cote, typeCharge, resiste):
#            bm = wx.EmptyBitmap(bmp.GetWidth(), bmp.GetHeight())
#            dc = DCPlus(bm)
#            dc.Clear()
            tanA_ = 1
            dc.SetLogicalFunction(wx.AND)
            if resiste:
                dc.SetPen(penOk)
            else:
                dc.SetPen(penNo)
            if typeCharge == 1:
                dc.DrawLineArrow(Xcentres[cote]-DimLiaison*3, Ycentres, 
                                 Xcentres[cote]+DimLiaison*3, Ycentres, 
                                 style = 2, tanF = tanA_)
            elif typeCharge == 2:
                dc.DrawLineArrow(Xcentres[cote]-DimLiaison*3, Ycentres, 
                                 Xcentres[cote]+DimLiaison*3, Ycentres, 
                                 style = 1, tanF = tanA_)
            elif typeCharge == 3:
                dc.DrawLineArrow(Xcentres[cote]-DimLiaison*3, Ycentres, 
                                 Xcentres[cote]+DimLiaison*3, Ycentres, 
                                 style = 3, tanF = tanA_)
            elif typeCharge == 4:
                dc.DrawLineArrow(Xcentres[cote], Ycentres-DimLiaison*3, 
                                 Xcentres[cote], Ycentres+DimLiaison*3, 
                                 style = 1, tanF = tanA_)
            elif typeCharge == 5:
                dc.DrawLineArrow(Xcentres[cote]-DimLiaison*2, Ycentres+DimLiaison*2, 
                                 Xcentres[cote]+DimLiaison*2, Ycentres-DimLiaison*2, 
                                 style = 2, tanF = tanA_)
            elif typeCharge == 6:
                dc.DrawLineArrow(Xcentres[cote]-DimLiaison*2, Ycentres+DimLiaison*2, 
                                 Xcentres[cote]+DimLiaison*2, Ycentres-DimLiaison*2, 
                                 style = 1, tanF = tanA_)
            elif typeCharge == 7:
                dc.DrawLineArrow(Xcentres[cote]-DimLiaison*2, Ycentres+DimLiaison*2, 
                                 Xcentres[cote]+DimLiaison*2, Ycentres-DimLiaison*2, 
                                 style = 3, tanF = tanA_)
            dc.SetLogicalFunction(wx.COPY)

        
        # Regroupement des images
        bmp = wx.EmptyBitmap(200, 100)
        memdc = DCPlus(bmp)
        memdc.SetBackground(wx.Brush(wx.Colour(255,255,254))) #wx.TRANSPARENT_BRUSH)
        memdc.Clear()
#        memdc.SetBrush(wx.TRANSPARENT_BRUSH)
        memdc.SetBrush(memdc.GetBackground())
        for cote, l in self.liaisons.items():
            if l <> "Aucune":
                if l == "AppPlan" or l[:-1] == "AppPlan":
                    dec = 1
                else:
                    dec = 0
                dessinerBati(memdc, cote, dec)
                dessinerLiaison(memdc, l, cote)
        dessinerArbr(memdc, self.liaisons.values())
        for cote, l in self.liaisons.items():
            if l <> "Aucune":
                if charges is not None:
                    dessinerFlecheCharge(memdc, cote, charges[cote][0],charges[cote][1])
        memdc.SelectObject(wx.NullBitmap)
        img = wx.ImageFromBitmap(bmp)
        img.SetMaskColour(255,255,254)
        img.SetMask(True)
        bmp = wx.BitmapFromImage(img)
        return bmp



        