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

        self.SetSizer(self.grid)
        self.grid.AddSpacer(5,5)
        self.label = wx.StaticText(self, label="Peak Filters")
        self.grid.Add(self.label)
        
        self.grid.AddSpacer(5,5)
        self.addPeakFilter = wx.Button(self, label="Add new Peak Filter")
        self.grid.Add(self.addPeakFilter)
        self.addPeakFilter.Bind(wx.EVT_BUTTON, self.onAddPeakFilter)
        self.grid.AddSpacer(5,5)
        self.Show()    
    
        
    def onAddPeakFilter(self, event):
        self.numFilters += 1
        self.grid.Add(peakFilterPanel(self, self.numFilters), wx.EXPAND)
        self.Fit()
        self.parent.Fit()
        
        # Known bug: C++ assertion "increment > 0" failed at /panfs/roc/groups/2/support/wangco/Downloads/wxPython-src-2.9.4.0/src/gtk/window.cpp(4573) in IsScrollIncrement(): 
        self.parent.parent.Fit()
        if self.parent.parent.parent.GetName()=='Evaluation':
            self.parent.parent.parent.Fit()
