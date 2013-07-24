import wx
import exceptions

class intensityQuantPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, name='intensityQuant')
        self.SetAutoLayout(True)

        # set parent
        self.parent = parent

        # set sizer
        self.grid = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.grid)
        self.grid.AddSpacer(5,5)
        
        # set font
        self.font1 = wx.Font(8, wx.ROMAN, wx.NORMAL, wx.NORMAL)
       
        # field for q
        self.lblq = wx.StaticText(self, label="  q:")
        self.grid.Add(self.lblq)
        self.editLblQ = wx.TextCtrl(self, value="3", size=(-1,-1))
        self.Bind(wx.EVT_TEXT, self.EvtQ, self.editLblQ)
        self.grid.Add(self.editLblQ)
        
        # instructions
        self.lblInst = wx.StaticText(self, label="  q is the number of partitions to break intensity into, k is the position to pull from. For instance if q=2 and k=1, the peaks above the median intensity will be used and if q=3 and k=2, the middle third of peaks by intensity will be used.", size=(-1,-1))
        self.lblInst.SetFont(self.font1)
        self.grid.Add(self.lblInst)
        
        self.grid.AddSpacer(10,10)
        
        # field for k
        self.lblk = wx.StaticText(self, label="  k:")
        self.grid.Add(self.lblk)
        self.editLblK = wx.TextCtrl(self, value="1", size=(-1,-1))
        self.Bind(wx.EVT_TEXT, self.EvtK, self.editLblK)
        self.grid.Add(self.editLblK)
        
        # instructions
        self.lblInst2 = wx.StaticText(self, label="  Filter all peaks whose intensity does not exceed this percent of total ion current.", size=(-1,-1))
        self.lblInst2.SetFont(self.font1)
        self.grid.Add(self.lblInst2)
        
        self.grid.AddSpacer(10,10)
        
        # tic threshold
        self.lblPercent = wx.StaticText(self, label="  Percent TIC Threshold:")
        self.grid.Add(self.lblPercent)
        self.editLblPercent = wx.TextCtrl(self, value="0.02", size=(-1,-1))
        self.Bind(wx.EVT_TEXT, self.EvtPercent, self.editLblPercent)
        self.grid.Add(self.editLblPercent)
        
        # instruction
        self.lblInst3 = wx.StaticText(self, label="  Filter all peaks whose intensity does not exceed this percent of total ion current.", size=(-1,-1))
        self.lblInst3.SetFont(self.font1)
        self.grid.Add(self.lblInst3)
        
        self.grid.AddSpacer(10,10)
        
        # set default values
        self.parent.filterVal['q'] = 3
        self.parent.filterVal['percent'] = 0.02
        
        # set default col title
        if self.parent.parent.parent.GetName() == 'colPanel':
            self.parent.parent.parent.colVal['title'] = 'Matched Peaks in top %d quantile of peaks above %.1f percent TIC' %(self.parent.filterVal['q'], self.parent.filterVal['percent']*100)

        self.Show()
    

# ==================================================================================== #

# helper functinos for handling error while changing entered strings to numeric values

    def toInt(self, value):
        try:
            return int(value)
        except exceptions.ValueError:
            print "field empty or contains invalid character: using 0"
            return 0

    # ----

    def toFloat(self, value):
        try:
            return float(value)
        except exceptions.ValueError:
            print "field empty or contains invalid character: using 0.0"
            return 0.0
    # ----

    def allEvent(self):
        if 'peak_filter_ref' in self.parent.filterVal: del self.parent.filterVal['peak_filter_ref']
        # TODO: error handling for empty fields (try except)
        self.parent.filterVal['type'] = 'quantile'
        self.parent.filterVal['q'] = self.toInt(self.editLblQ.GetValue())
        self.parent.filterVal['k'] = self.toInt(self.editLblK.GetValue())
        self.parent.filterVal['percent'] = self.toFloat(self.editLblPercent.GetValue())
        if self.parent.parent.parent.GetName() == 'colPanel':
            self.parent.parent.parent.colVal['title'] = 'Matched Peaks in top %d quantile of peaks above %.1f percent TIC' %(self.parent.filterVal['q'], self.parent.filterVal['percent']*100) 
    
    # ----
    def EvtQ(self, event):
        self.allEvent()
        
    # ----
    def EvtK(self, event):
        self.allEvent()
    
    # ----
    def EvtPercent(self, event):
        self.allEvent()
        
        
