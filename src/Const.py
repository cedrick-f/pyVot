#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##This file is part of PyVot
#############################################################################
#############################################################################
##                                                                         ##
##                                   Const                                 ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2006 Cédrick FAURY

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
import os

##import gui
#from Tkinter import *
import sys
#from Elements import listeElements, coefTaille
#from Widget import InfoBulle


##############################################################################
#     Polices     #
##############################################################################

Font_Titre       = [("Helvetica, ", "13", "bold",   "italic")             ,"blue"]
Font_Logo        = [("Helvetica, ", "30", "bold",   "italic")             ,"red"]

Font_AnalTitre   = [("Helvetica, ", "11", "bold",   "italic")             ,"dark red"]

Font_CdCFTitre   = [("Helvetica, ", "9",  "bold",   "roman")              ,"dark blue"]
Font_CdCFTitreS  = [("Helvetica, ", "10",  "bold",   "roman", "underline")   ,"dark blue"]
Font_CdCFValeur  = [("Helvetica, ", "10", "normal", "roman")              ,"dark red"]
Font_CdCFPetit   = [("Helvetica, ", "8",  "normal", "roman")              ,"dark grey"]
Font_CdCFMoy     = [("Helvetica, ", "9",  "normal", "italic")             ,"black"]

Font_Message     = [("Helvetica, ", "20", "bold",   "roman")              ,"black"]
Font_LienWeb     = [("Helvetica, ", "9",  "normal", "roman", "underline") ,"blue"]
Font_test        = [("Helvetica, ", "8",  "normal", "roman")              ,"black"]

Font_TitreBulle  = [("Helvetica, ", "9",  "bold", "roman", "underline") , "dark blue"]
Font_MessBulle   = [("Helvetica, ", "8",  "normal", "roman")              ,"black"]
Font_MessBulleI  = [("Helvetica, ", "8",  "normal", "italic")              ,"black"]
Font_MessBulleG  = [("Helvetica, ", "8",  "bold", "roman")              ,"black"]
Font_MessBulleS  = [("Helvetica, ", "8",  "normal", "roman", "underline")   ,"black"]

Font_Info        = [("Helvetica, ", "10",  "normal", "roman")              ,"dark red"]
Font_InfoNoir    = [("Helvetica, ", "9",  "normal", "roman")             ,"black"]
Font_Message     = [("Helvetica, ", "11",  "normal", "italic")             ,"dark blue"]
Font_PetitGrand  = [("Helvetica, ", "12",  "normal", "roman")              ,"dark red"]

Font_AnalDetail  = [("Helvetica, ", "9", "normal", "roman")              ,"dark red"]

Font_GrosBouton  = [("Helvetica, ", "11",  "normal", "roman")             ,"black"]

Font_Onglet = [("Helvetica, ", "8",  "normal", "roman")              ,"black"]
Font_OngletActif = [("Helvetica, ", "8",  "bold", "roman")              ,"black"]


##############################################################################
#     Message d'erreur d'analyse     #
##############################################################################
arg2str = {0    : ("sens",u"droite"),
           1    : ("sens",u"gauche"),
           "D"  : ("cote",u"droit"),
           "G"  : ("cote",u"gauche"),
           "GD" : ("cote",u""),
           "DG" : ("cote",u""),
           "Al" : ("radi",u"alésage"),
           "Ar" : ("radi",u"arbre"),
           "EAl" : ("etanch",u"statique"),
           "EAr" : ("etanch",u"dynamique")
           }


messagesAnalyse = { ''               : ('','black'),
                    'MontOk'         : (u"Montage correct","vert"),

                    # Remarques générales
                    'ManqueRlt'      : (u"Il manque un roulement pour faire une liaison pivot !", "rouge"),
                    'RltPasMaintenu' : (u"Une des bagues du roulement %(cote)s n'est pas maintenue.", "rouge"),
                    'RltPasMaintenus': (u"Une des bagues des roulements n'est pas maintenue.", "rouge"),
                    'RltsImcomp'     : (u"Roulements incompatibles.", "rouge"),
                    'OrientIncorr'   : (u"L'orientation des roulements à contact oblique est incorrecte.", "rouge"),
                    'RltPasArrete'   : (u"Le roulement %(cote)s devrait être arrêté des deux cotés sur l'%(radi)s.", "bleu"),
                    'RltPasArretes'  : (u"Les deux roulements devraient être arrêtés des deux cotés sur l'%(radi)s.", "bleu"),

                    # Immobilisation axiale du montage
                    'ArretArbreSens' : (u"L'arbre n'est pas arrêté axialement vers la %(sens)s" , "rouge"),
                    'Hyperstatique'  : (u"hyperstatique." , "bleu"),
                    'ImmobCorrect'   : (u"L'arbre est arrêté axialement." , "vert"),
                    'ArbreArrete'    : (u"L'arbre est correctement arrêté axialement." , "vert"),
                    'ArbrePasArrete' : (u"L'arbre n'est pas correctement arrêté axialement." , "rouge"),

                    # Résistance aux charges
                        # axial
                    'ChargeAxOk'     : (u"Le montage résiste à la charge axiale." , "vert"),
                    'ChargeAxNo'     : (u"Le montage ne résiste pas à la charge axiale." , "rouge"),
                    'ElemResistPas'  : (u"Les éléments suivants ne résistent pas :", "rouge"),
                        # roult
                    'RltSupportePas' : (u"ne supporte pas" , "rouge"),
                    'RltSupporte'    : (u"supporte" , "vert"),
                    'TRltSupportePas' : (u"Aucun roulement ne supporte la charge." , "rouge"),
                    '1RltSupportePas' : (u"Le roulement %(cote)s ne supporte pas la charge." , "rouge"),
                    'TRltSupporte'    : (u"Tous les roulements supportent la charge." , "vert"),

                        # 
                    'ChargeRadOk'    : (u"Résiste à la charge radiale.", "vert"),
                    'EffortRadial'   : (u"Ne résiste pas à la charge radiale.", "rouge"),

                    # Montabilité
                    'MontImposs'     : (u"Le Montage/Démontage de certains éléments est impossible !" , "rouge"),
                    'Possible'       : (u"possible" , "vert"),
                    'Impossible'     : (u"impossible" , "rouge"),
                    'Collision'      : (u"Collision entre les éléments suivants :", "rouge"),
                    'ElemNonDem'     : (u"L'élément %s n'est pas montable/démontable.", "rouge"),
                    'RltGonfl'       : (u"Le roulement %(cote)s ne peut pas être monté sur l'%(radi)s !", "rouge"),
                    'MontPoss'       : (u"Le Montage/Démontage des éléments est possible." , "vert"),
                    'MontImpossRlt'  : (u"Le roulement %(cote)s ne peut pas être monté sur l'%(radi)s !", "rouge"),
                    'CollisionRlt'   : (u"Collision avec les éléments suivants :" , "rouge"),
                    'BagueIsolee'    : (u"Le roulement suivant\nn'est pas montable sur son logement sérré.", "rouge"),
                    'BagueIsolees'   : (u"Les roulements suivants\nne sont pas montables sur leur logement sérré.", "rouge"),

                    # Entachéité
                    'EtanchStat'      : (u"L'étanchéité statique est assurée." , "vert"),
                    'PasEtanchStat'   : (u"L'étanchéité statique n'est pas assurée !" , "rouge"),
                    'EtanchDyn'       : (u"L'étanchéité dynamique est assurée." , "vert"),
                    'PasEtanchDyn'    : (u"L'étanchéité dynamique n'est pas assurée !" , "rouge"),
                    'IncompLubHuil'   : (u"La lubrification à l'huile est impossible avec les chicanes !" , "rouge"),
                    'IncompLubChic'   : (u"Les chicanes sont incompatibles avec la pression souhaitée !" , "rouge"),
                    'ManqueJoint'     : (u"Il manque un dispositif d'étanchéité du coté %(cote)s.", "rouge"),
                    'VitesseTrop'     : (u"La vitesse est trop élevée pour le joint du coté %(cote)s.", "rouge"),
                    'FactPVTrop'      : (u"Le facteur PV est trop élevé pour le joint du coté %(cote)s.", "rouge"),
                    'VittPVTrop'      : (u"La vitesse et le facteur PV sont trop élevés pour certains joints.", "rouge"),
                    'PressTrop'       : (u"La pression est trop élevée pour le joint du coté %(cote)s.", "rouge"),
                    
                    'LubrifComp'      : (u"Les joints sont compatibles avec la lubrification choisie.", "vert"),
                    'LubrifPasComp'   : (u"Les chicanes ne sont pas compatibles avec une lubrification à l'huile.", "rouge")
                    }

#########################################################################################
class StyleDeTexte:
    def __init__(self, font, color):
        self.font = font
        self.color = color
        
    def applique(self, win, color = None):
        if color != None:
            self.color = color
        win.SetFont(self.font)
        win.SetForegroundColour(self.color)
        
############################################################################################
class MessageAnalyse:
    def __init__(self, clef = '', lstArg = [], mess = None, coul = None):

##        print
##        print "Initialisation messsage : clef =",clef," ; args =",args

        strArg = {}
        for comp in lstArg:
            strArg[arg2str[comp][0]] = arg2str[comp][1]
    
        self.clef = clef

        if "GD" in lstArg or "DG" in lstArg:
            clef += "s"
            
        if clef <> '':
            self.mess = messagesAnalyse[clef][0] %strArg
            self.coul = messagesAnalyse[clef][1]
        else:
            self.mess = mess
            self.coul = coul

    

################################################################################
#      Liens vers l'aide       #
################################################################################
dossierTravail = os.getcwd()
dossierAide = "/Aide/"
lienAide = {"index"   : "index.html",
            "cdcf"    : "cdcf.html",
            "analyse" : "analyse.html"}

def afficherAide(options, clef):
##    webbrowser.open(lienAide[clef])
##    print "Affichage de l'aide :",lienAide[clef]
    if options.typeAide.get() == 0 and sys.platform == 'win32':
        os.startfile(dossierAide+'pyvotaide.chm')
    else:
        os.chdir(dossierTravail+dossierAide+"html/")
        webbrowser.open('index.html')
        os.chdir(dossierTravail)



##############################################################################
#     Zone de message     #
##############################################################################

#messages = {'SelectElem' : u"Selectionner un élément à placer sur le montage",
#            'FaireGliss' : u"Faire glisser l'élément sur le montage",
#            'MenuContex' : u"Bouton droit de la souris pour modifier l'élément",
#            'PlacerElem' : u"Cliquer pour placer l'élément sur le montage",
#            'ModifCdCF'  : u"Modification du CdCF"}
#
#class ZoneMessage(Frame):
#    "classe définissant la zone de message"
#    def __init__(self, master):
#        Frame.__init__(self, bd = 2, relief = FLAT,
#                       width = 400, height = 30, padx = 3, pady = 3)
#        self.grid_propagate(0)
#        self.master = master
#        self.message = StringVar()
#        self.messageSauv = messages['SelectElem']
#        Label(self, textvariable = self.message, \
#              font = Font_Message[0], \
#              fg = Font_Message[1], \
#              anchor = E, justify = LEFT,
#              ) \
#              .grid(column = 0, row = 0, sticky = W)
#
#    def afficher(self, clef, sauv = False):
#        if sauv:
#            self.messageSauv = self.message.get()
#        self.message.set(messages[clef])
#        
#    def restaurer(self):
#        self.message.set(self.messageSauv)
        


##############################################################################
#     Info bulle     #
##############################################################################
bulles = {'vide'    : u"",
          'Ouvrir'  : u"Ouvrir un montage depuis un fichier",
          'Enregi'  : u"Enregistrer le montage dans un fichier",
          'ModCdcf' : u"Modifier le CdCF",
          'Analyse' : u"Analyser le montage",
          'Reinit'  : u"Réinitialiser le montage\nTous les éléments sont supprimés !",
          'CdCFCurs'    : u"Faire glisser le curseur\npour modifier la faleur de l'indice",
          'CdCFAide'    : u"Affiche l'aide relative au CdCF",
          'CdCFCharg'   : u"Répartition et indices des charges\nappliquées sur l'arbre",
          'CdCFBague'   : u"Désigne la bague qui tourne\npar rapport à la charge radiale\nappliquée sur l'arbre",
          'CdCF'        : u"Cahier des Charges Fonctionnel",
          'CdCFCout'    : u"Indice de Coût maximum du montage",
          'CdCFPress'   : u"Indice de Pression Relative dans la liaison",
          'CdCFVitt'    : u"Indice de Vitesse Angulaire de la liaison",
          'AnalyAnim'   : u"Effectue une animation illustrant le manque d'arrêts",
          'AnalyChai'   : u"Trace la chaîne d'action de l'effort axial",
          'SelectRoul'  : u"Selectionner les éléments ne résistant pas à la charge axiale",
          'AnalyHypr'   : u"La chaîne d'action est double ...",
          'EnsPasDemont': u"Démonter l'ensemble pour pouvoir\n",
          'Dem'         : u"Démonter",
          'Rem'         : u"Remonter",
          'Ens'         : u"l'ensemble",
          'Rlt'         : u"le roulement",
          'G'           : u"gauche",
          'D'           : u"droit",
          'Al'          : u"arbre",
          'Ar'          : u"alésage",
          'vers'        : u"vers la",
          'depuis'      : u"depuis la",
          'sens0'       : u"droite.",
          'sens1'       : u"gauche.",
          'AnalyMtgEns': u"Effectue une animation de l'opération\nde démontage/montage de l'ensemble\nvers/depuis la droite",
          'AnalyMtgEns1': u"Effectue une animation de l'opération\nde démontage/montage de l'ensemble\nvers/depuis la gauche",
          'AnalyMtgRlt' : u"Effectue une animation de l'opération\nde démontage/montage du roulement %s\nvers/depuis la %s",
          'AnalyMtgObs' : u"Met en évidence les différents obstacles au démontage"
          }


#################################################################################
class InfoBulleSimple:
    def __init__(self, zone, clefBulle):
        bulle = InfoBulle(zone)  
        Label(bulle, text = bulles[clefBulle], bg = bulle['bg']).grid()



#################################################################################
class InfoBulleMulti:
    def __init__(self, zone, lstClefBulle):
        bulle = InfoBulle(zone)
        self.label = Label(bulle, text = '', bg = bulle['bg'])
        self.label.grid()
        self.changer(lstClefBulle)

    def changer(self,lstClefBulle):
        txt = ''
        for c in lstClefBulle:
            txt += bulles[c]+" "
        self.label['text'] = txt
        
        

#################################################################################
class InfoBulleDetails:
    def __init__(self, zone, lstNoms,
                 commandEntrer, commandQuitter):
        self.bulle = InfoBulle(zone)
        self.commandEntrer = commandEntrer
        self.commandQuitter = commandQuitter
        
        Label(self.bulle, text = lstNoms['mess'],
              bg = self.bulle['bg'],
              justify = LEFT) \
            .pack(anchor = W)

        self.l = []
        for n in lstNoms['lst']:
            self.l.append(Label(self.bulle, text = n,
                              bg = self.bulle['bg'],
                              justify = LEFT))
        
        for n in range(len(self.l)):
            self.l[n].pack(anchor = W)
            self.l[n].bind("<Enter>",lambda evt = None, arg = n : self.entrer(evt,arg))
            self.l[n].bind("<Leave>",lambda evt = None, arg = n : self.quitter(evt,arg))

        self.bulle.zone.bind("<Leave>",self.quitterZone)
        self.bulle.bind("<Leave>",self.quitterBulle)
        self.bulle.bind("<Enter>",self.entrerBulle)

    def quitterBulle(self, event):
        if event.widget == self.bulle:
            self.bulle.efface()

    def quitterZone(self, event):
        self.action = self.bulle.after(100,self.bulle.efface)
        self.bulle.zone.quitter()

    def entrerBulle(self,event):
        self.bulle.after_cancel(self.action)
        
    def entrer(self, event = None, num = None):
        self.l[num]['bg'] = "dark blue"
        self.l[num]['fg'] = "white"
        self.commandEntrer(num)

    def quitter(self, event = None, num = None):
        self.l[num]['bg'] = self.bulle['bg']
        self.l[num]['fg'] = "black"
        self.commandQuitter(num,False)



#################################################################################        
class InfoBulleElem:
    """ Classe définissant l'info-bulle pour un élément """
    
    def __init__(self, zone, numElem, taille = ["P","G"]):
        bulle = InfoBulle(zone)
        
        if type(taille) <> list: taille = [taille]
            
        Label(bulle, text = listeElements[numElem]['nom'],
              bg = bulle['bg'],
              font = Font_TitreBulle[0],
              fg = Font_TitreBulle[1],
              justify = RIGHT) \
            .grid(row = 0, column = 0,
                  columnspan = 4, sticky = W)

        c = 1
        for t in taille:
            if t == "P":
                tx = u"petit"
            else:
                tx = u"grand"
            Label(bulle, text = tx,
                  bg = bulle['bg'],
                  justify = RIGHT, anchor = E) \
                .grid(row = 1, column = c, sticky = E)
            c += 1
            
        if listeElements[numElem]['type'] == "R":
            Label(bulle, text = u"Indices de charge admissible :",
                  bg = bulle['bg'],
                  justify = RIGHT, anchor = E,
                  font = Font_MessBulleG[0]) \
                .grid(row = 1, column = 0, sticky = E)
            Label(bulle, text = u"axiale :",
                  bg = bulle['bg'],
                  justify = RIGHT, anchor = E) \
                .grid(row = 2, column = 0, sticky = E)
            Label(bulle, text = u"radiale :",
                  bg = bulle['bg'],
                  justify = RIGHT, anchor = E) \
                .grid(row = 3, column = 0, sticky = E)
            Label(bulle, text = u"combinée :",
                  bg = bulle['bg'],
                  justify = RIGHT, anchor = E) \
                .grid(row = 4, column = 0, sticky = E)

            r = 2
            c = 1
            for i in ["axial","radial","combi"]:
                for t in taille:
                    Label(bulle, text = str(coefTaille(listeElements[numElem]['chargeAdm'][i],
                                                      numElem,t)),
                          justify = RIGHT, bg = bulle['bg']) \
                        .grid(row = r, column = c)
                    c += 1
                Label(bulle, text = adaptation[listeElements[numElem]['chargeAdm'][i]],
                      justify = RIGHT, bg = bulle['bg'],
                      font = Font_MessBulleI[0]) \
                    .grid(row = r, column = c)
                c = 1
                r += 1

            Label(bulle, text = u"Indice de Coût :",
                  bg = bulle['bg'],
                  justify = RIGHT, anchor = E,
                  font = Font_MessBulleG[0]) \
                .grid(row = r, column = 0, sticky = E)
            c = 1
            for t in taille:
                Label(bulle, text = str(coefTaille(listeElements[numElem]['cout'],
                                                      numElem,t)),
                          justify = RIGHT, bg = bulle['bg']) \
                        .grid(row = r, column = c)
                c += 1
         
        elif listeElements[numElem]['type'] == "A":
            Label(bulle, text = u"Indice de charge admissible :",
                  bg = bulle['bg'],
                  justify = RIGHT, anchor = E,
                  font = Font_MessBulleG[0]) \
                .grid(row = 2, column = 0, sticky = E)
            c = 1
            for t in taille:
                Label(bulle, text = str(coefTaille(listeElements[numElem]['chargeAdm']["axial"],
                                                  numElem,t)),
                          justify = RIGHT, bg = bulle['bg']) \
                        .grid(row = 2, column = c)
                c += 1
            
            Label(bulle, text = u"Indice de Coût :",
                  bg = bulle['bg'],
                  justify = RIGHT, anchor = E,
                  font = Font_MessBulleG[0]) \
                .grid(row = 3, column = 0, sticky = E)
            c = 1
            for t in taille:
                Label(bulle, text = str(coefTaille(listeElements[numElem]['cout'],
                                                       numElem,t)),
                          justify = RIGHT, bg = bulle['bg']) \
                        .grid(row = 3, column = c)
                c += 1

        elif listeElements[numElem]['type'] == "J":
            Label(bulle, text = u"Pression admissible :",
                  bg = bulle['bg'],
                  justify = RIGHT, anchor = E,
                  font = Font_MessBulleG[0]) \
                .grid(row = 2, column = 0, sticky = E)

            c = 0
            for e in listeElements[numElem]['pos']:
                Label(bulle, text = str(coefTaille(listeElements[numElem]['pressAdm'][e],
                                                   numElem,t)),
                      justify = RIGHT, bg = bulle['bg']) \
                      .grid(row = 2, column = c)
                c += 1
                
            
            Label(bulle, text = u"Vitesse admissible :",
                  bg = bulle['bg'],
                  justify = RIGHT, anchor = E,
                  font = Font_MessBulleG[0]) \
                .grid(row = 3, column = 0, sticky = E)

            Label(bulle, text = str(coefTaille(listeElements[numElem]['vittAdm'],
                                               numElem,t)),
                  justify = RIGHT, bg = bulle['bg']) \
                  .grid(row = 3, column = c)
                

        
##class infoBulle(Toplevel):
##    def __init__(self, parent, lstMess = [], lstClef = [], numElem = None,
##                 frameSpec = None, temps = 400, side = LEFT, position = "bord"):
##
####        if lstMess <> []:
####            t = "lstMess ="
####            a = lstMess
####        elif lstClef <> []:
####            t = "lstClef ="
####            a = lstClef
####        elif elemMess <> None:
####            t = "elemMess ="
####            a = elemMess
####        elif frameSpec <> None:
####            t = "frameSpec ="
####            a = frameSpec
####        
####        print
####        print "Initialisation Bulle :"
####        print t,a
##        
##        Toplevel.__init__(self,parent,bd=2,bg='lightyellow',relief = RIDGE)
##        self.tps = temps
##        self.parent=parent
##        self.withdraw()
##        self.overrideredirect(1)
##        self.transient()
##        self.position = position
##        self.side = side
##        self.lstLabel = []
##
##        self.lstMess = lstMess
##        self.lstClef = lstClef
##
##        self.tipwidth = 0
##        self.tipheight = 0
##            
##        if numElem <> None:
##            self.ajouterFrame(numElem)
##        elif frameSpec <> None:
##            self.ajouterFrameSpec(frameSpec)  
##        else:
##            self.ajouterLabel()
##
##        self.parent.bind('<Enter>',self.delai)
##        self.parent.bind('<Button-1>',self.efface)
##        self.parent.bind('<Leave>',self.efface)
##
##    ############################################################################
##    def listeMessages(self):
##        lstMess = []
##        for c in self.lstClef:
##            lstMess.append({'str' : bulles[c],
##                            'fon' : Font_MessBulle})
##        for c in self.lstMess:
##            lstMess.append(c)
##            
##        return lstMess
##
##    ####################################################################################################
##    def majLabel(self,lstClef = None):
##        
##        if lstClef is not None:
##            self.lstClef = lstClef
##            
##        lstMess = self.listeMessages()
##        
####        print "  majLabel",self.lstClef,lstMess
####        print " tailles : labels =",len(self.lstLabel)
####        print "           mess =",len(lstMess)
##
##        for i in range(len(self.lstLabel)):
##            txt = lstMess[i]['str']
##            if txt[-1:] == "\n":
##                txt = txt[:-1]
##                packside = TOP
##            else:
##                packside = self.side
##            
##            self.lstLabel[i]['text'] = txt
##            self.lstLabel[i]['font'] = lstMess[i]['fon'][0]
##            self.lstLabel[i]['fg'] = lstMess[i]['fon'][1]
##            
##            self.lstLabel[i].pack(side = packside)
####            print i
##
##        self.attribuerDimensions()
##        
####        print "dimensions =",self.tipwidth,self.tipheight
##
##
##    ####################################################################################################
##    def ajouterLabel(self):
####        print "  ajouter label"
##        self.lstLabel = []
##        for m in range(len(self.lstClef) + len(self.lstMess)):
##            t = Label(self, bg = "lightyellow")
##            self.lstLabel.append(t)
####        print "   ...",len(self.lstLabel)," labels ajoutés"
##        self.majLabel()
##        
##
##
##
##    ####################################################################################################
##    def ajouterFrame(self, numElem):
####        print "  ajouter frame",elemMess
##        
##        t = FrameBulleElem(self, numElem)
##        t.pack()
##
##        self.attribuerDimensions()
##        
##
##    ####################################################################################################
##    def ajouterFrameSpec(self, frameSpec):
##        t = frameSpec
##        t.__init__(self, t.lstObstacles, t.sens)
##
##        self.attribuerDimensions()
##
##
##    ##################################################################################################
##    def attribuerDimensions(self):
##        self.update_idletasks()
##        self.tipwidth = self.winfo_width()
##        self.tipheight =  self.winfo_height()
##
##        
##    ####################################################################################################
##    def delai(self,event):
##        self.x,self.y = event.x,event.y
##        self.action = self.parent.after(self.tps,self.affiche)
##
##
##    ####################################################################################################
##    def affiche(self):
##        self.update_idletasks()
####        print
####        print "Affichage bulle :"
####        print "  dimensions bulle =",self.tipwidth,self.tipheight
##
##        if self.position == "bord":
##            posX = self.parent.winfo_rootx()+self.parent.winfo_width()/2
##            posY = self.parent.winfo_rooty()+self.parent.winfo_height()
##        else:
##            posX = self.parent.winfo_rootx() 
##            posY = self.parent.winfo_rooty()
##
####        print "  position avant =",posX,posY
##
##        # Correction pour que ça rentre dans l'écran
##        if posX + self.tipwidth > self.winfo_screenwidth():          
##            posX = posX - self.tipwidth
##        if posY + self.tipheight > self.winfo_screenheight():
##            if self.position == "bord":
##                posY = self.parent.winfo_rooty() - self.tipheight
##            else:
##                posY = posY - self.tipheight
##
####        print "  position après =",posX,posY
##        #~ print posX,print posY
##        self.geometry('+%d+%d'%(posX,posY))
##        self.deiconify()
##
##    #########################################################################################
##    def efface(self,event):
##        self.withdraw()
##        self.parent.after_cancel(self.action)
##
##

############################################################################################
##class FrameBulleElem(Frame):
##    """ Classe définissant l'info-bulle pour un élément """
##    
##    def __init__(self, master, options):
##
##        Frame.__init__(self, bg = "lightyellow")
##
##        numElem = options['numElem']
##        
##        if 'taille' in options:
##            lstTaille = [options['taille']]
##        else:
##            lstTaille = ["P","G"]
##            
##
##        Label(self, text = listeElements[numElem]['nom'],
##              bg = "lightyellow",
##              font = Font_TitreBulle[0],
##              fg = Font_TitreBulle[1],
##              justify = RIGHT) \
##            .grid(row = 0, column = 0,
##                  columnspan = 4, sticky = W)
##
##        c = 1
##        for t in lstTaille:
##            if t == "P":
##                tx = u"petit"
##            else:
##                tx = u"grand"
##            Label(self, text = tx,
##                  bg = "lightyellow",
##                  justify = RIGHT, anchor = E) \
##                .grid(row = 1, column = c, sticky = E)
##            c += 1
##            
##        if listeElements[numElem]['type'] == "R":
##            Label(self, text = u"Indices de charge admissible :",
##                  bg = "lightyellow",
##                  justify = RIGHT, anchor = E,
##                  font = Font_MessBulleG[0]) \
##                .grid(row = 1, column = 0, sticky = E)
##            Label(self, text = u"axiale :",
##                  bg = "lightyellow",
##                  justify = RIGHT, anchor = E) \
##                .grid(row = 2, column = 0, sticky = E)
##            Label(self, text = u"radiale :",
##                  bg = "lightyellow",
##                  justify = RIGHT, anchor = E) \
##                .grid(row = 3, column = 0, sticky = E)
##            Label(self, text = u"combinée :",
##                  bg = "lightyellow",
##                  justify = RIGHT, anchor = E) \
##                .grid(row = 4, column = 0, sticky = E)
##
##            r = 2
##            c = 1
##            for i in ["axial","radial","combi"]:
##                for t in lstTaille:
##                    Label(self, text = str(coefTaille(listeElements[numElem]['chargeAdm'][i],
##                                                      numElem,t)),
##                          justify = RIGHT, bg = "lightyellow") \
##                        .grid(row = r, column = c)
##                    c += 1
##                Label(self, text = adaptation[listeElements[numElem]['chargeAdm'][i]],
##                      justify = RIGHT, bg = "lightyellow",
##                      font = Font_MessBulleI[0]) \
##                    .grid(row = r, column = c)
##                c = 1
##                r += 1
##
##            Label(self, text = u"Indice de Coût :",
##                  bg = "lightyellow",
##                  justify = RIGHT, anchor = E,
##                  font = Font_MessBulleG[0]) \
##                .grid(row = r, column = 0, sticky = E)
##            c = 1
##            for t in lstTaille:
##                Label(self, text = str(coefTaille(listeElements[numElem]['cout'],
##                                                      numElem,t)),
##                          justify = RIGHT, bg = "lightyellow") \
##                        .grid(row = r, column = c)
##                c += 1
##         
##        else:
##            Label(self, text = u"Indice de charge admissible :",
##                  bg = "lightyellow",
##                  justify = RIGHT, anchor = E,
##                  font = Font_MessBulleG[0]) \
##                .grid(row = 2, column = 0, sticky = E)
##            c = 1
##            for t in lstTaille:
##                Label(self, text = str(coefTaille(listeElements[numElem]['chargeAdm']["axial"],
##                                                  numElem,t)),
##                          justify = RIGHT, bg = "lightyellow") \
##                        .grid(row = 2, column = c)
##                c += 1
##            
##            Label(self, text = u"Indice de Coût :",
##                  bg = "lightyellow",
##                  justify = RIGHT, anchor = E,
##                  font = Font_MessBulleG[0]) \
##                .grid(row = 3, column = 0, sticky = E)
##            c = 1
##            for t in lstTaille:
##                Label(self, text = str(coefTaille(listeElements[numElem]['cout'],
##                                                       numElem,t)),
##                          justify = RIGHT, bg = "lightyellow") \
##                        .grid(row = 3, column = c)
##                c += 1
        
        
        
        

################################################################################
#     Types de charge     #
################################################################################

typeCharge = {0 : u"aucune\ncharge",
              1 : u"charge\npurement axiale",
              2 : u"charge\npurement axiale",
              3 : u"charge\npurement axiale",
              4 : u"charge\npurement radiale",
              5 : u"charge\ncombinée",
              6 : u"charge\ncombinée",
              7 : u"charge\ncombinée"}


adaptation = {0 : u"inadapté",
              1 : u"peu adapté",
              2 : u"satisfaisant",
              3 : u"bon",
              4 : u"excellent"}







################################################################################
# Traductions en textes #
################################################################################

cote2text = {"G" : "gauche",
             "D" : "droit"}


###################################################################################################
palierOppose = {"G" : "D",
                "D" : "G"}

##def cote2txt(cote):
##    if cote == "G":
##        return = u"gauche"
##    elif cote == "D":
##        return = u"droit"
##    else:
##        return


        
