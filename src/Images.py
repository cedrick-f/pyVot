#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##This file is part of PyVot
#############################################################################
#############################################################################
##                                                                         ##
##                               Images                                    ##
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


#import Image,ImageTk,ImageChops,ImageOps
import time
import wx
import Icones
import globdef
import os.path

# Dossiers ############################################################################
dosImg = {'root'       : "Images",
          'arrets'     : "Arrets",
          'roulements' : "Roulements",
          'boutons'    : "Boutons",
          'arbrales'   : "Arbre_Alesage",
          'joints'     : "Joints",
          'schema'     : "Schema",
          'icones'     : "Icones"}

# Icones du montage
def Img_Icones(key):
     lst = {"Proprietes"     : Icones.getbookBitmap(), 
            "Structure"      : Icones.getIcon_StructureBitmap(), 
            "Etancheite"     : Icones.getIcon_EtancheiteBitmap(), 
            "Specifications" : Icones.getIcon_SpecificationsBitmap(), 
            "CdCF"           : Icones.getIcon_CdCFBitmap()
            }
     return lst[key]

# Boutons des éléments
def Img_Elem(key):
    lst =  {0 : Icones.get_0Bitmap(),
            1 : Icones.get_1Bitmap(),
            2 : Icones.get_2Bitmap(),
            3 : Icones.get_3Bitmap(),
            4 : Icones.get_4Bitmap(),
            5 : Icones.get_5Bitmap(),
            6 : Icones.get_6Bitmap(),
            7 : Icones.get_7Bitmap(),
            8 : Icones.get_8Bitmap(),
            9 : Icones.get_9Bitmap(),
            10: Icones.get_10Bitmap(),
            11: Icones.get_11Bitmap(),
              
            100 : Icones.get_100Bitmap(),
            101 : Icones.get_101Bitmap(),
            102 : Icones.get_102Bitmap(),
            103 : Icones.get_103Bitmap(),

            200 : Icones.get_200Bitmap(),
            201 : Icones.get_201Bitmap(),
            202 : Icones.get_202Bitmap(),
            203 : Icones.get_203Bitmap(),
            204 : Icones.get_204Bitmap()
            }
    return lst[key]

# Icones des ensembles d'éléments
def Img_IconesEns(key):
     lst = {1     : Icones.getIcon_RoultsBitmap(), 
            2     : Icones.getIcon_ArretsBitmap(), 
            3     : Icones.getIcon_JointsBitmap(), 
            }
     return lst[key]

# Boutons Analyse Montabilité 
def Img_BoutonMont(key, ajout = False):
    
    def ajouteSensInterdit(ico):
        bmp = wx.EmptyBitmap(ico.GetWidth(),(ico.GetHeight()))
#        msk = ico.GetMask()
#        bmp.SetMask(msk)
        mdc = wx.MemoryDC(bmp)
        mdc.SetBackground(wx.Brush(wx.Colour(254, 254, 254)))
        mdc.Clear()
        si = wx.BitmapFromImage(wx.ImageFromBitmap(lst["SensInterditR"]).AdjustChannels(1.0, 1.0, 1.0, 0.8))
        mdc.DrawBitmap(ico, 0, 0, True)
        mdc.DrawBitmap(si, (ico.GetWidth() - si.GetWidth())/2,(ico.GetHeight() - si.GetHeight())/2, True)
        mdc.SelectObject(wx.NullBitmap)
        
        mask = wx.Mask(bmp, wx.Colour(255,255,254, 255))
        bmp.SetMask(mask)
        
#        img = bmp.ConvertToImage()
#        img.SetMaskColour(254, 254, 254)
#        bmp = img.ConvertToBitmap()
        return bmp
    
    lst ={'AnimEnsb0Ar' : Icones.getBout_AnimEnsb0ArBitmap(),
          'AnimEnsb1Ar' : Icones.getBout_AnimEnsb1ArBitmap(),
          'AnimEnsb0Al' : Icones.getBout_AnimEnsb0AlBitmap(),
          'AnimEnsb1Al' : Icones.getBout_AnimEnsb1AlBitmap(),
          
          'AnimRltG0Ar' : Icones.getBout_AnimRltG0ArBitmap(),
          'AnimRltG1Ar' : Icones.getBout_AnimRltG1ArBitmap(),
          'AnimRltG0Al' : Icones.getBout_AnimRltG0AlBitmap(),
          'AnimRltG1Al' : Icones.getBout_AnimRltG1AlBitmap(),

          'AnimRltD0Ar' : Icones.getBout_AnimRltD0ArBitmap(),
          'AnimRltD1Ar' : Icones.getBout_AnimRltD1ArBitmap(),
          'AnimRltD0Al' : Icones.getBout_AnimRltD0AlBitmap(),
          'AnimRltD1Al' : Icones.getBout_AnimRltD1AlBitmap(),

          'AnimEnsb0ArR' : Icones.getBout_AnimEnsb0ArRBitmap(),
          'AnimEnsb1ArR' : Icones.getBout_AnimEnsb1ArRBitmap(),
          'AnimEnsb0AlR' : Icones.getBout_AnimEnsb0AlRBitmap(),
          'AnimEnsb1AlR' : Icones.getBout_AnimEnsb1AlRBitmap(),
          
          'AnimRltG0ArR' : Icones.getBout_AnimRltG0ArRBitmap(),
          'AnimRltG1ArR' : Icones.getBout_AnimRltG1ArRBitmap(),
          'AnimRltG0AlR' : Icones.getBout_AnimRltG0AlRBitmap(),
          'AnimRltG1AlR' : Icones.getBout_AnimRltG1AlRBitmap(),

          'AnimRltD0ArR' : Icones.getBout_AnimRltD0ArRBitmap(),
          'AnimRltD1ArR' : Icones.getBout_AnimRltD1ArRBitmap(),
          'AnimRltD0AlR' : Icones.getBout_AnimRltD0AlRBitmap(),
          'AnimRltD1AlR' : Icones.getBout_AnimRltD1AlRBitmap(),

#          'SensInterditE' : Icones.getBout_SensInterditEBitmap(),
          'SensInterditR' : Icones.getBout_SensInterditRBitmap(),

          'Chaine0' : Icones.getBout_Chaine0Bitmap(),
          'Chaine1' : Icones.getBout_Chaine1Bitmap(),

          '_Chaine0' : Icones.getBout__Chaine0Bitmap(),
          '_Chaine1' : Icones.getBout__Chaine1Bitmap(),

          'Arret0' : Icones.getBout_Arret0Bitmap(),
          'Arret1' : Icones.getBout_Arret1Bitmap(),

          'BagueIsolee' : Icones.getBout_BagueIsoleeBitmap()}
    
    if ajout:
        return ajouteSensInterdit(lst[key])
    else:  
        return lst[key] 
    
    


#####################################################################################
#####################################################################################
#####################################################################################
class ImagePlus:
    """ Classe définissant  une(des) wxImage(s)    : .orig = []
                            une wxImage "courante" : .img  ,
                            une wxBitmap           : .bmp
                            un offset (en pixels)  : .ofst      
    """
    
    def __init__(self, dossier, lstFichiersImage, offset = 0):

        # Ouverture des fichiers
        #-----------------------
        self.orig = []
        for fich in lstFichiersImage:
#            print os.path.splitext(fich)
            if os.path.splitext(fich)[1] == ".png":
                self.orig.append(wx.Image(os.path.join(dossier,fich), wx.BITMAP_TYPE_PNG))
            else:
                self.orig.append(wx.Image(os.path.join(dossier,fich), wx.BITMAP_TYPE_GIF))

        for img in self.orig:
            img.InitAlpha()

        # Affectation image courante
        #---------------------------
        self.num = 0
        if len(self.orig) > 0:
            self.img = self.orig[0]
            self.bmp = self.img.ConvertToBitmap()
            # Pour débuggage :
            self.nom = lstFichiersImage[0]
        else:
            self.nom = '_'
        # Affectation de l'offset
        #------------------------
        self.ofst = offset
        
        

#        # Conversion de l'image en bmp
#        #-----------------------------
#        self.bmp = self.img.ConvertToBitmap()

    def largeur(self):
        return self.img.GetWidth()
        
    def conv2Bmp(self):
        self.bmp = wx.BitmapFromImage(self.img)
        self.sauveBmp()
        
    def sauveBmp(self):
        self.bmp0  = self.bmp.GetSubBitmap(wx.Rect(0, 0, self.bmp.GetWidth(), self.bmp.GetHeight()))
#        self.bmp = self.img.ConvertToBitmap()

    def inverser(self):
        if len(self.orig) > 1:
            self.num = not self.num
            self.img = self.orig[self.num]
        else:
            img = self.img.Mirror(True)
            self.img = img
#        self.conv2Bmp()
        
#    def estomper(self, niv):
#        self.bmp = wx.BitmapFromImage(wx.ImageFromBitmap(self.bmp).AdjustChannels(1.0, 1.0, 1.0, (1.0*niv)/100))

    

    def fondu(self, bmp1, bmp2, niv):
        """ Renvoie une image fondue à <niv> % avec <bmp>
        """
        def AdjustAlpha(bmp, alpha):
            return wx.BitmapFromImage(wx.ImageFromBitmap(bmp).AdjustChannels(1.0, 1.0, 1.0, alpha))
        
#        bmp0 = wx.BitmapFromImage(wx.ImageFromBitmap(self.bmp).Copy().AdjustChannels(1.0, 1.0, 1.0, (1.0*niv)/100))
#        img = wx.ImageFromBitmap(self.bmp).AdjustChannels(1.0, 1.0, 1.0, alpha)
#        bmp0 = wx.BitmapFromImage(img)

        alpha = (1.001*niv)/100
        bmp0 = AdjustAlpha(bmp1, alpha)
        
        # Création d'une copie de l'image ... ou d'une image vide
        if bmp2 is not None:
            bmpf = bmp2.GetSubBitmap(wx.Rect(0, 0, bmp2.GetWidth(), bmp2.GetHeight()))
            memdc = wx.MemoryDC(bmpf)
            memdc.DrawBitmap(bmp0, 0, 0, True)
            memdc.SelectObject(wx.NullBitmap)
        else:
            bmpf = bmp0
            
        return bmpf

    def surbrillance(self, effet = 0):
#        img = self.img.Copy()
#        print img.HasAlpha()
#        self.bmp = self.img.Copy().SetAlpha(0.5).ConvertToBitmap()
        
        if effet == 0:
            self.bmp = wx.BitmapFromImage(wx.ImageFromBitmap(self.bmp).AdjustChannels(1.0, 1.0, 1.0, 0.5))
#            self.bmp = wx.BitmapFromImage(self.img.Copy().AdjustChannels(1.0, 1.0, 1.0, 0.5))
        else:
            self.bmp = wx.BitmapFromImage(wx.ImageFromBitmap(self.bmp).AdjustChannels(2.0, 2.0, 2.0, 1.0))
#            self.bmp = wx.BitmapFromImage(self.img.Copy().AdjustChannels(2.0, 2.0, 2.0, 1.0))
#        self.bmp = self.img.Copy().AdjustChannels(1.0, 1.0, 1.0, 0.5)


##    def surbrillanceTk(self):
##        self.changerCouleur(0)

#
#    def ajouterSensInterdit(self):
#        if self.largeur() == 50:
#            ssint = BoutonMont['SensInterditR']
#        else:
#            ssint = BoutonMont['SensInterditE']
#            
#        img = blend(self.img,ssint,0.5)
##        self.tk = ImageTk.PhotoImage(img)


    def rogner(self, cote, dist):
        if cote == "G":
            b = 0
        else:
            b = 2
        box = self.img.getbbox()
        nbox = []
        for xy in box:
            nbox.append(xy)
#        print "Rogner :",cote, dist, nbox
        nbox[b] += -dist
        img = self.img.copy().crop(nbox)
#        self.tk = ImageTk.PhotoImage(img)
        
    def changerCouleur(self, coul):
#        self.bmp = wx.BitmapFromImage(wx.ImageFromBitmap(self.bmp).AdjustChannels(2.0, 2.0, 2.0, 1.0))
        self.bmp = wx.BitmapFromImage(wx.ImageFromBitmap(self.bmp).AdjustChannels(0.5, 0.5, 0.5, 1.0))
        r,v,b = 1.0, 1.0, 1.0
        if coul == "blanc":
            r,v,b = 1.5, 1.5, 1.5
        elif coul == "noir":
            r,v,b = 0.4, 0.4, 0.4
        elif coul == "rouge":
            r,v,b = 3.0, 0.5, 0.5
        elif coul == "vert":
            v = 3.0
        else:
            r,v,b = 0.5, 0.5, 3.0
        
        self.bmp = wx.BitmapFromImage(wx.ImageFromBitmap(self.bmp).AdjustChannels(r, v, b, 1.0))
        
#        self.tk = ImageTk.PhotoImage(img)
##        dt = time.time() -t
##        print "temps :", dt

    def normal(self):
        self.bmp  = self.bmp0.GetSubBitmap(
                             wx.Rect(0, 0, self.bmp0.GetWidth(), self.bmp0.GetHeight()))
#        self.conv2Bmp()

    def silhouetteTk(self):
        img = self.img.point(lambda i: i / 5)
#        self.tk = ImageTk.PhotoImage(img)
        
    def copie(self):
        i = ImagePlus('',(),self.ofst)
        for im in self.orig:
            i.orig.append(im.Copy())
        i.img = self.img.Copy()
        i.bmp = self.img.ConvertToBitmap()
        i.bmp0  = i.bmp.GetSubBitmap(
                             wx.Rect(0, 0, i.bmp.GetWidth(), i.bmp.GetHeight()))
#        try:
        i.ofst = self.ofst
        i.nom = self.nom
#        except:
#            pass
        return i

#    def couper(self, largeur):
#        bbox = self.img.getbbox()
#        box = (bbox[0],bbox[1],largeur,bbox[3])
#        self.img = self.img.crop(box).load()
#        self.conv2tk()
        
##    def position(self, mtg, palier, radiale,
##                 pAligne = None, pAffich = None,
##                 ecarter = True, largRlt = None,
##                 offset = None):
##        "Calcul de la position en x d'une image"
##        
##        # Palier Opposé
##        if palier == "G":
##            palierOpp = "D"
##        else:
##            palierOpp = "G"
##
##        # Sens du coté Intérieur / Extérieur au montage
##        if pAligne == None:
##            pAligne = self.pAligne
##        if pAligne == "I":      # coté Intérieur
##            sm = 1
##        elif pAligne == "O":    # coté Opposé
##            sm = 1
##            palier = palierOpp
##        else:                   # coté Extérieur
##            sm = -1
##
##         # Sens du coté Palier
##        if palier == "G":
##            sp = 1
##        else:
##            sp = -1
##
##
##        # Sens du coté affichage
##        if pAffich == None:
##            pAffich = self.pAffich
##        if pAffich == "I":
##            sa = 1
##        else:
##            sa = -1
##
##        # Largeur du roulement associé
##        if largRlt is None:
##            largRlt = mtg.tailleRltDefaut
##        
##            
##        # Ecart par rapport au bord du roulement
##        if ecarter:
##            ecart = mtg.ecartRoultEpaul[radiale]
##        else:
##            ecart = 0
##
##        if offset == None:
##            offset = self.ofst
##            
####        print "x :",palier,sp,sm,largRlt,ecart,sa
##        x = mtg.milieuPalier[palier] + sp * sm * (largRlt + ecart + sa * (self.largeur()/2 - offset))
##
####        print "Position x ...",palier,radiale," = ",x
##        return x


#############################################################################
##class ImageMtg(ImagePlus):
##    def __init__(self, lstImage, cotemtg, coteaff, transpose = False):
##        ImagePlus.__init__(self, lstImage)
##        
##        self.item = None
##                 
##        if transpose:
##            self.inverser()
##
##        self.conv2tk()
##
##        self.pAligne = cotemtg
##        self.pAffich = coteaff


# Curseur Elements ##################################################################################

#CurseursElem = {0 : "@Curseur_Rlt_BillesRadial.cur",
#                1 : "@Curseur_Rlt_BillesObliq.cur",
#                2 : "@Curseur_Rlt_BillesObliq.cur",
#                3 : "@Curseur_Rlt_BillesObliq.cur",
#                4 : "@Curseur_Rlt_BillesObliq.cur",
#                5 : "@Curseur_Rlt_BillesObliq.cur",
#                6 : "@Curseur_Rlt_BillesObliq.cur",
#                7 : "@Curseur_Rlt_ButeeRoulx.cur",
#                8 : "@Curseur_Rlt_BillesObliq.cur",
#                9 : "@Curseur_Rlt_ButeeRoulx.cur",
#               
#                100 : "@Curseur_Rlt_BillesObliq.cur",
#                101 : "@Curseur_Rlt_BillesObliq.cur",
#                102 : "@Curseur_Rlt_BillesObliq.cur",
#                103 : "@Curseur_Rlt_BillesObliq.cur",
#
#                200 : "@Curseur_Rlt_BillesObliq.cur",
#                201 : "@Curseur_Rlt_BillesObliq.cur",
#                202 : "@Curseur_Jnt_Chapeau.cur"}
               


# Images des éléments ###########################################################################################
imageElem = {}
def charger_imageElem():
    dosrlt = os.path.join(dosImg['root'], dosImg['roulements'])
    dosjnt = os.path.join(dosImg['root'], dosImg['joints'])
    dosarr = os.path.join(dosImg['root'], dosImg['arrets'])
    
    # Roulements (petits)
    #############################################################################################
    imageElem["0P"]       = ImagePlus(dosrlt ,( 'Rlt_BilleRadial.gif',)                        )
    imageElem["1PAl"]     = ImagePlus(dosrlt ,( 'Rlt_BillesOblique G(BE).gif',)                )
    imageElem["1PAr"]     = ImagePlus(dosrlt ,( 'Rlt_BillesOblique G(BI).gif',)                )
    imageElem["2P"]       = ImagePlus(dosrlt ,( 'Rlt_RotuleBilles.gif',)                       )
    imageElem["3P"]       = ImagePlus(dosrlt ,( 'Rlt_ButeeBilles.gif',)                        )
    imageElem["4PAr"]     = ImagePlus(dosrlt ,( 'Rlt_RouleauxCyl(BI).gif',)                    )
    imageElem["4PAl"]     = ImagePlus(dosrlt ,( 'Rlt_RouleauxCyl(BE).gif',)                    )
    imageElem["5PAr"]     = ImagePlus(dosrlt ,( 'Rlt_RouleauxConiq_G(BI).gif',)        ,7      )
    imageElem["5PAl"]     = ImagePlus(dosrlt ,( 'Rlt_RouleauxConiq_G(BE).gif',)        ,9      )
    imageElem["6P"]       = ImagePlus(dosrlt ,( 'Rlt_RotuleRouleaux.gif',)                     )
    imageElem["7P"]       = ImagePlus(dosrlt ,( 'Rlt_ButeeRouleaux.gif',)                      )
    imageElem["8P"]       = ImagePlus(dosrlt ,( 'Rlt_ButeeBillesDbl.png',)                     )
    imageElem["9P"]       = ImagePlus(dosrlt ,( 'Rlt_ButeeRouleauxDbl.png',)                   )
    imageElem["89P"]      = ImagePlus(dosrlt ,( 'EntretoiseButeeDbl.png',)                     )
    imageElem["10P"]      = ImagePlus(dosrlt ,( 'Rlt_BillesObliqueDbl.png',)                   )
    imageElem["11P"]      = ImagePlus(dosrlt ,( 'Rlt_RouleauxConiqDbl.png',)                   )
    
    # Arrets (petits)
    #############################################################################################
    imageElem["100PArE"]  = ImagePlus(dosarr ,( 'Arret_Ecrou_G.png',
                                                'Arret_Ecrou_D.png')                ,82     )
    imageElem["100PArV"]  = ImagePlus(dosarr ,( 'Arret_Ecrou_G(Vide).png',
                                                'Arret_Ecrou_D(Vide).png')          ,82     )
    imageElem["100PAlE"]  = ImagePlus(dosarr ,( 'Arret_Chapeau_G.png',)                      )
#    imageElem["100PAlV"]  = ImagePlus(dosarr ,( 'Arret_Chapeau_G(Vide).png',)        ,74     )
    imageElem["101PAr"]   = ImagePlus(dosarr ,( 'Arret_Anneau_G.gif',)               ,4      )
    imageElem["101PArV"]  = ImagePlus(dosarr ,( 'Arret_Anneau(Vide).gif',)           ,4      )
    imageElem["101PAl"]   = ImagePlus(dosarr ,( 'Arret_Anneau_Ales_G.gif',)          ,3      )
    imageElem["101PAlV"]  = ImagePlus(dosarr ,( 'Arret_Anneau_Ales(Vide).gif',)      ,3      )
    imageElem["102PArE"]  = ImagePlus(dosarr ,( 'Arret_Epaul_G.gif',)                        )
    imageElem["102PArI"]  = ImagePlus(dosarr ,( 'Arret_Epaul.gif',)                          )
    imageElem["102PAlE"]  = ImagePlus(dosarr ,( 'Arret_Epaul_Ales_G.png',)                   )
    imageElem["102PAlI"]  = ImagePlus(dosarr ,( 'Arret_Epaul_Ales_GD.png',)    ,              )
#    imageElem["102PAlI"]  = ImagePlus(dosarr ,( 'Arret_Epaul_Ales_Bout.png',)                  )
    imageElem["103PAr"]   = ImagePlus(dosarr ,( 'Arret_Entret_G.png',)                       )
    imageElem["103PAlR"]  = ImagePlus(dosarr ,( 'Rondelle.gif',)                             )
    imageElem["103PAl"]   = ImagePlus(dosarr ,( 'Arret_Entret_Ales_G.png',)                  )

    # Joints (petits)
    #############################################################################################
    imageElem["200PArP"]  = ImagePlus(dosjnt ,( 'Joint_1levre_G_surEcrou.png',)      ,-59    )
    imageElem["200PArE"]  = ImagePlus(dosjnt ,( 'Joint_1levre_G_surEpaul.png',)      ,-44    )
    imageElem["200PAr"]   = ImagePlus(dosjnt ,( 'Joint_1levre_G.png',)               ,-44    )
    imageElem["201PAl"]   = ImagePlus(dosjnt ,( 'Joint_ToriqueAlesage_G.png',)       ,-16     )
    imageElem["201PAlV"]  = ImagePlus(dosjnt ,( 'Joint_ToriqueAlesage_G_Vide.png',)       ,-16     )
    imageElem["201PArE"]  = ImagePlus(dosjnt ,( 'Joint_ToriqueArbre_G_surEpaul.png',),-78    )
    imageElem["201PArP"]  = ImagePlus(dosjnt ,( 'Joint_ToriqueArbre_G_surEcrou.png',),-78    )
    imageElem["201PAr"]   = ImagePlus(dosjnt ,( 'Joint_ToriqueArbre_G.png',)         ,-78    )
    imageElem["203PArE"]  = ImagePlus(dosjnt ,( 'Chicanes_surEpaul.png',),-50    )
    imageElem["203PArP"]  = ImagePlus(dosjnt ,( 'Chicanes_surEcrou.png',),-69    )
    imageElem["203PAr"]   = ImagePlus(dosjnt ,( 'Chicanes.png',)         ,-58    )
    imageElem["202PAr"]   = ImagePlus(dosjnt ,( 'Joint_Chapeau_G.png',)              ,-81    )
    imageElem["204PAl"]   = ImagePlus(dosjnt ,( 'Joint_Plat.png',)         ,-31    )

    imageElem["SupPAl"]   = ImagePlus(dosarr ,( 'Support_Chapeau_G.png',)            ,74     )
    imageElem["SupPAlV"]  = ImagePlus(dosarr ,( 'Arret_Chapeau_G(Vide).png',)        ,74     )

    
    # Roulements (grands)
    #############################################################################################
    imageElem["0G"]       = ImagePlus(dosrlt ,( 'g_Rlt_BilleRadial.gif',)                      )
    imageElem["1GAl"]     = ImagePlus(dosrlt ,( 'g_Rlt_BillesOblique G(BE).gif',)              )
    imageElem["1GAr"]     = ImagePlus(dosrlt ,( 'g_Rlt_BillesOblique G(BI).gif',)              )
    imageElem["2G"]       = ImagePlus(dosrlt ,( 'g_Rlt_RotuleBilles.gif',)                     )
    imageElem["3G"]       = ImagePlus(dosrlt ,( 'g_Rlt_ButeeBilles.gif',)                      )
    imageElem["4GAr"]     = ImagePlus(dosrlt ,( 'g_Rlt_RouleauxCyl(BI).gif',)                  )
    imageElem["4GAl"]     = ImagePlus(dosrlt ,( 'g_Rlt_RouleauxCyl(BE).gif',)                  )
    imageElem["5GAr"]     = ImagePlus(dosrlt ,( 'g_Rlt_RouleauxConiq_G(BI).gif',)      ,12     )
    imageElem["5GAl"]     = ImagePlus(dosrlt ,( 'g_Rlt_RouleauxConiq_G(BE).gif',)      ,11     )
    imageElem["6G"]       = ImagePlus(dosrlt ,( 'g_Rlt_RotuleRouleaux.gif',)                   )
    imageElem["7G"]       = ImagePlus(dosrlt ,( 'g_Rlt_ButeeRouleaux.gif',)                    )
    imageElem["8G"]       = ImagePlus(dosrlt ,( 'g_Rlt_ButeeBillesDbl.png',)                   )
    imageElem["9G"]       = ImagePlus(dosrlt ,( 'g_Rlt_ButeeRouleauxDbl.png',)                 )
    imageElem["89G"]      = ImagePlus(dosrlt ,( 'g_EntretoiseButeeDbl.png',)                   )
    imageElem["10G"]      = ImagePlus(dosrlt ,( 'g_Rlt_BillesObliqueDbl.png',)                 )
    imageElem["11G"]      = ImagePlus(dosrlt ,( 'g_Rlt_RouleauxConiqDbl.png',)                 )
             
    # Arrets (grands)
    #############################################################################################
    imageElem["100GArE"]  = ImagePlus(dosarr ,( 'g_Arret_Ecrou_G.png',
                                                'g_Arret_Ecrou_D.png')              ,100    )
    imageElem["100GArV"]  = ImagePlus(dosarr ,( 'g_Arret_Ecrou_G(Vide).png',
                                                'g_Arret_Ecrou_D(Vide).png')        ,100    )
    imageElem["100GAlE"]  = ImagePlus(dosarr ,( 'g_Arret_Chapeau_G.png',)                    )
#    imageElem["100GAlV"]  = ImagePlus(dosarr ,( 'g_Arret_Chapeau_G(Vide).png',)      ,74     )
    imageElem["101GAr"]   = ImagePlus(dosarr ,( 'g_Arret_Anneau_G.gif',)             ,3      )
    imageElem["101GArV"]  = ImagePlus(dosarr ,( 'g_Arret_Anneau(Vide).gif',)         ,3      )
    imageElem["101GAl"]   = ImagePlus(dosarr ,( 'g_Arret_Anneau_Ales_G.gif',)        ,3      )
    imageElem["101GAlV"]  = ImagePlus(dosarr ,( 'g_Arret_Anneau_Ales(Vide).gif',)    ,3      )
    imageElem["102GArE"]  = ImagePlus(dosarr ,( 'g_Arret_Epaul_G.gif',)                      )
    imageElem["102GArI"]  = ImagePlus(dosarr ,( 'g_Arret_Epaul.gif',)                        )
    imageElem["102GAlE"]  = ImagePlus(dosarr ,( 'g_Arret_Epaul_Ales_G.png',)                 )
    imageElem["102GAlI"]  = ImagePlus(dosarr ,( 'g_Arret_Epaul_Ales_GD.png',)                )
#    imageElem["102GAlB"]  = ImagePlus(dosarr ,( 'g_Arret_Epaul_Ales_Bout.png',)                )
    imageElem["103GAr"]   = ImagePlus(dosarr ,( 'g_Arret_Entret_G.png',)                     )
    imageElem["103GAl"]   = ImagePlus(dosarr ,( 'g_Arret_Entret_Ales_G.png',)                )

    # Joints (grands)
    #############################################################################################
    imageElem["200GArP"]  = ImagePlus(dosjnt ,( 'g_Joint_1levre_G_surEcrou.png',)    ,-63    )
    imageElem["200GArE"]  = ImagePlus(dosjnt ,( 'g_Joint_1levre_G_surEpaul.png',)    ,-37    )
    imageElem["200GAr"]   = ImagePlus(dosjnt ,( 'g_Joint_1levre_G.png',)             ,-37    )
    imageElem["201GAl"]   = ImagePlus(dosjnt ,( 'g_Joint_ToriqueAlesage_G.png',)     ,-17     )
    imageElem["201GAlV"]  = ImagePlus(dosjnt ,( 'g_Joint_ToriqueAlesage_G_Vide.png',)     ,-17     )
    imageElem["201GArP"]  = ImagePlus(dosjnt ,( 'g_Joint_ToriqueArbre_G_surEcrou.png',), -78 )
    imageElem["201GArE"]  = ImagePlus(dosjnt ,( 'g_Joint_ToriqueArbre_G_surEpaul.png',), -77 )
    imageElem["201GAr"]   = ImagePlus(dosjnt ,( 'g_Joint_ToriqueArbre_G.png',)       ,-77    )
    imageElem["203GArE"]  = ImagePlus(dosjnt ,( 'g_Chicanes_surEpaul.png',),-42    )
    imageElem["203GArP"]  = ImagePlus(dosjnt ,( 'g_Chicanes_surEcrou.png',),-64    )
    imageElem["203GAr"]   = ImagePlus(dosjnt ,( 'g_Chicanes.png',)         ,-52    )
    imageElem["202GAr"]   = ImagePlus(dosjnt ,( 'g_Joint_Chapeau_G.png',)            ,-85    )
    imageElem["204GAl"]   = ImagePlus(dosjnt ,( 'g_Joint_Plat.png',)         ,-32    )

    imageElem["SupGAl"]   = ImagePlus(dosarr ,( 'g_Support_Chapeau_G.png',)          ,74     )
    imageElem["SupGAlV"]  = ImagePlus(dosarr ,( 'g_Arret_Chapeau_G(Vide).png',)      ,74     )


#####################################################################################################
# Images d'Alésage ##################################################################################
imageAl = {}
def charger_imagesAl():
    dos = os.path.join(dosImg['root'], dosImg['arbrales'])
            #taille : G ou P
            # bout  : B = Logement
            #  dim  : P = petit ; N = normal ; G = grand
    imageAl["GB"] = ImagePlus(dos,('g_Alesage_Logement_G.png',)   )
    imageAl["G"]  = ImagePlus(dos,('g_Alesage_Milieu_G.png',)    ) 
    imageAl["P"]  = ImagePlus(dos,('Alesage_Entier.png',) )   
    imageAl["H"]  = ImagePlus(dos,('Hachures2.png',) )   
                

###################################################################################################
# Images d'Arbre ##################################################################################
imageAr = {}
def charger_imagesAr():
    dos = os.path.join(dosImg['root'], dosImg['arbrales'])
            # Eléments FIXES :
            #taille  : G ou P
            # bout  : B = bout chanfreiné (arrêté) ; F = "infini"
            #  dim  : P = petit ; N = normal ; G = grand
    imageAr["GBN"] = ImagePlus(dos, ('g_BoutArbreG.png',)            ,-20     )
    imageAr["PBN"] = ImagePlus(dos, ('BoutArbreG.png',)              ,-20        )
              
    imageAr["GBP"] = ImagePlus(dos, ('g_BoutArbreG_SurEcrou.png',)   ,-20     )
    imageAr["PBP"] = ImagePlus(dos, ('BoutArbreG_SurEcrou.png',)     ,-16        )

    imageAr["GBG"] = ImagePlus(dos, ('g_BoutArbreG_SurEpaul.png',)   ,-20     )
    imageAr["PBG"] = ImagePlus(dos, ('BoutArbreG_SurEpaul.png',)     ,-16        )

    imageAr["GFN"] = ImagePlus(dos, ('g_BoutArbre_Infini_G.png',)    ,-20     )
    imageAr["PFN"] = ImagePlus(dos, ('BoutArbre_Infini_G.png',)      ,-20        )
        
    imageAr["GFP"] = ImagePlus(dos, ('g_BoutArbre_Infini_G_SurEcrou.png',) ,-20  )
    imageAr["PFP"] = ImagePlus(dos, ('BoutArbre_Infini_G_SurEcrou.png',)   ,-20  )

    imageAr["GFG"] = ImagePlus(dos, ('g_BoutArbre_Infini_G_SurEpaul.png',),-20)
    imageAr["PFG"] = ImagePlus(dos, ('BoutArbre_Infini_G_SurEpaul.png',)  ,-20   )

                # à l'Intérieur du montage :
                # E = épaulement
    imageAr["PE" ] = ImagePlus(dos, ('g_InterArbre_Epaul_G.png',)    ,40        )
    imageAr["P"  ] = ImagePlus(dos, ('InterArbre_G.png',)            ,30        )
    imageAr["G"  ] = ImagePlus(dos, ('g_InterArbre_G.png',)          ,40     )

                # Sous le roulement (Logement)
    imageAr["GM" ] = ImagePlus(dos, ('g_LogementArbre_M.png',)               )
    imageAr["PM" ] = ImagePlus(dos, ('LogementArbre_M.png',)                 )
            
                # Eléments MOBILE (selon les éléments du montage)
                #     autour de l'arrêt (ou du bord du roulement)
                # I = intérieur ; E = extérieur
    imageAr["GRI"] = ImagePlus(dos, ('g_BordLogementArbre_Inter.png',)        )
    imageAr["PRI"] = ImagePlus(dos, ('BordLogementArbre_Inter.png',)          )
    imageAr["GRE"] = ImagePlus(dos, ('g_BordLogementArbre_Exter.png',)        )
    imageAr["PRE"] = ImagePlus(dos, ('BordLogementArbre_Exter.png',)          )

#
#
#
#
#
## Logos ############################################################################################
#           
#Logo_Principal = Image.open(dosImg['root'] + 'logo 0.3.png')
#
#



###################################################################################################
# Images du Schéma de CdCF ##################################################################################
imageSchema = {}
dos = os.path.join(dosImg['root'], dosImg['schema'])
def charger_imagesSchema():
#    Sch = 
    Fle = wx.Image(os.path.join(dos, 'Fleche.png'), wx.BITMAP_TYPE_PNG)
#    Fle.SetMask(True)
    Fba = wx.Image(os.path.join(dos, 'FlecheBarree.png'), wx.BITMAP_TYPE_PNG)
#    Fba.SetMask(True)
    imageSchema ["Fle"] = wx.BitmapFromImage(Fle, depth=-1)
    imageSchema ["Sch"] = wx.BitmapFromImage(wx.Image(os.path.join(dos, 'Schema CdCF.png'), wx.BITMAP_TYPE_PNG), depth=-1) 
    
    imageSchema ["Fba"] = wx.BitmapFromImage(Fba, depth=-1)


## Curseurs ? ######################################################################
#
#Curseur = dosImg['root'] + 'Schema petit.gif'
#
## Fleche rotation ##############################################################
#dos = dosImg['root'] + dosImg['boutons'] 
#FlecheRotation = Image.open(dos + 'Fleche.png')
#FlecheRotationBarree = Image.open(dos + 'Fleche barree.png')
#
#
#
#

              
#def ajouterSensInterdit(tagimg1):
#    img1 = BoutonMont[tagimg1].convert("RGBA")
#    
#    if img1.size[0] == 50:
#        ssint = BoutonMont['SensInterditR']
#    else:
#        ssint = BoutonMont['SensInterditE']
#
#    mask = ssint.copy().point(lambda i: i * 0.7)
###    img = Image.blend(img1, ssint, 0.5)
#    img = Image.composite(ssint, img1, mask)
###    img1.paste(ssint)
#    
#    return img


def ombrer(bmp, e = 4):
    
#    dc.SetBackground(wx.Brush(wx.Colour(255,255,254)))
#    bmp = wx.BitmapFromImage(img)
    
#    ombr = wx.BitmapFromImage(imgOmbr)
#    mask = bmp.GetMask()
#    maskBrush = wx.BrushFromBitmap(ombr)
    
    # Création du masque
    bmpMask = wx.EmptyBitmap(bmp.GetWidth()+2*e, bmp.GetHeight()+2*e)
    maskDC = wx.MemoryDC(bmpMask)
    maskDC.SetBackground(wx.Brush(wx.WHITE))
    maskDC.Clear()
    maskDC.DrawBitmap(bmp, e, e, True)
    maskDC.SelectObject(wx.NullBitmap)
#    bmpMask.SetMask(wx.Mask(bmpMask, wx.WHITE))
    
    

    ombreBmp = bmpMask.ConvertToImage().ConvertToMono(255, 255, 255).Blur(e/2).ConvertToBitmap()
    imageBmp = bmpMask.ConvertToImage().ConvertToMono(255, 255, 255).ConvertToBitmap()
    imageBmp.SetMask(wx.Mask(imageBmp, wx.WHITE))
#    imageBmp.InitAlpha()
    bmpMask = wx.EmptyBitmap(bmp.GetWidth()+2*e, bmp.GetHeight()+2*e)
    maskDC = wx.MemoryDC(bmpMask)
    maskDC.SetBackground(wx.Brush(wx.WHITE))
    maskDC.Clear()
    maskDC.DrawBitmap(ombreBmp, 0, 0, True)
    maskDC.DrawBitmap(imageBmp, -e, -e, True)
    maskDC.SelectObject(wx.NullBitmap)
#    
#    return negatif(bmpMask)
    bmpMask = negatif(bmpMask)
    bmpMask = bmpMask.ConvertToImage().ConvertToGreyscale().ConvertToBitmap()
#    return bmpMask
#    maskbmp = bmp.ConvertToImage()#.AdjustChannels(0.2, 0.2, 0.2, 1)
##    maskbmp = maskbmp.ConvertToGreyscale().AdjustChannels(0.3, 0.3, 0.3)
#    maskbmp = maskbmp.ConvertToMono(255, 255, 255)
#    maskbmp = maskbmp.ConvertToBitmap()
#    maskOmbr = bmp.ConvertToImage().ConvertToMono(255, 255, 255).Blur(e).ConvertToBitmap()
#    maskDC.DrawBitmap(maskOmbr, e, e, True)
##    maskDC.DrawBitmap(maskbmp, 0, 0, True)
#    maskDC.SelectObject(wx.NullBitmap)
    
    # Création de l'image ombrée
#    ombr = bmp.ConvertToImage().AdjustChannels(0.5, 0.5, 0.5, 0.5).Blur(e).ConvertToBitmap()
    bmpOmbr = wx.EmptyBitmap(bmp.GetWidth()+2*e, bmp.GetHeight()+2*e)
    dc = wx.MemoryDC(bmpOmbr)
    dc.SetBackground(wx.Brush(wx.BLACK))
    dc.Clear()
#    dc.DrawBitmap(ombreBmp, 0, 0, True)
    dc.DrawBitmap(bmp, 0, 0, True)
    dc.SelectObject(wx.NullBitmap)
    
    imMask = wx.ImageFromBitmap(bmpMask)
    grn = ''.join([gg for i,gg in enumerate(imMask.GetData()) if not (i+2)%3])
    imOmbr = wx.ImageFromBitmap(bmpOmbr)
    imOmbr.SetAlphaData(grn)
    bmpOmbr = imOmbr.ConvertToBitmap()

#    bmpOmbr.SetMask(wx.Mask(bmpMask))
#    bmpOmbr.SetMask(maskOmbr)
#    imgOmbre = wx.ImageFromBitmap(bmpOmbr)
#    bmpOmbr.SetMask(wx.Mask(bmpOmbr))
    return bmpOmbr

def negatif(bmp):
    mask = bmp.GetMask()
    bmpPos = wx.EmptyBitmap(bmp.GetWidth(), bmp.GetHeight())
    bmpNeg = wx.EmptyBitmap(bmp.GetWidth(), bmp.GetHeight())
    
    srcDC = wx.MemoryDC(bmpPos)
    srcDC.SetBackground(wx.Brush(wx.WHITE))
    srcDC.Clear()
    srcDC.DrawBitmap(bmp, 0, 0)
    
    dstDC = wx.MemoryDC(bmpNeg)
    dstDC.SetBackground(wx.Brush(wx.WHITE))
    dstDC.Clear()
    dstDC.Blit(0,0,bmp.GetWidth(), bmp.GetHeight(),
               srcDC, 0,0,
               wx.SRC_INVERT)
    
    srcDC.SelectObject(wx.NullBitmap)
    dstDC.SelectObject(wx.NullBitmap)
    
    return bmpNeg



def ombre(bmp, e = 4):
    ombr = wx.BitmapFromImage(wx.ImageFromBitmap(bmp).AdjustChannels(0.5, 0.5, 0.5, 0.5).Blur(e))
    return ombr
