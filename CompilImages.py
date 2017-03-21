#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##This file is part of PyVot
#############################################################################
#############################################################################
##                                                                         ##
##                                  CompilImages                           ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2006-2008 Cédrick FAURY

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

# Programme de compilation des images .png en un unique fichier icones.py
#
# !!!  Effacer toutes les lignes de icones.py après la remarque :
#          " Supprimer tout ce qui suit avant compilation "
#


#from img2py import *
import wx.tools.img2py

# Dossiers ##########################################################################################
dosImg = {'root'       : "Images/",
          'compil'     : "_Pour compil/",
          'arrets'     : "Arrets/",
          'roulements' : "Roulements/",
          'boutons'    : "Boutons/",
          'arbrales'   : "Arbre_Alesage/",
          'joints'     : "Joints/",
          'schema'     : "Schema/",
          'icones'     : "Icones/"}
dosbout = dosImg['root']+dosImg['compil']+dosImg['boutons']
dosarr = dosImg['root']+dosImg['arrets']
dosjnt = dosImg['root']+dosImg['joints']
dosCompil = dosImg['root']+dosImg['compil']
dosbout = dosCompil+dosImg['boutons']
dosicon = dosCompil+dosImg['icones']

# Fichier de sortie
fichIcone = "src/Icones.py"

#Images diverses
FichiersDivers = {'BagueTournExt'   : dosCompil + 'BT_Ext.png',
                  'BagueTournInt'   : dosCompil + 'BT_Int.png',
                  'LubrifHuile'     : dosCompil + 'Lubrif huile.png',
                  'LubrifGraisse'   : dosCompil + 'Lubrif graisse.png',
                  }

# Fichiers Icone & Logo #############################################################################
FichiersImage = {'IconeFenetre' : dosCompil + 'logo32b.ico',
                 'LogoSplash'   : dosCompil + "logo 0.6.png"}

# Boutons Elements ##################################################################################
FichiersBoutonsElem = {0 : dosbout + "Bouton_RoulementBilleRadial.png",
                       1 : dosbout + "Bouton_RoulementBilleOblique.png",
                       2 : dosbout + "Bouton_RoulementRotuleBilles.png",
                       3 : dosbout + "Bouton_RoulementButeeBilles.png",
                       4 : dosbout + "Bouton_RoulementRouleauxCyl.png",
                       5 : dosbout + "Bouton_RoulementRouleauxConiques.png",
                       6 : dosbout + "Bouton_RoulementRotuleRouleaux.png",
                       7 : dosbout + "Bouton_RoulementButeeRouleaux.png",
                       8 : dosbout + "Bouton_RoulementButeeBillesDbl.png",
                       9 : dosbout + "Bouton_RoulementButeeRouleauxDbl.png",
                       10: dosbout + "Bouton_RoulementBilleObliqueDbl.png",
                       11: dosbout + "Bouton_RoulementRouleauxDbl.png",
               
                     100 : dosbout + "Bouton_ArretElemFiletes.png",
                     101 : dosbout + "Bouton_ArretAnneauElastique.png",
                     102 : dosbout + "Bouton_ArretEpaulement.png",
                     103 : dosbout + "Bouton_ArretEntretoise.png",

                     200 : dosbout + "Bouton_Joint1Levre.png",
                     201 : dosbout + "Bouton_JointTorique.png",
                     202 : dosbout + "Bouton_JointChapeau.png",
                     203 : dosbout + "Bouton_Chicanes.png",
                     204 : dosbout + "Bouton_JointPlat.png"
                     }


# Bouton de la barre d'outil ########################################################################
dos = dosImg['root']+dosImg['boutons']
Bouton = {'RAZ'         : dosbout + "Bouton_RAZ.png",
          'Analyser'    : dosbout + "Bouton_Analyser.png",
          'Ouvrir'      : dosbout + "Bouton_Ouvrir.png",
          'Enregistrer' : dosbout + "Bouton_Enregistrer.png",
          'Imprimer'    : dosbout + "Bouton_Imprime.png",
          'Retourner'   : dosbout + "Bouton_Retourner.png",
          'CdCF'        : dosbout + "Bouton_CdCF.png",
          'Rapport'     : dosbout + "Bouton_Rapport.png",
          }

# Icones divers ########################################################################
IconesDivers = {'Valider'    : dosicon + "Valider.png",
                'Annuler'    : dosicon + "Annuler.png",
                }

# Icones de l'arbre de montage ########################################################################
Icones = {'code'          : dosicon + "Icone_CdCF.png",
          'Proprietes'    : dosicon + "Icone_CdCF.png",
          'Structure'     : dosicon + "Icone_CdCF.png",
          'Etancheite'    : dosicon + "Icone_CdCF.png",
          'CdCF'          : dosicon + "Icone_CdCF.png",
          'Specifications': dosicon + "Icone_CdCF.png"
          }

# Icones de l'arbre des boutons ########################################################################
IconesElem = {'Roults'    : dosicon + "Ensemble Rlts.png",
              'Arrets'    : dosicon + "Ensemble Arrets.png",
              'Joints'    : dosicon + "Ensemble Joints.png",
              }

# Icones de l'arbre d'analyse ########################################################################
IconesAnal = {'AnalysArret'    : dosicon + "Analyse_Arret.png",
              'AnalysEffort'    : dosicon + "Analyse_Effort.png",
              'AnalysMonta'    : dosicon + "Analyse_Monta.png",
              'AnalysEtanch'    : dosicon + "Analyse_Etanch.png",
              'AnalysDevis'    : dosicon + "Analyse_Devis.png",
              }

# Bouton de l'analyse de la Montabilité ################################################################
BoutonMont = {'AnimEnsb0Ar' : dosbout + "AnalyseMontage_Ens_0_Ar.png",
              'AnimEnsb1Ar' : dosbout + "AnalyseMontage_Ens_1_Ar.png",
              'AnimEnsb0Al' : dosbout + "AnalyseMontage_Ens_1_Al.png",
              'AnimEnsb1Al' : dosbout + "AnalyseMontage_Ens_0_Al.png",
              
              'AnimRltG0Ar' : dosbout + "AnalyseMontage_Rlt_G_0_Ar.png",
              'AnimRltG1Ar' : dosbout + "AnalyseMontage_Rlt_G_1_Ar.png",
              'AnimRltG0Al' : dosbout + "AnalyseMontage_Rlt_G_0_Al.png",
              'AnimRltG1Al' : dosbout + "AnalyseMontage_Rlt_G_1_Al.png",

              'AnimRltD0Ar' : dosbout + "AnalyseMontage_Rlt_D_0_Ar.png",
              'AnimRltD1Ar' : dosbout + "AnalyseMontage_Rlt_D_1_Ar.png",
              'AnimRltD0Al' : dosbout + "AnalyseMontage_Rlt_D_0_Al.png",
              'AnimRltD1Al' : dosbout + "AnalyseMontage_Rlt_D_1_Al.png",

              'AnimEnsb0ArR' : dosbout + "AnalyseMontage_Ens_0_Ar_R.png",
              'AnimEnsb1ArR' : dosbout + "AnalyseMontage_Ens_1_Ar_R.png",
              'AnimEnsb0AlR' : dosbout + "AnalyseMontage_Ens_1_Al_R.png",
              'AnimEnsb1AlR' : dosbout + "AnalyseMontage_Ens_0_Al_R.png",
              
              'AnimRltG0ArR' : dosbout + "AnalyseMontage_Rlt_G_0_Ar_R.png",
              'AnimRltG1ArR' : dosbout + "AnalyseMontage_Rlt_G_1_Ar_R.png",
              'AnimRltG0AlR' : dosbout + "AnalyseMontage_Rlt_G_0_Al_R.png",
              'AnimRltG1AlR' : dosbout + "AnalyseMontage_Rlt_G_1_Al_R.png",

              'AnimRltD0ArR' : dosbout + "AnalyseMontage_Rlt_D_0_Ar_R.png",
              'AnimRltD1ArR' : dosbout + "AnalyseMontage_Rlt_D_1_Ar_R.png",
              'AnimRltD0AlR' : dosbout + "AnalyseMontage_Rlt_D_0_Al_R.png",
              'AnimRltD1AlR' : dosbout + "AnalyseMontage_Rlt_D_1_Al_R.png",

              'SensInterditE' : dosbout + "Sens_interdit_80x45.png",
              'SensInterditR' : dosbout + "Sens_interdit_50x45.png",

              'Chaine0' : dosbout + "AnalyseChaine0.png",
              'Chaine1' : dosbout + "AnalyseChaine1.png",

              '_Chaine0' : dosbout + "AnalyseChaine0.png",
              '_Chaine1' : dosbout + "AnalyseChaine1.png",

              'Arret0' : dosbout + "AnalyseArret0.png",
              'Arret1' : dosbout + "AnalyseArret1.png",

              'BagueIsolee' : dosbout + "Bouton_BagueIsolee.png"}


#####################################################################################################
# Compilation de tout ca ..........

for idFichierImage in FichiersDivers.keys():
    wx.tools.img2py.img2py(FichiersDivers[idFichierImage], fichIcone,
           imgName = str(idFichierImage),
           append = True, icon = True)

for idFichierImage in FichiersBoutonsElem.keys():
    wx.tools.img2py.img2py(FichiersBoutonsElem[idFichierImage], fichIcone,
           imgName = str(idFichierImage),
           append = True, icon = True)
    
for idFichierImage in FichiersImage.keys():
    wx.tools.img2py.img2py(FichiersImage[idFichierImage], fichIcone, 
           imgName = idFichierImage,
           append = True, icon = True)
    
for idFichierImage in Bouton.keys():
    wx.tools.img2py.img2py(Bouton[idFichierImage], fichIcone,
           imgName = "Bout_"+idFichierImage,
           append = True, icon = True)
    
for idFichierImage in Icones.keys():
    wx.tools.img2py.img2py(Icones[idFichierImage], fichIcone,
           imgName = "Icon_"+idFichierImage,
           append = True, icon = True)
    
for idFichierImage in IconesDivers.keys():
    wx.tools.img2py.img2py(IconesDivers[idFichierImage], fichIcone,
           imgName = "Icon_"+idFichierImage,
           append = True, icon = True)
    
for idFichierImage in IconesElem.keys():
    wx.tools.img2py.img2py(IconesElem[idFichierImage], fichIcone,
           imgName = "Icon_"+idFichierImage,
           append = True, icon = True)
    
for idFichierImage in IconesAnal.keys():
    wx.tools.img2py.img2py(IconesAnal[idFichierImage], fichIcone,
           imgName = "Icon_"+idFichierImage,
           append = True, icon = True)
    
for idFichierImage in BoutonMont.keys():
    wx.tools.img2py.img2py(BoutonMont[idFichierImage], fichIcone,
           imgName = "Bout_"+idFichierImage,
           append = True, icon = True)
    