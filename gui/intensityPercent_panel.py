import wx

class intensityPercentPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, name='intensityPercent')
        self.parent = parent
        self.SetAutoLayout(True)
        self.grid = wx.BoxSizer(wx.VERTICAL)
        
        self.SetSizer(self.grid)
        self.grid.AddSpacer(5,5)
        
        self.lblPercent = wx.StaticText(self, label="  Percent of Maximum Peak Intensity")
        self.grid.Add(self.lblPercent)
        self.editLblPercent = wx.TextCtrl(self, value="0.1", size=(-1,-1))
        self.grid.Add(self.editLblPercent)

        self.grid.AddSpacer(5,5)

        self.Show()
