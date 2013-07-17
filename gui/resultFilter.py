import wx
import exceptions

class resultFilter(wx.Panel):
    def __init__(self, parent, filterNum):
        wx.Panel.__init__(self, parent, name='filter')
        self.SetAutoLayout(True)
        self.filterNum = filterNum
        self.parent = parent

        self.grid = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.grid)

        self.columns = self.parent.colLbls
        self.editCol = wx.ComboBox(self, choices=self.columns, style=wx.CB_DROPDOWN)
        self.grid.Add(self.editCol)
        self.Bind(wx.EVT_COMBOBOX, self.EvtCol, self.editCol)
        self.grid.AddSpacer(3,3)
        
        self.specifiers = ['>', '<', '=', '>=', '<=']
        self.editSpec = wx.ComboBox(self, choices=self.specifiers, style=wx.CB_DROPDOWN)
        self.grid.Add(self.editSpec)
        self.Bind(wx.EVT_COMBOBOX, self.EvtSpec, self.editSpec)
        
        self.grid.AddSpacer(3,3)

        self.editBound = wx.TextCtrl(self, value='0')
        self.grid.Add(self.editBound)
        self.Bind(wx.EVT_TEXT, self.EvtBound, self.editBound)
        self.grid.AddSpacer(3,3)

        self.execute = wx.Button(self, label="Execute")
        self.grid.Add(self.execute)
        self.Bind(wx.EVT_BUTTON, self.onExecute, self.execute)

        self.grid.AddSpacer(3,3)

        self.Fit()
        
    def EvtCol(self, event):
        pass
    def EvtSpec(self, event):
        pass
    def EvtBound(self, event):
        pass
    # Helper function for turning strings from cells to floats
    def num(self, string):
        try:
            return float(string)
        except exceptions.ValueError:
            return str(string)
    def onExecute(self, event):
        field1 = self.editCol.GetValue()
        field2 = self.editSpec.GetValue()
        field3 = self.editBound.GetValue()
        if field1 == '' or field2 == '' or field3 == '':
            print "Please specify every field"
            return
        else:
            requirement = [self.num(field1), self.num(field2), self.num(field3)]
            self.parent.specified[self.num(field1)] = [self.num(field2), self.num(field3)]
        print "Current Filter(s): "
        print [(key, value) for key, value in self.parent.specified.iteritems()]
        self.filter(self.parent)
    # Actually filter
    def filter(self, parent):
        reqs = parent.specified
        parent.myGrid.ClearGrid()
        
        toFilterData = parent.data
        filteredData = []
        for i in range(len(toFilterData)):
            if self.check(toFilterData[i], parent.columnIndexDict, reqs):
                filteredData.append(toFilterData[i])
        rowNum = len(filteredData)
        if rowNum != 0:
            colNum = len(filteredData[0])
        for i in range(rowNum):
            for j in range(colNum):
                self.parent.myGrid.SetCellValue(i, j, filteredData[i][j])
        self.parent.myGrid.AutoSize()

    def check(self, toFilter, colIndexDict, requirements):
        passed = []
        for key in requirements:
            colIndex = colIndexDict[key]
            passed.append(self.compare(toFilter[colIndex], requirements[key][0], requirements[key][1]))
        for value in passed:
            if value == False:
                return False
        return True

    def compare(self, value, symbol, threshold):
        if symbol == '>':
            try:
                return float(value) > float(threshold)
            except exceptions.ValueError:
                print "Can't filter: incompatible types"
                return True
        elif symbol == '<':
            try:
                return float(value) < float(threshold)
            except exceptions.ValueError:
                print "Can't filter: incompatible types"
                return True
        elif symbol == '>=':
            try:
                return float(value) >= float(threshold)
            except exceptions.ValueError:
                print "Can't filter: incompatible types"
                return True
        elif symbol == '<=':
            try:
                return float(value) <= float(threshold)
            except exceptions.ValueError:
                print "Can't filter: incompatible types"
                return True
        else:
            try:
                return float(value) == float(threshold)
            except exceptions.ValueError:
                print "Can't filter: incompatible types"
                return True

        
                


        
        
        
        
