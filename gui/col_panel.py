import wx
from numPeaks_panel import *
class colPanel(wx.Panel):
    # ToDo: When initiating, pass in all list of choices for setting up the choices box
    # ToDo: Error handling
    def __init__(self, parent, colNum):
        wx.Panel.__init__(self, parent)
        self.SetAutoLayout(True)
        self.colNum = colNum
        self.parent = parent
        self.numPeaks = 0
        
        self.grid = wx.BoxSizer(wx.VERTICAL)
        self.grid.AddSpacer(5,5)

        self.SetSizer(self.grid)
        
        # Define other variables / lists /widgets to be used
        # Coltype combobox list
        self.colType = ['Peptide Sequence', 'Scan Index', 'Scan Number', 'Scan ID', 'Peak List', 'Number of Peaks', 'Peaks Matched Statistics', 'Ions Matched Statistics', 'Total Ion Current', 'Statistic from PSM Source', 'Protvis Link']
        
        self.colTypeLbl = wx.StaticText(self, label="Column %d \n \n Column Type:" % self.colNum, name=str(self.colNum))

        self.grid.Add(self.colTypeLbl, userData=self.colTypeLbl.GetName())    
        self.editColType = wx.ComboBox(self, size=(-1, -1), choices=self.colType, style=wx.CB_DROPDOWN, name=str(self.colNum))
        # Create Column type comboBox
        self.grid.Add(self.editColType, userData=self.editColType.GetName())
        self.Bind(wx.EVT_COMBOBOX, self.EvtColType, self.editColType)
        self.addRemoveButton()
        self.Show()
        
    def addRemoveButton(self):
        self.removeCol = wx.Button(self, label="Remove Column %d" % self.colNum, name=str(self.colNum))
        self.grid.Add(self.removeCol, userData=self.removeCol.GetName())
        self.removeCol.Bind(wx.EVT_BUTTON, self.onRemoveCol)
        self.Fit()
        #self.grid.AddSpacer(20,20)
        self.Fit()
    
    def onRemoveCol(self, event):
        self.parent.numCols -= 1
        self.Hide()
        self.parent.SetSizerAndFit(self.parent.grid)
        self.Destroy()
        #self.removeItem(event)
        #self.numCols -= 1
        #self.grid.Layout()
        #self.Fit()
    
    # Helper function for removing columns
    def removeItem(self,event):
        Childrens=self.grid.GetChildren()
        for child in Childrens:
            if child.GetWindow()!=None and child.GetWindow().GetName()=='pkList':
                self.grid.Hide(child.GetWindow())
                self.grid.Remove(child.GetWindow())
    
    def EvtColType(self, event):
        self.removeItem(event)
        self.Fit()
        if event.GetString()=='Number of Peaks':
            self.handleNumPeaks(event)

    def handleNumPeaks(self, event):
        self.grid.Add(numPeaksPanel(self), wx.EXPAND)
        self.Fit()
        self.parent.Fit()
