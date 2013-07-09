import wx
from ionCurrent_panel import *
from intensityQuant_panel import *
from intensityPercent_panel import *

class peakFilterPanel(wx.Panel):
    def __init__(self, parent, filterNum):
        wx.Panel.__init__(self, parent, name='peakFilterPanel')
        self.SetAutoLayout(True)
        self.parent = parent
        
        self.filterNum = filterNum
        
        self.grid = wx.BoxSizer(wx.VERTICAL)
        self.grid.AddSpacer(5,5)

        self.SetSizer(self.grid)
        
        self.filterOnLbl = wx.StaticText(self, label="  Peak Filter %d \n \n   Filter Peaks On:" % self.filterNum, name=str(self.filterNum))
        self.grid.Add(self.filterOnLbl, userData=self.filterOnLbl.GetName())
        self.filterType = ['Intensity as a Percent of Total Ion Current', 'Intensity Quantile', 'Intensity as a Percent of Maximum Spectrum Peak Intensity']
        self.editFilterType = wx.ComboBox(self, size=(-1, -1), choices=self.filterType, style=wx.CB_DROPDOWN, name=str(self.filterNum))
        # Create Column type comboBox
        self.grid.Add(self.editFilterType, userData=self.editFilterType.GetName())
        self.Bind(wx.EVT_COMBOBOX, self.EvtFilterType, self.editFilterType)
        
        self.removeFilter = wx.Button(self, label="Remove Peak Filter %d" % self.filterNum, name=str(self.filterNum))
        self.grid.Add(self.removeFilter, userData=self.removeFilter.GetName())
        self.removeFilter.Bind(wx.EVT_BUTTON, self.onRemoveFilter)
        # Todo: determine fit, layout, and show sequence
        
        self.Fit()
        self.parent.Fit()
        self.Show()

    def onRemoveFilter(self, event):
        self.parent.numFilters -= 1
        self.parent.itemIndex -= 1
        parent = self.parent
        self.Hide()
        self.parent.Fit()
        self.parent.parent.Fit()
        #self.parent.SetSizerAndFit(self.parent.grid)
        self.Destroy()
        parent.rename()
        
        # Helper function for removing columns
    def removeItem(self,event):
        Childrens = self.grid.GetChildren()
        nameList = ['ionCurrent', 'intensityPercent', 'intensityQuant']
        for child in Childrens:
            if child.GetWindow()!=None and child.GetWindow().GetName() in nameList:
                self.grid.Hide(child.GetWindow())
                self.grid.Remove(child.GetWindow())
        
    def EvtFilterType(self, event):
        self.removeItem(event)
        self.Fit()
        selection = event.GetString()
        if selection==self.filterType[0]:
            self.handleFilter1(event)
        if selection==self.filterType[1]:
            self.handleFilter2(event)
        if selection==self.filterType[2]:
            self.handleFilter3(event)

    def FitWindows(self):
        self.Fit()
        parent = self.parent
        while parent.GetName() != 'Evaluation':
            parent.Fit()
            parent = parent.parent
        parent.Fit()
        
    def handleFilter1(self, event):
        self.grid.Add(ionCurrentPanel(self), wx.EXPAND)
        self.FitWindows()

    def handleFilter2(self, event):
        self.grid.Add(intensityQuantPanel(self), wx.EXPAND)
        self.FitWindows()

    def handleFilter3(self, event):
        self.grid.Add(intensityPercentPanel(self), wx.EXPAND)
        self.FitWindows()
        
