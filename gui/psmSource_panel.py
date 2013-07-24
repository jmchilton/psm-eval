import wx

class psmSourcePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, name='psmSource')
        self.SetAutoLayout(True)
        
        # set parent
        self.parent = parent
        
        # set sizer
        self.grid = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.grid)
        self.grid.AddSpacer(5,5)
        
        # psm cource statistic
        self.sources = ['xcorr', 'MyriMatch: MVH', 'MyriMatch: mzFidelity', 'Conf']
        self.sourcesLbl = wx.StaticText(self, label="  PSM Source Statistic:")
        self.grid.Add(self.sourcesLbl)
        self.editSourcesLbl = wx.ComboBox(self, size=(-1,-1), choices=self.sources, style = wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.EvtSources, self.editSourcesLbl)
        self.grid.Add(self.editSourcesLbl)

        # set default
        self.editSourcesLbl.SetValue(self.sources[0])

        # set default col title
        self.parent.colVal['statistic_name'] = str(self.editSourcesLbl.GetValue())
        self.parent.colVal['title'] = 'Source statistic: '+ self.parent.colVal['statistic_name']

        self.grid.AddSpacer(5,5)

        self.Show(True)


# ========================================================================= #

# Events
       
    def EvtSources(self, event):
        self.parent.colVal['statistic_name'] = str(self.editSourcesLbl.GetValue())
        self.parent.colVal['title'] = 'Source statistic: '+ self.parent.colVal['statistic_name']
