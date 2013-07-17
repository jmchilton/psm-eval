import wx
import wx.grid as gridlib
import wx.lib.scrolledpanel as scrolled
from resultFilter import *

class tablePanel(scrolled.ScrolledPanel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent, evalNum, dataFile):
        """Constructor"""
        scrolled.ScrolledPanel.__init__(self, parent, name='Result of Evaluation %d' % evalNum)
        self.SetAutoLayout(True)
        self.evalNum = evalNum
        self.parent = parent
	
        self.colLbls = dataFile.readline().split('\t')[:-1]
        
        self.data = [line.split('\t')[:-1] for line in dataFile]
        
        self.rows = len(self.data)
        self.cols = len(self.data[0])
        self.myGrid = gridlib.Grid(self)
        self.myGrid.CreateGrid(self.rows, self.cols)
       
        self.columnIndexDict = {}
        
        #for i in range(len(self.colLbls)):
            #self.columnDict[self.colLbls[i]] = [col[i] for col in self.data]

        for i in range(len(self.colLbls)):
            self.columnIndexDict[self.colLbls[i]] = i
            self.myGrid.SetColLabelValue(i, self.colLbls[i])

        for i in range(self.rows):
            for j in range(self.cols):
                self.myGrid.SetCellValue(i, j, self.data[i][j])

        self.myGrid.AutoSize()
 
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.myGrid, 1)
        self.SetSizer(self.sizer)
        self.SetupScrolling()
        
        self.sizer.AddSpacer(5,5)
        # Add filtering functions
        self.filterCount = 0
        self.filter = wx.Button(self, label="Add Filter (by columns)")
        self.sizer.Add(self.filter)
        self.filter.Bind(wx.EVT_BUTTON, self.onFilter)

        self.reset = wx.Button(self, label="Reset")
        self.sizer.Add(self.reset)
        self.reset.Bind(wx.EVT_BUTTON, self.onReset)

	
        
        self.specified = {}
        
    def onFilter(self, event):
        self.filterCount += 1
        self.sizer.Add(resultFilter(self, self.filterCount))
        self.Fit()
        
    def onReset(self, event):
        Childrens = self.GetChildren()
        for child in Childrens:
            if child.GetName() == 'filter':
                self.filterCount -= 1
                self.sizer.Hide(child)
                self.sizer.Remove(child)
        self.specified.clear()
        for i in range(self.rows):
            for j in range(self.cols):
                self.myGrid.SetCellValue(i, j, self.data[i][j])
        self.Fit()
        
        



 
