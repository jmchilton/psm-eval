import wx
import wx.grid as gridlib
import wx.lib.scrolledpanel as scrolled
from resultFilter import *
import ast

class tablePanel(scrolled.ScrolledPanel):
    def __init__(self, parent, evalNum, stats, filepath, outFile):
        """Constructor"""
        scrolled.ScrolledPanel.__init__(self, parent, name='Result %d' % evalNum)
        self.SetAutoLayout(True)

        # set the number of evaluation it is indexed at
        self.evalNum = evalNum

        # set parent-nb
        self.parent = parent

        # set peak list file path
        self.filepath = filepath
	
        # set column labels
        self.colLbls = stats[0]
        
        # set data
        self.data = stats[1:]
        
        # create the grid
        self.rows = len(self.data)
        self.cols = len(self.data[0])
        
        # number of implicit columns
        self.implicitCols = self.cols-len(self.colLbls)
        
        self.myGrid = gridlib.Grid(self)
        self.myGrid.CreateGrid(self.rows, self.cols-self.implicitCols)
        self.myGrid.SetSelectionBackground('blue')
        
        # dictionary for keeping track of col index corresponding to col labels
        self.columnIndexDict = {}
        
        # fill in col labels
        for i in range(len(self.colLbls)):
            self.columnIndexDict[self.colLbls[i]] = i
            self.myGrid.SetColLabelValue(i, self.colLbls[i])

        # fill in data
        for i in range(self.rows):
            for j in range(self.cols-self.implicitCols):
                # total ion current loses a little precision when using str()
                self.myGrid.SetCellValue(i, j, str(self.data[i][j]))
        
        # self.x, self.y keeps the current spectrum view index
        self.x = 0
        self.y = 0
                
        # keep a list of scan numbers
        self.scanNums = [int(self.data[i][self.cols-self.implicitCols]) for i in range(self.rows)]

        # keep a list of matched ion peak pairs
        self.matched = [self.data[i][self.cols-self.implicitCols+1:self.cols] for i in range(self.rows)]

        # right click to view spectrum
        self.myGrid.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK, self.showPopupMenu)

        self.myGrid.AutoSize()

        # store results to file if output is True
        print outFile
        if outFile:
            f = open('./results.tsv', 'w')
            for column in self.colLbls:
                f.write(column+'\t')
            f.write('\n')
            '''
            for row in self.data:
                for item in row:
                    f.write(str(item))
                    f.write('\t')
                f.write('\n')'''
            for i in range(self.rows):
                for j in range(self.cols-self.implicitCols):
                    f.write(str(self.data[i][j]))
                    f.write('\t')
                f.write('\n')
            f.close()
        
        # set sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.myGrid)
        
        self.sizer.AddSpacer(8,8)
        
        # add spectrum viewing button
        self.lblView = wx.StaticText(self, label="Enter Scan IDs, separated by commas:")
        self.sizer.Add(self.lblView)
        self.editView = wx.TextCtrl(self, value='1')
        self.scanStr = '1'
        self.Bind(wx.EVT_TEXT, self.EvtView, self.editView)
        self.sizer.Add(self.editView)
        self.buttonView = wx.Button(self, -1, label="View Spectrum")
        self.buttonView.SetBackgroundColour(wx.BLUE)
        self.buttonView.Bind(wx.EVT_BUTTON, self.onButtonView)
        self.sizer.Add(self.buttonView, 0)
        
        self.sizer.AddSpacer(5,5)

        self.SetSizer(self.sizer)
        self.SetupScrolling()
        
        
        
        # add filtering functions
        self.filterCount = 0
        self.filter = wx.Button(self, label="Add Filter (by columns)")
        self.filter.Bind(wx.EVT_BUTTON, self.onFilter)
        self.sizer.Add(self.filter)

        # reset function
        self.reset = wx.Button(self, label="Reset")
        self.reset.Bind(wx.EVT_BUTTON, self.onReset)
        self.sizer.Add(self.reset)
        
        # dictionary for keeping track of current filter standards
        self.specified = {}
        
# =============================================================== #
        
# Events
        
    def EvtView(self, event):
        self.scanStr = str(self.editView.GetValue())
    
    # ----

    def onButtonView(self, event):
        self.parent.parent.onSpectViewer()
        scanlist = [int(i) for i in self.scanStr.split(',')]
        
        self.parent.parent.onButtonView(self.filepath, scanlist)
    
    # ----
    def onClickView(self, event):
        self.parent.parent.onSpectViewer()
        scanlist = [self.scanNums[self.x]]
        matched = self.matched[self.x]
        matchedlist = [match for match in matched]
        self.parent.parent.onButtonView(self.filepath, scanlist, matchedlist)

    # ----
    def showPopupMenu(self, event):
        self.x, self.y = event.GetRow(), event.GetCol()
        self.myGrid.SelectRow(self.x)
        if not hasattr(self, "ViewSpectrum"):
            self.ViewSpectrum = wx.NewId()
        
        menu = wx.Menu()
        item = wx.MenuItem(menu, self.ViewSpectrum, "View Spectrum")
        menu.AppendItem(item)
        self.PopupMenu(menu)
        self.Bind(wx.EVT_MENU, self.onClickView, id = self.ViewSpectrum)
        
        menu.Destroy()
        self.myGrid.DeselectRow(self.x)
        
    # ----
    def onFilter(self, event):
        self.filterCount += 1
        self.sizer.Add(resultFilter(self, self.filterCount))
        self.FitInside()
        self.parent.Layout()

    # ----
        
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
                self.myGrid.SetCellValue(i, j, str(self.data[i][j]))
        self.Fit()
        self.parent.Layout()
        
        



 
