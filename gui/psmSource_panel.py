import wx

class psmSourcePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, name='psmSource')
        self.parent = parent
        self.SetAutoLayout(True)
        self.grid = wx.BoxSizer(wx.VERTICAL)
        
        self.SetSizer(self.grid)
        self.grid.AddSpacer(5,5)
        
        self.sources = ['xcorr', 'MyriMatch: MVH', 'MyriMatch: mzFidelity', 'Conf']
        self.sourcesLbl = wx.StaticText(self, label="  PSM Source Statistic:")
        self.grid.Add(self.sourcesLbl)
        
        self.editSourcesLbl = wx.ComboBox(self, size=(-1,-1), choices=self.sources, style = wx.CB_DROPDOWN)
        self.grid.Add(self.editSourcesLbl)
        self.Bind(wx.EVT_COMBOBOX, self.EvtSources, self.editSourcesLbl)
        self.grid.AddSpacer(5,5)
        
        self.Show(True)
       
    def EvtSources(self, event):
        pass
