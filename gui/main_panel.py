import wx
import wx.lib.scrolledpanel as scrolled
import yaml
from col_panel import *
import wx.lib.buttons as buttons
import os


class mainPanel(scrolled.ScrolledPanel):
    # ToDo: When initiating, pass in all list of choices for setting up the choices box
    # ToDo: Error handling
    def __init__(self, parent, id, title):
        scrolled.ScrolledPanel.__init__(self, parent, name=title)
        self.SetAutoLayout(True)
        self.parent = parent

        self.itemIndex = 0
        # Variable to keep track of number of columns added
        self.numCols = 0

        self.grid = wx.BoxSizer(wx.VERTICAL)
        font1 = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD)
        font2 = wx.Font(10, wx.ROMAN, wx.NORMAL, wx.BOLD)
        
        t = wx.StaticText(self, -1, "Please specify requirements:")
        t.SetFont(font1)
        self.grid.Add(t)
        self.grid.AddSpacer(5,5)
        self.itemIndex += 2

        self.SetSizer(self.grid)
        self.SetupScrolling()
       
        font1 = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD)

        # List of variables
        self.psms_typeVal = ''
        self.psmsVal = ''
        self.mass_toleranceVal = ''
        self.columns = ''
        self.peak_listVal = ''
        self.outtypeVal = ''
        self.masstypeVal = ''
        # Define peak_filterVals for reference
        self.top_third = {'type': 'quantile', 'q': 3, 'k': 1, 'percent': 0.02}
        self.peak_filter_defs = {'top_third': self.top_third}
        # Define ion_defs for reference
        self.ionseries = ['y1', 'b1', 'internal', 'm1', 'm2']
        self.ionlosses = ['H2O', 'CO', 'NH3']
        self.aggressive = {'series': self.ionseries, 'losses': self.ionlosses}
        self.ions_defs = {'aggressive': self.aggressive}
        
        # PSMs Type combobox
        self.psmType = ['mzid', 'ProteinPilot Peptide Report']
        self.lblPsmType = wx.StaticText(self, label="PSMs Type:")
        self.lblPsmType.SetFont(font2)
        self.grid.Add(self.lblPsmType)
        self.editPsmType = wx.ComboBox(self, size=(-1, -1), choices=self.psmType, style=wx.CB_DROPDOWN)
        self.grid.Add(self.editPsmType)
        self.editPsmType.SetValue(self.psmType[0])
        
        self.psms_typeVal = self.psmType[0]
        
        self.Bind(wx.EVT_COMBOBOX, self.EvtPsmType, self.editPsmType)
        self.grid.AddSpacer(5,5)
        self.itemIndex += 3
        
        # ProteinPilot Peptide Report combobox
        # Need to replace contents dynamically
        self.report = ['test-data/test2.mzid']
        self.lblReport = wx.StaticText(self, label="ProteinPilot Peptide Report:")
        self.lblReport.SetFont(font2)
        self.grid.Add(self.lblReport)
        self.editReport = wx.ComboBox(self,size=(-1, -1), choices=self.report, style=wx.CB_DROPDOWN)
        self.grid.Add(self.editReport)
        self.editReport.SetValue(self.report[0])
        
        self.psmsVal = str(self.report[0])
        
        self.Bind(wx.EVT_COMBOBOX, self.EvtReport, self.editReport)
        self.grid.AddSpacer(5,5)
        self.itemIndex += 3

        # Peak list listbox
        # Need to replace contents dynamically
        self.fType = ['files directly', 'by multifile']
        self.peakList = ['test-data/test2.mzML']
        self.multiList = ['test-data/test2.mzML', 'e']
        
        self.lblPeakList = wx.StaticText(self, label="Peak List (mzML):")
        self.lblPeakList.SetFont(font2)
        self.grid.Add(self.lblPeakList)
        self.itemIndex += 1
        
        # Add option to select dierectly or by multifile
        self.fTypeBox = wx.RadioBox(self, label="select ", choices=self.fType, style=wx.RA_SPECIFY_COLS)
        self.grid.Add(self.fTypeBox)
        self.Bind(wx.EVT_RADIOBOX, self.EvtFType, self.fTypeBox)
        # Default to select by file directly
        self.editPeakList = wx.ListBox(self, size=(-1, -1), choices=self.peakList, style=wx.LB_MULTIPLE, name='direct')
        for i in range(len(self.peakList)):
            self.editPeakList.Select(i)
        
        self.peak_listVal = [self.peakList[i] for i in self.editPeakList.GetSelections()]
        
        self.grid.Add(self.editPeakList)
        self.Bind(wx.EVT_LISTBOX, self.EvtPeakList, self.editPeakList)

        # by multifile
        self.editMultiList = wx.ComboBox(self, size=(-1, -1), choices=self.multiList, style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.EvtMultiList, self.editMultiList)
        self.grid.Add(self.editMultiList)
        self.editMultiList.SetValue(self.multiList[0])
        self.grid.Hide(self.editMultiList)
        
        self.grid.AddSpacer(5,5)
        self.itemIndex += 3
        
        # Output type combobox
        self.outType = ['Tabular (tsv)', 'HTML']
        self.lblOutType = wx.StaticText(self, label="Output Type:")
        self.lblOutType.SetFont(font2)
        self.grid.Add(self.lblOutType)
        self.editOutType = wx.ComboBox(self, size=(-1, -1), choices=self.outType, style=wx.CB_DROPDOWN)
        self.grid.Add(self.editOutType)
        self.Bind(wx.EVT_COMBOBOX, self.EvtOutType, self.editOutType)
        self.editOutType.SetValue(self.outType[0])

        self.outtypeVal = self.outType[0]

        self.grid.AddSpacer(5,5)
        self.itemIndex += 3
        
        # Default mass tolerance edit control
        self.lblMass = wx.StaticText(self, label="Default Mass Tolerance:")
        self.lblMass.SetFont(font2)
        self.grid.Add(self.lblMass)
        self.editMass = wx.TextCtrl(self, value="1.5")

        self.grid.Add(self.editMass)
        self.Bind(wx.EVT_TEXT, self.EvtMass, self.editMass)
        self.grid.AddSpacer(5,5)
        
        # Mass type combobox
        self.massType = ['Monoisotopic', 'Average (has known problem)']
        self.lblmassType = wx.StaticText(self, label="Mass Type")
        self.lblmassType.SetFont(font2)
        self.grid.Add(self.lblmassType)
        self.editMassType = wx.ComboBox(self, size=(-1, -1), choices=self.massType, style=wx.CB_DROPDOWN)
        self.grid.Add(self.editMassType)
        self.Bind(wx.EVT_COMBOBOX, self.EvtMassType, self.editMassType)
        self.editMassType.SetValue(self.massType[0])
        
        self.masstypeVal = self.massType[0]
        
        self.grid.AddSpacer(5,5)
        self.itemIndex += 3
        
        # Columns
        # Static line
        self.lblCol = wx.StaticText(self, label="Columns")
        self.lblCol.SetFont(font2)
        self.grid.Add(self.lblCol)
        
        self.addCol = wx.Button(self, label="Add new Column")
        self.addCol.Bind(wx.EVT_BUTTON, self.onAddCol)
        self.grid.Add(self.addCol)
        self.itemIndex += 2
        self.grid.AddSpacer(10,10)
        # self.removeCol = wx.Button(self, label="Remove Column %d" % self.numCols)
        # self.grid.Add(self.removeCol)
        # self.removeCol.Bind(wx.EVT_BUTTON, self.onRemoveCol)
        self.buttonExe = wx.Button(self, -1, label="Execute", size=(-1, -1))
        self.buttonExe.Bind(wx.EVT_BUTTON, self.onButtonExe)
        
        self.buttonExe.SetForegroundColour(wx.WHITE)
        self.buttonExe.SetBackgroundColour(wx.BLUE)
        self.grid.Add(self.buttonExe, 0)
        self.itemIndex += 1
        
        self.buttonCancel = wx.Button(self, -1, label="Cancel", size=(-1, -1))
        self.buttonCancel.Bind(wx.EVT_BUTTON, self.onButtonCancel)
        self.grid.Add(self.buttonCancel, 0)
        self.itemIndex += 1
        # Define other variables / lists /widgets to be used

        
        # Coltype combobox list
        self.colType = ['Peptide Sequence', 'Scan Index', 'Scan Number', 'Scan ID', 'Peak List', 'Number of Peaks', 'Peaks Matched Statistics', 'Ions Matched Statistics', 'Total Ion Current', 'Statistic from PSM Source', 'Protvis Link']
        
        self.submission = {}
        self.columns = []
        self.columnTitles = []
    def onButtonExe(self, event):
        self.submission['peak_list'] = self.peak_listVal
        self.submission['psms_type'] = self.psms_typeVal
        self.submission['psms'] = self.psmsVal
        self.submission['mass_tolerance'] = float(self.editMass.GetValue())
        self.submission['ions_defs'] = self.ions_defs
        self.submission['peak_filter_defs'] = self.peak_filter_defs
        self.submission['columns'] = self.columns
        f = open('../columns.txt', 'w')
        for col in self.submission['columns']:
            f.write("%s\n" % col['title'])
        f.close()
        self.submission['outtype'] = self.outtypeVal
        self.submission['masstype'] = self.masstypeVal
        stream = file('settings2.yaml', 'w')
        yaml.dump(self.submission, stream, default_flow_style=False)
        #This can be made better and cleaner?
        #python 2.7 needed to run pyteomics, but 2.6 needed to run the installed version of wxpython
        os.system('module load python-epd && cd .. && python -m psme.main')

    def onAddCol(self, event):
        self.itemIndex += 1
        self.numCols += 1
        self.grid.Insert(self.itemIndex-2, colPanel(self, self.numCols), wx.EXPAND)
        #self.grid.AddSpacer(5,5)
        self.Fit()
       
    
    # Helper function for removing columns
    def removeItem(self,event):
        Childrens=self.grid.GetChildren()
        for child in Childrens:
            if child.GetUserData()==event.GetEventObject().GetName():
                self.itemIndex -= 1
                self.grid.Hide(child.GetWindow())
                self.grid.Remove(child.GetWindow())
    
    def EvtFType(self, event):        
        value = self.fTypeBox.GetSelection()
        if value == 0:
            if self.editMultiList.IsShown():
                self.grid.Hide(self.editMultiList)
                self.grid.Show(self.editPeakList)
                self.peak_listVal = [self.peakList[i] for i in self.editPeakList.GetSelections()]
                self.Fit()
        else:
            if self.editPeakList.IsShown():
                self.grid.Hide(self.editPeakList)
                self.grid.Show(self.editMultiList)
                self.peak_listVal = str(self.editMultiList.GetValue())
                self.Fit()
            
        pass
    # Helper function to rename col button numbers after removing
    def rename(self):
        childrens = self.grid.GetChildren()
        colChildrens = []
        for child in childrens:
            if child.GetWindow() != None and child.GetWindow().GetName() == 'colPanel':
                colChildrens.append(child)
        for i in range(len(colChildrens)):
            colChildrens[i].GetWindow().colNum = i+1
            colChildrens[i].GetWindow().colTypeLbl.SetLabel("Column %d \n \n Column Type:" % (i+1))
            colChildrens[i].GetWindow().removeCol.SetLabel("Remove Column %d" % (i+1))
            colChildrens[i].GetWindow().colTypeLbl.SetName("Column %d \n \n Column Type:" % (i+1))
            colChildrens[i].GetWindow().removeCol.SetName("Remove Column %d" % (i+1))
            
    def EvtPsmType(self, event):
        self.psm_typeVal = self.editPsmType.GetValue()
        # need to record variable, prolly sth like self.type=
    def EvtReport(self, event):
        self.psmsVal = self.editReport.GetValue()
        # again, set variable
    def EvtPeakList(self, event):
        # Same
        self.peak_listVal = [self.peakList[i] for i in self.editPeakList.GetSelections()]
    def EvtMultiList(self, event):
        self.peak_listVal = str(self.editMultiList.GetValue())
    def EvtOutType(self, event):
        self.outtypeVal = self.editOutType.GetValue()
    def EvtMass(self, event):
        self.mass_toleranceVal = self.editMass.GetValue()
    def EvtMassType(self, event):
        self.masstypeVal = self.editMassType.GetValue()
                              
    

    # A helper function to find the insert position
    # GetEventObject
        #Useless function
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
        return insertIndex

    def onButtonCancel(self, event):
        self.parent.DeletePage(0)
