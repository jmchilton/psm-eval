import wx

class ionCurrentPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, name='ionCurrent')
        self.parent = parent
        self.SetAutoLayout(True)
        self.grid = wx.BoxSizer(wx.VERTICAL)
        
        self.SetSizer(self.grid)
        self.grid.AddSpacer(5,5)
        
        self.lblPercent = wx.StaticText(self, label="  Percent TIC Threshold:")
        self.grid.Add(self.lblPercent)
        self.editLblPercent = wx.TextCtrl(self, value="0.02", size=(-1,-1))
        self.grid.Add(self.editLblPercent)
        self.lblInst = wx.StaticText(self, label="  Filter all peaks whose intensity does not exceed this percent of total ion current.", size=(-1,-1))
        self.grid.Add(self.lblInst)

        self.grid.AddSpacer(5,5)

        self.Show()
        
