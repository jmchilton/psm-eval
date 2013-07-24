import wx
import exceptions

class ionCurrentPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, name='ionCurrent')
        self.SetAutoLayout(True)
       
        # set parent
        self.parent = parent
        
        # set sizer
        self.grid = wx.BoxSizer(wx.VERTICAL)  
        self.SetSizer(self.grid)
        self.grid.AddSpacer(5,5)

        # set font
        self.font1 = wx.Font(8, wx.ROMAN, wx.NORMAL, wx.NORMAL)
       
        # TIC threshold, default to 0.02
        self.lblPercent = wx.StaticText(self, label="  Percent TIC Threshold:")
        self.grid.Add(self.lblPercent)
        self.editLblPercent = wx.TextCtrl(self, value="0.02", size=(-1,-1))
        self.Bind(wx.EVT_TEXT, self.EvtPercent, self.editLblPercent)
        self.grid.Add(self.editLblPercent)
        
        
        # set default column title
        self.parent.filterVal['percent'] = float(self.editLblPercent.GetValue())
        if self.parent.parent.parent.GetName() == 'colPanel':
            self.parent.parent.parent.colVal['title'] = 'Number of Peaks above %.1f percent TIC' % (self.parent.filterVal['percent'] * 100)

        # instruction label
        self.lblInst = wx.StaticText(self, label="  Filter all peaks whose intensity does not exceed this percent of total ion current.", size=(-1,-1))
        self.lblInst.SetFont(self.font1)
        self.grid.Add(self.lblInst)

        self.grid.AddSpacer(5,5)

        self.Show()
    
# =============================================================================== #

    # helper function to handle error while changing entered field to float
    def toFloat(self, value):
        try:
            return float(value)
        except exceptions.ValueError:
            print "field empty or contains invalid character: using 0.0"
            return 0.0
    
    # ----
    def EvtPercent(self,event):
        percent = self.toFloat(self.editLblPercent.GetValue())
        self.parent.filterVal['percent'] = percent
        # set col title
        if self.parent.parent.parent.GetName() == 'colPanel':
            self.parent.parent.parent.colVal['title'] = 'Number of Peaks above %.1f percent TIC' % (percent * 100)
        # Might need an else depending on the name requirement for columns

        
