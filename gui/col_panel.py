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
        
        # Define other variables / lists /widgets to be used
        # Coltype combobox list
        self.colType = ['Peptide Sequence', 'Scan Index', 'Scan Number', 'Scan ID', 'Peak List', 'Number of Peaks', 'Peaks Matched Statistics', 'Ions Matched Statistics', 'Total Ion Current', 'Statistic from PSM Source', 'Protvis Link']
        
        # ToDo: Might need to Get rid of name string for incorrespondence after removing buttons and relabelling
        self.colTypeLbl = wx.StaticText(self, label="Column %d \n \n Column Type:" % self.colNum, name=str(self.colNum))
        self.colTypeLbl.SetFont(font1)
        self.grid.Add(self.colTypeLbl, userData=self.colTypeLbl.GetName())    
        self.editColType = wx.ComboBox(self, size=(-1, -1), choices=self.colType, style=wx.CB_DROPDOWN, name=str(self.colNum))
        # Create Column type comboBox
        self.grid.Add(self.editColType, userData=self.editColType.GetName())
        self.Bind(wx.EVT_COMBOBOX, self.EvtColType, self.editColType)
        self.grid.AddSpacer(5,5)
        
        # Remove col button
        self.removeCol = wx.Button(self, label="Remove Column %d" % self.colNum, name=str(self.colNum))
        self.grid.Add(self.removeCol, userData=self.removeCol.GetName())
        self.removeCol.Bind(wx.EVT_BUTTON, self.onRemoveCol)
        self.grid.AddSpacer(5,5)
        self.Show()
    
    # Remove column event
    def onRemoveCol(self, event):
        self.parent.numCols -= 1
        self.parent.itemIndex -= 1
        parent = self.parent
        self.Hide()
        self.parent.Fit()
        self.Destroy()
        parent.rename()
        
        
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
        if selection==self.colType[5]:
            self.handleNumPeaks(event)
        if selection==self.colType[6]:
            self.handlePeaksMatched(event)
        if selection==self.colType[7]:
            self.handleIonsMatched(event)
        if selection==self.colType[9]:
            self.handlePSM(event)

    def handleNumPeaks(self, event):
        self.grid.Add(numPeaksPanel(self), wx.EXPAND)
        self.Fit()
        self.parent.Fit()

    def handlePeaksMatched(self, event):
        self.grid.Add(peaksMatchedPanel(self), wx.EXPAND)
        self.Fit()
        self.parent.Fit()
    
    def handleIonsMatched(self, event):
        self.grid.Add(ionsMatchedPanel(self), wx.EXPAND)
        self.Fit()
        self.parent.Fit()
    
    def handlePSM(self, event):
        self.grid.Add(psmSourcePanel(self), wx.EXPAND)
        self.Fit()
        self.parent.Fit()
    
