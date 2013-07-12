import wx

class intensityQuantPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, name='intensityQuant')
        self.parent = parent
        self.SetAutoLayout(True)
        self.grid = wx.BoxSizer(wx.VERTICAL)
        
        self.SetSizer(self.grid)
        self.grid.AddSpacer(5,5)
        
        self.font1 = wx.Font(8, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.lblq = wx.StaticText(self, label="  q:")
        self.grid.Add(self.lblq)
        self.editLblQ = wx.TextCtrl(self, value="3", size=(-1,-1))
        self.grid.Add(self.editLblQ)
        self.Bind(wx.EVT_TEXT, self.EvtQ, self.editLblQ)
        self.lblInst = wx.StaticText(self, label="  q is the number of partitions to break intensity into, k is the position to pull from. For instance if q=2 and k=1, the peaks above the median intensity will be used and if q=3 and k=2, the middle third of peaks by intensity will be used.", size=(-1,-1))
        self.lblInst.SetFont(self.font1)
        self.grid.Add(self.lblInst)
        
        self.grid.AddSpacer(10,10)
        
        self.lblk = wx.StaticText(self, label="  k:")
        self.grid.Add(self.lblk)
        self.editLblK = wx.TextCtrl(self, value="1", size=(-1,-1))
        self.grid.Add(self.editLblK)
        self.Bind(wx.EVT_TEXT, self.EvtK, self.editLblK)
        self.lblInst2 = wx.StaticText(self, label="  Filter all peaks whose intensity does not exceed this percent of total ion current.", size=(-1,-1))
        self.lblInst2.SetFont(self.font1)
        self.grid.Add(self.lblInst2)
        
        self.grid.AddSpacer(10,10)
        
        self.lblPercent = wx.StaticText(self, label="  Percent TIC Threshold:")
        self.grid.Add(self.lblPercent)
        self.editLblPercent = wx.TextCtrl(self, value="0.02", size=(-1,-1))
        self.grid.Add(self.editLblPercent)
        self.Bind(wx.EVT_TEXT, self.EvtPercent, self.editLblPercent)
        self.lblInst3 = wx.StaticText(self, label="  Filter all peaks whose intensity does not exceed this percent of total ion current.", size=(-1,-1))
        self.lblInst3.SetFont(self.font1)
        self.grid.Add(self.lblInst3)
        
        self.grid.AddSpacer(10,10)
        
        self.Show()

    def allEvent(self):
        if 'peak_filter_ref' in self.parent.filterVal: del self.parent.filterVal['peak_filter_ref']
        self.parent.filterVal['type'] = 'quantile'
        self.parent.filterVal['q'] = float(self.editLblQ.GetValue())
        self.parent.filterVal['k'] = float(self.editLblK.GetValue())
        self.parent.filterVal['percent'] = float(self.editLblPercent.GetValue())

    def EvtQ(self, event):
        self.allEvent()

    def EvtK(self, event):
        self.allEvent()
    
    def EvtPercent(self, event):
        self.allEvent()
        
        
