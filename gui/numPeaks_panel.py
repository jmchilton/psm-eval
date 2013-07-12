import wx
from peakFilter_panel import *
class numPeaksPanel(wx.Panel):
    def __init__(self, parent):
        #print evtId
        wx.Panel.__init__(self, parent, name='pkList')
        self.parent = parent
        self.SetAutoLayout(True)
        self.grid = wx.BoxSizer(wx.VERTICAL)
        
        self.numFilters = 0
        self.itemIndex = 0

        self.SetSizer(self.grid)
        self.grid.AddSpacer(5,5)
        self.label = wx.StaticText(self, label="  Peak Filters")
        self.grid.Add(self.label)
        
        self.grid.AddSpacer(5,5)
        self.addPeakFilter = wx.Button(self, label="Add new Peak Filter")
        self.grid.Add(self.addPeakFilter)
        self.addPeakFilter.Bind(wx.EVT_BUTTON, self.onAddPeakFilter)
        self.grid.AddSpacer(5,5)
        self.Show()
        self.itemIndex += 5

        self.filters = []
        
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
        # Known bug: C++ assertion "increment > 0" failed at /panfs/roc/groups/2/support/wangco/Downloads/wxPython-src-2.9.4.0/src/gtk/window.cpp(4573) in IsScrollIncrement(): 
        self.parent.parent.Fit()
        if self.parent.parent.parent.GetName()=='Evaluation':
            self.parent.parent.parent.Fit()

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
        
