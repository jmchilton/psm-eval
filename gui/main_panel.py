import wx
import wx.lib.scrolledpanel as scrolled
from col_panel import *
class mainPanel(scrolled.ScrolledPanel):
    # ToDo: When initiating, pass in all list of choices for setting up the choices box
    # ToDo: Error handling
    def __init__(self, parent, id, title):
        scrolled.ScrolledPanel.__init__(self, parent)
        self.SetAutoLayout(True)
        self.parent = parent

        self.itemIndex = 0
        # Variable to keep track of number of columns added
        self.numCols = 0

        self.grid = wx.BoxSizer(wx.VERTICAL)
        
        t = wx.StaticText(self, -1, "Please specify requirements:")
        self.grid.Add(t)
        self.grid.AddSpacer(5,5)
        self.itemIndex += 2

        self.SetSizer(self.grid)
        self.SetupScrolling()
       
        # PSMs Type combobox
        self.psmType = ['MzidentML (mzid)', 'ProteinPilot Peptide Report']
        self.lblPsmType = wx.StaticText(self, label="PSMs Type:")
        self.grid.Add(self.lblPsmType)
        self.editPsmType = wx.ComboBox(self, size=(-1, -1), choices=self.psmType, style=wx.CB_DROPDOWN)
        self.grid.Add(self.editPsmType)
        self.Bind(wx.EVT_COMBOBOX, self.EvtPsmType, self.editPsmType)
        self.grid.AddSpacer(5,5)
        self.itemIndex += 3
        
        # ProteinPilot Peptide Report combobox
        # Need to replace contents dynamically
        self.report = ['1', '2', '3']
        self.lblReport = wx.StaticText(self, label="ProteinPilot Peptide Report:")
        self.grid.Add(self.lblReport)
        self.editReport = wx.ComboBox(self,size=(-1, -1), choices=self.report, style=wx.CB_DROPDOWN)
        self.grid.Add(self.editReport)
        self.Bind(wx.EVT_COMBOBOX, self.EvtReport, self.editReport)
        self.grid.AddSpacer(5,5)
        self.itemIndex += 3

        # Peak list listbox
        # Need to replace contents dynamically
        self.fType = ['files directly', 'by multifile']
        self.peakList = ['a', 'b', 'c']
        self.multiList = ['d', 'e']
        
        self.lblPeakList = wx.StaticText(self, label="Peak List (mzML):")
        self.grid.Add(self.lblPeakList)
        self.itemIndex += 1
        # Add option to select dierectly or by multifile
        self.ListBox = wx.RadioBox(self, label="select ", choices=self.fType, style=wx.RA_SPECIFY_COLS)
        self.grid.Add(self.ListBox)
        self.Bind(wx.EVT_RADIOBOX, self.EvtFType, self.ListBox)

        self.editPeakList = wx.ListBox(self, size=(-1, -1), choices=self.peakList, style=wx.LB_MULTIPLE)
        self.grid.Add(self.editPeakList)
        self.Bind(wx.EVT_LISTBOX, self.EvtPeakList, self.editPeakList)
        self.grid.AddSpacer(5,5)
        self.itemIndex += 3
        # Output type combobox
        self.outType = ['Tabular (tsv)', 'HTML']
        self.lblOutType = wx.StaticText(self, label="Output Type:")
        self.grid.Add(self.lblOutType)
        self.editOutType = wx.ComboBox(self, size=(-1, -1), choices=self.outType, style=wx.CB_DROPDOWN)
        self.grid.Add(self.editOutType)
        self.Bind(wx.EVT_COMBOBOX, self.EvtOutType, self.editOutType)
        self.grid.AddSpacer(5,5)
        self.itemIndex += 3
        # Default mass tolerance edit control
        self.lblMass = wx.StaticText(self, label="Default Mass Tolerance:")
        self.grid.Add(self.lblMass)
        self.editMass = wx.TextCtrl(self, value='0.01')
        self.grid.Add(self.editMass)
        self.Bind(wx.EVT_TEXT, self.EvtMass, self.editMass)
        self.grid.AddSpacer(5,5)
        
        # Mass type combobox
        self.massType = ['Monoisotopic', 'Average (has known problem)']
        self.lblmassType = wx.StaticText(self, label="Mass Type")
        self.grid.Add(self.lblmassType)
        self.editMassType = wx.ComboBox(self, size=(-1, -1), choices=self.massType, style=wx.CB_DROPDOWN)
        self.grid.Add(self.editMassType)
        self.Bind(wx.EVT_COMBOBOX, self.EvtMassType, self.editMassType)
        self.grid.AddSpacer(5,5)
        self.itemIndex += 3
        # Columns
        # Static line
        self.lblCol = wx.StaticText(self, label="Columns")
        self.grid.Add(self.lblCol)
        
        self.addCol = wx.Button(self, label="Add new Column")
        self.addCol.Bind(wx.EVT_BUTTON, self.onAddCol)
        self.grid.Add(self.addCol)
        self.itemIndex += 2
        # self.removeCol = wx.Button(self, label="Remove Column %d" % self.numCols)
        # self.grid.Add(self.removeCol)
        # self.removeCol.Bind(wx.EVT_BUTTON, self.onRemoveCol)
        
        self.buttonDone = wx.Button(self, -1, label="Done", size=(80,25))
        self.buttonDone.Bind(wx.EVT_BUTTON, self.onButtonDone)
        self.grid.Add(self.buttonDone, 0, wx.ALIGN_BOTTOM, 200)
        self.grid.AddSpacer(20,20)
        self.itemIndex += 2
        # Define other variables / lists /widgets to be used
        # Coltype combobox list
        self.colType = ['Peptide Sequence', 'Scan Index', 'Scan Number', 'Scan ID', 'Peak List', 'Number of Peaks', 'Peaks Matched Statistics', 'Ions Matched Statistics', 'Total Ion Current', 'Statistic from PSM Source', 'Protvis Link']
        
        
    def onAddCol(self, event):
        self.numCols += 1
        self.grid.Add(colPanel(self, self.numCols), wx.EXPAND)
        self.grid.AddSpacer(5,5)
        self.Fit()
        '''
        self.numCols += 1
        self.colTypeLbl = wx.StaticText(self, label="Column %d \n \n Column Type:" % self.numCols, name=str(self.numCols))

        self.grid.Add(self.colTypeLbl, userData=self.colTypeLbl.GetName())    
        self.grid.Layout()
        self.Fit()
        self.editColType = wx.ComboBox(self, size=(-1, -1), choices=self.colType, style=wx.CB_DROPDOWN, name=str(self.numCols))
        # Create Column type comboBox
        self.grid.Add(self.editColType, userData=self.editColType.GetName())
        self.Bind(wx.EVT_COMBOBOX, self.EvtColType, self.editColType)
        self.removeCol = wx.Button(self, label="Remove Column %d" % self.numCols, name=str(self.numCols))
        self.grid.Add(self.removeCol, userData=self.removeCol.GetName())
        self.removeCol.Bind(wx.EVT_BUTTON, self.onRemoveCol)
        self.grid.Layout()
        self.Fit()
        #self.grid.AddSpacer(20,20)
        self.grid.Layout()
        self.Fit()
        self.itemIndex += 3
        '''
    
    # Helper function for removing columns
    def removeItem(self,event):
        Childrens=self.grid.GetChildren()
        for child in Childrens:
            if child.GetUserData()==event.GetEventObject().GetName():
                self.itemIndex -= 1
                self.grid.Hide(child.GetWindow())
                self.grid.Remove(child.GetWindow())
    '''
    def onRemoveCol(self, event):
        self.removeItem(event)
        self.numCols -= 1
        self.grid.Layout()
        self.Fit()
        '''
            
    def EvtPsmType(self, event):
        # need to record variable, prolly sth like self.type=
        pass
    def EvtReport(self, event):
        # again, set variable
        pass
    def EvtPeakList(self, event):
        # Same
        pass
    def EvtOutType(self, event):
        pass
    def EvtMass(self, event):
        pass
    def EvtMassType(self, event):
        pass
    def EvtFType(self, event):        
        pass

    # A helper function to find the insert position
    # GetEventObject
    def findIndex(self, event):
        # Get event's object (window)
        # go through the panel and find child's window matching the event object window
        # keep a counter that increments until that point
        eventWindow=event.GetEventObject()
        childrens=self.grid.GetChildren()
        insertIndex=0
        for i in range(len(childrens)):
            if childrens[i].GetWindow() != eventWindow:
                insertIndex += 1
            else:
                insertIndex += 1
                break
        print insertIndex
        return insertIndex
    '''
    def EvtColType(self, event):
        eventName=event.GetEventObject().GetName()
        InsertObjectPos=self.findIndex(event)
        if event.GetString()=='Number of Peaks':
            label = wx.StaticText(self, label="Peak Filters", name=eventName)
            
            self.grid.Insert(InsertObjectPos, label, userData=eventName)
            self.grid.Layout()
            self.Fit()
            # Maybe use button name?
            addPeakFilter = wx.Button(self, label="Add new Peak Filter", name=eventName)
            self.grid.Insert(InsertObjectPos+1, addPeakFilter, userData=eventName)
            addPeakFilter.Bind(wx.EVT_BUTTON, self.onAddPeakFilter)
            self.grid.Layout()
            self.Fit()
            self.itemIndex += 2
    # handling addPeakFilter
    '''
    def onAddPeakFilter(self, event):
        pass
    def onButtonDone(self, event):
        self.parent.DeletePage(0)

        
        #self.label = wx.StaticText(parent, -1, "Peptide-Spectrum-Matches Evaluation of File:")
        # self.text = wx.TextCtrl(parent, -1, "Filename", size=(175, -1))

        #grid = wx.GridBagSizer(hgap=10, vgap=10)
        #hSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        #grid.Add(self.label, pos=(10,0))
        # sizer.Add(self.text)
        
        
        #self.Show()
