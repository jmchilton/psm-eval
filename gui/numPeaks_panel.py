import wx

class numPeaksPanel(wx.Panel):
    def __init__(self, parent):
        #print evtId
        wx.Panel.__init__(self, parent, name='pkList')
        self.parent = parent
        self.SetAutoLayout(True)
        self.grid = wx.BoxSizer(wx.VERTICAL)
        
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
        pass
