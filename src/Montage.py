#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##This file is part of PyVot
#############################################################################
#############################################################################
##                                                                         ##
##                                  Montage                                  ##
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

import wx,os
import Images
import FenPrincipale
from Elements import *
import ConfigParser
import xml.etree.ElementTree as ET

# pour tester optimisation
import time


USE_CUSTOMTREECTRL = False
myEVT_DATA_CHANGED = wx.NewEventType()
EVT_DATA_CHANGED = wx.PyEventBinder(myEVT_DATA_CHANGED, 1)

###############################################################################
# Evenement indiquant que des données ont été modifiées dans le Montage
###############################################################################
class MtgModifiedEvent(wx.PyCommandEvent):
    def __init__(self, evtType):
        wx.PyCommandEvent.__init__(self,evtType)

myEVT_MTG_MODIFIED = wx.NewEventType()
EVT_MTG_MODIFIED = wx.PyEventBinder(myEVT_MTG_MODIFIED,1)
#----------------------------------------------------------------------


#class MyEvent(wx.PyCommandEvent):
#    def __init__(self, evtType, id):
#        wx.PyCommandEvent.__init__(self, evtType, id)
#        self.myVal = None

    #def __del__(self):
    #    print '__del__'
    #    wx.PyCommandEvent.__del__(self)

#    def SetMyVal(self, val):
#        self.myVal = val
#
#    def GetMyVal(self):
#        return self.myVal


#from wx.lib.mixins.treemixin import ExpansionState
#if USE_CUSTOMTREECTRL:
#    import wx.lib.customtreectrl as CT
#    TreeBaseClass = CT.CustomTreeCtrl
#else:
#    TreeBaseClass = wx.TreeCtrl
#    
#
#class ArbreMontage(ExpansionState, TreeBaseClass):
#    
#    def __init__(self, parent, mtgComplet):
#        TreeBaseClass.__init__(self, parent, style=wx.TR_DEFAULT_STYLE|
#                               wx.BORDER_NONE|wx.TR_HAS_VARIABLE_ROW_HEIGHT)
##        self.BuildTreeImageList()
#        self.mtgComplet = mtgComplet
#        
##        self.Bind(EVT_DATA_CHANGED, self.RecreateTree)
#        
#        if USE_CUSTOMTREECTRL:
#            self.SetSpacing(10)
#            self.SetWindowStyle(self.GetWindowStyle() & ~wx.TR_LINES_AT_ROOT)
#
##    def AppendItem(self, parent, text, image=-1, wnd=None):
##        if USE_CUSTOMTREECTRL:
##            item = TreeBaseClass.AppendItem(self, parent, text, image=image, wnd=wnd)
##        else:
##            item = TreeBaseClass.AppendItem(self, parent, text, image=image)
##        return item
#            
#    def BuildTreeImageList(self):
#        imgList = wx.ImageList(16, 16)
#        for png in _Pngs:
#            imgList.Add(Images.Img_Icones(png))
#        self.AssignImageList(imgList)
#        
#
#    def GetItemIdentity(self, item):
#        return self.GetPyData(item)
#
#    #---------------------------------------------    
#    def RecreateTree(self, evt=None):
#        # Catch the search type (name or content)
##        searchMenu = self.filter.GetMenu().GetMenuItems()
##        fullSearch = searchMenu[1].IsChecked()
##        DonneesMtg = {0 : None,
##                      1 : None,
##              
##                      10 : self.mtg.palier['G'].rlt,
##                      11 : self.mtg.palier['G'].arr['Al']['D'],
##                      12 : self.mtg.palier['G'].arr['Al']['G'],
##                      13 : self.mtg.palier['G'].arr['Ar']['D'],
##                      14 : self.mtg.palier['G'].arr['Ar']['G'],
##                      
##                      20 : self.mtg.palier['D'].rlt,
##                      21 : self.mtg.palier['D'].arr['Al']['D'],
##                      22 : self.mtg.palier['D'].arr['Al']['G'],
##                      23 : self.mtg.palier['D'].arr['Ar']['D'],
##                      24 : self.mtg.palier['D'].arr['Ar']['G'],
##                      
##                      30 : None,
##                      31 : None,
##                      
##                      40: None,
##                      
##                      50: self.cdcf.effortAxial[0],
##                      51: self.cdcf.effortAxial[1],
##                      52: self.cdcf.effortRadial["G"],
##                      53: self.cdcf.effortRadial["G"],
##                      55: self.cdcf.bagueTournante,
#                      
##                      }
##        expansionState = self.GetExpansionState()
#        print "Recréation arbre montage :\n", self.mtgComplet.mtg
#        print self.mtgComplet.CdCF
#        
#        xml = self.mtgComplet.tree
#        root = self.AddRoot(xml.tag)
#        def add(parent, elem):
#            for e in elem:
#                item = self.AppendItem(parent, e.tag, data=None)
#                try:
#                    text = e.text.strip()
#                except:
#                    text = None
#                if text:
#                    val = self.AppendItem(item, text)
#                    self.SetPyData(val, e)
#                add(item, e)
#        add(root, xml)
#        
#        
#        
##        current = None
##        item = self.GetSelection()
##        if item:
##            prnt = self.GetItemParent(item)
##            if prnt:
##                current = (self.GetItemText(item),
##                           self.GetItemText(prnt))
##                    
##        self.Freeze()
##        self.DeleteAllItems()
##        self.root = self.AddRoot("Montage de roulements")
##        self.SetItemImage(self.root, 0)
##        self.SetItemPyData(self.root, self.mtg)
##
##        treeFont = self.GetFont()
##        catFont = self.GetFont()
##
##        # The old native treectrl on MSW has a bug where it doesn't
##        # draw all of the text for an item if the font is larger than
##        # the default.  It seems to be clipping the item's label as if
##        # it was the size of the same label in the default font.
##        if 'wxMSW' not in wx.PlatformInfo or wx.GetApp().GetComCtl32Version() >= 600:
##            treeFont.SetPointSize(treeFont.GetPointSize()+2)
##            treeFont.SetWeight(wx.BOLD)
##            catFont.SetWeight(wx.BOLD)
##            
##        self.SetItemFont(self.root, treeFont)
##        
##        firstChild = None
##        selectItem = None
###        filter = self.filter.GetValue()
##        
##        def createItem(parent, item, num):
##            child = self.AppendItem(parent, item)
###            self.SetItemFont(child, catFont)
##            d = DonneesMtg[num]
##            self.SetPyData(child, d)
##            try:
##                n = ' : ' + d.AfficheDansArbre()
##                print " mise a jour arbre : ",d 
##            except:
##                n = ''
##            self.SetItemText(child,self.GetItemText(child) + n)
##              
##            
##        def createBranche(parent, lst):
##            if type(lst[1]) == list:
##                child = self.AppendItem(parent, lst[0])
##                self.SetItemFont(child, catFont)
##                self.SetPyData(child, None)
##                for br in lst[1]:
##                    createBranche(child,br)
##            else:
##                createItem(parent,lst[0],lst[1])
##                    
##        
##        for items in _treeList:
##            createBranche(self.root,items)
##        
##        
###        
##        self.Thaw()
##        self.searchItems = {}
##        self.Expand(self.root)
#        self.ExpandAll()


#############################################################################                
#############################################################################
#               #
#     Palier    #
#               #
#############################################################################
#############################################################################
class Palier:
    "Classe définissant un palier = 1 rlt + 4 arrêts + joints"
    
    
    def __init__(self, taille = "P"):

        # Roulement
        self.rlt = Element()

        # Arrets
        self.arr = {"Ar" : {"G" : Element(),
                            "D" : Element()},
                    "Al" : {"G" : Element(),
                            "D" : Element()}}
        
        # Joints
        self.jnt = {"Al" : Element(),
                    "Ar" : Element()}

        # Taille du palier
        self.taille = taille
        
        self._tree = FenPrincipale.StructureArbre(
        # Structure de l'arbre
        #---------------------
        _treeStruct = {'Roulement'  : [1, {'ArretAl'    : [2,{'G' : [20,],
                                                              'D' : [21,]}],
                                           'ArretAr'    : [3,{'G' : [30,],
                                                              'D' : [31,]}]}],
                       'Etancheite' : [4, {'Statique'  : [40,],
                                           'Dynamique' : [41,]}]},
        # Images de l'arbre
        #-------------------
        _treeImageList = {1  : None,
                          2  : None,
                          20 : None,
                          21 : None,
                          3  : None,
                          30 : None,
                          31 : None,
                          4  : None,
                          40 : None,
                          41 : None
                          },
    
        # Labels de l'arbre
        #-------------------
        _treeLabelList = {1  : u"Roulement",
                          2  : u"Arrêts sur Alésage",
                          20 : u"gauche",
                          21 : u"droite",
                          3  : u"Arrêts sur Arbre",
                          30 : u"gauche",
                          31 : u"droite",
                          4  : u"Dispositif d'étanchéité",
                          40 : u"statique",
                          41 : u"dynamique"
                          },                           
        # Données de l'arbre
        #--------------------
        _treeData = {1  : self.rlt,
                     2  : None,
                     20 : self.arr["Al"]["G"],
                     21 : self.arr["Al"]["D"],
                     3  : None,
                     30 : self.arr["Ar"]["G"],
                     31 : self.arr["Ar"]["D"],
                     4  : None,
                     40 : self.jnt["Al"],
                     41 : self.jnt["Ar"]
                     }
        )

    def MaJ(self):
        self.rlt = self._tree._treeData[1] 
        self.arr["Al"]["G"] = self._tree._treeData[20] 
        self.arr["Al"]["D"] = self._tree._treeData[21] 
        self.arr["Ar"]["G"] = self._tree._treeData[30] 
        self.arr["Ar"]["D"] = self._tree._treeData[31] 
        self.jnt["Al"] = self._tree._treeData[40] 
        self.jnt["Ar"] = self._tree._treeData[41] 
        
        self.taille = self.rlt.taille
#        try:
#            self.orientation = self.rlt.orientation
#        except:
#            pass

    def __repr__(self):
        ligne='<Palier:>\n'
        ligne=ligne+str(self.arr["Al"]["G"].__repr__())+"   "+str(self.arr["Al"]["D"].__repr__())+'\n'
        ligne=ligne+"  "+str(self.rlt.__repr__())+self.taille+"\n"
        ligne=ligne+str(self.arr["Ar"]["G"].__repr__())+"   "+str(self.arr["Ar"]["D"].__repr__())+'\n'
        return ligne

#    def creerBranche(self,branche):
#        """ Crée une branche ElementTree
#            --> Pour sauvegarde
#        """
#        def strnum(num):
#            if num == None:
#                return ""
#            else:
#                return str(num)
#        
#        # Roulement
#        rlt = ET.SubElement(branche,"rlt")
##        rlt.text = u'Roulement'
#        rlt.attrib["num"] = strnum(self.rlt.num)
#        rlt.attrib["taille"] = self.rlt.taille
#        
#        #Arrêts
#        arrAr = ET.SubElement(branche,"arrAr")
##        arrAr.text = u'Arrets arbre'
#        G = ET.SubElement(arrAr,"G")
##        G.text = "gauche"
#        G.attrib["num"] = strnum(self.arr['Ar']["G"].num)
#        D = ET.SubElement(arrAr,"D")
##        D.text = "droit"
#        D.attrib["num"] = strnum(self.arr['Ar']["D"].num)
#        
#        arrAl = ET.SubElement(branche,"arrAl")
##        arrAl.text = u'Arrets alésage'
#        G = ET.SubElement(arrAl,"G")
##        G.text = "gauche"
#        G.attrib["num"] = strnum(self.arr['Al']["G"].num)
#        D = ET.SubElement(arrAl,"D")
##        D.text = "droit"
#        D.attrib["num"] = strnum(self.arr['Al']["D"].num)
#        
#        # Joints
#        jnt = ET.SubElement(branche,"jnt")
##        jnt.text = u"Dispositifs d'étanchéité"
#        Al = ET.SubElement(jnt,"Al")
##        Al.text = u"statique"
#        Al.attrib["num"] = strnum(self.jnt['Al'].num)
#        Ar = ET.SubElement(jnt,"Ar")
##        Ar.text = u"dynamique"
#        Ar.attrib["num"] = strnum(self.jnt['Ar'].num)
#
#
#    def actualiserDepuisBranche(self, branche):
#        """ Actualise le Palier depuis une branche ElementTree
#            --> après ouverture fichier
#        """
#        
#        def evalnum(str):
#            if str == "":
#                return None
#            else:
#                return eval(str)
#            
#        # Roulement
#        rlt = branche.getiterator("rlt")[0]
#        self.rlt = Element(evalnum(rlt.get("num")),rlt.get("taille"))
#        
#        #Arrêts
#        arrAr = branche.getiterator("arrAr")[0]
#        G = arrAr.getiterator("G")[0]
#        D = arrAr.getiterator("D")[0]
#        self.arr['Ar']["G"] = Element(evalnum(G.get("num")))
#        self.arr['Ar']["D"] = Element(evalnum(D.get("num")))
#        
#        arrAl = branche.getiterator("arrAl")[0]
#        G = arrAl.getiterator("G")[0]
#        D = arrAl.getiterator("D")[0]
#        self.arr['Al']["G"] = Element(evalnum(G.attrib["num"]))
#        self.arr['Al']["D"] = Element(evalnum(D.attrib["num"]))
#        
#        # Joints
#        jnt = branche.getiterator("jnt")[0]
#        Al = jnt.getiterator("Al")[0]
#        Ar = jnt.getiterator("Ar")[0]
#        self.jnt['Al'] = Element(evalnum(Al.attrib["num"]))
#        self.jnt['Ar'] = Element(evalnum(Ar.attrib["num"]))
#        

        
##########################################################################
#    Montage    #
##########################################################################
class Montage:
    "Classe définissant une liaison pivot = 2 paliers"
    
    def __init__(self, parent, pascout = False):

        # Il faut une wxWindow parente pour avoir GetEventHandler
        self.parent = parent
        
        # Un montage = 2 paliers
        self.palier = {"G" : Palier(), "D" : Palier()}
        
        self._tree = FenPrincipale.StructureArbre(
        # Structure de l'arbre
        #---------------------
        _treeStruct = {'PalierG'  : [1,self.palier["G"]._tree],
                       'PalierD'  : [2,self.palier["D"]._tree]},
        # Images de l'arbre
        #-------------------
        _treeImageList = {1  : None,
                          2  : None,
                          },

        # Labels de l'arbre
        #-------------------
        _treeLabelList = {1  : u"Palier Gauche",
                          2  : u"Palier Droit",
                          },                          
        # Données de l'arbre
        #--------------------
        _treeData = {1  : None,
                     2  : None}
        )
        
        
        self.cout = 0
#        if not pascout:
#            

        # Frame ou est affiché le montage
##        self.frame = ZoneMontage(self.master , self)
#        self.frame = self.master.zoneMontage
##        self.frame.afficherBoutArbre(self)

#    def creerBranche(self,branche):
#        """ Crée une branche ElementTree
#            --> Pour sauvegarde
#        """
#        PG = ET.SubElement(branche,"PalierG")
##        PG.text = "Palier Gauche"
#        self.palier["G"].ajouteBranche(PG)
#        PD = ET.SubElement(branche,"PalierD")
##        PD.text = "Palier Droit"
#        self.palier["D"].ajouteBranche(PD)
#        
#    def actualiserDepuisBranche(self, branche):
#        """ Actualise le Montage depuis une branche ElementTree
#            --> après ouverture fichier
#        """
#        PG = branche.getiterator("PalierG")[0]
#        self.palier["G"].miseAJour(PG)
#        PD = branche.getiterator("PalierD")[0]
#        self.palier["D"].miseAJour(PD)
    
    def MaJ(self):
        for p in self.palier.values():
            p.MaJ()

    #############################################################################
    def tousLesElem(self):
        return [self.palier["G"].rlt,
                self.palier["D"].rlt,
                self.palier["G"].arr["Al"]["G"],
                self.palier["G"].arr["Al"]["D"],
                self.palier["G"].arr["Ar"]["G"],
                self.palier["G"].arr["Ar"]["D"],
                self.palier["D"].arr["Al"]["G"],
                self.palier["D"].arr["Al"]["D"],
                self.palier["D"].arr["Ar"]["G"],
                self.palier["D"].arr["Ar"]["D"],
                self.palier["G"].jnt["Al"],
                self.palier["G"].jnt["Ar"],
                self.palier["D"].jnt["Al"],
                self.palier["D"].jnt["Ar"]]


    #############################################################################
    def tousLesCodesPos(self):
        return ["RG---",
                "RD---",
                "AGGAr",
                "AGDAr",
                "ADGAr",
                "ADDAr",
                "AGGAl",
                "AGDAl",
                "ADGAl",
                "ADDAl",
                "JDDAl",
                "JGGAl",
                "JDDAr",
                "JGGAr"]




    #############################################################################        
    def __repr__(self):
        p = self.palier["G"].jnt["Al"].__repr__() + "  " + self.palier["G"].arr["Al"]["G"].__repr__()+"  "+self.palier["G"].arr["Al"]["D"].__repr__() +"   "+ \
            self.palier["D"].arr["Al"]["G"].__repr__()+"  "+self.palier["D"].arr["Al"]["D"].__repr__() +"  "+ self.palier["D"].jnt["Al"].__repr__() +"\n" + \
            "       "+self.palier["G"].rlt.__repr__()+"         "+ \
            self.palier["D"].rlt.__repr__() + "\n" + \
            self.palier["G"].jnt["Ar"].__repr__() +"  "+ self.palier["G"].arr["Ar"]["G"].__repr__()+"  "+self.palier["G"].arr["Ar"]["D"].__repr__() +"   "+ \
            self.palier["D"].arr["Ar"]["G"].__repr__()+"  "+self.palier["D"].arr["Ar"]["D"].__repr__() +"  "+ self.palier["D"].jnt["Ar"].__repr__() +"\n"
        return p 


    #############################################################################        
    def majCout(self):
        """ Mise à jour du cout indicatif du montage """
        self.devis = []
        self.cout = 0
        support = {"G" : 0, "D" : 0}
        entretoise = {"Ar" : 0, "Al" : 0}
        
        for e in self.tousLesElem():
            if e.num is None or (e.estEntretoise() and entretoise[e.pos.radiale] == 1):
                self.devis.append((e,0))
            else:    
                self.devis.append((e,e.Cout()))
                self.cout += e.Cout()
            
            if e.estEntretoise():
                entretoise[e.pos.radiale] = 1
            
            # Determine si il faudra rajouter un support de joint
            if e.estChapeau():
                support[e.pos.palier] = 1
#            if e.necessiteChapeauCentre():
#                support[e.pos.palier] = 2
#            elif e.estJoint() and chapeau[e.pos.palier] < 2:
#                support[e.pos.palier] = 1
        
        for p in ["G" , "D"]:
            if self.palier[p].jnt["Ar"].necessiteChapeauCentre() and support[p] == 0:
                c = Element(100, self.palier[p].taille).Cout()
            elif self.palier[p].jnt["Al"].num != None and support[p] == 0:
                c = Element(100, self.palier[p].taille).Cout()*2/3
            else:
                c = 0
            self.devis.append((p,c))
            self.cout += c
            
        

    #############################################################################        
    def deuxrlt(self):
        "Tester si le montage a 2 roulements"
        return self.palier["G"].rlt.estDefini() and self.palier["D"].rlt.estDefini()

       
    ############################################################################
    def typeNum(self,num):
        return listeElements[num]['type']

    def estEntretoise(self, num):
        return num == 103

    def estEpaulement(self, num):
        return num == 102

    def estChapeau(self, num, pos):
        return num == 100 and pos.radiale == "Al"
    
    def estEcrou(self, num, pos):
        return num == 100 and pos.radiale == "Ar"
    
    def estEnlevable(self, codePos):
        elem = self.clefElemPosCode(codePos)[0]
        if not elem.estEpaulement() and self.estAccessible(codePos):
            return True
    
    def estAccessible(self, codePos):
        if codePos[0] == "R":
            return False
        palier = codePos[1]
        cotelem = codePos[2]
        if palier == cotelem:
            return True
        elif (cotelem == "D" and not self.yaUnRlt("D")) \
            or (cotelem == "G" and not self.yaUnRlt("G")):
            return True
        return False
    
    
    ############################################################################
    def GetEntretoises(self, sousMtg = None):
        lst = []
        tm = {"Ar" : "G", "Al" : "P"}
        if sousMtg is not None:
            for c in sousMtg:
                elem = self.elemPos(self.posCode(c))
                elemOpp = self.elemPos(self.posCode(c).opposee())
                if elem.estEntretoise() or elemOpp.estEntretoise():
                    rad = c[-2:]
                    if self.palier["D"].taille == tm[rad] or self.palier["G"].taille == tm[rad]:
                        t = tm[rad]
                    else:
                        if tm[rad] == "G": t = "P"
                        else : t = "G"
                    lst.append(rad+t)
        else:
            for rad in ["Ar","Al"]:
                if self.palier["D"].taille == tm[rad] or self.palier["G"].taille == tm[rad]:
                    t = tm[rad]
                else:
                    if tm[rad] == "G": t = "P"
                    else : t = "G"
                if self.palier["G"].arr[rad]["D"].estEntretoise() \
                  or self.palier["D"].arr[rad]["G"].estEntretoise():
                    lst.append(rad+t)
        return lst
    
    ############################################################################
    def GetChapeaux(self, sousMtg = None):
        lst = []
        for cot in ["G","D"]:
            if self.palier[cot].arr["Al"][cot].estChapeau()\
                or self.palier[cot].jnt["Al"].num is not None\
                or self.palier[cot].jnt["Ar"].num is not None:
                t = self.palier[cot].taille
                lst.append(cot+t)
        return lst
        
    ############################################################################
    def GetEcrous(self, sousMtg = None):
        lst = []
        for cot in ["G","D"]:
            if self.palier[cot].arr["Ar"][cot].estEcrou():
                t = self.palier[cot].taille
                lst.append(cot+t)
        return lst    
        
     
    
    
    ############################################################################
    def elemPos(self, pos):
        """Renvoie l'élément à l'emplacement <pos>"""
        
        if pos is None:
            return Element()

        e = self.palier[pos.palier]
        if pos.typelem == "R":
            return e.rlt
        elif pos.typelem == "A":
            return e.arr[pos.radiale][pos.cotelem]
        elif pos.typelem == "J":
            return e.jnt[pos.radiale]
            
        return Element()


    ############################################################################
    def clefElemPosCode(self,pcode):
        """ Renvoi l'élément à l'emplacement codé <pcode> """
        
        elem = self.elemPos(PositionDansPivot().posCode(pcode))
        if elem.num is not None:
            if pcode[0] == "R":
                if pcode[3:5] == "Ar":
                    lstclef = ['imagAr']
                elif pcode[3:5] == "Al":
                    lstclef = ['imag']
                else:
                    lstclef = elem.item.keys()
            else:
                lstclef = elem.item.keys()
        else:
            lstclef = []
                    
        return (elem,lstclef)


    ############################################################################
    def existe(self,pcode):
        elem = self.elemPos(PositionDansPivot().posCode(pcode))
        if elem.num <> None:
            return True
        else:
            return False
        

    #############################################################################
    def posCode(self,code):
        "Renvoie la position à partir du code d'une position"
##        print code
        pos = PositionDansPivot(typelem = code[0],
                                palier = code[1])
        if code[0] == "A":
            pos.cotelem = code[2]
            pos.radiale = code[3:]
        elif code[0] == "J":
            pos.cotelem = code[1]
            pos.radiale = code[3:]
            
        return pos

    ###########################################################################
    def yaUneEntretoise(self, rad):
        if self.palier["G"].arr[rad]["D"].estEntretoise() or self.palier["D"].arr[rad]["G"].estEntretoise():
            return True
        else:
            return False
        
    ###########################################################################
    def yaUnJoint(self, cote = None):
        lst = {}
        ya = False
        
        if cote is not None:
            lstCote = [cote]
        else:
            lstCote = ["G","D"]

        for c in lstCote:
            lst[c] = []
            for rad in ["Ar","Al"]:
                if self.palier[c].jnt[rad].num is not None:
                    lst[c].append(rad)
                    ya = True

        if ya:
            return lst
        else:
            return False
                
    ###########################################################################
    def yaUnRlt(self, cote = None):
        if cote is not None:
            lstCote = [cote]
        else:
            lstCote = ["G","D"]

        ya = True
        for p in lstCote:
            ya = ya and self.palier[p].rlt.num is not None

        return ya
            

    #############################################################################
    def placeLibre(self,pos):
        "Renvoi <True> si la place est libre"
        el = self.elemPos(pos)
        p =     (el.num is None) \
            or  (el is None) \
            or  (el.estEntretoise() and el.taille <> self.palier[pos.palier].taille)
        return p



    #############################################################################
    def placeCompatible(self, pos, num):
        "Renvoie <True> si la place <pos> est compatible avec l'élément <elem>"

##        print "Test élément :", elem.num,pos
        
        # pas de position valide
        if pos is None:
#            print " ** pas de position"
            return False


        # mauvais type d'élément
        if self.typeNum(num) <> pos.typelem:
#            print " ** mauvais type :",self.typeNum(num),"<>",pos.typelem
            return False


        # mauvaise position
        if self.typeNum(num) == "A":
            if listeElements[num]['pos'] == "E":
                if pos.interieur():
#                    print " ** mauvaise position : E"
                    return False
            elif listeElements[num]['pos'] == "I":
                if not pos.interieur():
#                    print " ** mauvaise position : I"
                    return False

            if self.palier[pos.palier].rlt.num is None:
#                print " ** pas de roulement"
                return False

        elif self.typeNum(num) == "J":
            if not (pos.radiale in listeElements[num]['pos']):
                return False
            
                
##        # pas d'image définie
##        if not 'imag' in elem.images.keys():
##            print " ** pas d'image"
##            return False

##        # S'il y a déja une entretoise
##        if self.elemPos(pos).item.has_key('imag') and self.elemPos(pos).item['imag'] <> None \
##           and self.elemPos(pos).estEntretoise() and not self.estEpaulement(num):
##            print " ** pas autorisé sous entretoise"
##            return False

        # Cas des entretoises
        if self.estEntretoise(num):
            elemOpp = self.elemPos(pos.opposee())
            
            if self.palier[pos.opposee().palier].rlt.num is None:
#                print " ** pas de roulement de l'autre coté"
                return False

            if elemOpp.estAffiche():
                if not elemOpp.estEpaulement():
#                    print " ** entretoise déja affichée"
                    return False
                else:
                    if   pos.radiale == "Ar" and self.palier[pos.palier].taille == "P" \
                      or pos.radiale == "Al" and self.palier[pos.palier].taille == "G" \
                      or self.palier[pos.palier].taille == self.palier[pos.opposee().palier].taille:
#                        print " ** tailles différentes"
                        return False
                    

        # Cas des arrets de butée      
        if self.typeNum(num)== "A":
            if self.palier[pos.palier].rlt.estButee():
                p = pos
            elif self.estEntretoise(num) and self.palier[pos.opposee().palier].rlt.estButee():
                p = pos.opposee()
            else:
                p = False
            
            if p and ((p.cotelem == self.palier[p.palier].rlt.orientation and p.radiale == "Al") \
                  or (p.cotelem <> self.palier[p.palier].rlt.orientation and p.radiale == "Ar")):
#                print " ** butée en",p," : "
                return False


        # Imcompatibilité Arret + Joint     
        if self.typeNum(num) == "A" and pos.radiale == "Al" and not pos.interieur():
            if not self.estChapeau(num, pos) and self.yaUnJoint(pos.palier):
#                print " ** ya un joint"
                return False
        if self.typeNum(num) == "J":
            arret = self.palier[pos.palier].arr["Al"][pos.palier]
            if arret.num is not None and not arret.estChapeau():
                return False
#            if self.palier[pos.palier].rlt.num is None:
#                return False

        return True




    ##############################################################################    
    def placerElem(self, num, pos, taille = "P"):
        "Placer un élément dans le palier à la position <elem.pos>"


        ### Affectation de la taille
        if self.typeNum(num) == "R":
            self.palier[pos.palier].taille = taille


        ### Affectation de la position et Retournement entretoises ...
        if self.estEntretoise(num) \
           and self.palier[pos.palier].taille <> taille:
            pass
#            print "Retournement entretoise"
#            pos = pos.opposee()
##            img = elem.item['imag']
##            elem.item['imag'] = elem.item['opp']
##            elem.item['opp'] = img


        ### Initialisation de l'élément sur le montage
        self.elemPos(pos).__init__(num, taille = taille,
                                   orientation = pos.cotelem,
                                   pos = pos)
            
        if self.estEntretoise(num) and self.placeLibre(pos.opposee()):
#            print "Place opposée libre"
            self.elemPos(pos.opposee()).__init__(num, taille = taille,
                                       pos = pos.opposee())

#        self.parent.GetEventHandler().ProcessEvent(MtgModifiedEvent(myEVT_MTG_MODIFIED))
        
##            self.placerElem(num,pos.opposee(),taille)
##            
##        elif elem.type == "R" and elem.estOblique():
##            nouvelem.orientation = elem.pos.cotelem
##
##        self.majCout()
##
##        self.master.affichageEnCours = False

##        print u"\n Palier :"
##        print self



             
    ##########################################################################
    def supprimerElem(self, pos):
        "Supprimer un élément du palier"
        elemSuppr = self.elemPos(pos)
#        print "Supprimer",pos
        
        if elemSuppr.num is not None:
            if pos.typelem == "R":
                self.palier[pos.palier].taille = "P"
            if elemSuppr.estEntretoise() and self.elemPos(pos.opposee()).estEntretoise():
                self.supprimer1Elem(pos.opposee())
##            if self.elemPos(pos.opposee()).estEntretoise():
##                self.supprimer1Elem(self.elemPos(pos.opposee()))
            elif elemSuppr.type == "R":
                # Insérer ici message "attention"
                pp = PositionDansPivot()
                pp = pos.copie()
                pp.typelem = "A"
                pp.cotelem = "G"
                pp.radiale = "Ar"
                self.supprimerElem(pp)
                pp.cotelem = "D"
                self.supprimerElem(pp)
                pp.radiale = "Al"
                self.supprimerElem(pp)
                pp.cotelem = "G"
                self.supprimerElem(pp)
            self.supprimer1Elem(pos)
           
        #print u" -- élément supprimé :", pos
        self.majCout()
        if self.parent.zMont.numElemProv == None:
            self.parent.GetEventHandler().ProcessEvent(MtgModifiedEvent(myEVT_MTG_MODIFIED))
##        print u"\n Palier :"
##        print self.__repr__()


    ##########################################################################
    def supprimer1Elem(self, pos):
        "Supprimer un unique élément du palier"
        elem = self.elemPos(pos)
        elem.efface()
        elem.__init__()
#        self.parent.GetEventHandler().ProcessEvent(MtgModifiedEvent(myEVT_MTG_MODIFIED))
        

    ###########################################################################
    def effacerElem(self,elem):
        "Effacer l'item d'un élément"
##        if elem.pos.palier is not None:
####            print elem.pos.palier
##            elem.taille = self.palier[elem.pos.palier].taille
        self.frame.effacerItemElem(elem)
        for e in elem.elemEnfant:
            self.frame.effacerItemElem(e)
        elem.elemEnfant = []

##        ### On affiche ...
##        if elem.type == "A" and not elem.pos.interieur():
##            yaJnt = self.yaUnJoint(elem.pos.palier)
##            if yaJnt:
##                for rad in yaJnt[elem.pos.palier]:
##                    self.montrerElem(self.palier[elem.pos.palier].jnt[rad])
##        self.frame.afficherIconeElem(elem,x,y)
##        elem.pos.__init__()




    ###########################################################################
    def cacherElem(self,elem):
        self.frame.cacherItemElem(elem)




    ###########################################################################
    def montrerElem(self,elem):
        self.frame.montrerItemElem(elem)


            
    ###########################################################################
    def afficherElem(self, zoneMtg, elem, pos, hachurer = True):
        "Afficher un élément <elem> à la place <pos>"

#        print "Affichage de :",elem, "hachurage =", hachurer

        ### Affectation de la position et Retournement entretoises ...
#        if elem.estEntretoise() \
#           and self.palier[pos.palier].taille <> elem.taille:
#            print "Retournement entretoise"
#            elem.pos = pos.opposee()
##            img = elem.item['imag']
##            elem.item['imag'] = elem.item['opp']
##            elem.item['opp'] = img
##        else:
##            elem.pos = pos

            
        ### Ajout d'un éventuel support (pour joints ou chapeau) : 'supp'
        #################################################################
        
        if elem.type == "J" or elem.estChapeau():
##           and self.palier[pos.palier].arr["Al"][pos.palier].num is None:
            if not zoneMtg.presenceSupport[elem.pos.palier] and 'supp' in elem.item.keys() :
                zoneMtg.afficherItemElem(elem, 'supp', elem.pos, hachurer = hachurer)
                zoneMtg.presenceSupport[elem.pos.palier] = True

        
        ### Affichage de l'item par défaut : 'imag'
        ### =======================================
                
        zoneMtg.afficherItemElem(elem, 'imag', elem.pos, hachurer = hachurer)

##        ### On cache ...
##        if elem.type == "A" and not pos.interieur():
##            yaJnt = self.yaUnJoint(pos.palier)
##            if yaJnt:
##                for rad in yaJnt[pos.palier]:
##                    self.cacherElem(self.palier[pos.palier].jnt[rad])
            
            
        ### Traitement des entretoises : items 'opp' et 'rond'
        #######################################################
        
        if elem.estEntretoise():
            self.elemPos(elem.pos.opposee()).pos = elem.pos.opposee()
            zoneMtg.afficherItemElem(elem, 'opp', elem.pos.opposee(), hachurer = hachurer)

            # Cas des petites entretoises sur roulements grands : 'rond'
            if elem.taille == "P" and pos.radiale == "Al" \
              and (self.placeLibre(pos.opposee()) or self.elemPos(pos.opposee()).estEntretoise()):
                tailleElem = self.palier[pos.palier].taille
                tailleElemOpp = self.palier[pos.opposee().palier].taille
                if tailleElemOpp == "G":
                    zoneMtg.afficherItemElem(elem, 'rond', pos.opposee(),  hachurer = hachurer)
                elif tailleElem == "G":
                    zoneMtg.afficherItemElem(elem, 'rond', pos, hachurer = hachurer)



        ### Traitement des entretoise pour butées double effet : items 'supp'
        ######################################################################
                    
        if elem.type == "A" and pos.radiale == "Ar" and self.palier[pos.palier].rlt.estButeeDbl():
            zoneMtg.afficherItemElem(elem, 'supp', elem.pos,  hachurer = hachurer)



        ### Traitement des roulements à bagues séparables : 'imagAr'
        #############################################################
                    
        if elem.estSeparable() or elem.nom == u'Roulement à billes à contact oblique':
            zoneMtg.afficherItemElem(elem, 'imagAr', pos, hachurer = hachurer)



        ### Traitement des épaulements intérieurs : 'opp'
        ##################################################
            
        if elem.estEpaulement() and pos.interieur():
            tailleElem = self.palier[pos.palier].taille
            arrOpp = self.elemPos(elem.pos.opposee())
            tailleElemOpp = self.palier[pos.opposee().palier].taille

            if (tailleElemOpp == tailleElem and not arrOpp.estEpaulement()) \
               or ( pos.radiale == "Ar" and tailleElemOpp > tailleElem ) \
               or ( pos.radiale == "Al" and tailleElemOpp < tailleElem ):
##                print "Affichage bout épaulement"
                zoneMtg.afficherItemElem(elem, 'opp', pos.opposee(), hachurer = hachurer)


        ### Affichage des éléments d'arbre et d'alésage
##        print "Affiche arbre alésage et bouts ?",elem.pos
##        if elem.type == "R":
####            print "  Affiche arbre alésage et bouts",elem.pos
##            self.frame.afficherArbreAlesage(elem, self, elem.taille)
##            self.frame.afficherBoutArbre(elem.pos.palier, elem.taille)





    ##########################################################################
#    def enregistrer(self,fichPyv):
#        "Enregistre les données de montage dans le fichPyv ConfigParser"
#
###        print "Enregistrement de :"
###        print self
#        
#        fichPyv.add_section('General')
#        fichPyv.set('General', 'version', self.frame.master.version)
#
#        fichPyv.add_section('Montage')
#        for p in ["G","D"]:
#            fichPyv.set('Montage', "taille "+p, self.palier[p].taille)
#            if self.palier[p].rlt.num <> None and self.palier[p].rlt.estOblique():
#                fichPyv.set('Montage', "orient "+p, self.palier[p].rlt.orientation)
#
###        for elem in self.tousLesElem():
###            if elem.num is not None:
#####                print elem.pos
###                fichPyv.set('Montage', elem.pos.code(), elem.num)
#        for c in self.tousLesCodesPos():
#            elem = self.clefElemPosCode(c)[0]
#            if elem.num is not None:
###                print elem.pos
#                fichPyv.set('Montage', c, elem.num)



#    ##########################################################################
#    def ouvrir02(self, fichier, can):
#        "Ouvrir un montage"
#
###        self = pickle.load(fichier)
#        
###        self.__init__(can, True)
#        # Taille des paliers
#        self.palier["G"].__init__(pickle.load(fichier))
#        self.palier["D"].__init__(pickle.load(fichier))
#
#        # Arrets alésage
#        self.palier["G"].arr["Al"]["G"].__init__(self.conv03(pickle.load(fichier)))
#        self.palier["G"].arr["Al"]["D"].__init__(self.conv03(pickle.load(fichier)))
#        self.palier["D"].arr["Al"]["G"].__init__(self.conv03(pickle.load(fichier)))
#        self.palier["D"].arr["Al"]["D"].__init__(self.conv03(pickle.load(fichier)))
#
#        # Roulements et orientation
#        self.palier["G"].rlt.__init__(self.conv03(pickle.load(fichier)))
#        if self.palier["G"].rlt.num <> None and self.palier["G"].rlt.estOblique():
#            self.palier["G"].rlt.orientation = pickle.load(fichier)
#
#        self.palier["D"].rlt.__init__(self.conv03(pickle.load(fichier)))
#        if self.palier["D"].rlt.num <> None and self.palier["D"].rlt.estOblique():
#            self.palier["D"].rlt.orientation = pickle.load(fichier)
#
#        # Arrets arbre
#        self.palier["G"].arr["Ar"]["G"].__init__(self.conv03(pickle.load(fichier)))
#        self.palier["G"].arr["Ar"]["D"].__init__(self.conv03(pickle.load(fichier)))
#        self.palier["D"].arr["Ar"]["G"].__init__(self.conv03(pickle.load(fichier)))
#        self.palier["D"].arr["Ar"]["D"].__init__(self.conv03(pickle.load(fichier)))
#
#
###        print "Avant conversion :\n", self
#        # Version
###        self.convertir()
#
#        self.toutAfficher()
#        self.majCout()


    ##########################################################################
    def ouvrir(self,fichier):
        """ Ouvrir un montage
            - Version 0.3 -
        """

        # Taille des paliers
        self.palier["G"].taille = fichier.get('Montage', 'taille g')
        self.palier["D"].taille = fichier.get('Montage', 'taille d')
        
        pos = PositionDansPivot()
        for poscode in self.tousLesCodesPos():
##            print "pos =",pos.posCode(poscode)
            if poscode[0] == "R":
                try:
                    orient = fichier.get('Montage', "orient "+poscode[1])
                except (ConfigParser.NoSectionError,ConfigParser.NoOptionError):
                    orient = ''
                    pass

            # Lecture du numéro élément dans le fichier
            try:
                numElem = fichier.getint('Montage', poscode)
            except: # Pas d'élément ici !
                numElem = None
                pass

            # Initialisation de l'élément du montage
            self.clefElemPosCode(poscode)[0].__init__(numElem,
                                                      self.palier[poscode[1]].taille,
                                                      orient)
            
#        print "Fin ouverture Montage :"
#        print self   
#        self.toutAfficher()
#        self.majCout()


    ##########################################################################
    def conv03(self,num):
        if num >=6:
            return num - 6 +100
        elif num >=3:
            return num + 1
        return num
        

    ##########################################################################
    def toutAfficher(self, zoneMtg ,lstCodes = None, hachurer = True):
#        print "Tout afficher ..."
#        print self

#        tm = time.clock()
#        nc = 100
#        for n in range(nc):

        zoneMtg.presenceSupport = {"G" : False,
                                   "D" : False}
        
        if lstCodes == None:
            lstCodes = self.tousLesCodesPos()
            
        for code in lstCodes:
            elem = self.clefElemPosCode(code)[0]
            pos = PositionDansPivot(code = code)
            
##            print
##            print "Element",pos,elem.item.keys()
##            print "Opposé",pos.opposee(),self.elemPos(pos.opposee()).item.keys()
            
            if (elem.num is not None) and not elem.estAffiche():
                
#                print "...test affichage élément :",elem.num, pos
                if elem.estOblique():
                    pos.cotelem = elem.orientation
                
                elem.definirImages(self, zoneMtg, self.palier[pos.palier].taille, pos)
                elem.pos = pos
#                print "    ...pos = ",pos
#                print "    ...elem.pos = ",elem.pos
#                print "    ...elem.item = ",elem.item
#                print "    ...elem.image = ",elem.images.keys()
                if self.placeCompatible(pos, elem.num):
#                    print " ...affichage élément", pos
                    self.afficherElem(zoneMtg, elem, pos, hachurer = hachurer)
##                    if elem.estEntretoise() \
##                       and self.palier[pos.palier].taille == self.palier[pos.opposee().palier].taille:
##                        self.elemPos(elem.pos.opposee()).copier(elem)
##                        self.elemPos(elem.pos.opposee()).pos = elem.pos.opposee()
#                else:
#                    pass
#                    print "*** ANOMALIE AFFICHAGE !!! ***"
##            elif pos.typelem == "R":
##                self.frame.afficherArbreAlesage(self)
##                self.frame.afficherBoutArbre(pos.palier, "P")
                
        zoneMtg.MiseAJourArbreAlesage(hachurer = hachurer)
    ##        self.frame.afficherBoutArbre(self)

#        print "Temps Redessiner", nc, "cycles :",time.clock()- tm

        zoneMtg.Redessiner()

##        self.frame["cursor"] = 'arrow'
##        print self
##        print "Précédent :"
##        print "......elem.pos = ",sauvelem.pos
##        print "......elem.item = ",sauvelem.item


    #############################################################################        
    def RAZ(self):
        """ Réinitialiser le montage """
        for c in self.tousLesCodesPos():
            self.supprimer1Elem(PositionDansPivot().posCode(c))
        
        for p in self.palier.values():
            p.taille = "P"
        


    ##########################################################################
    def estNonVide(self):
        for i in self.tousLesElem():
            if i.num is not None:
                return True
        return False




    #################################################################################################
    #################################################################################################
    def testerInverserSensElem(self,app,elem):
        "Test avant changement d'orientation de l'élément <elem>"
        # Si l'élément est une butée
        if elem.estButee():
            arrets = self.arretsButeeaSupprimer(elem.pos.palier, elem.sensOppose())
            if len(arrets) > 0:
                dlg = wx.MessageDialog(app,self.texteArretsaSupprimer(arrets), 
                               u"Suppression arrêt(s) de butée",
                               wx.OK |wx.CANCEL| wx.ICON_WARNING
                               #wx.YES_NO | wx.NO_DEFAULT |  wx.ICON_INFORMATION
                               )
                if dlg.ShowModal() == wx.ID_OK:
                    self.supprimerArretsButee(arrets)
                    elem.inverserSens()
                    inverse = True
                else:
                    inverse = False

            else:
                elem.inverserSens()
                inverse = True
        else:
            elem.inverserSens()
            inverse = True
        if inverse:
            self.parent.GetEventHandler().ProcessEvent(MtgModifiedEvent(myEVT_MTG_MODIFIED))
        

    #################################################################################################
    #################################################################################################
    def testerChangerTailleElem(self, app, elem):
        "Test avant changement de taille de l'élément <elem>"
        
        def changerTailleElemEtSuppr(elem,dicElem,dicPos):
            for i in dicElem.keys():
                if dicPos[i+"entretoise"] is not None:
                    self.supprimerElem(dicPos[i+dicElem[i]]) 
            changerTailleElem(elem, None)

        def changerTailleElem(elem,supprElem):
            if elem.taille == "G":
                nouvTaille = "P"
            else:
                nouvTaille = "G"
            self.parent.GetEventHandler().ProcessEvent(MtgModifiedEvent(myEVT_MTG_MODIFIED))
            
    ##        # Suppression de l'entretoise ou l'épaulement incompatible #############
    ##        if supprElem is not None:
    ####            print "Suppression de :", supprElem
    ##            self.supprimerElem(supprElem)
                
            # Changement de la taille du palier #####################################
            self.palier[elem.pos.palier].rlt.taille = nouvTaille
            self.palier[elem.pos.palier].taille = nouvTaille

        palier = self.palier[elem.pos.palier]

        palierOpp = self.palier[elem.pos.opposee().palier]
        
        # Détermination du coté "intérieur" du palier ######################################
        if elem.pos.palier == "D":
            i="D"
        else:
            i=1

#        changer = True
#        elemASupprimer = []
        
        # Toutes les positions contenant des séléments succeptibles d'être supprimés
        dicPos = {"Arentretoise" : None,
                  "Arepaulement" : None,
                  "Alentretoise" : None,
                  "Alepaulement" : None}
        
        # Les éléments qui devront être supprimés
        dicElem = {"Ar" : "entretoise",
                   "Al" : "entretoise"}
        
        for rad in ["Ar","Al"]:
#            print palier.arr[rad][elem.pos.opposee().palier]
#            print palierOpp.arr[rad][elem.pos.palier]
            if     palier.arr[rad][elem.pos.opposee().palier].estEntretoise() \
               and palierOpp.arr[rad][elem.pos.palier].estEpaulement():
                dicPos[rad+"entretoise"] = palier.arr[rad][elem.pos.opposee().palier].pos
                dicPos[rad+"epaulement"] = palierOpp.arr[rad][elem.pos.palier].pos
##                dicPos[p[0][i].pos.radiale+"entretoise"] = p[0][i].pos
##                dicPos[p[0][i].pos.radiale+"epaulement"] = p[1][1-i].pos
                
            elif palier.arr[rad][elem.pos.opposee().palier].estEpaulement() \
               and palierOpp.arr[rad][elem.pos.palier].estEntretoise():
                dicPos[rad+"entretoise"] = palierOpp.arr[rad][elem.pos.palier].pos
                dicPos[rad+"epaulement"] = palier.arr[rad][elem.pos.opposee().palier].pos
##                dicPos[p[0][i].pos.radiale+"entretoise"] = p[1][1-i].pos
##                dicPos[p[0][i].pos.radiale+"epaulement"] = p[0][i].pos

#        print dicPos    
                
        if dicPos["Arentretoise"] is not None \
           or dicPos["Alentretoise"] is not None :
            f = FenChoixElementaSupprimer(app, dicElem, dicPos)
            if f.ShowModal() == wx.ID_OK:
                changerTailleElemEtSuppr(elem, dicElem, dicPos)
        else:
            changerTailleElem(elem, None)



    #################################################################################################
    #################################################################################################
    def changerElemRoul(self,elem):
##        print "Changement de type d'élément roulant ..."

        lstB = listeFamilles[0][1][0][1]
        lstR = listeFamilles[0][1][1][1]
        
        if elem.num in lstB:
            num = lstR[lstB.index(elem.num)]
        else:
            num = lstB[lstR.index(elem.num)]
        
        if hasattr(elem, 'orientation'):
            o = elem.orientation
        else:
            o = ''
        elem.__init__(num, elem.taille, o, elem.pos)

#        elem.nom = listeElements[elem.num]['nom']
        self.parent.GetEventHandler().ProcessEvent(MtgModifiedEvent(myEVT_MTG_MODIFIED))


    #############################################################################
    def arretsButeeaSupprimer(self, palier, orient):
        "Renvoie la liste des arrêts à supprimer pour la butée <rlt>"

        arrets = []
            
        for pos in [PositionDansPivot(palier,"A","G","Al"), \
                    PositionDansPivot(palier,"A","D","Al"), \
                    PositionDansPivot(palier,"A","G","Ar"), \
                    PositionDansPivot(palier,"A","D","Ar")]:
##            print self.elemPos(pos).num
            if self.elemPos(pos).num is not None \
               and ((pos.cotelem == orient and pos.radiale == "Al") \
                or (pos.cotelem <> orient and pos.radiale == "Ar")):
                arrets.append(pos.code())
                
##        print "Arrets à supprimer :",arrets

        return arrets

    ##########################################################################
    def supprimerArretsButee(self, arrets):
        pos = PositionDansPivot()
        for a in arrets:
            self.supprimerElem(pos.posCode(a))


    ############################################################################
    def texteArretsaSupprimer(self,arrets):
        ar = []
        for a in arrets:
            if a[2] == "G":
                sa = u"gauche "
            else:
                sa = u"droit "
            if a[3:] == "Ar":
                sa = sa + u"/ arbre"
            else:
                sa = sa + u"/ alésage"
            
            sa += u" : "+self.clefElemPosCode(a)[0].nom
            ar.append(sa)
            
        if len(arrets) == 1:
            t = u"L'arrêt suivant est incompatible\n"
        else:
            t = u"Les arrêts suivants sont incompatibles\n"

        t += u"avec une butée orientée dans le sens prévu :\n"
        for tt in ar:
            t += u"  - "+tt+u"\n"

        if len(arrets) == 1:
            t += u"\nIl sera supprimé ! "
        else:
            t += u"\nIls seront supprimés !"
        
        return t



    #################################################################################################
    #################################################################################################
    def testerChangerTypeElem(self, app, elem, typ):
        "Test avant changement de type de l'élément <elem> en <typ>"
            
        def changerTypeElem(elem, typ, oo = "G"):
##        print "Changement de type ...", typ

            if elem.estOblique():
                orient = elem.orientation
            else:
                orient = oo
                
#            elem.num = typ
            
            elem.__init__(typ, self.palier[elem.pos.palier].taille,orient, elem.pos)  
            
            self.parent.GetEventHandler().ProcessEvent(MtgModifiedEvent(myEVT_MTG_MODIFIED))    
                
        # Si le nouveau type est 'butée' simple effet
        if typ in [3,7]:
            if elem.estOblique():
                arrets = self.arretsButeeaSupprimer(elem.pos.palier, elem.orientation)
                oo = elem.orientation
            else:
                arret = {}
                for o in ["G","D"]:
                    arret[o] = self.arretsButeeaSupprimer(elem.pos.palier, o)
                if len(arret["D"]) > len(arret["G"]):
                    arrets = arret["G"]
                    oo = "G"
                else:
                    arrets = arret["D"]
                    oo = "D"
                
            if len(arrets) > 0:
                dlg = wx.MessageDialog(app,self.texteArretsaSupprimer(arrets), 
                               u"Suppression arrêt(s) de butée",
                               wx.OK |wx.CANCEL| wx.ICON_WARNING
                               #wx.YES_NO | wx.NO_DEFAULT |  wx.ICON_INFORMATION
                               )
                if dlg.ShowModal() == wx.ID_OK:
                    self.supprimerArretsButee(arrets)
                    changerTypeElem(elem,typ,oo)
            else:
                changerTypeElem(elem,typ,oo)
        else:
            changerTypeElem(elem,typ)




    #################################################################################################
    #################################################################################################
    def rafraichirAffichage(self, zoneMtg, lstCodes = None, codePosProv = None, hachurer = True):
        
#        tm = time.clock()
#        nc = 100
#        
#        for n in range(nc):

        # Etablissement de la liste des items
        if lstCodes == None:
            lstElem = self.tousLesElem()
        else:
            lstElem = []
            for c in lstCodes:
                lstElem.append(clefElemPosCode(c))[0]
            
        # Effacement de tous les item ###########################################
        for e in lstElem:
            zoneMtg.effacerItemElem(e)
        
        # Rétablissament de la couleur normale
        for i in zoneMtg.lstItemMtg:
                i.normale()
        
        # Rafraichissement de l'affichage #######################################
        self.toutAfficher(zoneMtg, lstCodes, hachurer = hachurer)

#        print "Temps affichage", nc, "cycles :",time.clock()- tm


    ##########################################################################
    def elemProxim(self, x, y, zoneMtg, exist = False):
        "Renvoyer la position de l'''élément à proximité d'un point"
        
##        dy = 200
        
        pos = PositionDansPivot()

        # palier (X):
        #------------
        if x > zoneMtg.milieuX:
            pos.palier =  "D"
        else:
            pos.palier =  "G"

##        if mtg is not None:
##            taille = self.palier[pos.palier].taille
##        else:
##            taille = "P"
            
        taille = self.palier[pos.palier].taille
        

        # cotelem (X):
        #-------------
        if x > zoneMtg.milieuPalier[pos.palier]:
            pos.cotelem = "D"
        else:
            pos.cotelem = "G"


        # radiale (Y):
        #-------------
        if abs(y - zoneMtg.milieuY) < zoneMtg.centreRoult_Y[taille]:
            pos.radiale = "Ar"
        else:
            pos.radiale = "Al"


        # typelem (X):
        #-------------
          # zone "roulement"
        dxr = 40

          # zone "arrets"
        dxa = 80

          # limite ...
        dxl = 170

        if abs(x - zoneMtg.milieuPalier[pos.palier]) < dxr :
            pos.typelem = "R"
        elif abs(x - zoneMtg.milieuPalier[pos.palier]) < dxa:
            pos.typelem = "A"
        elif abs(x - zoneMtg.milieuX) > abs(zoneMtg.milieuPalier[pos.palier] - zoneMtg.milieuX) \
             and (abs(x - zoneMtg.milieuX) - abs(zoneMtg.milieuPalier[pos.palier] - zoneMtg.milieuX)) < dxl:
            pos.typelem = "J"
        else:
            pos = None

        if exist:
            lstElemExist = self.elemProximExistant(x,y)
            if (pos is not None and self.elemPos(pos).num is None) \
               or (pos is None) :
                if len(lstElemExist) > 0:
                    pos = lstElemExist[0]

##        print pos.code()
        
        return pos


    ##########################################################################
    def elemProximExistant(self, x, y):
        """Renvoie une liste de positions d'éléments existants à proximité d'un point"""
        lst = []
#        for tag in self.frame.gettags(self.frame.find_closest(x,y)):
#            pos = PositionDansPivot().posCode(tag)
#            if pos is not None:
#                if self.elemPos(pos).num is not None:
#                    lst.append(pos)
#        lst.reverse()
        return lst

#    def retourner:
#        self.tree._treeData 
#        
#        _treeData = {1  : self.rlt,
#                     2  : None,
#                     20 : self.arr["Al"]["G"],
#                     21 : self.arr["Al"]["D"],
#                     3  : None,
#                     30 : self.arr["Ar"]["G"],
#                     31 : self.arr["Ar"]["D"],
#                     4  : None,
#                     40 : self.jnt["Al"],
#                     41 : self.jnt["Ar"]
#                     }

    def retourner(self):
        
        def orientInverse(orient):
            if orient == "G" : return "D"
            elif orient == "D": return "G"
            
        def inverser (elem1,elem2):
            n1, n2 = elem1.num, elem2.num
            t1, t2 = elem1.taille, elem2.taille
            o1, o2 = '', ''
            p1, p2 = elem1.pos, elem2.pos
            if hasattr(elem1, 'orientation'):
                o1 = orientInverse(elem1.orientation)
            if hasattr(elem2, 'orientation'):
                o2 = orientInverse(elem2.orientation)
           
            elem1.__init__(n2, t2, o2, p2)
            elem2.__init__(n1, t1, o1, p1)
            
        inverser(self.palier["G"].rlt, self.palier["D"].rlt)
#        self.palier["D"].rlt.taille, self.palier["G"].rlt.taille = self.palier["G"].rlt.taille, self.palier["D"].rlt.taille 
        inverser(self.palier["G"].arr["Al"]["G"], self.palier["D"].arr["Al"]["D"])
        inverser(self.palier["G"].arr["Al"]["D"], self.palier["D"].arr["Al"]["G"])
        inverser(self.palier["G"].arr["Ar"]["G"], self.palier["D"].arr["Ar"]["D"])
        inverser(self.palier["G"].arr["Ar"]["D"], self.palier["D"].arr["Ar"]["G"])
        inverser(self.palier["G"].jnt["Al"], self.palier["D"].jnt["Al"])
        inverser(self.palier["G"].jnt["Ar"], self.palier["D"].jnt["Ar"])

        self.palier["G"].taille, self.palier["D"].taille = self.palier["D"].taille, self.palier["G"].taille 
        
        self.parent.GetEventHandler().ProcessEvent(MtgModifiedEvent(myEVT_MTG_MODIFIED))
#        for p in ["G","D"]:
#            if self.palier[p].rlt.estOblique():
#                self.palier[p].rlt.inverserSens()
                
        return 

        
    



#############################################################################
#############################################################################
#                           #    
#     PositionDansPivot     #
#                           #
#############################################################################
#############################################################################
class PositionDansPivot:
    "Classe définissant l'emplacement d'un élément dans une liaison pivot"

    def __init__(self, palier = None, typelem = None, cotelem = None, radiale = None, code = None):
        if code is None:
            self.typelem = typelem           # "R" ou "A" ou ...
            self.palier = palier             # "G" ou "D"
            self.cotelem = cotelem           # "D" ou "G"
            self.radiale = radiale           # "Ar" ou "Al"
        else:
            self.posCode(code)


    #############################################################################
    def __repr__(self):
        if self.typelem is None:
            return "None"
        return self.code()


    #############################################################################
    def code(self, bague = '--'):
        "Renvoie le code de la position"
        if self.palier == None:
            p = "-"
        else:
            p = self.palier
        c = self.typelem + p

        if self.cotelem is None or self.typelem == "R" or self.typelem == "J":
            c += '-'
        else:
            c += self.cotelem

        if hasattr(self, 'radiale') and bague == "--":
#        if self.typelem == "A" or self.typelem == "J":
            c += self.radiale
        else:
            c += bague
        
        return c


    #############################################################################
    def posX(self):
        """Renvoie la position en X à partir d'une position"""

        pcode = self.code()

        return self.posXCode(pcode)


    ############################################################################
    def posXCode(self,code):
        """Renvoie la position en X à partir du code d'une position"""
        x = 1
        if code[0] == "A":
            x += -1

        if code[1] == "D":
            x += 3

        if code[2] == "D":
            x += 2

        return x

    
    
    #############################################################################
    def posCode(self,code):
        "Renvoie la position à partir d'un code de position <code>"
##        print "code",code
        if code == "":
            self = None
        elif code[1] in ["G","D"]:
            self.typelem = code[0]
            self.palier = code[1]
            self.cotelem = code[2]
            self.radiale = code[3:5]
        else:
            self = None
            
        return self



    ############################################################################
    def traduireEnTexte(self, pcode):
        if pcode[0] == "R":
            texte = u"roulement"
        elif pcode[0] == "A":
            texte = u"arret palier"
        else:
            texte = u"portée de roulement"
            if pcode[3:5] == "Ar":
                texte += u" arbre"
            else:
                texte += u" alésage"

        if pcode[1] == "G":
            texte += u" gauche"
        elif pcode[1] == "D":
            texte += u" droit"

        if pcode[0] == "R":
            if pcode[3:5] == "Ar":
                texte += u" bague intérieure"
            elif pcode[3:5] == "Al":
                texte += u" bague extérieure"
        else:
            if pcode[2] == "G":
                texte += u" coté gauche"
            if pcode[2] == "D":
                texte += u" coté droit"

        return texte
        

    #############################################################################            
    def numPos(self, param):
        "Renvoi <0> si le paramètre <param> est de type 'G' "
        if param == "cotelem":
            e = self.cotelem
        elif param == "palier":
            e = self.palier
        else:
            return
        if "G" in e:
            return 0
        else:
            return 1

        
    #############################################################################        
    def suivant(self, typeAvance, sens):
        "Progresse dans le palier selon <typeAvance> et dans le sens <sens>"
        suiv = PositionDansPivot(self.palier,self.typelem,self.cotelem,self.radiale)
        if typeAvance == "DansChaine":
            if suiv.typelem == "A" and suiv.radiale == "Ar":
                if (sens == 0 and suiv.cotelem == "G") or (sens == 1 and suiv.cotelem == "D"):
                    suiv.typelem = "R"
                else:
                    suiv = None
            elif suiv.typelem == "R":
                suiv.typelem = "A"
                suiv.radiale = "Al"
                if sens == 0:
                    suiv.cotelem = "D"
                else:
                    suiv.cotelem = "G"
            elif suiv.typelem == "A" and suiv.radiale == "Al":

                if sens == 0:
                    if suiv.palier == "D" and suiv.cotelem == "G":
                        suiv.cotelem = "D"
                    else:
                        suiv = None
                else:
                    if suiv.palier == "G" and suiv.cotelem == "D":
                        suiv.cotelem = "G"
                    else:
                        suiv = None       
            else:
                suiv = None
                
        elif typeAvance == "SautePalier":
            suiv.radiale = "Ar"
            suiv.typelem = "A"
            if sens == 0:
                if suiv.palier == "G":
                    suiv.palier = "D"
                    suiv.cotelem = "G"
                else:
                    suiv = None
                    
            else:
                if suiv.palier == "D":
                    suiv.palier = "G"
                    suiv.cotelem = "D"
                else:
                    suiv = None
                    
        elif typeAvance == "SauteEntre":
            if suiv.radiale == "Ar":
                suiv.typelem = "R"
                if sens == 0:
                    suiv.palier = "D"
                else:
                    suiv.palier = "G"
            else:
                if sens == 0:
                    suiv.palier = "D"
                    suiv.cotelem = "D"
                else:
                    suiv.palier = "G"
                    suiv.cotelem = "G"
                
                
        elif typeAvance == "SauteRoult":
            if sens == 0:
                if suiv.palier == "G":
                    suiv.cotelem = "D"
                else:
                    suiv = None
                    
            else:
                if suiv.palier == "D":
                    suiv.cotelem = "G"
                else:
                    suiv = None

        elif typeAvance == "RoultSuiv":
            suiv.typelem = "R"
            if sens == 0:
                suiv.palier = "D"
            else:
                suiv.palier = "G"

        elif typeAvance == "RoultSaute":
            suiv.typelem = "R"
                                
        return suiv


    #############################################################################
    def opposee(self):
        "Renvoie la position opposée, sans modifier <self>"
        pp = PositionDansPivot()
        if self.palier == "G":
            pp.palier = "D"
        else:
            pp.palier = "G"
        if self.cotelem == "G":
            pp.cotelem = "D"
        else:
            pp.cotelem = "G"
        pp.typelem = self.typelem
        pp.radiale = self.radiale  
        return pp


    #############################################################################
    def interieur(self):
        u"Renvoie <True> s'il s'agit d'un arret intérieur"
        if self is None:
            return False
        if self.typelem == 'A' \
            and self.palier != self.cotelem :
            return True
        else:
            return False


    #############################################################################
    def copie(self):
        "Renvoie une copie de la position, sans modifier <self>"
        pp = PositionDansPivot()
        pp.palier = self.palier
        pp.cotelem = self.cotelem
        pp.typelem = self.typelem
        pp.radiale = self.radiale  
        return pp


    #############################################################################
    def egal(self,pos):
        "Renvoie <True> si les 2 positions sont égales" 
        if pos is None:
            return False
        return (self.typelem == pos.typelem) \
               and (self.palier == pos.palier) \
               and (self.cotelem == pos.cotelem or self.cotelem == None or pos.cotelem == None ) \
               and (self.radiale == pos.radiale or self.radiale == None or pos.radiale == None)


    #############################################################################
    def __eq__(self,pos):
        """ Teste l'égalité de deux positions """
        if pos is None: return False
        return (self.typelem == pos.typelem) \
               and (self.palier == pos.palier) \
               and (self.cotelem == pos.cotelem or self.cotelem == None or pos.cotelem == None ) \
               and (self.radiale == pos.radiale or self.radiale == None or pos.radiale == None \
                    or self.typelem == "R")


    #############################################################################
    def __ne__(self,pos):
        """ Teste si deux positions sont différentes """
        if pos is None or type(pos) != type(self): return True
        return     (self.typelem != pos.typelem) \
               or  (self.palier  != pos.palier) \
               or  (self.cotelem != pos.cotelem and self.cotelem != None and pos.cotelem != None ) \
               or  (self.radiale != pos.radiale and self.radiale != None and pos.radiale != None \
                    and self.typelem <> "R")


#############################################################################
#############################################################################
class FenChoixElementaSupprimer(wx.Dialog):
    "Choix de l'élément incompatible à supprimer pour un changement de taille"

    def __init__(self, parent, dicElem, dicPos):

        message = u"Un changement de taille du roulement entraînerait \n" +\
                  u"une incompatibilité entre épaulement et entretoise !\n" + \
                  u"Un ou plusieurs élément(s) doit(vent) être supprimé(s).\n\n" + \
                  u"Sélectionner les éléments à supprimer :"

        messagefin = u'... ou "Annuler" pour ne rien changer.'
        
        # Liste des éléments à supprimer
        self.Selection = dicElem
       
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, -1, u"Incompatibilité")
        self.PostCreate(pre)

        # This extra style can be set after the UI object has been created.
        if 'wxMac' in wx.PlatformInfo and useMetal:
            self.SetExtraStyle(wx.DIALOG_EX_METAL)

        sizer = wx.BoxSizer(wx.VERTICAL)
        
        msizer = wx.BoxSizer(wx.HORIZONTAL)
        bmp = wx.ArtProvider.GetBitmap(wx.ART_WARNING, wx.ART_MESSAGE_BOX, (32,32))
        icon = wx.StaticBitmap(self, -1, bmp)
        msizer.Add(icon, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        label = wx.StaticText(self, -1, message)
        label.SetHelpText(u"Il suffit de lire !")
        msizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        
        sizer.Add(msizer, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        box = wx.BoxSizer(wx.HORIZONTAL)

        lstChoix = []
        lstChoix.append(u"Entretoise")
        lstChoix.append(u"Epaulement")
        for i in dicElem.keys():
            if dicPos[i+"entretoise"] is not None:
                if i == "Ar":
                    t = u"arbre"
                    n = 0
                else:
                    t = u"alésage"
                    n = 1
                rbox = wx.RadioBox(self, n, "Sur l'"+t+" :", 
                                   choices = lstChoix, name = i)
                self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, rbox)
                box.Add(rbox, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        label = wx.StaticText(self, -1, messagefin)
        label.SetHelpText(u"Aucun changement ne sera apporté au montage.")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        btnsizer = wx.StdDialogButtonSizer()
        
        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
        
        btn = wx.Button(self, wx.ID_OK)
        btn.SetLabel("Supprimer")
        btn.SetHelpText(u"Supprime les éléments selectionnés")
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btn.SetLabel("Annuler")
        btn.SetHelpText(u"Ne change rien au montage (pas de changement de taille")
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)
        
#        self.ShowModal()
        
#        self.SetEscapeId(wx.ID_CANCEL).SetLabel("Annuler")
#        self.SetAffirmativeId(wx.ID_OK).SetLabel("Supprimer")
   
    def EvtRadioBox(self,event):
#        print event.GetInt(), event.GetId()
        id = event.GetId()
        int = event.GetInt()
        if id == 0:
            a = "Ar"
        else:
            a = "Al"
        
        if int == 0:
            e = "entretoise"
        else:
            e = "epaulement"
        
        self.Selection[a] = e
        
    def GetSelection(self):
        return self.Selection


#
#    ##########################################    
#    def annuler(self):
#        self.dicElem = {"Ar" : StringVar(),
#                        "Al" : StringVar()}
#        self.destroy()

