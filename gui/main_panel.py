import wx
import wx.lib.scrolledpanel as scrolled
import yaml
import wx.lib.buttons as buttons

import os
import exceptions

from col_panel import *
from table_panel import *
from psme.driver import *
from psme.settings import *


class mainPanel(scrolled.ScrolledPanel):
    # ToDo: Set default values, including for the filter
    # ToDo: Error handling
    def __init__(self, parent, id, title, evalNum):
        scrolled.ScrolledPanel.__init__(self, parent, name=title)

        # This might not be necessary
        self.SetAutoLayout(True)
        
        self.parent = parent
        
        # boolean to keep track of whether to output results in tsv file
        self.outFile = False
       
        # keep track of the number of eavaluation pages added
        self.evalNum = evalNum
        
        # keep track of the index of each widget
        self.itemIndex = 0
        
        # keep track of number of columns added
        self.numCols = 0

        # keep track of the file path of Peak lists for opening in spectrum viewer later
        self.filepath = ""

        # set up the sizer
        self.grid = wx.BoxSizer(wx.VERTICAL)        
        self.SetSizer(self.grid)
        self.SetupScrolling()

        # set up fonts
        font1 = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD)
        font2 = wx.Font(10, wx.ROMAN, wx.NORMAL, wx.BOLD)
        
        # init list of variables
        self.psms_typeVal = ''
        self.psmsVal = ''
        self.mass_toleranceVal = 0.0
        self.columns = ''
        self.peak_listVal = ''
        self.outtypeVal = ''
        self.masstypeVal = ''

        self.submission = {}
        self.columns = []
        
        # Define peak_filterVals for reference
        self.top_third = {'type': 'quantile', 'q': 3, 'k': 1, 'percent': 0.02}
        self.peak_filter_defs = {'top_third': self.top_third}
        
        # Define ion_defs for reference
        self.ionseries = ['y1', 'b1', 'internal', 'm1', 'm2']
        self.ionlosses = ['H2O', 'CO', 'NH3']
        self.aggressive = {'series': self.ionseries, 'losses': self.ionlosses}
        self.ions_defs = {'aggressive': self.aggressive}
        
        # Prompt at top
        t = wx.StaticText(self, -1, "Please specify requirements:")
        t.SetFont(font1)
        self.grid.Add(t)
        self.grid.AddSpacer(10,10)
        self.itemIndex += 2
        
        # PSMs Type combobox
        self.psmType = ['mzid', 'proteinpilot_peptide_report']
        self.lblPsmType = wx.StaticText(self, label="PSMs Type:")
        self.lblPsmType.SetFont(font2)
        self.grid.Add(self.lblPsmType)
        self.editPsmType = wx.ComboBox(self, size=(-1, -1), choices=self.psmType, style=wx.CB_DROPDOWN)        
        self.Bind(wx.EVT_COMBOBOX, self.EvtPsmType, self.editPsmType)
        self.grid.Add(self.editPsmType)

        self.editPsmType.SetValue(self.psmType[0])        
        self.psms_typeVal = self.psmType[0]
                
        self.grid.AddSpacer(5,5)
       
        self.itemIndex += 3
        
        # ProteinPilot Peptide Report combobox
        # TESTING doesnt work
        
        # keeps track of what is already in the choices of the combobox
        self.report = []

        self.lblReport = wx.StaticText(self, label="MzidentML containing PSMs:")
        self.lblReport.SetFont(font2)
        self.grid.Add(self.lblReport)

        # load button
        self.load = wx.Button(self, size=(60, 25),label="load")
        self.load.Bind(wx.EVT_BUTTON, self.onLoad)
        self.grid.Add(self.load)
        self.itemIndex += 1

        self.editReport = wx.ComboBox(self,size=(-1, -1), choices=self.report, style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.EvtReport, self.editReport)
        self.grid.Add(self.editReport)
        
        #self.editReport.SetValue(self.report[0])
        #self.psmsVal = self.str(self.report[0])
        
        self.grid.AddSpacer(5,5)
       
        self.itemIndex += 3

        # Peak list listbox
        self.fType = ['by multifile', 'files directly']
        self.peakList = []
        self.multiList = []
        
        self.lblPeakList = wx.StaticText(self, label="Peak List (mzML):")
        self.lblPeakList.SetFont(font2)
        self.grid.Add(self.lblPeakList)
        self.itemIndex += 1
        
        # Add option to select dierectly or by multifile
        self.fTypeBox = wx.RadioBox(self, label="select ", choices=self.fType, style=wx.RA_SPECIFY_COLS)
        self.Bind(wx.EVT_RADIOBOX, self.EvtFType, self.fTypeBox)
        self.grid.Add(self.fTypeBox)
        
        # load button
        self.load2 = wx.Button(self, size=(60, 25), label="load")
        self.load2.Bind(wx.EVT_BUTTON, self.onLoad2)
        self.grid.Add(self.load2)
        self.itemIndex +=1

        # Default to by multifile
        self.editMultiList = wx.ComboBox(self, size=(-1, -1), choices=self.multiList, style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.EvtMultiList, self.editMultiList)
        self.grid.Add(self.editMultiList)

        # by file directly
        self.editPeakList = wx.ListBox(self, size=(-1, -1), choices=self.peakList, style=wx.LB_MULTIPLE, name='direct')
        self.Bind(wx.EVT_LISTBOX, self.EvtPeakList, self.editPeakList)
        self.grid.Add(self.editPeakList)
        
        self.grid.Hide(self.editPeakList)
        
        self.grid.AddSpacer(5,5)
        self.itemIndex += 3
        
        # Output type combobox
        self.outType = ['Tabular (tsv)', 'HTML']
        self.lblOutType = wx.StaticText(self, label="Output Type:")
        self.lblOutType.SetFont(font2)
        self.grid.Add(self.lblOutType)
        
        self.editOutType = wx.ComboBox(self, size=(-1, -1), choices=self.outType, style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.EvtOutType, self.editOutType)
        self.grid.Add(self.editOutType)
       
        self.editOutType.SetValue(self.outType[0])
        self.outtypeVal = self.outType[0]

        self.grid.AddSpacer(5,5)
        self.itemIndex += 3
        
        # Default mass tolerance edit control
        self.lblMass = wx.StaticText(self, label="Default Mass Tolerance:")
        self.lblMass.SetFont(font2)
        self.grid.Add(self.lblMass)
        
        self.editMass = wx.TextCtrl(self, value="1.5")
        self.mass_toleranceVal = 1.5
        self.Bind(wx.EVT_TEXT, self.EvtMass, self.editMass)
        self.grid.Add(self.editMass)
        
        self.grid.AddSpacer(5,5)
        self.itemIndex += 3
        
        # Mass type combobox
        self.massType = ['Monoisotopic', 'Average (has known problem)']
        self.lblmassType = wx.StaticText(self, label="Mass Type")
        self.lblmassType.SetFont(font2)
        self.grid.Add(self.lblmassType)
        
        self.editMassType = wx.ComboBox(self, size=(-1, -1), choices=self.massType, style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.EvtMassType, self.editMassType)
        self.grid.Add(self.editMassType)
       
        self.editMassType.SetValue(self.massType[0])
        self.masstypeVal = self.massType[0]
        
        self.grid.AddSpacer(5,5)
        self.itemIndex += 3
        
        # Add Columns button
        # Static line
        self.lblCol = wx.StaticText(self, label="Columns")
        self.lblCol.SetFont(font2)
        self.grid.Add(self.lblCol)
        
        self.addCol = wx.Button(self, label="Add new Column")
        self.addCol.Bind(wx.EVT_BUTTON, self.onAddCol)
        self.grid.Add(self.addCol)
        
        self.grid.AddSpacer(10,10)
        self.itemIndex += 3
        
        # Output to file checkbox
        self.checkOut = wx.CheckBox(self, label="Output Results to File")
        self.checkOut.Bind(wx.EVT_CHECKBOX, self.onCheckOut)
        self.grid.Add(self.checkOut, 0)
        self.itemIndex += 1
        
        # Execute button
        self.buttonExe = wx.Button(self, -1, label="Execute", size=(-1, -1))
        self.buttonExe.SetForegroundColour(wx.WHITE)
        self.buttonExe.SetBackgroundColour(wx.BLUE)
        self.buttonExe.Bind(wx.EVT_BUTTON, self.onButtonExe)        
        self.grid.Add(self.buttonExe, 0)
        
        self.itemIndex += 1
        
        # Cancel button
        self.buttonCancel = wx.Button(self, -1, label="Cancel", size=(-1, -1))
        self.buttonCancel.Bind(wx.EVT_BUTTON, self.onButtonCancel)
        self.grid.Add(self.buttonCancel, 0)
        self.itemIndex += 1
        
# ========================================================================= #
# Events 
    def onCheckOut(self, event):
        if self.checkOut.GetValue():
            self.outFile = True
        else:
            self.outFile = False
    
    def onLoad(self, event):
        filters = 'mzid file (*.mzid) |*.mzid| text files (*.txt) |*.txt| All files (*.*)|*.*'
        dialog = wx.FileDialog(None, message = 'Load report for PSME', wildcard = filters, style = wx.FD_OPEN | wx.FD_MULTIPLE)
        if dialog.ShowModal() == wx.ID_OK:
            selected = dialog.GetPaths()
            for selection in selected:
                if selection not in self.report:
                    self.report.append(selection)
                    self.editReport.Append(selection)
            self.editReport.SetSelection(0)
            self.psmsVal = str(self.editReport.GetValue())
            self.FitInside()
            self.parent.Layout()
        else:
            print 'Nothing Selected'

    # ----

    def onLoad2(self, event):
        filters = 'mzml files (*.mzML) |*.mzML| mgf files (*.mgf) |*.mgf| text files (*.txt) |*.txt| All files (*.*)|*.*'
        dialog = wx.FileDialog(None, message = 'Load Peak List for PSME', wildcard = filters, style = wx.FD_OPEN | wx.FD_MULTIPLE)
        if dialog.ShowModal() == wx.ID_OK:
            selected = dialog.GetPaths()
            for selection in selected:
                if selection not in self.multiList:
                    self.multiList.append(selection)
                    self.editMultiList.Append(selection)
                    self.editPeakList.AppendAndEnsureVisible(selection)
                    self.editPeakList.SetStringSelection(selection)
            if self.editMultiList.IsShown():
                self.editMultiList.SetSelection(0)
                self.peak_listVal = str(self.editMultiList.GetValue())
            else:
                self.peak_listVal = [str(self.editPeakList.GetString(i)) for i in self.editPeakList.GetSelections()]
            self.FitInside()
            self.parent.Layout()
        else:
            print 'Nothing Selected'
    
    # ----
                
    def onButtonExe(self, event):
        # Wait till analysis finishes before changing back to original button label
        self.buttonExe.SetLabel('Working...')
        wx.Yield()
        
        # create submission list
        self.submission['peak_list'] = self.peak_listVal
        self.submission['psms_type'] = self.psms_typeVal
        self.submission['psms'] = self.psmsVal
        # set default for convenient debugging
        # self.submission['peak_list'] = '/home/ubuntu/psm-eval/test-data/test2.mzML'
        # self.submission['psms'] = '/home/ubuntu/psm-eval/test-data/test2.mzid'
        self.submission['mass_tolerance'] = self.mass_toleranceVal
        self.submission['ions_defs'] = self.ions_defs
        self.submission['peak_filter_defs'] = self.peak_filter_defs
        self.submission['columns'] = self.columns
        self.submission['outtype'] = self.outtypeVal
        self.submission['masstype'] = self.masstypeVal

        # record the path to the mzML file for opening spectrum viewer later
        self.filepath = self.submission['peak_list']
        
        # create yaml file based on submission
        stream = file('settings.yaml', 'w')
        yaml.dump(self.submission, stream, default_flow_style=False)
        
        # TODO: Maybe add a progress bar
        # os.system('cd .. && python -m psme.main')
        
        settings = load_settings()
        
        # evaluate(settings)

        stats = collect_statistics(settings)
        colLbls = [col['title'] for col in self.submission['columns']]
        stats.insert(0, colLbls)

        self.buttonExe.SetLabel('Execute')
        
        curPage = self.parent.AddPage(tablePanel(self.parent, 1, stats, self.filepath, self.outFile), "Result %d" % self.evalNum, select = True)
       
    # ----

    def onAddCol(self, event):
        self.itemIndex += 1
        self.numCols += 1
        self.grid.Insert(self.itemIndex-5, colPanel(self, self.numCols), wx.EXPAND)
        self.FitInside()
        self.parent.Layout()
       
    # ----
    
    def EvtFType(self, event):        
        value = self.fTypeBox.GetSelection()
        if value == 1:
            if self.editMultiList.IsShown():
                self.grid.Hide(self.editMultiList)
                self.grid.Show(self.editPeakList)
                self.peak_listVal = [str(self.editPeakList.GetString(i)) for i in self.editPeakList.GetSelections()]
                self.FitInside()
        else:
            if self.editPeakList.IsShown():
                self.grid.Hide(self.editPeakList)
                self.grid.Show(self.editMultiList)
                self.peak_listVal = str(self.editMultiList.GetValue())
                self.FitInside()
        self.parent.Layout()

    # ----
    def EvtPeakList(self, event):
        self.peak_listVal = [str(self.editPeakList.GetString(i)) for i in self.editPeakList.GetSelections()]
    
    # ----
    def EvtMultiList(self, event):
        self.peak_listVal = str(self.editMultiList.GetValue())
    
    # ----
    def EvtPsmType(self, event):
        self.psms_typeVal = str(self.editPsmType.GetValue())
        if self.psms_typeVal == 'mzid':
            self.lblReport.SetLabel('MzidentML containing PSMs:')
        else:
            self.lblReport.SetLabel('ProteinPilot Peptied Report:')
        
    
    # ----
    def EvtReport(self, event):
        self.psmsVal = str(self.editReport.GetValue())
        
    # ----
    def EvtOutType(self, event):
        self.outtypeVal = str(self.editOutType.GetValue())
    
    # Helper function for turning field into float value
    def toFloat(self, value):
        try:
            return float(value)
        except exceptions.ValueError:
            print "field empty or contains invalid character: using 0.0"
            return 0.0
   
    # ----
    def EvtMass(self, event):
        self.mass_toleranceVal = self.toFloat(self.editMass.GetValue())
        
    # ----            
    def EvtMassType(self, event):
        self.masstypeVal = str(self.editMassType.GetValue())
        
    # ----
    def onButtonCancel(self, event):
        index = self.parent.GetPageIndex(self)
        self.parent.DeletePage(index)
    
    # Helper function to rename col button numbers after removing (called by column childrens)
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
