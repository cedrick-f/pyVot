#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##This file is part of PyVot
#############################################################################
#############################################################################
##                                                                         ##
##                               Elements                                   ##
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


#import Image, ImageTk, GifImagePlugin, PngImagePlugin, ImageFilter, ImageGrab
from Images import imageElem #,ImagePlus
#import Const
import Affichage
import wx  
import  wx.lib.popupctl as  pop

#############################################################################
# Liste des éléments
#############################################################################
listeElements = {0 : {'nom'  : u'Roulement à billes à contact radial',
                      'type' : 'R',
                      'chargeAdm' : {"radial"  : 2,
                                     "axial"   : 2,
                                     "combi"   : 2},
                      'cout'  : 10},
                 1 : {'nom'  : u'Roulement à billes à contact oblique',
                      'type' : 'R',
                      'chargeAdm' : {"radial"  : 2,
                                      "axial"   : 2,
                                      "combi"   : 3},
                      'orientation' : None,
                      'cout' : 12},
                 2 : {'nom'  : u'Roulement à rotule sur billes',
                      'type' : 'R',
                      'chargeAdm' : {"radial"  : 2,
                                      "axial"   : 1,
                                      "combi"   : 1},
                      'cout' : 24},
                 3 : {'nom'  : u'Butée à billes simple effet',
                      'type' : 'R',
                      'chargeAdm' : {"radial"  : 0,
                                      "axial"   : 3,
                                      "combi"   : 0},
                      'orientation' : None,
                      'cout' : 14},
                 4 : {'nom'  : u'Roulement à rouleaux cylindriques',
                      'type' : 'R',
                      'chargeAdm' : {"radial"  : 3,
                                      "axial"   : 0,
                                      "combi"   : 0},
                      'dimension' : 2,
                      'cout' : 14},
                 5 : {'nom'  : u'Roulement à rouleaux coniques',
                      'type' : 'R',
                      'chargeAdm' : {"radial"  : 3,
                                      "axial"   : 3,
                                      "combi"   : 4},
                      'orientation' : None,
                      'dimension' : 4,
                      'cout' : 16},
                 6 : {'nom' : u'Roulement à rotule sur rouleaux',
                      'type': 'R',
                      'chargeAdm' : {"radial"  : 4,
                                      "axial"   : 2,
                                      "combi"   : 4},
                      'cout' : 26},
                 7 : {'nom'  : u'Butée à rouleaux simple effet',
                      'type' : 'R',
                      'chargeAdm' : {"radial"  : 0,
                                      "axial"   : 4,
                                      "combi"   : 0},
                      'orientation' : None,
                      'cout' : 18},
                 8 : {'nom'  : u'Butée à billes double effet',
                      'type' : 'R',
                      'chargeAdm' : {"radial"  : 0,
                                      "axial"   : 3,
                                      "combi"   : 0},
                      'cout' : 20},
                 9 : {'nom'  : u'Butée à rouleaux double effet',
                      'type' : 'R',
                      'chargeAdm' : {"radial"  : 0,
                                      "axial"   : 4,
                                      "combi"   : 0},
                      'cout' : 28},
                 10: {'nom'  : u'Roulement à 2 rangées de billes à contact oblique',
                      'type' : 'R',
                      'chargeAdm' : {"radial"  : 4,
                                      "axial"   : 2,
                                      "combi"   : 4},
                      'cout' : 20},
                 11: {'nom'  : u'Roulement à 2 rangées de rouleaux coniques',
                      'type' : 'R',
                      'chargeAdm' : {"radial"  : 5,
                                      "axial"   : 3,
                                      "combi"   : 5},
                      'cout' : 30},
                 
                 100 : {'nom'  : u'Eléments filetés',
                        'type' : 'A',
                        'pos'  : 'E', 
                        'chargeAdm' : {"axial" : 7},
                        'cout' : 10},
                 101 : {'nom'  : u'Anneau élastique',
                        'type' : 'A',
                        'pos'  : 'IE',
                        'chargeAdm' : {"axial" : 1},
                        'cout' : 2},
                 102 : {'nom'  : u'Epaulement',
                        'type' : 'A',
                        'pos'  : 'IE',
                        'chargeAdm' : {"axial" : 8},
                        'cout' : 1},
                 103 : {'nom'  : u'Entretoise',
                        'type' : 'A',
                        'pos'  : 'I',
                        'chargeAdm' : {"axial" : 8},
                        'cout' : 2},
                 

                 200 : {'nom'  : u'Joint à une lèvre',
                        'type' : 'J',
                        'pos'  : ['Ar'],
                        'pressAdm' : {"Ar" : 2},
                        'vittAdm'  : 8,
                        'facteurPV' : 8,
                        'cout' : 4},
                 201 : {'nom'  : u'Joint torique',
                        'type' : 'J',
                        'pos'  : ['Al','Ar'],
                        'pressAdm' : {"Ar" : 8,
                                      "Al" : 10},
                        'vittAdm'  : 1,
                        'facteurPV' : 5,
                        'cout' : 2},
                 202 : {'nom'  : u'Chapeau',
                        'type' : 'J',
                        'pos'  : ['Ar'],
                        'pressAdm' : {"Ar" : 10},
                        'vittAdm'  : 10,
                        'facteurPV' : 10,
                        'cout' : 0},
                 203 : {'nom'  : u'Chicanes',
                        'type' : 'J',
                        'pos'  : ['Ar'],
                        'pressAdm' : {"Ar" : 0},
                        'vittAdm'  : 10,
                        'facteurPV' : 0,
                        'cout' : 3},
                 204 : {'nom'  : u'Joint plat',
                        'type' : 'J',
                        'pos'  : ['Al'],
                        'pressAdm' : {"Al" : 10},
                        'vittAdm'  : 10,
                        'facteurPV' : 0,
                        'cout' : 2}
                 }

def dictCopy(dic):
    newDic = {}
    for k,v in dic.items():
        if type(v) == str or type(v) == unicode or type(v) == int:
            newDic[k] = v
        elif type(v) == list:
            newDic[k] = listCopy(v)
        elif type(v) == dict:
            newDic[k] = dictCopy(v)
        else:
            newDic[k] = v
    return newDic

def listCopy(lst):
    newLst = []
    for v in lst:
        newLst.append(v)
    return newLst

#############################################################################
# Classement des éléments
#############################################################################
listeFamilles = [
                         [u'Roulements', [[u'à billes',  [0,1,10,2,3,8]],
                                          [u'à rouleaux',[4,5,11,6,7,9]]]
                         ],
                         [u'Arrêts',range(100,104)],
                         [u'Joints',range(200,205)]
                        ]

listeIconesFamilles = []

#############################################################################
# Label Taille
#############################################################################
taille = {"P" : "Petit",
          "G" : "Grand"}

#############################################################################
#  Fonctions
#############################################################################

def coefTaille(param, numElem, taille):
    
##    if taille == '':
##        taille = self.taille
        
    if taille == "G" \
       and not numElem in [100,102,103]:#['nom'] in [u'Epaulement',u'Entretoise']:
        return param * 2
    else:
        return param
        

#############################################################################        
#############################################################################
#                   #
#      Elément      #
#                   #
#############################################################################
#############################################################################
class Element:
    "Classe définissant un Element d'une liaison pivot"
    
    def __init__(self, num = None, taille = "P", orientation = '', pos = None):
        self.num = num
        self.pos = pos
        self.taille = taille
#        print "Init elem :", num, taille, orientation
        if hasattr(self,"item"):
            for i in self.item.values():
                i.efface()
        else:
            self.item = {}

        
##        print u">Initialisation élément",num
        if num <> None:
            self.nom = listeElements[num]['nom']
            self.type = listeElements[num]['type']
            if self.type == "J":
                self.pressAdm = listeElements[num]['pressAdm']
                self.vittAdm = listeElements[num]['vittAdm']
                self.facteurPV = listeElements[num]['facteurPV']
            else:
                self.chargeAdm = listeElements[num]['chargeAdm']
            self.cout = listeElements[num]['cout']
            
            try:
                self.orientation = listeElements[num]['orientation']
                self.orientation = orientation
            except:
#                print "Pas d'orientation !!"
                pass
            
            try:
                self.dimension = listeElements[num]['dimension']
            except:
                pass
            
        else:
            return



##        self.imageB = ImageTk.PhotoImage(CurseurElem[num])

    def Cout(self):
        if self.taille == "G":
            if self.type == "R":
                return self.cout*2
            elif self.type == "A" or self.type == "J":
                return self.cout*3/2
        else:
            return self.cout

    def AfficheDansArbre(self):
        return self.nom
        
    #############################################################################
    def estAffiche(self):
        if 'imag' in self.item:
            return self.item['imag'].estAffiche
        return False
            
    #############################################################################
    def efface(self):
        for i in self.item.values():
            i.efface()


    #############################################################################
    def definirImages(self, mtg, zoneMtg, taille,  pos = None):
        """ Détermine toutes les images susceptibles de servir
            pour l'élément, suivant sa position et sa taille,
            sous forme d'item.
            --> self.item : dic de ItemElem
            --> self.taille
           
        """
#        print type(pos)
        # Classe d'item d'élément
        def itemElem(clef):
            return Affichage.ItemElem(zoneMtg, mtg, clef)

##        print "Definition images pour ",self.type, pos

        if self.num == None or pos == None:
##            print "Pas d'image !!"
            return
##        print pos
        
        ##  (Re)Initialisation des images de l'élément   ##############################
        self.item = {}

        
        ##   Affectation de la Taille   #############################################
        if self.type == "R":
            self.taille = taille
        else:
            if self.estEntretoise() \
               and mtg.palier[pos.palier].taille <> mtg.palier[pos.opposee().palier].taille:
                if pos.radiale == "Ar":
                    self.taille = "G"
                else:
                    self.taille = "P"
            else:
                self.taille = mtg.palier[pos.palier].taille
##        print "...taille affectée :",self.taille


        ## >>> Cas général (roulements non séparables) --> 'imag'
        #--------------------------------------------------------
        clefImg = str(self.num) + self.taille
        if clefImg in imageElem.keys():
            self.item['imag'] = itemElem(clefImg)
            if pos.cotelem == "D" and self.estOblique():
                self.item['imag'].inverser()

        
        ## >>> Cas des roulements à bagues séparables --> 'imag' et 'imagAr'
        #-------------------------------------------------------------------
        if self.type == "R":
            if clefImg + "Al" in imageElem.keys():
                self.item['imag'] = itemElem(clefImg + "Al")
                self.item['imagAr'] = itemElem(clefImg + "Ar")
#                print type(pos.cotelem)
                if pos.cotelem == "D" and self.estOblique():
                    self.item['imag'].inverser()
                    self.item['imagAr'].inverser()

       
        # >>> Cas des Arrets et Joints --> 'imag'
        #----------------------------------------
        else:
            clefImg = clefImg + pos.radiale
            if clefImg in imageElem.keys():
                self.item['imag'] = itemElem(clefImg)

            # >>> Cas des Arrets
            if self.type == "A":
                if pos.interieur():
                    if clefImg + "I" in imageElem.keys():
                        self.item['imag'] = itemElem(clefImg + "I")
                else:
                    if clefImg + "E" in imageElem.keys():
                        self.item['imag'] = itemElem(clefImg + "E")

                ## >>> cas des entretoises --> 'opp' et 'rond'
                #---------------------------------------------
                if self.estEntretoise():
                    self.item['opp'] = itemElem(clefImg)
                    self.item['opp'].inverser()
                    if clefImg + "R" in imageElem.keys():
                        self.item['rond'] = itemElem(clefImg+"R")

                ## >>> cas des emplacements vides --> 'vide'
                #-------------------------------------------
                if clefImg + "V" in imageElem.keys():
#                    if pos.cotelem == "D":
#                        inverser = True
#                    else:
#                        inverser = False
                    self.item['imag'].imagVide(clefImg+"V")
                    
#                    self.item['vide'] = itemElem(clefImg+"V")
            
                ## >>> cas des épaulement intérieurs --> 'opp'
                #---------------------------------------------
                if self.estEpaulement() and pos.interieur():
                    self.item['opp'] = itemElem(clefImg + "I")
#                    self.item['opp'].img = self.item['imag'].img.copie()
                    self.item['opp'].inverser()

                ## >>> cas des entretoises pour butee double effet --> 'supp'
                #------------------------------------------------------------
                if not self.estEpaulement() and not self.estEntretoise():
                    self.item['supp'] = itemElem("89" + self.taille)

                ## >>> cas des arrets nécessitant un support (chapeau) --> 'supp'
                #----------------------------------------------------------------
                if self.estChapeau(pos):
                    self.item['supp'] = itemElem("Sup"+self.taille+"Al")
                    if "Sup"+self.taille+"Al" + "V" in imageElem.keys():
                        self.item['supp'].imagVide("Sup"+self.taille+"Al" + "V")

            # >>> Cas des Joints
            elif self.type == "J":
                if mtg.palier[pos.palier].arr["Ar"][pos.palier].estEcrou():
                    if clefImg + "P" in imageElem.keys():
                        self.item['imag'] = itemElem(clefImg + "P")
                if mtg.palier[pos.palier].arr["Ar"][pos.palier].estEpaulement():
                    if clefImg + "E" in imageElem.keys():
                        self.item['imag'] = itemElem(clefImg + "E")
                        
                ## >>> cas des joints nécessitant un support --> 'supp'
                #-------------------------------------------------------
                if mtg.palier[pos.palier].arr["Al"][pos.palier].num is None:
                    self.item['supp'] = itemElem("Sup"+self.taille+"Al")
                    if "Sup"+self.taille+"Al" + "V" in imageElem.keys():
                        self.item['supp'].imagVide("Sup"+self.taille+"Al" + "V")
                
                ## >>> cas des emplacements vides --> 'vide'
                #-------------------------------------------
                if clefImg + "V" in imageElem.keys():
#                    if pos.cotelem == "D":
#                        inverser = True
#                    else:
#                        inverser = False
                    self.item['imag'].imagVide(clefImg+"V")
                
            # Retournement des éléments coté 'droit'
            if pos.cotelem == "D":
                for i in self.item.values():
                    i.inverser()


##        # Réinitialisation du dictionnaire des items
##        for c in self.images.keys():
##            self.item[c] = None

            
##        print "Images de l'élément :",self.images.keys()

            

    #############################################################################
    def __repr__(self):
        if self.num is None:
##            if self.type == "R":
##                return "-"
##            else:
            return "---"
        else:
            if self.type == "R":
                ch = self.taille + str(self.num)
                if self.estOblique():
                    ch = ch + self.orientation
            else:
                ch = str(self.num)
            return ch


##    #############################################################################
##    def codeTag(self,pos):
##        "Renvoie un code comprenant la position et le numéro de l'élément"
##        return str(self.num)+pos.code()


    #############################################################################
    def doubler(self,pos):
        "Détermine si un arrêt doit être doublé ou pas"
        if pos is None:
            return False
        if self.estEntretoise() and pos.interieur():
            return True
##        if self.type =='A' and self.nom == "Epaulement":
##            if pos is not None \
##               and ((pos.palier == "G" and pos.cotelem == "D") \
##                    or (pos.palier == "D" and pos.cotelem == "G")):
##                return True
        return False


    #############################################################################
    def supporteEffortAxial(self,sens = 0, pos = None):
        "Détermine si un élément supporte un effort axial dans un sens"
#        print self,
        if self.num is None:
            return False
        if self.type == "A":
            if self.estEntretoise():
                return False
            elif self.chargeAdm["axial"] <> 0 \
                and (pos == None \
                or  (sens == 0 and pos.cotelem == "D" and pos.radiale == "Al") \
                or  (sens == 1 and pos.cotelem == "G" and pos.radiale == "Al") \
                or  (sens == 0 and pos.cotelem == "G" and pos.radiale == "Ar") \
                or  (sens == 1 and pos.cotelem == "D" and pos.radiale == "Ar")):
                return True
            else:
                return False
        
        if self.type == "R":
            if not self.estOblique():
#                print self.chargeAdm["axial"],
                if self.chargeAdm["axial"] <> 0:
                    return True
                else:
                    return False
            else:
                if sens == 0:
                    ss = "G"
                else:
                    ss = "D"
##                print u"ss = ",ss
##                print u"oblique = ",self.orientation
                if self.orientation == ss:
                    return True
                else:
                    return False
        return False


    #############################################################################
    def effortAxialSupporte(self):
        "Renvoi l'indice de charge axiale supportée"
        return self.coefTaille(self.chargeAdm["axial"])
       

    #############################################################################
    def coefTaille(self,param, taille = ''):
        if taille == '':
            taille = self.taille
        if taille == "G" and not self.nom in [u'Epaulement',u'Entretoise']:
            return param * 2
        else:
            return param
           

    #############################################################################
    def copier(self,elem):
        u"Copier un élément à une position <pos>"
        self.__init__(elem.num)
        if self.num is not None:
            self.item = elem.item.copy()
            self.type = elem.type
            self.pos = elem.pos.copie()
            self.taille = elem.taille
            self.cout = elem.cout
            if hasattr(elem, 'orientation'):
                self.orientation = elem.orientation
            if hasattr(elem, 'dimension'):
                self.dimension = elem.dimension


    #############################################################################
    def copy(self):
        "Renvoie la copie d'un élément"
        elem = Element(self.num)
        elem.copier(self)
##        if self.num is not None:
##            elem.images = self.images.copy()
##            elem.item = self.item.copy()
##            elem.type = self.type
##            elem.num = self.num
##            elem.pos = self.pos.copie()
##            elem.taille = self.taille
##            elem.cout = self.cout
##            if self.estOblique():
##                elem.orientation = self.orientation
##            if self.estSeparable():
##                elem.dimension = self.dimension

        return elem
    
    #############################################################################
    def estDefini(self):
        "Renvoie <True> si l'élément est défini"
        if self.num == None:
            return False
        else:
            return True


    #############################################################################
    def estEpaulement(self):
        "Renvoie <True> si l'élément est un épaulement"
        if self.num is not None:
            if self.type == "A" and self.nom == u"Epaulement":
                return True
        return False


    #############################################################################
    def estRltRoulConiques(self):
        "Renvoie <True> si l'élément est un roulements à rouleaux coniques"
        if self.num is not None:
            if self.type == "R" and self.nom == u'Roulement à rouleaux coniques':
                return True
        return False


    #############################################################################
    def estEntretoise(self):
        "Renvoie <True> si l'élément est une entretoise"
        if self.num is not None:
            if self.type == "A" and self.nom == u"Entretoise":
                return True
        return False


    #############################################################################
    def estEcrou(self):
        if self.num is not None:
            if self.type == "A" and self.nom == u'Eléments filetés' \
               and self.pos.radiale == "Ar":
                return True
        return False


    #############################################################################
    def estChapeau(self, pos = None):
        if self.num is not None:
            if pos is None:
                pos = self.pos
            if pos == None:
                return False
            if self.type == "A" and self.num == 100 \
               and pos.radiale == "Al":
                return True
        return False

    #############################################################################
    def estJointChapeau(self, pos = None):
        if self.num is not None:
            if pos is None:
                pos = self.pos
            if self.num == 202 \
               and pos.radiale == "Ar":
                return True
        return False
        
    def estJoint(self):
        if self.num == None:
            return False
        if self.num >= 200:
            return True
        else:
            return False
        
    def necessiteChapeauCentre(self):
        if self.num == None:
            return False
        if self.num in [200, 201, 203] and self.pos.radiale == "Ar":
            return True
        return False
    
    #############################################################################
    def estSeparable(self):
        "Renvoie <True> si l'élément est à bagues séparables"
        if self.num is not None:
            if self.type == "R" and self.nom in [u'Roulement à rouleaux coniques', \
                                                 u'Roulement à rouleaux cylindriques']:
                return True
        return False


    #############################################################################
    def estSeparableSens(self,sens,bague):
        "Renvoie <True> si la <bague> du roulement est séparable dans le sens <sens>"
        if self.estSeparable():
            if not self.estOblique():
                return True
            if  ((self.orientation == "G" and sens == 1 and bague == "Ar") \
              or (self.orientation == "G" and sens == 0 and bague == "Al") \
              or (self.orientation == "D" and sens == 0 and bague == "Ar") \
              or (self.orientation == "D" and sens == 1 and bague == "Al")):
                return True
        return False
    

    #############################################################################
    def estOblique(self):
        "Renvoie <True> si l'élément est à contact oblique"
        if self.num is not None:
            if self.type == "R" and self.num in [1,3,5,7]:# in [u'Roulement à billes à contact oblique', \
#                                                 u'Roulement à rouleaux coniques', \
#                                                 u'Butée à billes simple effet', \
#                                                 u'Butée à rouleaux simple effet']:
                return True
        return False
    

    #############################################################################
    def estButee(self):
        "Renvoie <True> si l'élément est une butée"
        if self.num is not None:
            if self.type == "R" and self.nom in [u'Butée à billes simple effet', \
                                                 u'Butée à rouleaux simple effet']:
                return True
        return False

    #############################################################################
    def estButeeDbl(self):
        "Renvoie <True> si l'élément est une butée double"
        if self.num is not None:
            if self.type == "R" and self.num in [8,9]:
                return True
        return False

    #############################################################################
    def pasDemontable(self, unSeulRlt, pos = None):
        u"Renvoie <True> si l'élément n'est pas démontable"

        # Pas d'élément
        if self.num == None:
            return False

        # Elément a priori démontable
        if self.nom in [u"Entretoise", u"Anneau élastique", u'Eléments filetés']:
            if pos is not None and pos.interieur():
                if not unSeulRlt:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return True


    #############################################################################
    def profondeur(self):
        """Renvoie la profondeur relative à laquelle doit être affiché l'élément"""
        if self.estEpaulement():
            if self.pos.radiale == "Al":
                if self.taille == "P":
                    return 0
                else:
                    return 2
            else:
                if self.taille == "G":
                    return 0
                else:
                    return 2

    def ajout_tag(self,tag):
        self.canvas(tag, self.id)
  

    #############################################################################
    def dimensions(self, radiale, int_ext, taille = None):
        """Renvoie les dimensions de l'élément
            radiale : coté arbre ou alésage
            int_ext : vue de l'extérieur ou de l'intérieur
            """

        # Format
        dimension = {'entier' : 0,
                     'demonte' : 0}

        # Coefficient de taille
        if taille is None and self.num <> None:
            taille = self.taille
        elif self.estEntretoise() and radiale == "Ar":
            taille = self.taille 
        if taille == "P":
            t = 0
        else:
            t = 1

        # Dimension de base logements intérieure/extérieure
        if radiale == "Al":
            l = 5
        else:
            l = 0

        # Coefficient de prise en compte de la dimension de base
        if int_ext == "I" and radiale == "Al":
            s = -1
        elif int_ext == "E" and radiale == "Ar":
            s = 1
        else:
            s = 0
        
        # S'il n'y a pas d'élément ==> dimension de l'arbre ou alésage
        if self.num == None:
            dimension['entier'] = t + l
            dimension['demonte'] = dimension['entier']
            return dimension

        
        # Cas des arrets
        if self.type == "A":

            # Dimension relative de base arret
            if self.estEcrou():
                a = 3
            elif self.estEntretoise() and self.taille <> taille:
                a = 2
            else:
                a = 1

            dimension['demonte'] = t + l
            dimension['entier'] = dimension['demonte'] + s * a
            return dimension

        # Cas des roulements
        elif self.type == "R":
            # Dimension de base bague intérieure/extérieure
            if int_ext == "I":
                r = 0
            else:
                r = 5

            dimension['entier'] = t + r

            # Cas de roulements séparables
            if self.estSeparable():
                if self.nom == u'Roulement à rouleaux coniques':
                    if int_ext == "I" and radiale == "Al":
                        r = 3
                    elif int_ext == "E" and radiale == "Ar":
                        r = 4
                else:
                    if int_ext == "I" and radiale == "Al":
                        r = 2
                    elif int_ext == "E" and radiale == "Ar":
                        r = 2
            
            dimension['demonte'] = t + r

            return dimension
            
##       
    #############################################################################
    def inverserSens(self):
        u"Change le sens du roulement"
##        print "Change le sens du roulement"
        if self.orientation == "D":
            self.orientation = "G"
            self.pos.cotelem = "G"
        else:
            self.orientation = "D"
            self.pos.cotelem = "D"
         

    #############################################################################
    def sensOppose(self):
        "Renvoie le sens opposé de l'élément"
        if self.orientation == "D":
            return "G"
        else:
            return "D"

    def largeur(self):
        return self.item['imag'].largeur()


#class PopupPropriete(pop.PopupControl):
#    def __init__(self, parent, num):
#        pop.PopupControl.__init__(self, parent)
#
#        self.win = Propriete(parent, num)
#        
##        bz = self.win.GetBestSize()
##        self.win.SetSize(bz)
#
#        # This method is needed to set the contents that will be displayed
#        # in the popup
#        self.SetPopupContent(self.win)


####################################################################################################
class Propriete(wx.Dialog):
    def __init__(
            self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE,
            num = None, useMetal=False,
            ):
        
        element = Element(num)
        
        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size, style)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
        self.PostCreate(pre)

        # This extra style can be set after the UI object has been created.
        if 'wxMac' in wx.PlatformInfo and useMetal:
            self.SetExtraStyle(wx.DIALOG_EX_METAL)


        # Now continue with the normal construction of the dialog
        # contents
        sizer = wx.GridBagSizer()
        
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetWeight(wx.BOLD)
        self.SetFont(font)
        self.SetForegroundColour(wx.BLUE)
        
        label = wx.StaticText(self, -1, element.nom)
        sizer.Add(label, (0,0), (1,4), flag = wx.ALIGN_CENTRE|wx.ALL, border = 5)
        
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        self.SetFont(font)
        self.SetForegroundColour(wx.BLACK)
        

        label = wx.StaticText(self, -1, u"petit")
        sizer.Add(label, (1,1), flag = wx.ALIGN_CENTRE|wx.ALL, border = 5)
        label = wx.StaticText(self, -1, u"grand")
        sizer.Add(label, (1,2), flag = wx.ALIGN_CENTRE|wx.ALL, border = 5)
        l = 2

        if element.type == "R":
            font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            font.SetWeight(wx.BOLD)
            self.SetFont(font)
            self.SetForegroundColour(wx.BLACK)
            
            label = wx.StaticText(self, -1, u"Charge admissible :")
            sizer.Add(label, (l,0), flag = wx.ALIGN_RIGHT|wx.ALL, border = 5)
            
            font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            self.SetFont(font)
            self.SetForegroundColour(wx.BLACK)
        
            l += 1
            label = wx.StaticText(self, -1, u"Radiale :")
            sizer.Add(label, (l,0), flag = wx.ALIGN_RIGHT|wx.ALL, border = 5)
            label = wx.StaticText(self, -1, str(element.chargeAdm["radial"]))
            sizer.Add(label, (l,1), flag = wx.ALIGN_CENTRE|wx.ALL, border = 5)
            label = wx.StaticText(self, -1, str(coefTaille(element.chargeAdm["radial"], num, "G")))
            sizer.Add(label, (l,2), flag = wx.ALIGN_CENTRE|wx.ALL, border = 5)
            
            l += 1
            label = wx.StaticText(self, -1, u"Axiale :")
            sizer.Add(label, (l,0), flag = wx.ALIGN_RIGHT|wx.ALL, border = 5)
            label = wx.StaticText(self, -1, str(element.chargeAdm["axial"]))
            sizer.Add(label, (l,1), flag = wx.ALIGN_CENTRE|wx.ALL, border = 5)
            label = wx.StaticText(self, -1, str(coefTaille(element.chargeAdm["axial"], num, "G")))
            sizer.Add(label, (l,2), flag = wx.ALIGN_CENTRE|wx.ALL, border = 5)
            
            l += 1
            label = wx.StaticText(self, -1, u"Combinée :")
            sizer.Add(label, (l,0), flag = wx.ALIGN_RIGHT|wx.ALL, border = 5)
            label = wx.StaticText(self, -1, str(element.chargeAdm["combi"]))
            sizer.Add(label, (l,1), flag = wx.ALIGN_CENTRE|wx.ALL, border = 5)
            label = wx.StaticText(self, -1, str(coefTaille(element.chargeAdm["combi"], num, "G")))
            sizer.Add(label, (l,2), flag = wx.ALIGN_CENTRE|wx.ALL, border = 5)
            
            
            font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            font.SetWeight(wx.BOLD)
            self.SetFont(font)
            self.SetForegroundColour(wx.BLACK)

        elif element.type == "A":
            font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            font.SetWeight(wx.BOLD)
            self.SetFont(font)
            self.SetForegroundColour(wx.BLACK)
            
            label = wx.StaticText(self, -1, u"Charge axiale admissible :")
            sizer.Add(label, (l,0), flag = wx.ALIGN_RIGHT|wx.ALL, border = 5)
            
            font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            self.SetFont(font)
            self.SetForegroundColour(wx.BLACK)
        
            label = wx.StaticText(self, -1, str(element.chargeAdm["axial"]))
            sizer.Add(label, (l,1), flag = wx.ALIGN_CENTRE|wx.ALL, border = 5)
            label = wx.StaticText(self, -1, str(coefTaille(element.chargeAdm["axial"], num, "G")))
            sizer.Add(label, (l,2), flag = wx.ALIGN_CENTRE|wx.ALL, border = 5)
            
        elif element.type == "J":
            font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            font.SetWeight(wx.BOLD)
            self.SetFont(font)
            self.SetForegroundColour(wx.BLACK)
                       
            label = wx.StaticText(self, -1, u"Pression admissible :")
            sizer.Add(label, (l,0), flag = wx.ALIGN_RIGHT|wx.ALL, border = 5)
            
            font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            self.SetFont(font)
            self.SetForegroundColour(wx.BLACK)
        
            if "Al" in element.pressAdm.keys():
                l += 1
                
                label = wx.StaticText(self, -1, "Statique :")
                sizer.Add(label, (l,0), flag = wx.ALIGN_RIGHT|wx.ALL, border = 5)
        
                label = wx.StaticText(self, -1, str(element.pressAdm["Al"]))
                sizer.Add(label, (l,1), flag = wx.ALIGN_CENTRE|wx.ALL, border = 5)
            
            if "Ar" in element.pressAdm.keys():
                l += 1
                label = wx.StaticText(self, -1, "Dynamique :")
                sizer.Add(label, (l,0), flag = wx.ALIGN_RIGHT|wx.ALL, border = 5)
            
                label = wx.StaticText(self, -1, str(element.pressAdm["Ar"]))
                sizer.Add(label, (l,1), flag = wx.ALIGN_CENTRE|wx.ALL, border = 5)
            
            l += 1
            font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            font.SetWeight(wx.BOLD)
            self.SetFont(font)
            self.SetForegroundColour(wx.BLACK)
                        
            label = wx.StaticText(self, -1, u"Vitesse admissible :")
            sizer.Add(label, (l,0), flag = wx.ALIGN_RIGHT|wx.ALL, border = 5)
            
            font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            self.SetFont(font)
            self.SetForegroundColour(wx.BLACK)
            
            label = wx.StaticText(self, -1, str(element.vittAdm))
            sizer.Add(label, (l,1), flag = wx.ALIGN_CENTRE|wx.ALL, border = 5)
        
            l += 1
            font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            font.SetWeight(wx.BOLD)
            self.SetFont(font)
            self.SetForegroundColour(wx.BLACK)
                        
            label = wx.StaticText(self, -1, u"Facteur PV :")
            sizer.Add(label, (l,0), flag = wx.ALIGN_RIGHT|wx.ALL, border = 5)
            
            font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            self.SetFont(font)
            self.SetForegroundColour(wx.BLACK)
            
            label = wx.StaticText(self, -1, str(element.facteurPV))
            sizer.Add(label, (l,1), flag = wx.ALIGN_CENTRE|wx.ALL, border = 5)

        
        l += 1
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetWeight(wx.BOLD)
        self.SetFont(font)
        self.SetForegroundColour(wx.BLACK)
        
        label = wx.StaticText(self, -1, u"Coût :")
        sizer.Add(label, (l,0), flag = wx.ALIGN_RIGHT|wx.ALL, border = 5)
        
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        self.SetFont(font)
        self.SetForegroundColour(wx.BLACK)
        label = wx.StaticText(self, -1, str(element.Cout()))
        sizer.Add(label, (l,1), flag = wx.ALIGN_CENTRE|wx.ALL, border = 5)
        element.taille = "G"
        label = wx.StaticText(self, -1, str(element.Cout()))
        sizer.Add(label, (l,2), flag = wx.ALIGN_CENTRE|wx.ALL, border = 5)


        btnsizer = wx.StdDialogButtonSizer()
        
#        if wx.Platform != "__WXMSW__":
#            btn = wx.ContextHelpButton(self)
#            btnsizer.AddButton(btn)
        
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        
        l += 1
        sizer.Add(btnsizer, (l,0), (1,4), flag = wx.ALIGN_CENTER_VERTICAL|wx.ALL, border = 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

#        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
#        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
#        self.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
#        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)

        
        
        
#    def OnMouseLeftDown(self, evt):
#        self.Refresh()
#        self.ldPos = evt.GetEventObject().ClientToScreen(evt.GetPosition())
#        self.wPos = self.ClientToScreen((0,0))
#        self.CaptureMouse()
#
#    def OnMouseMotion(self, evt):
#        if evt.Dragging() and evt.LeftIsDown():
#            dPos = evt.GetEventObject().ClientToScreen(evt.GetPosition())
#            nPos = (self.wPos.x + (dPos.x - self.ldPos.x),
#                    self.wPos.y + (dPos.y - self.ldPos.y))
#            self.Move(nPos)
#
#    def OnMouseLeftUp(self, evt):
#        self.ReleaseMouse()
#
#    def OnRightUp(self, evt):
#        self.Show(False)
#        self.Destroy()