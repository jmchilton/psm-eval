import wx
from numPeaks_panel import *
from peaksMatched_panel import *
from ionsMatched_panel import *
from psmSource_panel import *

class colPanel(wx.Panel):
    # ToDo: When initiating, pass in all list of choices for setting up the choices box
    # ToDo: Error handling
    def __init__(self, parent, colNum):
        wx.Panel.__init__(self, parent, name='colPanel')
        self.SetAutoLayout(True)
        self.colNum = colNum
        self.parent = parent
        
        font1 = wx.Font(9, wx.ROMAN, wx.NORMAL, wx.BOLD)

        self.grid = wx.BoxSizer(wx.VERTICAL)
        self.grid.AddSpacer(5,5)
        self.SetSizer(self.grid)
        
        self.colVal = {}

        # Define other variables / lists /widgets to be used
        # Coltype combobox list
        self.colType = ['Peptide Sequence', 'Scan Index', 'Scan Number', 'Scan ID', 'Peak List', 'Number of Peaks', 'Peaks Matched Statistics', 'Ions Matched Statistics', 'Total Ion Current', 'Statistic from PSM Source', 'Protvis Link']
        self.titles = ['Peptide', 'Scan Index', 'Scan #', 'Scan', 'Peak List', 'Number of Peaks above 2% TIC', 'Aggressively Matched Peaks in Top Third of Peaks Above 2% TIC', 'Ions Matched', 'Total Ion Current']
        self.types = ['peptide', 'scan_index', 'scan_number', 'scan_id', 'scan_source', 'num_peaks', 'peaks_matched', 'ions_matched', 'total_ion_current', 'source_statistic', 'link']
        
        # ToDo: Might need to Get rid of name string for incorrespondence after removing buttons and relabelling
        self.colTypeLbl = wx.StaticText(self, label="Column %d \n \n Column Type:" % self.colNum, name=str(self.colNum))
        self.colTypeLbl.SetFont(font1)
        self.grid.Add(self.colTypeLbl, userData=self.colTypeLbl.GetName())
        self.editColType = wx.ComboBox(self, size=(-1, -1), choices=self.colType, style=wx.CB_DROPDOWN, name=str(self.colNum))
        # Create Column type comboBox
        self.grid.Add(self.editColType, userData=self.editColType.GetName())
        self.editColType.SetValue(self.colType[0])

        self.colVal['title'] = self.titles[0]
        self.colVal['type'] = self.types[0]
        self.parent.columns.insert(self.colNum-1, self.colVal)

        self.Bind(wx.EVT_COMBOBOX, self.EvtColType, self.editColType)
        self.grid.AddSpacer(5,5)
        
        # Remove col button
        self.removeCol = wx.Button(self, label="Remove Column %d" % self.colNum, name=str(self.colNum))
        self.grid.Add(self.removeCol, userData=self.removeCol.GetName())
        self.removeCol.Bind(wx.EVT_BUTTON, self.onRemoveCol, self.removeCol)
        self.grid.AddSpacer(5,5)
        self.Show()
    
    # Remove column event
    def onRemoveCol(self, event):
        parent = self.parent
        del parent.columns[self.colNum-1]
        parent.numCols -= 1
        parent.itemIndex -= 1
        self.Hide()
        parent.FitInside()
        self.Destroy()
        parent.rename()
        parent.parent.Layout()
        
        
    # Helper function for removing childrens when reselecting
    def removeItem(self,event):
        Childrens = self.grid.GetChildren()
        #TODO: complete the list
        nameList = ['pkList', 'pkMatched', 'ionMatched', 'psmSource']
        for child in Childrens:
            if child.GetWindow() != None and child.GetWindow().GetName() in nameList:
                self.grid.Hide(child.GetWindow())
                self.grid.Remove(child.GetWindow())
    
    def EvtColType(self, event):
        self.removeItem(event)
        self.Fit()
        selection = event.GetString()
        if selection==self.colType[0]:
            self.colVal['title'] = self.colType[0]
            self.colVal['type'] = self.types[0]
        if selection==self.colType[1]:
            self.colVal['title'] = self.colType[1]
            self.colVal['type'] = self.types[1]
        if selection==self.colType[2]:
            self.colVal['title'] = self.colType[2]
            self.colVal['type'] = self.types[2]
        if selection==self.colType[3]:
            self.colVal['title'] = self.colType[3]
            self.colVal['type'] = self.types[3]
        if selection==self.colType[4]:
            self.colVal['title'] = self.colType[4]
            self.colVal['type'] = self.types[4]
        if selection==self.colType[5]:
            self.colVal['title'] = self.colType[5]
            self.colVal['type'] = self.types[5]
            self.handleNumPeaks(event)
        if selection==self.colType[6]:
            self.colVal['title'] = self.colType[6]
            self.colVal['type'] = self.types[6]
            self.colVal['ions_ref'] = 'aggressive'
            self.colVal['mass_tolerance'] = 1.5
            self.handlePeaksMatched(event)
        if selection==self.colType[7]:
            self.colVal['title'] = self.colType[7]
            self.colVal['type'] = self.types[7]
            self.handleIonsMatched(event)
        if selection==self.colType[8]:
            self.colVal['title'] = self.colType[8]
            self.colVal['type'] = self.types[8]  
        if selection==self.colType[9]:
            self.colVal['title'] = self.colType[9]
            self.colVal['type'] = self.types[9]
            self.handlePSM(event)
        

    def handleNumPeaks(self, event):
        self.grid.Add(numPeaksPanel(self), wx.EXPAND)
        self.Fit()
        self.parent.Fit()
        self.parent.parent.Layout()

    def handlePeaksMatched(self, event):
        self.grid.Add(peaksMatchedPanel(self), wx.EXPAND)
        self.Fit()
        self.parent.Fit()
        self.parent.parent.Layout()
    
    def handleIonsMatched(self, event):
        self.grid.Add(ionsMatchedPanel(self), wx.EXPAND)
        self.Fit()
        self.parent.Fit()
        self.parent.parent.Layout()
    
    def handlePSM(self, event):
        self.grid.Add(psmSourcePanel(self), wx.EXPAND)
        self.Fit()
        self.parent.Fit()
        self.parent.parent.Layout()
    
