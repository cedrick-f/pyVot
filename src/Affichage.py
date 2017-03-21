#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##This file is part of PyVot
#############################################################################
#############################################################################
##                                                                         ##
##                               Affichage                                 ##
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
#import wx.lib.dragscroller
import Montage
import Elements
import Images
import FenPrincipale
import Const
from globdef import *
#import wx.lib.delayedresult as delayedresult
# Pour tester optimisation
#import time


#import Image,ImageTk

########################################################################################################
class Alesage:
    def __init__(self, zoneMtg):
        self.zoneMtg = zoneMtg
        # Liste de tous les items "alesage"
        self.lstItem = {}
        for palier in ["G","D"]:
            self.lstItem[palier+Const.palierOppose[palier]] = ItemArAl(zoneMtg, "Al" ,
                                                    posit = palier+Const.palierOppose[palier],
                                                    taille = "G")
            self.lstItem[palier+"M"] = ItemArAl(zoneMtg, "Al" ,
                                                 posit = palier+"M",
                                                 taille = "G",
                                                 bout = "B")
             

        # Structure "fixe" de l'alésage :
        self.itemFix = {"M_"  : ItemArAl(zoneMtg, "Al" , posit = "M_", taille = "P"),
                        "GM" : None,
                        "GD" : None,
                        "DG" : None,
                        "DM" : None}

        self.itemFix["M_"].calc_posX()

#        self.miseAJour(canvas.mtg)

        

    def miseAJour(self, mtg, hachurer = True):
        self.effacer()
        self.affecterItem(mtg)
        self.afficher(hachurer = hachurer)

    def effacer(self):
        for item in self.itemFix.values():
            if item is not None:
                item.efface()

    def afficher(self, hachurer = True):
        for clef in self.itemFix:
            if self.itemFix[clef] is not None:
                self.itemFix[clef].afficher(hachurer = hachurer)

    def affecterItem(self, mtg):
##        print
##        print "Affectation des items arbres :"
        
        # Affectation des items "fixes" ...
        for palier in ["G","D"]:
            if mtg.palier[palier].taille == "G":
                self.itemFix[palier+"M"] = self.lstItem[palier+"M"]
            else:
                self.itemFix[palier+"M"] = None
        if mtg.palier["G"].taille == mtg.palier["D"].taille \
           and mtg.palier["G"].taille == "G":
            self.itemFix["GD"] = self.lstItem["GD"]
            self.itemFix["DG"] = self.lstItem["DG"]
        else:
            self.itemFix["GD"] = None
            self.itemFix["DG"] = None


# Liste ordonnée des itemMtg à afficher
class ListeItemMtg(list):
    def __init__(self):
        list.__init__(self)
        
    def __repr__(self):
        s = ''
        for item in self:
            s += " "+item.nom
        return s
    
    def affiche(self, dc, offsetX = 0):
#        self.oterDoublons()
        self.trie()
        for item in self:
            item.affiche(dc, offsetX = offsetX)
#        print "AFFICHAGE",self
    
    def oterDoublons(self):
        s = set(self)
        self = list(s)

    
    def effacer(self, item):
        try:
            self.remove(item)
        except ValueError: 
#            print "!!! erreur effacement !!!"
            pass
    
    def trie(self):
        self.sort(cmp=lambda x,y: cmp(x.prof, y.prof))
    
    
        
    def get(self, tag):
        lstItem = []
        for i in self:
            if tag in i.tag:
                lstItem.append(i)
        return lstItem
    
    

class PositArAl:
    def __init__(self, palier, posit):
        self.palier = palier
        self.posit = posit

        
##################################################################################################
class Arbre:
    def __init__(self, zoneMtg):
        
        self.zoneMtg = zoneMtg
        # Structure "fixe" de l'arbre :
        #               posit
        self.itemFix = {"GD" : None,
                        "GM" : None,
                        "DM" : None,
                        "DG" : None,
                        }
        
        # Structure "mobile" de l'arbre :
        self.itemMob = {"GGG" : None,
                        "GGD" : None,
                        "GDG" : None,
                        "GDD" : None,
                        "GGB" : None,
                        "DGG" : None,
                        "DGD" : None,
                        "DDG" : None,
                        "DDD" : None,
                        "DDB" : None}


        # Chargement de TOUS les items "arbre" :
        #---------------------------------------
        self.lstItem = {}

        # items Fixes axialement
        for posit in self.itemFix:
            self.lstItem[posit] = {}
            for taille in ["P","G"]:
                self.lstItem[posit][taille] = {}
                for bout in ["E","R",""]:
                    self.lstItem[posit][taille][bout] = {}
                
                # Portées du roulement (1 morceau "R" en GM ou DM)
                if posit[1] == "M":           
                    self.lstItem[posit][taille]["R"][""] =  ItemArAl(zoneMtg, "Ar" ,
                                                                    posit = posit,
                                                                    taille = taille,
                                                                    bout = "M",
                                                                    dim = "")
                # Intérieur du montage (1 morceau "" en GD ou DG)
                else:                         
                    self.lstItem[posit][taille][""][""] =  ItemArAl(zoneMtg, "Ar" ,
                                                                    posit = posit,
                                                                    taille = taille,
                                                                    bout = "",
                                                                    dim = "")
        
            # Intérieur du montage épaulement (1 morceau "E" en GD ou DG)
            self.lstItem[posit]["P"]["E"][""] =  ItemArAl(zoneMtg, "Ar" ,
                                                            posit = posit,
                                                            taille = "P",
                                                            bout = "E",
                                                            dim = "")

        # items Mobiles axialement (en relation avec les éléments du montage)
        for posit in self.itemMob:
            self.lstItem[posit] = {}
            for taille in ["P","G"]:
                self.lstItem[posit][taille] = {}
                for bout in ["B","F","R"]:
                    self.lstItem[posit][taille][bout] = {}
                
                # Extrémités de l'arbre (1 morceau "B" ou "F" -3 diamètres- en GGB ou DDB)
                if posit[2] == "B":        
                    for bout in ["B","F"]:
                        for dim in ["P","N","G"]:
                            self.lstItem[posit][taille][bout][dim] = ItemArAl(zoneMtg, "Ar" ,
                                                                              posit = posit,
                                                                              taille = taille,
                                                                              bout = bout,
                                                                              dim = dim)
                # Bords des roulements (4 morceaux "E" et "I" en GGG ...)
                for dim in ["E","I"]:
                    self.lstItem[posit][taille]["R"][dim] =  ItemArAl(zoneMtg, "Ar" ,
                                                                posit = posit,
                                                                taille = taille,
                                                                bout = "R",
                                                                dim = dim)

        
    def miseAJour(self, mtg, hachurer = True):
        self.effacer()
        self.affecterItem(mtg)
        self.afficher(hachurer = hachurer)

    def effacer(self):
        for item in self.itemFix.values() + self.itemMob.values():
            if item is not None:
                item.efface()


    def afficher(self, hachurer = True):
        for item in self.itemFix.values() + self.itemMob.values():
            if item is not None:
                item.afficher(hachurer = hachurer)


    def affecterItem(self, mtg):
        """ Affecte des items aux éléments de structure de l'arbre """
##        print
##        print "Affectation des items arbres :"
        
        # Affectation des items "fixes" ...
        ####################################
        for clef in self.itemFix:

            # Détermination de la dimension relative (dim)
            #---------------------------------------------
            if clef[1] == "M":
                elem = mtg.palier[clef[0]].arr["Ar"][clef[0]]
                dim = ""
                if elem.num is not None and elem.estEcrou():        # pas de M si écrou
##                   and mtg.palier[clef[0]].taille == "P":
                    self.itemFix[clef] = None
                    continue                                        # fin de la boucle
            else:
                dim = ""
            if clef[1] == "M":
                bout = "R"
            else:
                if mtg.palier["G"].taille <> mtg.palier["D"].taille:
                    if mtg.palier[clef[0]].taille == "P":
                        bout = "E"
                    else:
                        bout = ""
                else:
                    bout = ""
            
##            print "Affectation",clef,": bout =",bout,"; dim =",dim
            self.itemFix[clef] = self.lstItem[clef][mtg.palier[clef[0]].taille][bout][dim]

        
        # Affectation des items "mobiles" ...
        #####################################
        for clef in self.itemMob:
            # On récupère ce qu'il y a "autour"
            arr = mtg.palier[clef[0]].arr["Ar"][clef[1]]
            rlt = mtg.palier[clef[0]].rlt
            
            # On détermine quel est l'élément pour le positionnement relatif
            if arr.num is None:
                if rlt.num is None:
                    elem = None
                else:
                    elem = rlt
            else:
                if arr.estEntretoise():
                    elem = rlt
                else:
                    elem = arr
            
            # Cas des extrémités de l'arbre
            #-------------------------------
            if clef[2] == "B":    
                # affectation du diamètre de l'extrémité selon le type d'arrêt ...
                if arr.num is not None:                         
                    if arr.estEcrou():                         
                        dim = "P"
                    elif arr.estEpaulement():
                        dim = "G"
                    else:
                        dim = "N"
                else:
                    dim = "N"
                    
                # Détermination du type d'extrémité (Chanfreiné ou infini)
                if mtg.palier[clef[0]].jnt["Ar"].estJointChapeau():
                    bout = "B"
                else:
                    bout = "F"
                
                self.itemMob[clef] = self.lstItem[clef][mtg.palier[clef[0]].taille][bout][dim]
                self.itemMob[clef].calc_posX(rlt)
            
            # Cas des bords de portée de roulement
            #--------------------------------------
            else:
                # Cas ou il ne faut pas en mettre
                if arr.num is not None and arr.estEcrou():
                    self.itemMob[clef] = None
                elif arr.num is not None and arr.estEpaulement() and (clef[2] == clef[1]):
                    self.itemMob[clef] = None
                    
                # Autres cas ...
                else:
                    if clef[2] == clef[1]:
                        dim = "E"
                        bout = "R"
                    else:
                        dim = "I"
                        bout = "R"
                    
                    self.itemMob[clef] = self.lstItem[clef][mtg.palier[clef[0]].taille][bout][dim]
                    self.itemMob[clef].calc_posX(elem)

                
#    def ajuster(self, clefItem, mtg):
#        pass






##############################################################################
##############################################################################
#
#    Items de la zone de Montage     #
#
##############################################################################
##############################################################################
class ItemMtg():
    def __init__(self, zoneMtg, imagePlus):
        self.zoneMtg = zoneMtg
        # Dict de toutes les images (de type ImagePlus !!) succeptibles d'être utiles
        self.images = {}
        self.images["def"] = imagePlus.copie() # L'image par défaut
        
        # Paramètres de position en X 
        #----------------------------
        self.xancre = 0
        self.ancre = "D"
        # Réelle position en pixels
        self.pos = (0,0)
        # Profondeur
        self.prof = 0
        
        self.tag = []
        
        # Image Bitmap à afficher 
        #------------------------
        self.keybmp = "def"
#        self.bmp = self.images.bmp
        self.defBmp0()
#        self.dragImage = None
        self.shown = True
    
    
    def defBmp0(self):
        self.bmp0 = self.GetBmp().GetSubBitmap(wx.Rect(0, 0,
                      self.GetWidth(), self.GetHeight())) 
    
    def GetBmp(self):
        return self.GetImg().bmp
        
    def GetImg(self):
        return self.images[self.keybmp]
    
    def SetBmp(self, bmp):
        self.GetImg().bmp = bmp
        
    def SetImg(self, bmp):
        self.GetImg().img = bmp.ConvertToImage()
#        self.GetImg().img.SetMask()
        
    def GetWidth(self):
        return self.GetBmp().GetWidth()
    
    def GetHeight(self):
        return self.GetBmp().GetHeight()
    
    def __repr__(self):
        s = ''
        for t in self.tag:
            s += t + ' '
        p = "("+str(self.pos[0])+","+str(self.pos[1])+")"
        return s#+p
        
    def place(self, xancre = None, ancre = None):
        """ Calcul la réelle position en pixels
            de l'image --> .pos
        """
        if ancre != None:
            self.ancre = ancre
        
        if self.ancre == "G":
#            anchor = W
            sensOffset = -1
        elif self.ancre == "D":
#            anchor = E
            sensOffset = 1
        else :
#            anchor = CENTER
            sensOffset = 0
        
        if xancre != None:
            self.xancre = xancre
        
        self.pos = (self.xancre + sensOffset * (self.GetImg().ofst+1) - ((sensOffset+1)*self.GetWidth())/2,
                    self.zoneMtg.milieuY - self.GetHeight()/2)
        
    def affiche(self, dc, tag = None, prof = None, inverser = False, offsetX = 0):
        """ Affiche l'image bmp dans le DC
        """
        if not self.shown:
            return
        
        x,y = self.pos[0]+offsetX, self.pos[1]
        
        dc.DrawBitmap(self.GetBmp(), x,y, True)
        
        if tag is not None:
            self.ajout_tag(tag)
        if prof is not None:
            self.prof = prof

    def hachurer(self, brush_hachure, pts = ((2,2),), simple = False):
        """ Hachurage de la bmp de l'item
            à partir des points <pts> (repère LOCAL de l'item)
        """
        
        # On crée une image à la taille de la zone entière pour une bonne superposition des hachures ...
        bmp = wx.EmptyBitmap(self.zoneMtg.maxWidth, self.zoneMtg.maxHeight)
        memdc = wx.MemoryDC(bmp)
        memdc.SetBackground(wx.Brush(wx.Colour(255,255,254, 255))) #
        memdc.Clear()
        
        memdc.SetBrush(wx.BLACK_BRUSH)
        memdc.SetPen(wx.BLACK_PEN)
#        memdc.SetPen(wx.TRANSPARENT_PEN)
#        memdc.DrawRectangle(0, 0, self.GetWidth(), self.GetHeight())
        
        memdc.DrawBitmap(self.GetBmp(), self.pos[0], self.pos[1])
        
        for pt in pts:
            # Calcul du point de hachurage dans le repère global
            if self.pos[0] > self.zoneMtg.milieuX:
                pt = (self.GetWidth() - pt[0], pt[1])
            cx,cy = self.pos[0] + pt[0] , self.pos[1] + pt[1]
            colour = memdc.GetPixel(cx,cy)
            # On hachure ...
            memdc.SetBrush(brush_hachure)
            if simple:
                memdc.FloodFill(cx, cy, colour)
            else:
                for y in [cy, self.zoneMtg.maxHeight - cy]:
                    memdc.FloodFill(cx, y, colour)

        memdc.SelectObject(wx.NullBitmap)
        
        # On découpe ...
        bmp = bmp.GetSubBitmap(self.GetRect())
        
        # On rétabli la transparence ...
#        img = wx.ImageFromBitmap(bmp)
#        img = bmp.ConvertToImage()
#        img.SetMaskColour(255,255,254)
#        if not img.HasAlpha():
#            img.InitAlpha()
#        img.SetMask(True)
#        bmp = img.ConvertToBitmap()
        
        mask = wx.Mask(bmp, wx.Colour(255,255,254, 255))
        bmp.SetMask(mask)
    
        self.SetBmp(bmp)
        self.GetImg().sauveBmp()
        self.bmp0 = bmp.GetSubBitmap(wx.Rect(0, 0,
                      self.GetWidth(), self.GetHeight()))

        
#        print "Durée hachurage",self.tag[0],",",nc,"cycles :",  time.clock()- tm
        
    def efface(self):
#        self.canvas.delete(self.id)
        self.zoneMtg.lstItemMtg.effacer(self)

    def cache(self):
        self.shown = False

    def ajout_tag(self,tag):
        self.tag.append(tag)

    def inverser(self):
        self.GetImg().inverser()
        self.GetImg().conv2Bmp()
        self.defBmp0()
#        self.bmp = self.image.bmp
        if "vid" in self.images:
            self.images["vid"].inverser()
            self.images["vid"].conv2Bmp()
#            self.vide = self.imgvide.bmp

    def surbrillance(self, effet):
        self.GetImg().surbrillance(effet)
#        self.bmp = self.image.bmp

    def estomper(self, niv):
        self.GetImg().estomper(niv)
#        self.bmp = self.image.bmp
        
    def fondu(self, item, niv):
        if "vid" in self.images:
            bmp = self.images["vid"].bmp
        else:
            bmp = None
        self.SetBmp(self.GetImg().fondu(self.bmp0, bmp, niv))
        
    def couleur(self, coul, vide = False):
        self.GetImg().changerCouleur(coul)
#        if vide:
#            self.imageVide.changerCouleur(coul)
#            self.bmp = self.imageVide.bmp
#        else:
#            self.image.changerCouleur(coul)
#            self.bmp = self.image.bmp
#        self.canvas.itemconfigure(self.id, image = self.image.tk)


    def normale(self):
        self.GetImg().normal()
#        self.bmp = self.image.bmp
#        self.canvas.itemconfigure(self.id, image = self.image.tk)


    def largeur(self):
        return self.GetImg().largeur()


#    def set_profondeur(self, prof):
###        print "Profondeur de", self.id,self.nom, "=",prof
#        dessous = self.profJusteDessous(prof)
#        if dessous != None:
###            print "  ..placé dessous",dessous
#            
#            self.canvas.tag_lower(self.id,dessous)
##        self.canvas.addtag_withtag("P"+str(prof),self.id)
#
#
#    def profJusteDessous(self, prof):
##        for i in self.canvas.find_withtag(ALL):
##            profItem = self.get_prof(i)
##            if profItem >= prof:
##                return i
#        return None


    def get_prof(self, Id):
#        for t in self.zoneMtg.gettags(Id):
#            if t[0] == "P":
#                return eval(t[1])
        return 0

                            
    def get_xbord(self, cote):
        if cote == "G":
            i = 0
        else:
            i = 1
        return self.pos[0] + i*self.GetWidth()
#        return self.zoneMtg.bbox(self.id)[i]+1-i


    def get_xancre(self):
#        return self.zoneMtg.coords(self.id)[0]
        return self.pos[0]


    def estAffiche():
        return self.zoneMtg.itemcget(state) == NORMAL

#    # Gestion des déplacements
#    #==========================
#    def debutDeplace(self):
##        self.zoneMtg.RefreshRect(self.GetRect(), True)
##        self.zoneMtg.Update()
#        self.dragImage = wx.DragImage(self.bmp)
#        self.dragImage.BeginDrag((0,0), self.zoneMtg, False)#, self.dragShape.fullscreen)
#        self.dragImage.Move(self.pos)
#        self.dragImage.Show()
#        
#        
#    def deplace(self, dx):
#        pt = (dx+self.pos[0], self.pos[1])
#        self.dragImage.Move(pt)
#        
#            
#    def deplacer(self, dc, dx):
#        pt = (dx+self.pos[0], self.pos[1])
#        self.dragImage.GetImageRect(pt)
##            self.dragImage.Move(pt)
#        dc.Clear()
#        self.dragImage.DoDrawImage(dc, pt)
#        
#
#    def finDeplace(self):
#        self.shown = True
#        self.dragImage.Hide()
#        self.dragImage.EndDrag()
##        self.zoneMtg.RefreshRect(self.GetRect(), True)
#        self.dragImage = None
#
#    
    def GetRect(self):
        return wx.Rect(self.pos[0], self.pos[1],
                      self.GetWidth(), self.GetHeight())

##############################################################################
#
#    Items d'élément     #
#
##############################################################################
class ItemElem(ItemMtg):
    """ Item d'élément du montage """
    
    def __init__(self, zoneMtg, mtg, clefImageElem):
        ItemMtg.__init__(self, zoneMtg, Images.imageElem[clefImageElem])
        self.nom = clefImageElem
        self.xancre = 0     # Abcisse élément
        self.ancre = ""     # Ancrage élément
       
    def imagVide(self, clef):
        self.images["vid"] = Images.imageElem[clef].copie()
        
    def calc_posX(self, pos, elem_rel = None, joint = False, elem = None, entre = False):
        """ Calcul de la position en x de l'item :
              pos = position dans le montage : <PositionDansPivot>
              elem_rel = élément relatif
              joint = <True> s'il s'agit d'un joint
              elem = element à placer
              entre = <True> si l'élément est une entretoise de butée double
        """
        
        # ... roulements :
        #-----------------
        if pos.typelem == "R":
            self.ancre = pos.cotelem
            self.xancre = self.zoneMtg.milieuPalier[pos.palier]     # Abcisse élément
            self.ancre = ""                                         # Ancrage élément
            return


        # ... arrêts :
        #-------------
         # Coefficient de coté du roulement
        if pos.cotelem == "G": s = -1
        else: s = 1

         # Largeur du roulement associé
        if elem_rel is None or elem_rel.num is None:                    # pas d'élément
            taille = self.zoneMtg.mtg.palier[pos.palier].taille
            largRlt = self.zoneMtg.largeurRltDefaut[taille]

##            # On écarte si l'arrêt ne fait que porter un joint
##            if joint:
##                ecart = self.canvas.ecartRoultJnt
##            else:
##            ecart = self.canvas.ecartRoultEpaul[taille][pos.radiale]
            if joint:
                self.xancre = self.zoneMtg.milieuPalier[pos.palier] \
                              + s * (largRlt/2+self.zoneMtg.ecartRoultJnt)
            else:
                self.xancre = self.zoneMtg.milieuPalier[pos.palier] \
                              + s * (self.zoneMtg.positElemFixe[taille][pos.radiale])# + largRlt/2)
                
            self.ancre = pos.opposee().cotelem
#            print s
#            print "xancre",pos, self.xancre
#            print "ancre",pos, self.ancre
            
        else:
            self.xancre = elem_rel.item['imag'].get_xbord(pos.cotelem)
            self.ancre = pos.opposee().cotelem
            
            # cas des roulements à rouleaux coniques --> décalage
            if elem_rel.num == 5:
#                print "Rlt roul Con. !!", pos, elem_rel.orientation, elem_rel.taille
                if elem_rel.orientation == pos.cotelem and pos.radiale == "Al" \
                   or elem_rel.orientation != pos.cotelem and pos.radiale == "Ar":
                    if elem_rel.taille == "P":
                        self.xancre += -s*8
                    else:
                        self.xancre += -s*12

            # cas des butées double effet --> décalage
            elif elem_rel.estButeeDbl() and elem is not None:
                if pos.radiale == "Ar":
                    if elem.estEntretoise() or elem.estEpaulement():
                        self.xancre += -s*self.zoneMtg.decalageButDbl[elem_rel.taille]
#                        if elem_rel.taille == "P":
#                            self.xancre += -s*44
#                        else:
#                            self.xancre += -s*51
                    else:
                        self.xancre += -s*self.zoneMtg.decalageRondButDbl[elem_rel.taille]
#                        if elem_rel.taille == "P":
#                            self.xancre += s*4
#                        else:
#                            self.xancre += s*6
                        # si l'élément est entretoise de butée : entre
                        if entre:
#                            self.xancre += s
                            self.ancre = pos.cotelem


##############################################################################
#
#    Items d'arbre/alésage     #
#
##############################################################################
tagArAl = {"Ar" : TAG_ARBRE,
           "Al" : TAG_ALESAGE}

class ItemArAl(ItemMtg):
    """ Item de morceau d'arbre/alésage """
    
    def __init__(self, zoneMtg, rad , posit , taille, bout = "", dim = ""):
        
        self.palier = posit[0]
        self.cote = posit[1]
        self.taille = taille
        self.bout = bout
        self.rad = rad
        self.dim = dim
        
        self.nom = self.rad+self.palier+self.cote

        t = self.taille
        
        if self.rad == "Ar":
            img = Images.imageAr[t + self.bout + self.dim]
        else:
            img = Images.imageAl[t + self.bout]

        ItemMtg.__init__(self, zoneMtg, img)

        # retourne les images de droite ...
        #----------------------------------
        if self.palier == "D":
            self.inverser()

        # On place l'item à la bonne profondeur ...
        #------------------------------------------
        if self.rad == "Al":
            if self.palier == "M":
                prof = 0
            elif self.bout == "B":
                prof = 1
            else:
                prof = 2
        else:
            if self.bout in ["G","D"] or len(posit) == 2:
                prof = 9
            else:
                prof = 8

        self.prof = prof


        # On calcule la position pour les items "fixes" ...
        #--------------------------------------------------
        if len(posit) == 2:
            self.fixe = True
            self.calc_posX()
        else:
            self.fixe = False
            if posit[2] == "B":
                self.coteopp = posit[0]
            else:
                self.coteopp = posit[2]

        if self.rad == "Al":
            self.ajout_tag(TAG_ALESAGE)
        else:
            self.ajout_tag(TAG_ARBRE)

        
    #########################################################################
    def afficher(self,  hachurer = True):
        self.place()
        self.zoneMtg.lstItemMtg.append(self)
        if  hachurer and 'GrpAlesage' in self.tag:
            self.hachurer(wx.BrushFromBitmap(Images.imageAl["H"].bmp))
        
    #########################################################################
    def get_xbordElem(self, cote, palier = None, elem = None, ecarter = False):
        """ Renvoie la position en X en pixel (absolue)
            - du bord de l'élément <elem> si elem
            - ecarté par rapport au centre du palier si pas d'elem
        """
        if cote == "G": s = -1
        else: s = 1
        
        if elem is not None:
            return elem.item['imag'].get_xbord(cote)+s
        else:
            taille = self.taille
            ecart = self.zoneMtg.largeurRltDefaut[taille]/2
            if ecarter:
                ecart = self.zoneMtg.positElemFixe[taille][self.rad]# - ecart
                
##            print "ecart :",ecart
            return self.zoneMtg.milieuPalier[palier] \
                          + s * (ecart)

            
    ####################################################################################
    def calc_posX(self, elem = None):
        """ Détermine la position en X du morceau 
            selon l'éventuel <elem> relatif
        """
        # Milieu du montage (pour l'alésage seulement)
        #----------------------------------------------
        if self.palier == "M":
            self.ancre = ""
            self.xancre = self.zoneMtg.milieuX
            return

##        print "Calcul X :", elem

        # Portée du roulement
        #---------------------
        if self.cote == "M":
            self.ancre = ""
            self.xancre = self.zoneMtg.milieuPalier[self.palier]
            return

        # Morceaux fixes
        #----------------
        if self.fixe:
            self.ancre = Const.palierOppose[self.cote]
            cote = self.cote
            if self.rad == "Al":
                ecarter = True
            else:
                ecarter = True
            self.xancre = self.get_xbordElem(cote, palier = self.palier, ecarter = ecarter)

        # Morceaux mobiles
        #------------------
        else:
            self.ancre = Const.palierOppose[self.coteopp]
            cote = self.cote
            ecarter = False
            
            # Pas d'élément relatif
            if elem is None or elem.num is None:
                self.xancre = self.get_xbordElem(cote, palier = self.palier, ecarter = ecarter)
            
            # Avec élément relatif
            else:
                if elem.type == "R":
                    cote = self.cote
                else:
                    cote = self.coteopp
                self.xancre = self.get_xbordElem(cote, elem = elem)
                
                # Décalage en cas de butée double effet
                if elem.estButeeDbl() and self.rad == "Ar" and self.cote == self.palier:
                    if cote == "G": s = -1
                    else: s = 1
                    arr = self.zoneMtg.mtg.palier[self.palier].arr['Ar'][self.palier]
                    if arr.estEntretoise() or arr.estEpaulement():
                        self.xancre += -s*self.zoneMtg.decalageButDbl[elem.taille]
                    else:
                        self.xancre += -s*self.zoneMtg.decalageRondButDbl[elem.taille]





##############################################################################
##############################################################################
#                           #
#      Zone de montage      #
#                           #
##############################################################################
##############################################################################
#####################################################################################################
#####################################################################################################
class ZoneMontage(wx.Panel):
    def __init__(self, parent, app, mtg):
        
        self.app = app
        self.parent = parent
        # Dimensionnement
        size = (680,510)
        self.maxWidth  = size[0]
        self.maxHeight = size[1]
        
        wx.Panel.__init__(self, parent, -1, (0, 0), size=size, style=wx.BORDER_RAISED|wx.RETAINED)
        
#        self.SetVirtualSize((self.maxWidth, self.maxHeight))
        self.SetMaxSize(size)
#        self.SetVirtualSizeHints(10, 10, size[0], size[1])
        
        # Le montage à afficher
        self.mtg = mtg
        
        # Liste ordonnée des itemMtg à afficher
        self.lstItemMtg = ListeItemMtg()
        
        # Définit si il doit y avoir surbrillance des élément au passage de la souris 
        self.SurBrillanceActive = True

        # Permet de mémoriser si un support de joint ou de chapeau est déja dessiné
        self.presenceSupport = {"G" : False,
                                "D" : False}
        
        # Paramètres de la fenêtre
        self.SetBackgroundColour("WHITE")
        
#        self.SetScrollRate(5,5)

        # Pour affichage dans thread
#        self.jobID = 0
#        self.abortEvent = delayedresult.AbortEvent()
        
        ################################
        # Chargement des images
        ################################
        Images.charger_imagesAr()
        Images.charger_imagesAl()
        Images.charger_imageElem()

        # Indique qu'un affichage est en cours
        self.affichageEnCours = False
#        self.curseurInterdit = False
        
        # Indique qu'un élément est mis en surbrillance
        self.surBrillanceEnCours = False
        
        # Indique qu'on est en mode analyse
        self.modeAnalyse = False

        # Instanciation d'un élément provisoire
        self.numElemProv = None

        # Position précédente de la souris
        self.posPreced = None

        # Paramètres de positionnement du montage
        #-----------------------------------------
        #  abscisses des centres des paliers
        self.milieuPalier = {"G":180,
                             "D":500}
        #  centre du montage
        self.milieuX , self.milieuY = size[0]/2, size[1]/2

        #  positions et dimensions des éléments (pour chaine)
        self.centreRoult_Y = {"P":99,
                              "G":115}
        self.dimRoult_Y = {"P":100,
                           "G":112}
        
        # Positions des éléments "fixes" d'arbre et d'alésage
        #  par rapport au centre du palier
        self.positElemFixe = {"P" :  {"Al" : 79 , "Ar" : 96},  # 79  126
                              "G" :  {"Al" : 104, "Ar" : 106}} # 104 136

        # Décalage sous butées doubles (avec et sans rondelle)
        self.decalageButDbl = {"P" : 44,
                               "G" : 51}
        self.decalageRondButDbl = {"P" : -4,
                                   "G" : -6}
        
        # Ecarts entre le roulement et les supports de joint
        self.ecartRoultJnt = 10
        
        # Définition des constantes
        self.largeurRltDefaut = {"G" : 105 ,
                                 "P" : 89}

        # Structure du montage (items affichés)
        #---------------------------------------
        #  Structure de l'ensemble Arbre
        self.arbre = Arbre(self)

        #  Structure de l'ensemble Alésage
        self.alesage = Alesage(self)

        #  Groupes d'item
        self.grpArbre = []
        self.grpAlesage = []
    

        # Pour la surbrillance des éléments 
        #-----------------------------------
        self.itemCourant = None
        self.posCourant = None
        self.elemSauv = None
        self.imageSauv = {}

        # Lancement de l'affichage
        #--------------------------
        self.MiseAJourArbreAlesage()
        self.InitBuffer()
        
        # Actions de la souris
        #----------------------
#        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftButtonEvent)
        self.Bind(wx.EVT_LEFT_UP,   self.mouseUp)
        self.Bind(wx.EVT_MOTION,    self.OnMove)
        self.Bind(wx.EVT_RIGHT_UP, self.OnContextMenu)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
#        self.Bind(wx.EVT_SCROLLWIN, self.OnResize)
        self.Bind(wx.EVT_KEY_UP, self.Escape)
        
        self.Bind(wx.EVT_MIDDLE_DOWN, self.OnMidDown)
        self.Bind(wx.EVT_MIDDLE_UP, self.OnMidUp)
        
        self.Bind(wx.EVT_PAINT,    self.OnPaint)
        
#        self.scroller = wx.lib.dragscroller.DragScroller(self)
#        self.scroller.SetSensitivity(0.04)
#        print "Sensibilité Scroller :", self.scroller.GetSensitivity()
        
        # Pour débuggage ...
        self.lstItemSousPointeurCourant = []
        
        

    #############################################################################            
    def Escape(self, event = None):
        "Op. à effectuer quand la touche <Echap> est pressée"
#        print "ECHAPPE"
        if event is None or event.GetKeyCode() == 27:
            if self.affichageEnCours:
                self.mtg.supprimerElem(self.posPreced)
            self.mouseUp(event)
            self.mtg.rafraichirAffichage(self)
            
            
    #############################################################################            
    def OnEnter(self, event):    
        if self.FindFocus() == self.parent:
            self.SetFocus()

        
    #############################################################################            
    def OnLeave(self, event):
#        print "LEAVE",
        if self.modeAnalyse:
            return
        self.surImage()
        if self.affichageEnCours:
            self.mtg.supprimerElem(self.posPreced)
            self.mtg.rafraichirAffichage(self)
            self.app.changerCurseur(elem = self.numElemProv)
            self.affichageEnCours = False
        
    #############################################################################            
    def OnResize(self, evt):
        self.InitBuffer()

    #############################################################################            
    def OnMidDown(self, event):
        self.scroller.Start(event.GetPosition())

    def OnMidUp(self, event):
        self.scroller.Stop()

    #############################################################################            
    def OnPaint(self, evt):
#        print "PAINT"
        dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)
#        self.DoPrepareDC(dc)
#        try:
##            dc = wx.AutoBufferedPaintDC(self)
##            
#            dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_CLIENT_AREA)
#        except:
#            self.InitBuffer()

#        dc = wx.BufferedPaintDC(self, self.buffer, wx.BUFFER_VIRTUAL_AREA)
        
    def InitBuffer(self):
        w,h = self.GetVirtualSize()
        self.buffer = wx.EmptyBitmap(w,h)
        self.Redessiner()
        
    def Redessiner(self, analyse = None):  
#        print "REDESSINER"
        cdc = wx.ClientDC(self)
#        self.parent.DoPrepareDC(cdc)
        dc = wx.BufferedDC(cdc, self.buffer, wx.BUFFER_VIRTUAL_AREA)
        self.DessineTout(dc, analyse)

        
    def DessineTout(self, dc, analyse = None, offsetX = 0):
        # Affichage "Arbre" et "Alésage"
#        print "/",
        dc.BeginDrawing()
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        self.lstItemMtg.affiche(dc, offsetX = offsetX)
        
        # Tracé des éléments d'analyse 
        #=============================
        if analyse is not None:
            analyse.tracerResultats(dc, self)
        
        dc.EndDrawing()
        
#        # Tracé de la chaine d'action 
#        #=============================
#        for s,t in self.chaineTracee.items():
#            if t is not None: self.tracerChaineAct(dc, t, s)
        


    def getWidth(self):
        return self.maxWidth

    def getHeight(self):
        return self.maxHeight


#    def SetXY(self, event):
#        self.x, self.y = self.ConvertEventCoords(event)
#
#    def ConvertEventCoords(self, event):
#        newpos = self.CalcUnscrolledPosition(event.GetX(), event.GetY())
#        return newpos

#    def OnLeftButtonEvent(self, event):
#        if event.LeftDown():
#            self.SetFocus()
#            self.SetXY(event)
#            self.curLine = []
#            self.CaptureMouse()
#            self.drawing = True

        
   

##    #############################################################################
##    def afficherPremierArbre(self):
##        print "affichage prem arbre"
##        self.ArbreAlesage["ArM"].afficher()
##
##    def afficherPremierAlesage(self):
##        print "affichage prem alesage"
##        self.ArbreAlesage["AlM"].afficher()


        
    ############################################################################         
    def MiseAJourArbreAlesage(self, hachurer = True):
#        print "Mise à Jour arbre/alésage"
#        self.InitBuffer()
        self.alesage.miseAJour(self.mtg, hachurer = hachurer)
        self.arbre.miseAJour(self.mtg, hachurer = hachurer)
        


  
    #############################################################################         
    def cacherItemElem(self,elem):
        for i in elem.item.values():
            self.cacherItem(i)

    def montrerItemElem(self,elem):
        for i in elem.item.values():
            self.montrerItem(i)


        
    ###########################################################################
    def effacerItemElem(self, elem):
        "Effacer les items d'un élément"
##        print "Effacement ?",elem.num,elem.pos,elem.item.keys()
        for i in elem.item.values():
            i.efface()
        
##        if elem.type == "A" and elem.pos.interieur() and elem.pos.radiale == "Al" \
##            and not elem.estEntretoise():
##            self.afficherCacherRondelle(elem.pos.cotelem,True)
##            
##        if elem.pos.radiale == "Ar" and elem.estEcrou():
##            self.afficherBoutArbre(elem.pos.palier, elem.taille)

            
##        elem.pos.__init__()
        elem.item = {}
        
##        if elem.pos is None:
##            return
##        if elem.pos.typelem is not None:
##            print "  Effacement",elem.pos,elem.item.values()
##            for i in elem.item.values():
##                i.cache()
####            self.delete(elem.pos.code())
##
##            if elem.type == "A" and elem.pos.interieur() and elem.pos.radiale == "Al" \
##               and not elem.estEntretoise():
####                print "montre Rondelle"+elem.pos.cotelem
##                self.afficherCacherRondelle(elem.pos.cotelem,True)
##            
##            if elem.pos.radiale == "Ar" and elem.estEcrou():
##                self.afficherBoutArbre(elem.pos.palier, elem.taille)
####            if elem.type == "R":
####                self.afficherBoutArbre(elem.pos.palier,"P")
##
##            
####        elem.pos.__init__()
##        elem.item = {}

        # On Affiche le curseur par défaut
        self.afficheCurseur()




#    ###########################################################################
#    def afficherCacherRondelle(self, cotelem, afficher):
#        if self.gettags("Rondelle"+cotelem) <> ():
#            if cotelem == "G":
#                s = 1
#            else:
#                s = -1
###            xr = self.coords("Rondelle"+cotelem)[0]
#            if afficher:
###                print "Affiche rondelle",cotelem
#                self.itemconfigure("Rondelle"+cotelem, state = NORMAL)
###                self.coords("Rondelle"+cotelem, xr, self.milieuY)
#                self.move("SurRond"+cotelem, -s*22,0)
#                
#            else:
###                print "Cache rondelle",cotelem
#                self.itemconfigure("Rondelle"+cotelem, state = HIDDEN)
###                self.coords("Rondelle"+cotelem, xr, -200)
#                self.move("SurRond"+cotelem, s*22,0)
            

    ############################################################################
    def HasSupport(self, palier):
        return False    


    ###########################################################################
    def afficherItemElem(self, elem, clef, pos,  hachurer = True):
        """ Afficher l'item de clef <clef> d'un élément <elem>
            à la position <pos> """

#        print "Affichage de", elem.num, clef, pos, elem.pos#, "Hachurage =", hachurer
        
#        # On Cache le curseur
#        if not self.affichageEnCours:
#            self.effaceCurseur()

        if not clef in elem.item.keys():
            return

        # Calcul de la position en x  ###############################
        #############################################################

        # ... roulements :
        #-----------------
        if pos.typelem == "R":
            elem.item[clef].calc_posX(pos)               # Abcisse élément

        #... arrets :
        #------------
        elif pos.typelem == "A":

            # Cas du complément d'épaulement : item 'opp'
            if elem.estEpaulement() and clef == 'opp' :
                elem.item[clef].calc_posX(pos)

            # Cas de l'entretoise pour butée double effet
            elif clef == 'supp' and pos.radiale == "Ar":
                elem.item[clef].calc_posX(pos, self.mtg.palier[pos.palier].rlt,
                                          elem = elem, entre = True)
            
            # Cas des supports
            elif clef == 'supp':
#                print "Support"
                elem.item[clef].calc_posX(pos,
                                          joint = True)
            #Autres cas ...
            else:
                elem.item[clef].calc_posX(pos, self.mtg.palier[pos.palier].rlt,
                                          elem = elem)

        #... joints :
        #------------
        elif pos.typelem == "J":
            # le joint lui même
            if clef == "imag":
                if 'supp' in elem.item.keys():              # il faut aussi un support
                    joint = elem.item['supp'].estAffiche
                else:                                       # pas besoin de support
                    joint = False
##                print "Joint ?",joint
                elem.item[clef].calc_posX(pos, #self.mtg.palier[pos.palier].rlt,
                                          joint = True)#joint)

            # le support du joint (type "arrêt")
            else:
                posSupp = pos.copie()
                posSupp.typelem = "A"
                elem.item[clef].calc_posX(posSupp, #self.mtg.palier[pos.palier].rlt,
                                          joint = True)
            
            
        # Ajout des tags par défaut
        ##########################################################
        elem.item[clef].ajout_tag(elem.pos.code())


        # Regroupage des items - Ajout de tag ####################       
        # Gestion des éléments spéciaux : 
        #   - roulements séparables
        #   - groupes "Arbre" et "Alésage"
        #   - Joint
        ##########################################################
        if elem.type == "R":
            if elem.estSeparable() or elem.nom == u'Roulement à billes à contact oblique':
                if clef == 'imagAr':
                    tag = pos.code("Ar")
                else:
                    tag = pos.code("Al")
                elem.item[clef].ajout_tag(tag)
            else:
                elem.item[clef].ajout_tag(pos.code("Al"))
                elem.item[clef].ajout_tag(pos.code("Ar"))

        elif elem.estEpaulement():
            if pos.radiale == "Al":
                elem.item[clef].ajout_tag(TAG_ALESAGE)
            else:
                elem.item[clef].ajout_tag(TAG_ARBRE)
    
            if clef == 'opp' and pos <> elem.pos:
                elem.item[clef].ajout_tag(elem.pos.opposee().code())


        elif elem.type == "J":
            elem.item[clef].ajout_tag("A"+pos.code()[1:3]+"Al")
            
#        if clef == 'vide':
#            if pos.radiale == "Al":
#                self.addtag_withtag(TAG_ALESAGE,elem.item[clef])
#            else:
#                self.addtag_withtag(TAG_ARBRE,elem.item[clef])
        
            

        # Gestion de la profondeur  #############################
        #########################################################
        if pos.typelem == "R":
            if clef == 'imag':
                prof = 5
            else:
                prof = 6
            
        elif pos.typelem == "A":
            if pos.radiale == "Al":
                if 'GrpAlesage' in elem.item[clef].tag:
                    if elem.taille == "G":
                        prof = 3
                    else:
                        prof = 4
#                    prof = 3
                elif elem.estChapeau():
                    prof = 4#5
                else:
                    prof = 4
#                if elem.taille == "G":
#                    prof = 4
#                else:
#                    prof = 4
            else:
                if elem.taille == "G":
                    prof = 12
                else:
                    prof = 11
            
            if elem.estEcrou():
                prof += -1
            # Entretoise
            elif elem.estEntretoise():
                if pos.radiale == "Al":
                    prof = 5#4
                else:
                    prof = 7#6

            # Support de joint ou de chapeau
            if clef == "supp":
                if pos.radiale == "Al":
                    prof = 3
                else:
                    prof = 7#6
                   
        elif pos.typelem == "J":
            if clef == "imag":
                if pos.radiale == "Al":
                    prof = 2
                else:
                    prof = 7
            else:
                if pos.radiale == "Al":
                    prof = 3#4
                else:
                    prof = 3#4
        
        elem.item[clef].prof = prof
 

        # Mise en place ##########################################
        ##########################################################
        
        elem.item[clef].place()
#        e = elem.item[clef]
#        print " ",e.xancre," ",e.ancre," ",e.image.ofst," ",e.prof," -->",e.pos   

     
        # Gestion de la rondelle #################################
        ##########################################################
        if clef == 'rond':
##            print "ajout Rondelle"+pos.cotelem
##            print "   rondelles :",self.find_withtag("Rondelle"+pos.cotelem)
            self.rondelle = elem.item[clef]
            if pos.palier <> elem.pos.palier:
                cle = 'opp'
            else:
                cle = 'imag'
                
            if pos.cotelem == "G":
                s = 1
            else:
                s = -1
                
            elem.item[cle].pos = (elem.item[cle].pos[0] - s*(self.rondelle.GetImg().largeur()-1),
                                  elem.item[cle].pos[1])
        

        # Ajout dans la liste des items à afficher ###############
        ##########################################################
        self.lstItemMtg.append(elem.item[clef])

            
        # Hachurage ###############################################
        ###########################################################
        # Hachurage du bâti
        #===================
        if hachurer:
            if 'GrpAlesage' in elem.item[clef].tag:
                elem.item[clef].hachurer(wx.BrushFromBitmap(Images.imageAl["H"].bmp))
            
            # Hachurage des entretoises
            #===========================
            elif elem.estEntretoise() and clef <> 'rond':
                if pos.radiale == "Ar":
                    h = wx.BDIAGONAL_HATCH
                else:
                    h = wx.FDIAGONAL_HATCH
                b = wx.Brush(wx.NamedColour("dark green") , h)    
                elem.item[clef].hachurer(b, pts = ((6,6),))
            
            # Hachurage des écrous
            #======================
            elif elem.estEcrou():
                elem.item[clef].hachurer(wx.Brush(wx.BLUE , wx.BDIAGONAL_HATCH), pts = ((70,74),), simple = True)
                pts = ((40,45),)
                elem.item[clef].hachurer(wx.Brush(wx.NamedColour("dark green") , wx.FDIAGONAL_HATCH), pts = pts)
            
            # Hachurage des chapeaux
            #========================
            elif elem.type == "J" or elem.estChapeau():
    #            print "hachurage chapeau", clef
                if clef == "supp":
                    pts = ((60, 10),(60,80))
                else:
                    pts = ((2, 2),)
                elem.item[clef].hachurer(wx.Brush(wx.BLACK , wx.BDIAGONAL_HATCH), pts = pts)
            
              
            
#            self.afficherRondelle(pos.cotelem,True)
#            if self.mtg.elemPos(pos).estEntretoise() or self.mtg.placeLibre(pos):
#                
#                
#            else:
#                self.itemconfigure("Rondelle"+pos.cotelem, state = HIDDEN)
##                xr = self.coords("Rondelle"+pos.cotelem)[0]
##                self.coords("Rondelle"+pos.cotelem, xr, -200)

                
#        # On gère l'affichage de la rondelle ...
#        if elem.type == "A" and pos.interieur() and pos.radiale == "Al" \
#           and not elem.estEntretoise():
#            self.afficherCacherRondelle(pos.cotelem,False)
#        if clef == 'rond':
###            print "ajout Rondelle"+pos.cotelem
###            print "   rondelles :",self.find_withtag("Rondelle"+pos.cotelem)
#            elem.item[clef].ajout_tag("Rondelle"+pos.cotelem)
#            if pos.palier <> elem.pos.palier:
#                cle = 'opp'
#            else:
#                cle = 'imag'
#            elem.item[cle].ajout_tag("SurRond"+pos.cotelem)
#            if self.mtg.elemPos(pos).estEntretoise() or self.mtg.placeLibre(pos):
#                self.afficherCacherRondelle(pos.cotelem,True)
#            else:
#                self.itemconfigure("Rondelle"+pos.cotelem, state = HIDDEN)
###                xr = self.coords("Rondelle"+pos.cotelem)[0]
###                self.coords("Rondelle"+pos.cotelem, xr, -200)
#
#                
#        # On gère l'affichage de la rondelle ...
#        if elem.type == "A" and pos.interieur() and pos.radiale == "Al" \
#           and not elem.estEntretoise():
#            self.afficherCacherRondelle(pos.cotelem,False)
            
#        self.InitBuffer()
##        self["cursor"] = 'target'


    ############################################################################
    def coordsBordElem(self, mtg, pos, cote = None, rad = None, entretoise = False):
        """ Renvoie les coordonnées du point au bord de l'élément 
            situé à la position <pos>
            du coté <cote> de l'élément
            
        """

        decalage = 6

        elem = mtg.elemPos(pos)
        elemOpp = mtg.elemPos(pos.opposee())

        p = pos.palier
        c = pos.numPos("cotelem")*2-1

        if elem.num is None and not entretoise:
            pasDElem = True
        else:
            pasDElem = False

                    
        # calcul du Y ###
        #----------------
        if elem.num is not None:
            # Si on doit prendre l'entretoise
            if entretoise \
               or ( elem.estEntretoise() and elemOpp.estEntretoise() ):
                if elemOpp.estEntretoise():
                    taille = elemOpp.taille
                else:
                    taille = elem.taille
            else:
                taille = elem.taille
        else:
            taille = mtg.palier[pos.opposee().palier].taille
#            taille = elemOpp.taille

        py = self.centreRoult_Y[taille]
        dpy = self.dimRoult_Y[taille]/2 - decalage
        
        if (pos.typelem == "A" and pos.radiale == "Ar") or (rad == "Ar"):
            y = - py + dpy
        elif (pos.typelem == "A" and pos.radiale == "Al") or (rad == "Al"):
            y =  - py - dpy
        else:
            y = - py



        # calcul du X ###
        #----------------
          # Pas d'élément ...
        if pasDElem:
##            print "pas d'elem"
            if p == "D":
                c = 1
            else:
                c = -1
##            print "Pas d'elem : "
##            print " pos = ",pos
##            print " c = ",c
            palierOpp = pos.opposee().palier
            x = self.milieuPalier[palierOpp] \
                + c * (self.positElemFixe[taille][pos.radiale])# - self.largeurRltDefaut[taille]/2)
            
##            x = self.milieuPalier[palierOpp] \
##                + c * (mtg.palier[palierOpp].rlt.largeur()/2 \
##                       + self.ecartRoultEpaul[taille][pos.radiale])
            
          # Arrets ...
        elif pos.typelem == "A":
            if cote is None or cote == p or cote != pos.cotelem:
                x = self.milieuPalier[p] \
                    + c * (mtg.palier[p].rlt.largeur()/2)
            else:
                if p == "D":
                    c = 1
                else:
                    c = -1
                palierOpp = pos.opposee().palier
                x = self.milieuPalier[palierOpp] \
                    + c * (self.positElemFixe[mtg.palier[pos.opposee().palier].taille][pos.radiale])

          # Roulements ...
        elif pos.typelem == "R":
            x = self.milieuPalier[p]
            if cote == "G":
                x += -mtg.palier[p].rlt.largeur()/2
            elif cote == "D":
                x += mtg.palier[p].rlt.largeur()/2

##        print pos,x,y
        return x,y
        


  


        

##    def quitterMenuContext(self, event = None):
##        self.frame.destroy()
##        self.frame = None


##    #############################################################################
##    def choixType(self, elem):
##        """Popup right-click menu of special parameter operations"""
##        ChoixElement(self.master, elem, elem.type)


        
    ##########################################################################    
    def surImage(self, pos = None):
        """ Gèrer la mise en surbrillance des items du montage
        """
    
        # 
        # On sort si on n'est pas en mode d'édition
        #
        if not self.SurBrillanceActive:
            return
        
        def restaureImages():
            self.posCourant = None
            if self.elemSauv is not None:
                for clef in self.elemSauv.item.keys():
                    if self.elemSauv.item[clef].estAffiche:
                        self.elemSauv.item[clef].normale()
                self.elemSauv = None
            
            if self.surBrillanceEnCours:
                self.app.statusBar.PopStatusText()
                self.surBrillanceEnCours = False
            
        def surbrillImage(elem):
            for clef in elem.item.keys():
                if clef in ['imag','imagAr','opp','rond'] \
                   and elem.item[clef] is not None:
#                            print "  Clef :",clef, "\tProf:", elem.item[clef].prof
                    self.elemSauv = elem
                    if elem.type == "R":
                        effet = 0
                    else:
                        effet = 1
                    elem.item[clef].surbrillance(effet)
            
            if not self.surBrillanceEnCours:
                self.app.statusBar.PushStatusText(u"Faire un clic-droit pour afficher le menu contextuel ...", 0)
                self.surBrillanceEnCours = True
        
        
        if pos != self.posCourant:
            #
            # S'il y a quelquechose sous le pointeur de la souris ...
            #
            if pos is not None:
                if self.surBrillanceEnCours:
                    restaureImages()
                elem = self.mtg.elemPos(pos)
                if elem.num is not None:
                    surbrillImage(elem)
                else:
                    if self.surBrillanceEnCours:
                        restaureImages()
            #
            # S'il n'y a rien sous le pointeur de la souris ...
            #   
            else:
                restaureImages()
            
            self.posCourant = pos
            
            self.Redessiner()
                
    




    ##########################################################################    
    def activer_desactiverBoutons(self):
        return
        self.master.barreElements.activer_desactiverBoutons(self.master.mtg.deuxrlt())


    def Intercepte(self):
        self.t.stop()


    ##########################################################################
    def sortie(self, event = None):
        if event.x <= 0 or event.y <=0:
#            print "sortie"
            self.surImage()
#            self.restaureImages()
            self.OnMove()


        
    ###########################################################################
    ##  Gestion du curseur ####################################################
    ###########################################################################
        
    def afficheCurseur(self, event = None):
        if event == None:
            x , y = 0 , 0
        else:
            x , y = event.x , event.y

        
##        if self.master.elemProv.num is not None \
##           and self.gettags("Curseur") == ():
####            self.configure(cursor = "@handno.ani")
####            self["cursor"] = ''
##            self.create_image(x , y,
##                              image = self.master.elemProv.imageB,
##                              tags = "Curseur")
            

    def deplaceCurseur(self, event):
        pass
##        self.coords("Curseur", event.x, event.y)
        

#    def effaceCurseur(self, event = None):
#        pass
##        self.delete("Curseur")
##        self["cursor"] = 'arrow'
##        self.master.zoneMessage.restaurer()
##        if self.master.affichageEnCours:
##            self.master.mtg.effacerElem(self.master.elemProv)

    def metDevantCurseur(self):
        pass
##        self.tag_raise("Curseur")

#    def _resultConsumer(self, delayedResult):
#        jobID = delayedResult.getJobID()
#        assert jobID == self.jobID
#        try:
#            result = delayedResult.get()
#        except Exception, exc:
#            print "Result for job %s raised exception: %s" % (jobID, exc)
#            return
#        
#    def _resultProducer(self, jobID, abortEvent):
#        self.mtg.rafraichirAffichage(self, hachurer = self.app.options.optGenerales["Hachurer"])
#        return jobID


    #############################################################################
    def OnMove(self, evt = None):
        """Op. à effectuer quand la souris se déplace
        """
        
        if evt == None:
            return
        
        # Pas de modification de l'affichage en mode "analyse" ...
        if self.modeAnalyse:
            return
        
        #        
        # Si on a cliqué sur le bouton d'un élément :
        #--------------------------------------------
        if self.numElemProv != None:
            x, y = evt.GetPosition()
            posSouris = self.mtg.elemProxim(x, y, self)

            # Si la souris survole une position différente de la précédente
            if posSouris != self.posPreced:
#                print ">>> Nouvelle position",posSouris
                rafraichir = False
#                self.abortEvent.set() #Abandon du tracé
                
                if self.affichageEnCours:
##                    print ">>> Suppression affichage en cours",posSouris
                    self.mtg.supprimerElem(self.posPreced)
                    self.app.changerCurseur(elem = self.numElemProv)
                    self.affichageEnCours = False
                    rafraichir = True

                self.posPreced = posSouris
            
                # Si la souris survole une position valide
                if posSouris != None \
                   and posSouris.typelem == self.mtg.typeNum(self.numElemProv):
##                    print ">>> Type compatible ..."

                    # Si la place est libre et compatible avec l'élément ...
                    if self.mtg.placeLibre(posSouris) \
                        and self.mtg.placeCompatible(posSouris,self.numElemProv):
#                        print ">>> Affichage ",posSouris          
                        self.mtg.placerElem(self.numElemProv, posSouris, self.app.taillelem)
                        self.affichageEnCours = True
                        rafraichir = True
                        if Elements.Element(self.numElemProv).estOblique():
                            self.app.changerCurseur(CURSEUR_ORIENTATION) 
                        else:
                            self.app.changerCurseur(CURSEUR_OK)                      
                    else:
                        self.affichageEnCours = False
                        self.app.changerCurseur(CURSEUR_INTERDIT) 
                else:
                    self.affichageEnCours = False
#                    if self.affichageEnCours: or self.curseurInterdit:
                    self.app.changerCurseur(elem = self.numElemProv)
                
                # On rafraichit l'affichage ...
                if rafraichir:
#                    print "Rafraichissement ..."
#                    self.abortEvent.set() #Abandon du tracé
#                    self.abortEvent.clear()
#                    self.jobID += 1
#                    delayedresult.startWorker(self._resultConsumer, self._resultProducer, 
#                                  wargs=(self.jobID,self.abortEvent), jobID=self.jobID)
                    wx.BeginBusyCursor(wx.HOURGLASS_CURSOR)
                    self.mtg.rafraichirAffichage(self, hachurer = self.app.options.optGenerales["Hachurer"])
                    wx.EndBusyCursor()

        #            
        # Mise en surbrillance :
        #-----------------------
        else:
           
            self.lstItemSousPointeur = self.LstItemSousPointeur(evt.GetPosition())
            
            # Pour débuggage :
#            if  self.lstItemSousPointeur <> self.lstItemSousPointeurCourant:
##                print
#                try:
#                    i = self.lstItemSousPointeur[0]
#                    print i.tag, "\t\t", i.prof#, "\t", i.xancre
#                except: pass
#                for i in self.lstItemSousPointeur:
##                    print i.tag#, "\t\t", i.prof, "\t", i.GetImg().nom, "\t\t", i.xancre
#                    self.lstItemSousPointeurCourant = self.lstItemSousPointeur 
                
            if len(self.lstItemSousPointeur) > 0: 
#                print lstItemSousPointeur,
                #
                # On prend l'élément du dessus ...
                #
                item = self.lstItemSousPointeur[0]
                posSouris = Montage.PositionDansPivot().posCode(item.tag[0])
                self.surImage(posSouris)
                
            

    #############################################################################            
    def mouseUp(self, event):
        """ Op. à effectuer quand le bouton gauche de la souris est relâché
        """
#        print "MOUSE UP"
#        x, y = event.m_x, event.m_y
        if self.numElemProv != None :
            if self.affichageEnCours:
                self.affichageEnCours = False
#                self.curseurInterdit = False
#                self.app.statusBar.PopStatusText()
    #        print "Desactivation",self.numElemProv,
            self.app.nbGauche.tbElem.desactiverBouton(self.numElemProv)
            if not self.app.nbGauche.tbElem.DClick:
                self.numElemProv = None
            self.app.nbGauche.tree.RecreateTree()
    #            self.app.barreElements.tacheEffectuee()
            self.app.changerCurseur()
            
            # On met le hachures si elles n'aparaissaient pas en mode édition
            if not self.app.options.optGenerales["Hachurer"]:
                self.mtg.rafraichirAffichage(self)
                
#            self.app.statusBar.PopStatusText()
            self.app.GetEventHandler().ProcessEvent(Montage.MtgModifiedEvent(Montage.myEVT_MTG_MODIFIED))
            
            
    #################################################################################
    def OnContextMenu(self, event):
        if self.modeAnalyse:
            return
        if self.numElemProv is not None:
            self.Escape()
            return
        id = event.GetId()
#        x,y = event.m_x, event.m_y
        x, y = event.GetPosition()
        self.x,self.y = x,y
#        pos = self.mtg.elemProxim(x,y, self, exist = True)
        pos = self.posCourant
        elem = self.mtg.elemPos(pos)
        
        def propriete(event):
#            print 'SUPPR',pos
            self.app.Propriete(elem.num)
            
        def supprime(event):
#            print 'SUPPR',pos
            self.mtg.supprimerElem(pos)
            self.mtg.rafraichirAffichage(self)
            
#            self.InitBuffer()
        
        def changetaille(event):
#            print 'CHANGE_T',elem
            self.mtg.testerChangerTailleElem(self.app, elem)
            self.mtg.rafraichirAffichage(self)
            
            
        def changersens(event):
            self.mtg.testerInverserSensElem(self.app, elem)
            self.mtg.rafraichirAffichage(self)
            
            
        def changerelemroul(event):
            self.mtg.changerElemRoul(elem)
            self.mtg.rafraichirAffichage(self)
            
            
        def changertype(event):
            win = FenPrincipale.FenChoixElemPopup(self, elem, self.mtg )
#            btn = event.GetEventObject()
#            pos = self.ClientToScreen( (0,0) )
            sz =  self.GetScreenPosition()
            win.Position((sz[0]+self.x,sz[1]+self.y),(0,0))
#            win.Position((self.x, self.y),(0,0))
            win.disableInterdits(pos)
            win.Popup()
            
            
            
        if not hasattr(self, "menuexist"):
            self.menuexist = True
        self.Bind(wx.EVT_MENU, propriete, id = 100)
        self.Bind(wx.EVT_MENU, propriete, id = 1001)
        self.Bind(wx.EVT_MENU, supprime, id = 101)
        self.Bind(wx.EVT_MENU, changersens, id = 102)
        self.Bind(wx.EVT_MENU, changetaille, id = 103)
        self.Bind(wx.EVT_MENU, changerelemroul, id = 104)
        self.Bind(wx.EVT_MENU, changertype, id = 105)
        
        if pos is not None:
            menu =  MenuContextuel(x, y, pos, self.mtg)
            self.PopupMenu(menu)
            menu.Destroy()
            
    def  LstItemSousPointeur(self, pt):
        lst = []
#        print "Point écran :",pt
#        pt = self.CalcUnscrolledPosition(pt)
#        print "point ZoneVirt :",pt
        for i in self.lstItemMtg:
            rect = wx.Rect(i.pos[0], i.pos[1], i.GetWidth(), i.GetHeight())
            if rect.Contains(pt) and i.GetImg().img.GetAlpha(pt[0]-i.pos[0], pt[1]-i.pos[1]) <> 0:
                lst.append(i)
        lst.reverse()
        return lst
        
    #############################################################################
    def creerElemProv(self, num):
        "Création d'un élément provisoire et de son item"
##        print u"Création d'un élément",num
##        if self.elemProv.num is not None:
##            self.barreElements.deverouille(self.elemProv.num)
##            self.barreElements.listeBouton[self.elemProv.num].configure(relief = RAISED)

        
        self.delete("Chaine")
        self.numElemProv = num     #instanciation Elément PROVISOIRE
        self.master.changerCurseur(num)
##        self.barreElements.activer_desactiverBoutonPG(0)
##
##        self.barreElements.listeBouton[num].configure(relief = SUNKEN)
##        
##        self.zoneMessage.afficher('FaireGliss')
      

##############################################################################
#    Point géométrique     #
##############################################################################
class Point:

    def __init__(self, zone, point = None):
        self.zone = zone
        if point is not None:
            self.copier(point)
        else:
            self.x = zone.milieuX
            self.y = zone.milieuY

    def __repr__(self):
        return "("+str(self.x)+","+str(self.y)+")"

    def dim2y(self, dim, bague):
        if bague == "Al":
            if dim == 0:
                return 160
            elif dim == 1:
                return 148
            elif dim == 2:
                return 130
        else:
            if dim == 0:
                return 50
            elif dim == 1:
                return 56
            elif dim == 2:
                return 65

    def copier(self,point):
        self.x = point.x
        self.y = point.y

    def bordElem(self, mtg, pos, dim, bague, sgnHautBas = 1, cote = "E"):
        if pos.typelem == "A":
            if pos.cotelem == "G":
                sgnCotelem = -1
            else:
                sgnCotelem = 1
                
            if cote == 'I':
                self.x = self.zone.milieuPalier[pos.palier] \
                         + sgnCotelem * mtg.palier[pos.palier].rlt.imagePlus[0].img.size[0]/2
            else:
                self.x = self.zone.milieuPalier[pos.palier] \
                         + sgnCotelem * (mtg.palier[pos.palier].rlt.imagePlus[0].img.size[0]/2 \
                                         +mtg.elemPos(pos).imagePlus[0].img.size[0])

            self.y = self.zone.milieuY + sgnHautBas * self.dim2y(dim,bague)
            
        else:
            if cote == 'I':
                sgn = 1
            else:
                sgn = -1
            self.x = self.zone.milieuPalier[pos.palier] + sgn * mtg.palier[pos.palier].rlt.imagePlus[0].img.size[0]/2
            if bague == "Al":
                self.y = self.zone.milieuY + sgnHautBas * mtg.palier[pos.palier].rlt.imagePlus[0].img.size[1]/2
            else:
                if mtg.palier[pos.palier].taille == "G":
                    self.y = self.zone.milieuY + sgnHautBas * 60
                else:
                    self.y = self.zone.milieuY + sgnHautBas * 50


#    def centreElem(mtg,pos,dim,sgnHautBas,bague,cote = "E"):
#        if pos.typelem == "A":
#            if pos.cotelem == "G":
#                sgnCotelem = -1
#            else:
#                sgnCotelem = 1
#            if cote == 'I':
#                self.x = zone.milieuPalier[pos.palier] \
#                         + sgnCotelem * mtg.palier[pos.palier].rlt.imagePlus[0].img.size[0]/2
#            else:
#                self.x = zone.milieuPalier[pos.palier] \
#                         + sgnCotelem * (mtg.palier[pos.palier].rlt.imagePlus[0].img.size[0]/2 \
#                                         +mtg.elemPos(pos).imagePlus[0].img.size[0])
#            self.y = zone.milieuY + sgnHautBas * dim2y(dim,bague)
#        else:
#            if cote == 'I':
#                sgn = 1
#            else:
#                sgn = -1
#            self.x = zone.milieuPalier[pos.palier] + sgn * mtg.palier[pos.palier].rlt.imagePlus[0].img.size[0]/2
#            if bague == "Al":
#                self.y = zone.milieuY + sgnHautBas * mtg.palier[pos.palier].rlt.imagePlus[1].img.size[0]/2
#            else:
#                if mtg.palier[pos.palier].taille == "G":
#                    self.y = zone.milieuY + sgnHautBas * 60
#                else:
#                    self.y = zone.milieuY + sgnHautBas * 50



                
##############################################################################
#    Ligne de points géométrique     #
##############################################################################
class Ligne:

    def __init__(self):
        self.lst = []
        

    def lgn2lst(self):
        lst = []
        for i in self.lst:
            lst.append(i.x)
            lst.append(i.y)
        return lst

    def trierX(self):
        self.quicksort()
            
    def ajouter(self,point):
        p = Point(point.zone, point)
        self.lst.append(p)

    def partition(self, start, end, compare):
        while start < end:
        # au début de cette boucle, notre élément permettant la partition 
        # est à la valeur 'start'
            while start < end:
                if compare(self.lst[start].x, self.lst[end].x):
                    (self.lst[start], self.lst[end]) = (self.lst[end], self.lst[start])
                    break
                end = end - 1
        # au début de cette boucle, notre élément permettant la partition 
        # est à la valeur 'end'
            while start < end:
                if compare(self.lst[start].x, self.lst[end].x):
                    (self.lst[start], self.lst[end]) = (self.lst[end], self.lst[start])
                    break
                start = start + 1
        return start
 
    def quicksort(self, compare=lambda x, y: x > y, start=None, end=None):
        """Le plus rapide des tris par échanges pour la plupart des usages."""
        if start is None: start = 0
        if end is None: end = len(self.lst)
        if start < end:
            i = self.partition(start, end-1, compare)
            self.quicksort(compare, start, i)
            self.quicksort(compare, i+1, end)

    def permuterHautBas(self):
        for i in self.lst:
            i.y = 2 * i.zone.milieuY - i.y





#############################################################################
#       Menu Contextuel         #
#############################################################################
class MenuContextuel(wx.Menu):
    def __init__(self, x,y, pos, mtg):
        """Popup right-click menu of special parameter operations"""
        
        wx.Menu.__init__(self)
        if pos.typelem is not None:
            self.elem = mtg.elemPos(pos)
            if self.elem.num is not None:
#                print "Menu Contextuel :",pos,self.elem.taille
#                print "   elem:",self.elem.num
                self.mtg = mtg
                
                titre = wx.MenuItem(self,100,self.elem.nom, u"Afficher les propriétés de l'élément")
                if 'wxMSW' in wx.PlatformInfo:
                    font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
                    font.SetWeight(wx.BOLD)
                    titre.SetFont(font)
                    titre.SetTextColour("blue")
                self.AppendItem(titre)
#                titre.Check(False)
#                titre.Enable(False)
                self.AppendSeparator()
                
                self.Append(101,u"Supprimer", u"Supprimer définitivement cet élément du montage")
                
#                self.menu.add_command(label   = self.elem.nom,
#                                        font = Const.Font_TitreBulle[0],
#                                        foreground = Const.Font_TitreBulle[1],
#                                        activebackground = "SystemButtonFace",
#                                        activeforeground = Const.Font_TitreBulle[1])
#                self.menu.add_command(label   = "Supprimer", \
#                                        command = lambda arg = pos : self.supprimer(arg))
                if self.elem.type == "R":
                    if self.elem.estOblique():
                        self.Append(102,u"Inverser le sens", u"Inverser le sens (orientation) du roulement à contact oblique")
                
#                        self.menu.add_command(label   = "Inverser le sens", \
#                                              command = self.inverserSens)
                    self.Append(103,u"Changer la taille", u"Modifier la taille du roulement")

#                    self.menu.add_command(label   = "Changer la taille", \
#                                          command = self.changerTaille)
                    self.Append(104,u"Changer éléments roulants", u"Changer le type d'éléments roulants")

#                    self.menu.add_command(label   = "Changer éléments roulants", \
#                                          command = self.changerElemRoul)
                self.Append(105,u"Changer le type", u"Changer le type d'élément")

                self.AppendSeparator()
                self.Append(1001,u"Propriétés", u"Afficher les propriétés de l'élément")
                
#                self.menu.add_command(label   = "Changer le type", \
#                                      command = self.changerType) 
                    
#                self.menu.post(x,y)

#    #############################################################################
#    def changerType(self):
#        ChoixElement(self.mtg, self.elem)
#
#    #############################################################################
#    def inverserSens(self):
#        self.mtg.testerInverserSensElem(self.elem)
#
#    #############################################################################
#    def changerTaille(self):
#        self.mtg.testerChangerTailleElem(self.elem)
#
#    #############################################################################
#    def changerElemRoul(self):
#        self.mtg.changerElemRoul(self.elem)
#
#    #############################################################################
#    def supprimer(self,pos):
#        self.mtg.supprimerElem(pos)
        



##############################################################################
#############################################################################
#class ChoixElement(Toplevel):
#    def __init__(self, mtg, elem):
#        Toplevel.__init__(self,  bd = 2, relief = RIDGE)
#
#        Label(self, text = u"Choisir un type",
#              font = Const.Font_TitreBulle[0],
#              foreground = Const.Font_TitreBulle[1]) \
#              .grid()
#              
#        self.entry = Entry(self, width = '21')
#        
#        # Get the current y-coordinate of the Entry
#        self.yf = self.entry.winfo_pointery()
#
#        # Get the current x-coordinate of the cursor
#        self.xf = self.entry.winfo_pointerx()
#        
###        self.parent = parent
#        self.mtg = mtg
#        self.elem = elem
#        self.withdraw()
#        self.overrideredirect(1)
#        self.transient()
#        self.focus_set()
#        self.grab_set()
#
#        self.tipwidth = 0
#        self.tipheight = 0
#
#        self.imageBouton = []
#
#        # Selection de la bonne liste     
#        if elem.type == "R":
#            numFam = 0
#        elif elem.type == "A":
#            numFam = 1
#        elif elem.type == "J":
#            numFam = 2
#
#        lst = BarreElem.listeFamilles[numFam].lst
#        
#        if elem.type == "R":
#            if elem.num in lst[0].lst:
#                lst = lst[0].lst
#            else:
#                lst = lst[1].lst
#
#
#        l,c = 1,0
#        for num in lst:
#            
#            # Calcul de la position dans la grille
#            if l>=4:
#                l = 1
#                c+=1
#
#            # Création du bouton
#            bouton = Button(self, relief = RAISED,
#                            command = lambda arg = num : self.selectionnerElem(arg))
#            bouton.image = ImageTk.PhotoImage(Images.BoutonsElem[num])
#            bouton['image'] = bouton.image                
#            bouton.grid(row = l+1, column = c, \
#                        padx = 2, pady = 2)
#            l += 1
#       
#        self.bind('<Leave>',self.efface)
#        self.bind_all("<Escape>", self.efface, "+")
#        
#        self.affiche()
#
#
#    ################################################################################
#    def affiche(self):
#        self.update_idletasks()
#        
#        self.tipwidth = self.winfo_width()
#        self.tipheight =  self.winfo_height()
#
#        if self.yf + self.tipheight > self.winfo_screenheight() - 25:
#            self.yf = self.winfo_screenheight() - self.tipheight - 25
#
#        
#        self.geometry('+%d+%d'%(self.xf,self.yf))
#        self.deiconify()
#
#
#    ################################################################################
#    def efface(self,event = None):
###        print "sortie"
###        self.withdraw()
#        
#        if event == None or event.widget.winfo_class() == "Toplevel":
#            self.destroy()
###        self.quit()
###        self.parent.after_cancel(self.action)
#
#
#    #################################################################################
#    def selectionnerElem(self, num):
#        self.efface()
#        self.mtg.testerChangerTypeElem(self.elem, num)




class DCPlus(wx.MemoryDC):
    def __init__(self, *args, **kwargs ):
        wx.MemoryDC.__init__(self, *args, **kwargs)
    
    def DrawLinesArrow(self, lstpoint, taille = 0, style = 3, tanF = 0.5):
        nbPt = len(lstpoint)
        pen = self.GetPen()
        brush = self.GetBrush()
        ep = pen.GetWidth()
        lf = (taille+ep/2)/tanF
#        print "ep =",ep, "lf =", lf
        
        def SinCos(pt1, pt2):
            h = ((pt2.y-pt1.y)**2+(pt2.x-pt1.x)**2)**0.5
            s = (pt2.y-pt1.y)/h
            c = (pt2.x-pt1.x)/h
            return s,c
        
        def LocToGlob(org, pt, s, c):
            pt2 = wx.Point(0,0)
            pt2.x = org.x+c*pt.x-s*pt.y
            pt2.y = org.y+s*pt.x+c*pt.y
#            print pt2.x, pt2.y
            return pt2
        
        if style&1:
            sinA, cosA = SinCos(lstpoint[0], lstpoint[1])
#            print "sinA =", sinA, "cosA =", cosA
#            print lstpoint[0].x,lstpoint[0].y
#            lstpoint[0] = LocToGlob(lstpoint[0], wx.Point(-ep/2, 0), sinA, cosA)
            fl1 = [lstpoint[0], 
                   LocToGlob(lstpoint[0], wx.Point(lf,  taille+ep/2), sinA, cosA),
                   LocToGlob(lstpoint[0], wx.Point(lf, -taille-ep/2), sinA, cosA),
                   lstpoint[0]]
            self.SetPen(wx.Pen(pen.GetColour(), 1))
            self.SetBrush(wx.Brush(pen.GetColour()))
            self.DrawPolygon(fl1)
            self.SetPen(pen)
            self.SetBrush(brush)
            lstpoint[0] = LocToGlob(lstpoint[0], wx.Point(lf, 0), sinA, cosA)

        if style&2:
            sinB, cosB = SinCos(lstpoint[nbPt-1], lstpoint[nbPt-2])
#            print "sinB =", sinB, "cosB =", cosB
#            print lstpoint[nbPt-1].x,lstpoint[nbPt-1].y
#            lstpoint[nbPt-1] = LocToGlob(lstpoint[nbPt-1], wx.Point(-ep/2, 0), sinB, cosB)
            fl2 = [lstpoint[nbPt-1], 
                   LocToGlob(lstpoint[nbPt-1], wx.Point(lf,  taille+ep/2), sinB, cosB),
                   LocToGlob(lstpoint[nbPt-1], wx.Point(lf,  -taille-ep/2), sinB, cosB),
                   lstpoint[nbPt-1]]
            self.SetPen(wx.Pen(pen.GetColour(), 1))
            self.SetBrush(wx.Brush(pen.GetColour()))
            self.DrawPolygon(fl2)
            self.SetPen(pen)
            self.SetBrush(brush)
            lstpoint[nbPt-1] = LocToGlob(lstpoint[nbPt-1], wx.Point(lf, 0), sinB, cosB)
            
        self.DrawLines(lstpoint)

    def DrawLineArrow(self, x1, y1, x2, y2, taille = 0, style = 3, tanF = 0.5):
        lstPt = [wx.Point(x1,y1), wx.Point(x2,y2)]
        self.DrawLinesArrow(lstPt, taille, style, tanF)


        

   
        
