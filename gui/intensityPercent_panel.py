import wx
import exceptions

class intensityPercentPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, name='intensityPercent')
        self.SetAutoLayout(True)

        # set parent
        self.parent = parent
        
        # set sizer
        self.grid = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.grid)
        self.grid.AddSpacer(5,5)
        
        # percent of max peak intensity field
        self.lblPercent = wx.StaticText(self, label="  Percent of Maximum Peak Intensity")
        self.grid.Add(self.lblPercent)
        self.editLblPercent = wx.TextCtrl(self, value="0.1", size=(-1,-1))
        self.Bind(wx.EVT_TEXT, self.EvtPercent, self.editLblPercent)
        self.grid.Add(self.editLblPercent)

        # set default values
        self.parent.filterVal['percent'] = 0.1
        self.grid.AddSpacer(5,5)
        
        # set default col title
        if self.parent.parent.parent.GetName() == 'colPanel':
            self.parent.parent.parent.colVal['title'] = 'Number of peaks greater than %.1f intensity of Maximum Peak Intensity' % (self.parent.filterVal['percent'] * 100)

        self.Show()

# ====================================================================== #
    
    # helper function for handling error while chaning entered strings to numeric values

    def toFloat(self, value):
        try:
            return float(value)
        except exceptions.ValueError:
            print "field empty or contains invalid character: using 0.0"
            return 0.0
    # ----
    
    def EvtPercent(self, event):
        percent = self.toFloat(self.editLblPercent.GetValue())
        self.parent.filterVal['percent'] = percent
        if self.parent.parent.parent.GetName() == 'colPanel':
            self.parent.parent.parent.colVal['title'] = 'Number of peaks greater than %.1f intensity of Maximum Peak Intensity' % (percent * 100)
