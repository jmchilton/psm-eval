import wx
from peakFilter_panel import *

class numPeaksPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, name='pkList', style=wx.BORDER_SUNKEN)
        
        # set parent
        self.parent = parent
        
        self.SetAutoLayout(True)
        
        # set filter number
        self.numFilters = 0
        
        # set index of widgets added
        self.itemIndex = 0

        # set sizer
        self.grid = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.grid)
        
        # peak filter button
        self.grid.AddSpacer(2,2)
        self.label = wx.StaticText(self, label="  Peak Filters")
        self.grid.Add(self.label)
        
        self.grid.AddSpacer(3,3)
        self.addPeakFilter = wx.Button(self, label="Add new Peak Filter")
        self.addPeakFilter.Bind(wx.EVT_BUTTON, self.onAddPeakFilter)
        self.grid.Add(self.addPeakFilter)
        self.grid.AddSpacer(3,3)
        self.Show()
        self.itemIndex += 5
        
        # keep a list of filter criteria
        self.filters = []

# ========================================================================== #
    # events

    def onAddPeakFilter(self, event):
        self.numFilters += 1
        self.itemIndex += 1
        self.grid.Insert(self.itemIndex-3, peakFilterPanel(self, self.numFilters), wx.EXPAND)
        if self.parent.GetName() == 'colPanel':
            self.parent.colVal['peak_filters'] = self.filters
        elif self.parent.parent.GetName() == 'colPanel':
            self.parent.parent.colVal['peak_filters'] = self.filters
        # else
        self.Fit()
        self.parent.Fit()
        self.parent.parent.Fit()
        
        if self.parent.parent.parent.GetName()=='Evaluation':
            self.parent.parent.parent.FitInside()
        self.parent.parent.parent.Layout()

    # ----

    # helper function called by children(peakfilter) panel to rename after deletion
    def rename(self):
        childrens = self.grid.GetChildren()
        colChildrens = []
        for child in childrens:
            if child.GetWindow() != None and child.GetWindow().GetName() == 'peakFilterPanel':
                colChildrens.append(child)
        for i in range(len(colChildrens)):
            colChildrens[i].GetWindow().filterNum = i+1
            colChildrens[i].GetWindow().filterOnLbl.SetLabel("  Peak Filter %d \n \n Filter Peaks On:" % (i+1))
            colChildrens[i].GetWindow().removeFilter.SetLabel("Remove Peak Filter %d" % (i+1))
            colChildrens[i].GetWindow().filterOnLbl.SetName("  Peak Filter %d \n \n Filter Peaks On:" % (i+1))
            colChildrens[i].GetWindow().removeFilter.SetName("Remove Column %d" % (i+1))
        
