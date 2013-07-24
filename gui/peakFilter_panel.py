import wx
from ionCurrent_panel import *
from intensityQuant_panel import *
from intensityPercent_panel import *

class peakFilterPanel(wx.Panel):
    def __init__(self, parent, filterNum):
        wx.Panel.__init__(self, parent, name='peakFilterPanel')
        self.SetAutoLayout(True)
        
        # set parent
        self.parent = parent
        
        # set filter number
        self.filterNum = filterNum
        
        # set sizer
        self.grid = wx.BoxSizer(wx.VERTICAL)
        self.grid.AddSpacer(5,5)
        self.SetSizer(self.grid)
        
        # set filter dictionary to store its detailed information
        self.filterVal = {}
        self.top_third = {'type': 'quantile', 'q': 3, 'k': 1, 'percent': 0.02}
        
        # filters
        self.filterOnLbl = wx.StaticText(self, label="  Peak Filter %d \n \n   Filter Peaks On:" % self.filterNum, name=str(self.filterNum))
        self.grid.Add(self.filterOnLbl, userData=self.filterOnLbl.GetName())
        
        self.filterType = ['Intensity as a Percent of Total Ion Current', 'Intensity Quantile', 'Intensity as a Percent of Maximum Spectrum Peak Intensity']
        
        # Based on psme/column/filters_peaks.py.Filter_factory_classes
        self.typeNames = ['percent_tic', 'quantile', 'percent_max_intensity', 'mz_range', 'intensity_range']
        self.editFilterType = wx.ComboBox(self, size=(-1, -1), choices=self.filterType, style=wx.CB_DROPDOWN, name=str(self.filterNum))
        
        # filter type combobox
        self.grid.Add(self.editFilterType, userData=self.editFilterType.GetName())
        self.editFilterType.SetValue(self.filterType[0])
        self.Bind(wx.EVT_COMBOBOX, self.EvtFilterType, self.editFilterType)

        # default to ioncurrent panel
        self.grid.Add(ionCurrentPanel(self), wx.EXPAND)        
        self.filterVal['type'] = self.typeNames[0]        
        
        self.parent.filters.insert(self.filterNum-1, self.filterVal)
        
        # remove button
        self.removeFilter = wx.Button(self, label="Remove Peak Filter %d" % self.filterNum, name=str(self.filterNum))
        self.grid.Add(self.removeFilter, userData=self.removeFilter.GetName())
        self.removeFilter.Bind(wx.EVT_BUTTON, self.onRemoveFilter)
        
        # layout
        self.Fit()
        self.parent.Fit()
        self.Show()


# ============================================================================= #

# events

    def onRemoveFilter(self, event):
        parent = self.parent
        del parent.filters[self.filterNum-1]
        parent.numFilters -= 1
        parent.itemIndex -= 1
        self.Hide()
        parent.Fit()
        parent.parent.Fit()
        self.Destroy()
        parent.rename()
        if parent.parent.parent.GetName() == 'Evaluation':
            parent.parent.parent.FitInside()
            parent.parent.parent.parent.Layout()
        else:
            parent.parent.parent.parent.FitInside()
            parent.parent.parent.parent.parent.Layout()

    # ----
        
    # Helper function for removing columns
    def removeItem(self,event):
        Childrens = self.grid.GetChildren()
        nameList = ['ionCurrent', 'intensityPercent', 'intensityQuant']
        for child in Childrens:
            if child.GetWindow()!=None and child.GetWindow().GetName() in nameList:
                self.grid.Hide(child.GetWindow())
                self.grid.Remove(child.GetWindow())

    # ----
        
    def EvtFilterType(self, event):
        self.removeItem(event)
        self.Fit()
        selection = event.GetString()
        if selection==self.filterType[0]:
            if 'top_third' in self.filterVal: del self.filterVal['top_third']
            if 'q' in self.filterVal: del self.filterVal['q']
            if 'k' in self.filterVal: del self.filterVal['k']
            self.filterVal['type'] = self.typeNames[0]
            self.handleFilter1(event)
        if selection==self.filterType[1]:
            if 'type' in self.filterVal: del self.filterVal['type']
            if 'percent' in self.filterVal: del self.filterVal['percent']
            self.filterVal['peak_filter_ref'] = 'top_third'
            self.handleFilter2(event)
        if selection==self.filterType[2]:
            if 'q' in self.filterVal: del self.filterVal['q']
            if 'k' in self.filterVal: del self.filterVal['k']
            if 'top_third' in self.filterVal: del self.filterVal['top_third']
            self.filterVal['type'] = self.typeNames[2]
            self.handleFilter3(event)

    # ----
    # Helper function for Window layout

    def FitWindows(self):
        self.Fit()
        parent = self.parent
        while parent.GetName() != 'Evaluation':
            parent.Fit()
            parent = parent.parent
        parent.FitInside()
        parent.parent.Layout()

    # ----
        
    def handleFilter1(self, event):
        self.grid.Add(ionCurrentPanel(self), wx.EXPAND)
        self.FitWindows()

    # ----

    def handleFilter2(self, event):
        self.grid.Add(intensityQuantPanel(self), wx.EXPAND)
        self.FitWindows()

        
    # ----
    def handleFilter3(self, event):
        self.grid.Add(intensityPercentPanel(self), wx.EXPAND)
        self.FitWindows()
        
