#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##This file is part of PyVot
#############################################################################
#############################################################################
##                                                                         ##
##                             ElementTable                                ##
##                                                                         ##
#############################################################################
#############################################################################

## Copyright (C) 2009 Cédrick FAURY

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

import  wx
import  wx.grid as gridlib
import Icones
import ConfigParser as cp
import globdef
import os, os.path

#---------------------------------------------------------------------------
#FICHIER_ELEMENTS = "Elements.txt"
PATH_ELEMENTS = os.path.join(globdef.PATH,"Donnees")
EXT_ELEMENTS = '.txt'

#
#FICHIER_ROULEMENTS = "Roulements.txt"
#FICHIER_ARRETS = "Arrets.txt"
#FICHIER_JOINTS = "Joints.txt"

def estFichierElem(fichier):
#    print "test", fichier
    elemparser = ElementParser()
    parser = cp.ConfigParser()
    try:
        parser.read(fichier)
    except:
        return False
#    print parser.sections()
    for s in elemparser.sect:
        if not parser.has_section(s):
            return False
    return True
#    except :
#        return False


class ElementsDataTable(gridlib.PyGridTableBase):
    def __init__(self):
        gridlib.PyGridTableBase.__init__(self)

        self.data = []
        
        self.modifie = False
        
#        try:
#            self.ReadData()
#        except IOError:
#            print self.fichier

    def SetData_(self, lstData):
        data = []
        for liste in lstData:
            lst = []
            for i in range(len(self.dataTypes)):
                dataType = self.dataTypes[i].split(':')[0]
                try :
                    val = liste[i]
                except:
                    val = '0'
                if dataType == gridlib.GRID_VALUE_NUMBER:
                    lst.append(eval(val))
                elif dataType == gridlib.GRID_VALUE_STRING:
                    if type(val) == str:
                        lst.append(unicode(val,'latin_1'))
                    elif type(val) == unicode:
                        lst.append(val)
                elif dataType == gridlib.GRID_VALUE_BOOL:
                    lst.append(val == '1')
            data.append(lst)
            
        self.data = data
    def SetData(self, lstData):
        
        self.SetData_(lstData)
        
        # tell the grid we've added a row
        msg = gridlib.GridTableMessage(self,            # The table
                gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, # what we did to it
                self.GetNumberRows()                    # how many
                )
        self.GetView().ProcessTableMessage(msg)
#        print self.data

#    def ReadData(self, fichier):
#        test_file = fichier
#        file = open(test_file,'r',1)
#        i = 0
#        print "Lecture :"
#        
#        def convertir(liste):
#            lst = []
#            for i in range(len(self.dataTypes)):
#                dataType = self.dataTypes[i].split(':')[0]
#                try :
#                    val = liste[i]
#                except:
#                    val = '0'
##                print i, val
#                if dataType == gridlib.GRID_VALUE_NUMBER:
#                    lst.append(eval(val))
#                elif dataType == gridlib.GRID_VALUE_STRING:
#                    lst.append(val)
#                elif dataType == gridlib.GRID_VALUE_BOOL:
#                    lst.append(val == '1')
#            return lst
#        
#        
#        data = []
#        while 1:
#            text = file.readline()
#            print text
#            text = text.strip()
#            if not text:
#                break
#
#            list_val = text.split('\t')
##            print list_val
#            list_val = convertir(list_val)
##            print list_val
#            data.append(list_val)
#        file.close()
#        
#        self.data = data
#        print self.data
#        
#        
#    def SaveData(self):
#        test_file = self.fichier
#        file = open(test_file,'w',1)
#        i = 0
#        print "Enregistrement :"
#        
#        def toStr(e):
#            if e == None or e == '':
#                return "0"
#            elif type(e) == str:
#                return e
#            elif type(e) == int:
#                return str(e)
#            elif type(e) == bool:
#                if e : return "1"
#                else: return "0"
#            else :
#                return str(e)
#            
#        for line in self.data:
#            st = ''
#            for e in line:
#                st += toStr(e) + '\t'
#            st = st[:-1]+'\n'
#            print st
#            file.write(st)
#        
#        file.close()
#        self.modifie = False

    #--------------------------------------------------
    # required methods for the wxPyGridTableBase interface

    def GetNumberRows(self):
        return len(self.data) 

    def GetNumberCols(self):
        return len(self.colLabels)

    def IsEmptyCell(self, row, col):
        try:
            return not self.data[row][col]
        except IndexError:
            return True

    # Get/Set values in the table.  The Python version of these
    # methods can handle any data-type, (as long as the Editor and
    # Renderer understands the type too,) not just strings as in the
    # C++ version.
    def GetValue(self, row, col):
        try:
            return self.data[row][col]
        except IndexError:
            return ''

    def SetValue(self, row, col, value):
#        print "SetValue", row,col
        def innerSetValue(row, col, value):
            try:
                self.data[row][col] = value
            except IndexError:
                # add a new row
                self.data.append([''] * self.GetNumberCols())
                innerSetValue(row, col, value)

                # tell the grid we've added a row
                msg = gridlib.GridTableMessage(self,            # The table
                        gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, # what we did to it
                        1                                       # how many
                        )

                self.GetView().ProcessTableMessage(msg)
#        innerSetValue(row, col, value)
        self.data[row][col] = value
        self.modifie = True
    #--------------------------------------------------
    # Some optional methods

    # Called when the grid needs to display labels
    def GetColLabelValue(self, col):
        return self.colLabels[col]

    # Called to determine the kind of editor/renderer to use by
    # default, doesn't necessarily have to be the same type used
    # natively by the editor/renderer if they know how to convert.
    def GetTypeName(self, row, col):
        return self.dataTypes[col]

    # Called to determine how the data can be fetched and stored by the
    # editor and renderer.  This allows you to enforce some type-safety
    # in the grid.
    def CanGetValueAs(self, row, col, typeName):
        colType = self.dataTypes[col].split(':')[0]
        if typeName == colType:
            return True
        else:
            return False

    def CanSetValueAs(self, row, col, typeName):
        return self.CanGetValueAs(row, col, typeName)


    def Ajouter(self):
#        print "Ajouter"
        self.data.append([''] * self.GetNumberCols())

        # tell the grid we've added a row
        msg = gridlib.GridTableMessage(self,            # The table
                gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, # what we did to it
                1                                       # how many
                )

        self.GetView().ProcessTableMessage(msg)
        
    def DeleteRows(self, pos = 0, numRows = 1, updateLabels = True):
#        print "Delete"
        
        return True

    def Clear(self):
#        print "Clear"
        n = self.GetNumberRows()
        self.data = []
        msg = wx.grid.GridTableMessage(self,
                                       wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED,
                                       0, n)
                                       #prevNumRows - newNumRows)
        self.GetView().ProcessTableMessage(msg) 
#        self.Clear()
        return True
    
    def Import(self, dicElem):     
        listeData = []
        for key, val in dicElem.items():
#            print val
            lstData = []
            lstData.append(str(key))
            lstData.append(val['nom'])
            
            if val['type'] == 'R':
                lstData.append(str(val['chargeAdm']['radial']))
                lstData.append(str(val['chargeAdm']['axial']))
                lstData.append(str(val['chargeAdm']['combi']))
                if 'orientation' in val:
                    lstData.append('1')
                else:
                    lstData.append('0')
                lstData.append('0')
            
            elif val['type'] == 'A':
                lstData.append(str(val['chargeAdm']['axial']))
                if 'I' in val['pos']:
                    lstData.append('1')
                else:
                    lstData.append('0')
                
                if 'E' in val['pos']:
                    lstData.append('1')
                else:
                    lstData.append('0')
                    
            elif val['type'] == 'J':
                if 'Al' in val['pos']:
                    lstData.append('1')
                else:
                    lstData.append('0')
                
                if 'Ar' in val['pos']:
                    lstData.append('1')
                else:
                    lstData.append('0')
                
                for k in ['Ar', 'Al']:
                    if k in val['pressAdm'].keys():
                        lstData.append(str(val['pressAdm'][k]))
                    else:
                        lstData.append('0')
                
                lstData.append(str(val['vittAdm']))
                lstData.append(str(val['facteurPV']))
            
            lstData.append(str(val['cout']))
            
            listeData.append(lstData)
#            print lstData
#        print listeData
#        listeData.sort(cmp=lambda x,y : cmp(x[0],y[0]))
#        print listeData
        self.SetData(listeData)
        
    def Export(self, dicElem):
        for l in self.data:
            num = l[0]
            pElem = dicElem[num]
            pElem['nom'] = l[1]
            pElem['type']

            if pElem['type'] == 'R':
                pElem['chargeAdm']['radial'] = l[2]
                pElem['chargeAdm']['axial']  = l[3]
                pElem['chargeAdm']['combi']  = l[4]
                pElem['cout'] = l[7]
                
            elif pElem['type'] == 'A':
                pElem['chargeAdm']['axial'] = l[2]
                pElem['pos'] = ''
                if l[3]:
                    pElem['pos'] += 'I'
                if l[4]:
                    pElem['pos'] += 'E'
                pElem['cout'] = l[5]
                    
            elif pElem['type'] == 'J':
                pElem['pos'] = []
                if l[2]:
                    pElem['pos'].append('Al')
                if l[3]:
                    pElem['pos'].append('Ar')
                
                i=4
                for k in ['Ar', 'Al']:
                    if k in pElem['pressAdm'].keys():
                        pElem['pressAdm'][k] = l[i] 
                    i += 1
                
                pElem['vittAdm'] = l[6] 
                pElem['facteurPV'] = l[7] 
                
                pElem['cout'] = l[8]
            
    
#---------------------------------------------------------------------------

class RoulementsDataTable(ElementsDataTable):
    def __init__(self):
        
        self.colLabels = [u'ID', u'Nom', u'Charge\nadmissible\nradiale', u'Charge\nadmissible\naxiale',
                          u'Charge\nadmissible\ncombinée',
                          u"Contact\noblique", u"Bagues\nséparables", u'Coût']


        self.dataTypes = [gridlib.GRID_VALUE_NUMBER + ':0,99',
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_NUMBER + ':0,10',
                          gridlib.GRID_VALUE_NUMBER + ':0,10',
                          gridlib.GRID_VALUE_NUMBER + ':0,10',
                          gridlib.GRID_VALUE_BOOL,
                          gridlib.GRID_VALUE_BOOL,
                          gridlib.GRID_VALUE_NUMBER,
                          ]
        ElementsDataTable.__init__(self)
        

class ArretsDataTable(ElementsDataTable):
    def __init__(self):
        
        self.colLabels = [u'ID', u'Nom', u'Charge\nadmissible\naxiale',
                          u"Intérieur", u"Extérieur", u'Coût']

        self.dataTypes = [gridlib.GRID_VALUE_NUMBER + ':100,199',
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_NUMBER + ':0,10',
                          gridlib.GRID_VALUE_BOOL,
                          gridlib.GRID_VALUE_BOOL,
                          gridlib.GRID_VALUE_NUMBER,
                          ]
        ElementsDataTable.__init__(self)
       
        
class JointsDataTable(ElementsDataTable):
    def __init__(self):
        
        self.colLabels = [u'ID', u'Nom', u'Etanchéité\nStatique', u'Etanchéité\nDynamique',
                          u"Pression\nadmissible\narbre", u"Pression\nadmissible\nalésage",
                          u"Vitesse\nadmissible", u"Produit PV\nadmissible",
                          u'Coût']

        self.dataTypes = [gridlib.GRID_VALUE_NUMBER + ':200,299',
                          gridlib.GRID_VALUE_STRING,
                          gridlib.GRID_VALUE_BOOL,
                          gridlib.GRID_VALUE_BOOL,
                          gridlib.GRID_VALUE_NUMBER,
                          gridlib.GRID_VALUE_NUMBER,
                          gridlib.GRID_VALUE_NUMBER,
                          gridlib.GRID_VALUE_NUMBER,
                          gridlib.GRID_VALUE_NUMBER,
                          ]
        ElementsDataTable.__init__(self)
       

class ElementsTableGrid(gridlib.Grid):
    def __init__(self, parent, table):
        gridlib.Grid.__init__(self, parent, -1)

        self.table = table

        # The second parameter means that the grid is to take ownership of the
        # table and will destroy it when done.  Otherwise you would need to keep
        # a reference to it and call it's Destroy method later.
        self.SetTable(self.table, True)

        self.SetRowLabelSize(0)
        self.SetMargins(0,0)
        self.AutoSizeColumns(True)
        self.AutoSizeRows(True)
        self.SetColLabelSize(-1)#gridlib.GRID_AUTOSIZE)

        gridlib.EVT_GRID_CELL_LEFT_DCLICK(self, self.OnLeftDClick)

    def MarquerColReadOnly(self, lstCol):
        attr = wx.grid.GridCellAttr()
        attr.SetReadOnly(True)
        for c in lstCol:
            self.SetColAttr(c, attr)

    # I do this because I don't like the default behaviour of not starting the
    # cell editor on double clicks, but only a second click.
    def OnLeftDClick(self, evt):
        if self.CanEnableCellControl():
            self.EnableCellEditControl()

    def Ajouter(self):
        self.table.Ajouter()
        
    def Import(self, dicElem):
        self.table.Import(dicElem)
#---------------------------------------------------------------------------

class ElementGridFrame(wx.Frame):
    def __init__(self, parent, lstElements = None, lstFamilles = None, fichier = ''):

        wx.Frame.__init__(
            self, parent, -1, u"Table des éléments"#, size=(640,480)
            )
        self.parent = parent
        self.parser = ElementParser()
        self.fichier = fichier
        
        p = wx.Panel(self, -1, style=0)
        
        bar = wx.BoxSizer(wx.HORIZONTAL)
        
        # Les boutons
        bOk = wx.BitmapButton(p, 1, Icones.getIcon_ValiderBitmap(), style = wx.NO_BORDER)
        bNo = wx.BitmapButton(p, 2, Icones.getIcon_AnnulerBitmap(), style = wx.NO_BORDER)
        self.Bind(wx.EVT_BUTTON, self.OnButton, bOk)
        self.Bind(wx.EVT_BUTTON, self.OnButton, bNo)
        bar.Add(bOk)
        bar.Add(bNo)
        
        # Le combobox
        sb1 = wx.StaticBox(p, -1, u'Propriétés personnalisées')
        sbs1 = wx.StaticBoxSizer(sb1, wx.HORIZONTAL)
           
        cbID = wx.NewId()
        self.combo = wx.ComboBox(
                p, cbID, self.fichier, choices=listeFichiersElem(),
                size=(150,-1), style=wx.CB_DROPDOWN
                )
        self.Bind(wx.EVT_COMBOBOX, self.OnCombo, id=cbID)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnText, id=cbID)
        self.Bind(wx.EVT_TEXT, self.OnText, id=cbID)
        
        sbs1.Add(self.combo)
        bar.Add(sbs1)
        
        self.nb = wx.Notebook(p, -1)
        
        self.pages = [ElementsTableGrid(self.nb, RoulementsDataTable()),
                      ElementsTableGrid(self.nb, ArretsDataTable()),
                      ElementsTableGrid(self.nb, JointsDataTable()) ]
        
        self.pages[0].MarquerColReadOnly([0,5,6])
        self.pages[1].MarquerColReadOnly([0,3,4])
        self.pages[2].MarquerColReadOnly([0,2,3])
        
        #
        # On rempli les tableaux ...
        #
        if lstElements != None and lstFamilles != None:
            self.Importer(lstElements, lstFamilles)
        else:
            self.Open(fichier = self.fichier)
        
        self.nb.AddPage(self.pages[0], u"Roulements")
        self.nb.AddPage(self.pages[1], u"Arrêts")
        self.nb.AddPage(self.pages[2], u"Joints")

        bs = wx.BoxSizer(wx.VERTICAL)
        bs.Add(bar)
        bs.Add(self.nb, 1, wx.GROW|wx.ALL, 5)
#        bar.Layout()
#        bs.Layout()
        
        p.SetSizerAndFit(bs)
        self.SetClientSize(p.GetSize())
#        self.SetToolBar(self.tb)
        p.Refresh()
        self.Bind(wx.EVT_CLOSE, self.OnQuit )
        

    def Importer(self, lstElements, lstFamilles):
        """ Import des propriétés par défaut des éléments
        """
        
        def LstId(lst, concat = False):
            li = []
            for l in lst:
                if type(l[1][1]) == list:
                    li.append(LstId(l[1], True))
                else:
                    if concat:
                        li.extend(l[1])
                    else:
                        li.append(l[1])       
            return li
            
        lstId = LstId(lstFamilles)
        
        lstEl = []
        for l in lstId:
            d = {}
            for k,v in lstElements.items():
                if k in l:
                    d[k] = v
            lstEl.append(d)        
        
        for i in range(len(self.pages)):
#                print lstEl[i]
            self.pages[i].Import(lstEl[i])
            self.pages[i].AutoSizeColumns(True)
            self.pages[i].AutoSizeRows(True)
    
               

    def OnText(self, event):
#        self.New()
        fichier = event.GetString()
        self.fichier = fichier
#        print "Fichier courant :", self.fichier
        
    def OnCombo(self, event):
#        print "Fichier courant :", self.fichier
        self.New()
        fichier = event.GetString()
        self.Open(fichier)

    def OnButton(self, evt):
        if evt.GetId() == 1:
            if self.OnSaveClick():
                self.parent.SetFichier(self.fichier)
                self.Destroy()
        elif evt.GetId() == 2:
            self.OnQuit()
        

    def OnButtonFocus(self, evt):
        pass
#        print "button focus"

    ######################################################################################################
    def New(self):
#        print "Nouveau"
        self.Save(self.fichier)
        for p in self.pages:
#            p.table.Clear()
#            p.table.data = []
            p.ClearGrid()
#            self.nb.GetCurrentPage().ForceRefresh()
#            print p.GetNumberRows()
#            p.DeleteRows(0,p.GetNumberRows())
            
        self.fichier = ''

    def OnNewClick(self, evt):
        self.New()
    
    ######################################################################################################
    def Open(self, fichier):
        self.parser = ElementParser()
        self.parser.read(os.path.join(PATH_ELEMENTS,fichier+EXT_ELEMENTS))
        rlt, arr, jnt = self.parser.getAll()
        
        rlt.sort(cmp=lambda x,y : cmp(x[0],y[0]))
        arr.sort(cmp=lambda x,y : cmp(x[0],y[0]))
        jnt.sort(cmp=lambda x,y : cmp(x[0],y[0]))
        
        self.pages[0].table.SetData(rlt)
        self.pages[1].table.SetData(arr)
        self.pages[2].table.SetData(jnt) 
#        self.nb.GetCurrentPage().ForceRefresh()
        self.fichier = fichier
        
        for p in self.pages:
            p.AutoSizeColumns(True)
            p.AutoSizeRows(True)
#        print "Fichier ouvert :", self.fichier
#        print rlt
#        print self.pages[0].table.data
        
    def OnOpenClick(self, evt):
        if self.fichier != '':
            self.Open(self.fichier)
    
    ######################################################################################################
    def Save(self, fichier):
#        print self.pages[0].table.data
        self.parser.setAll(self.pages[0].table.data, 
                           self.pages[1].table.data,
                           self.pages[2].table.data)
        self.parser.write(open(os.path.join(PATH_ELEMENTS,fichier+EXT_ELEMENTS), 'w'))
        self.combo.Clear()
        myList = [1,2,3,4,5]
        for item in listeFichiersElem():
            self.combo.Append(item) 
        
        
    def OnSaveClick(self, evt = None):
        if self.fichier != '':
            self.Save(self.fichier)
            return True
        else:
            dlg = wx.MessageDialog(self, u'Choisissez un nom de propriétés !',
                               u'Nom de propriétés',
                               wx.OK | wx.ICON_EXCLAMATION 
                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
            dlg.ShowModal()
            dlg.Destroy()
            return False
    
    ######################################################################################################
    def OnAjouterClick(self, evt):
        self.nb.GetCurrentPage().Ajouter()
           
    def OnQuit(self, event = None):
#        print "Quitter !!!!!!"
#        self.options.enregistrer()
#        event.Skip()

        pagesModifiees = []    
        for p in self.pages:
            if p.table.modifie:
                pagesModifiees.append(p)
                
        if pagesModifiees == []:
            self.Destroy()
            return
        
        texte = u"Le tableau à été modifié.\nVoulez vous enregistrer les changements ?"
        
        dialog = wx.MessageDialog(self, texte, 
                                  "Confirmation", wx.YES_NO | wx.CANCEL | wx.ICON_WARNING)
        retCode = dialog.ShowModal()
        if retCode == wx.ID_YES:
            for p in pagesModifiees:
                p.table.SaveData()
            self.Destroy()
        elif retCode == wx.ID_NO:
            self.Destroy()
            
def listeFichiersElem():
    try:
        listeFichiers = os.listdir(PATH_ELEMENTS)
        listeFichTxt = []
        for f in listeFichiers:
            if os.path.splitext(f)[1] == EXT_ELEMENTS:
                if estFichierElem(os.path.join(PATH_ELEMENTS, f)):
                   listeFichTxt.append(os.path.splitext(f)[0])
    #    print listeFichTxt
        return listeFichTxt
    except:
        return []
 
def Exporter(fichier, lstElements):
#    print "Export depuis :", fichier
    parser = ElementParser()
    parser.read(PATH_ELEMENTS+fichier+EXT_ELEMENTS)
    rlt, arr, jnt = parser.getAll()
#    print rlt
    tableRlt = RoulementsDataTable()
    tableArr = ArretsDataTable()
    tableJnt = JointsDataTable()
    tableRlt.SetData_(rlt)
    tableArr.SetData_(arr)
    tableJnt.SetData_(jnt)
    tableRlt.Export(lstElements)
    tableArr.Export(lstElements)
    tableJnt.Export(lstElements)
    
    


class ElementParser(cp.SafeConfigParser):
    def __init__(self, *args, **kw):
        cp.SafeConfigParser.__init__(self, *args, **kw)
        
        self.sect = ["Roulements", "Arrets", "Joints"]
        for s in self.sect:
            self.add_section(s)

        
    def _set(self, section, valeur):
        
        def toStr(e):
            if e == None or e == '':
                return "0"
            elif type(e) == str:
                return e
            elif type(e) == unicode:
                return e
            elif type(e) == int:
                return str(e)
            elif type(e) == bool:
                if e : return "1"
                else: return "0"
            else :
                return str(e)
        
        def lstToStr(lst):
            s = ''
            for i in lst:
                s += toStr(i) + '\t'
            return s[:-1]
#        print "Set", section, valeur
        if type(valeur) == list:
            for l in valeur:
#                print l[0]
#                print type(lstToStr(l[1:]))
                uni = lstToStr(l[1:]).encode('latin_1')#('iso8859_2')
                self.set(section, str(l[0]), uni)
#        else:
#            self.set(section, clef, valeur)
    
    def _get(self, section, clef = None):
        if clef == None:
            liste = []
            for l in self.options(section):
                ssLst = []
                ssLst.append(l)
                for c in self.get(section, l).split('\t'):
                    ssLst.append(c)
                liste.append(ssLst)
#            print section, liste
            return liste
        else:
            return self.get(section, clef)
                
    def isOk(self):
        for s in self.sect:
            if not self.has_section(s):
                return False
        return True
    
    
    def setAll(self, rlt, arr, jnt):
        self._set("Roulements", rlt)
        self._set("Arrets", arr)
        self._set("Joints", jnt)
        
        
    def getAll(self):
        return self._get("Roulements"), self._get("Arrets"), self._get("Joints")
        
#    def read(self, fichier):
#        pass
#    
#    def write(self, fichier):
#---------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    app = wx.PySimpleApp()
    frame = ElementGridFrame(None)
    frame.Show(True)
    app.MainLoop()


#---------------------------------------------------------------------------
