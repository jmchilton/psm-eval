import wx
from numPeaks_panel import *

class ionsMatchedPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, name='ionMatched')
        self.parent = parent
        self.SetAutoLayout(True)
        self.grid = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.grid)
        self.grid.AddSpacer(5,5)
        
        # Peak Matching Stats
        self.stats = ['Number of Matched Ions', 'Number of Unmatched Ions', 'Longest Stretch of Matched Ions', 'Percent of Matched Ions', 'Percent of Unmatched Ions', 'List Matched Ions', 'List Unmatched Ions']
        self.statsLbl = wx.StaticText(self, label="Ion Matching Statistic:")
        self.grid.Add(self.statsLbl)
        
        self.editStatsLbl = wx.ComboBox(self, size=(-1, -1), choices=self.stats, style=wx.CB_DROPDOWN)
        self.grid.Add(self.editStatsLbl)
        self.Bind(wx.EVT_COMBOBOX, self.EvtStats, self.editStatsLbl)
        
        self.grid.AddSpacer(5,5)
        
        # Ion series
        self.ions = ['a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'c1', 'c2', 'c3', 'x1', 'x2', 'x3', 'y1', 'y2', 'y3', 'z1', 'z2', 'z3', 'M1', 'M2', 'Internal Ions']
        self.ionLbl = wx.StaticText(self, label="Ion Series:")
        self.grid.Add(self.ionLbl)
        
        self.editIonsLbl = wx.CheckListBox(self, size=(-1, -1), choices=self.ions)
        self.grid.Add(self.editIonsLbl)
        self.Bind(wx.EVT_CHECKLISTBOX, self.EvtIons, self.editIonsLbl)

        self.grid.AddSpacer(5,5)

        # Losses
        self.losses = ['H2O', 'NH3', 'CO (-28) on internal ions']
        self.lossLbl = wx.StaticText(self, label="Losses:")
        self.grid.Add(self.lossLbl)
        
        self.editLossLbl = wx.ListBox(self, size=(-1,-1), choices=self.losses, style=wx.LB_EXTENDED)
        self.grid.Add(self.editLossLbl)
        self.Bind(wx.EVT_LISTBOX, self.EvtLosses, self.editLossLbl)
        self.grid.AddSpacer(5,5)

        # Peak Filters
        self.grid.Add(numPeaksPanel(self), wx.EXPAND)
        self.Fit()
        self.parent.Fit()
        self.grid.AddSpacer(5,5)

        # Mass Tolerance
        self.massTolerance = wx.CheckBox(self, size=(-1,-1), label='Specify Mass Tolerance:')
        self.grid.Add(self.massTolerance)
        self.Bind(wx.EVT_CHECKBOX, self.EvtMassTolerance, self.massTolerance)
        self.grid.AddSpacer(5,5)
        self.Show(True)
    
    #TODO: fill in event details
    def EvtMassTolerance(self, event):
        pass

    def EvtLosses(self, event):
        pass

    def EvtIons(self, event):     
        pass
        
    def EvtStats(self, event):
        pass