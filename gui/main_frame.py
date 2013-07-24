# load sytem functions
import time
import threading
import os

# import Python lilbraries
import wx
import wx.aui
import re

# load gui modules
from main_panel import *

# load mMass modules
import mMass
from mMass.gui.panel_spectrum import *
from mMass.gui.panel_documents import panelDocuments
from mMass.gui.panel_document_info import panelDocumentInfo
from mMass.gui.panel_peaklist import panelPeaklist
from ids import *
from mMass.gui.mwx import *
from mMass.gui.images import *
from mMass.gui.config import *
from mMass.gui.dlg_select_scans import dlgSelectScans
from mMass.gui.dlg_clipboard_editor import dlgClipboardEditor
import mMass.gui.doc as doc

# Main Frame

class mainFrame(wx.Frame):
    
    def __init__(self, parent, id, title):

        wx.Frame.__init__(self, parent, -1, title, size=(1000,800))

        # global counter for the sequence of files being evaluated
        self.evalNum = 0

        # init images
        images.loadImages()
        
        # set icon
        icons = wx.IconBundle()
        icons.AddIcon(images.lib['icon16'])
        icons.AddIcon(images.lib['icon32'])
        icons.AddIcon(images.lib['icon48'])
        icons.AddIcon(images.lib['icon128'])
        icons.AddIcon(images.lib['icon256'])
        self.SetIcons(icons)

        
        
        # init basics
        self.documents = []
        self.currentDocument = None
        self.currentDocumentXML = None
        self.currentSequence = None
        
        self.documentsSoloCurrent = None
        self.documentsSoloPrevious = {}
        self.usedColours = []
        
        self.bufferedScanlists = {}
        
        self.processingDocumentQueue = False
        self.tmpDocumentQueue = []
        self.tmpScanlist = None
        self.tmpSequenceList = None
        self.tmpCompassXport = None
        self.tmpLibrarySaved = None

        # Notebook widget for PSM-evaluations
        self.nb = wx.aui.AuiNotebook(self)
        self.makeMenuBar()
        
        # setup menubar
        self.SetMenuBar(self.menubar)
        self.updateControls()


#==========================================================================#

    def makeMenuBar(self):
        # init menubar
        # HK_ indicates hotkeys

        self.menubar = wx.MenuBar()

        # file
        document = wx.Menu()
        document.Append(ID_documentNew, "New"+HK_documentNew, "")
        document.Append(ID_documentOpen, "Open..."+HK_documentOpen, "")
        document.AppendSeparator()
        document.Append(ID_documentClose, "Close"+HK_documentClose, "")
        document.Append(ID_documentCloseAll, "Close All"+HK_documentCloseAll, "")
        document.AppendSeparator()
        document.Append(ID_quit, "Quit"+HK_quit, "Quit PSME")
        
        self.Bind(wx.EVT_MENU, self.onDocumentNew, id=ID_documentNew)        
        self.Bind(wx.EVT_MENU, self.onDocumentOpen, id=ID_documentOpen)
        self.Bind(wx.EVT_MENU, self.onDocumentClose, id=ID_documentClose)
        self.Bind(wx.EVT_MENU, self.onDocumentCloseAll, id=ID_documentCloseAll)
        self.Bind(wx.EVT_MENU, self.onQuit, id=ID_quit)
        
        self.menubar.Append(document, "File")

        # view
        view = wx.Menu()
        view.Append(ID_viewSpectrum, "Spectrum Viewer")
        self.Bind(wx.EVT_MENU, self.onSpectViewer, id=ID_viewSpectrum)

        viewCanvas = wx.Menu()
        viewCanvas.Append(ID_viewLegend, "Legend", "", wx.ITEM_CHECK)
        viewCanvas.Append(ID_viewGrid, "Gridlines", "", wx.ITEM_CHECK)
        viewCanvas.Append(ID_viewMinorTicks, "Minor Ticks", "", wx.ITEM_CHECK)
        viewCanvas.Append(ID_viewDataPoints, "Data Points", "", wx.ITEM_CHECK)
        viewCanvas.AppendSeparator()
        viewCanvas.Append(ID_viewPosBars, "Position Bars"+HK_viewPosBars, "", wx.ITEM_CHECK)
        viewCanvas.AppendSeparator()
        viewCanvas.Append(ID_viewGel, "Gel View"+HK_viewGel, "", wx.ITEM_CHECK)
        viewCanvas.Append(ID_viewGelLegend, "Gel View Legend", "", wx.ITEM_CHECK)
        viewCanvas.AppendSeparator()
        viewCanvas.Append(ID_viewTracker, "Cursor Tracker", "", wx.ITEM_CHECK)
        viewCanvas.Append(ID_viewCheckLimits, "Check Limits", "", wx.ITEM_CHECK)
        view.AppendMenu(-1, "Spectrum Canvas", viewCanvas)
        
        viewLabels = wx.Menu()
        title = ("Show Labels", "Hide Labels")
        viewLabels.Append(ID_viewLabels, title[bool(config.spectrum['showLabels'])]+HK_viewLabels, "")
        title = ("Show Ticks", "Hide Ticks")
        viewLabels.Append(ID_viewTicks, title[bool(config.spectrum['showTicks'])]+HK_viewTicks, "")
        viewLabels.AppendSeparator()
        viewLabels.Append(ID_viewLabelCharge, "Charge", "", wx.ITEM_CHECK)
        viewLabels.Append(ID_viewLabelGroup, "Group", "", wx.ITEM_CHECK)
        viewLabels.Append(ID_viewLabelBgr, "Background", "", wx.ITEM_CHECK)
        viewLabels.AppendSeparator()
        title = ("Vertical Labels", "Horizontal Labels")
        viewLabels.Append(ID_viewLabelAngle, title[bool(config.spectrum['labelAngle'])]+HK_viewLabelAngle, "")
        viewLabels.AppendSeparator()
        viewLabels.Append(ID_viewOverlapLabels, "Allow Overlapping"+HK_viewOverlapLabels, "", wx.ITEM_CHECK)
        viewLabels.Append(ID_viewAllLabels, "Labels in All Documents"+HK_viewAllLabels, "", wx.ITEM_CHECK)
        view.AppendMenu(-1, "Peak Labels", viewLabels)
        
        viewNotations = wx.Menu()
        title = ("Show Notations", "Hide Notations")
        viewNotations.Append(ID_viewNotations, title[bool(config.spectrum['showNotations'])], "")
        viewNotations.AppendSeparator()
        viewNotations.Append(ID_viewNotationMarks, "Marks", "", wx.ITEM_CHECK)
        viewNotations.Append(ID_viewNotationLabels, "Labels", "", wx.ITEM_CHECK)
        viewNotations.Append(ID_viewNotationMz, "m/z", "", wx.ITEM_CHECK)
        view.AppendMenu(-1, "Notations", viewNotations)
        
        viewSpectrumRuler = wx.Menu()
        viewSpectrumRuler.Append(ID_viewSpectrumRulerMz, "m/z", "", wx.ITEM_CHECK)
        viewSpectrumRuler.Append(ID_viewSpectrumRulerDist, "Distance", "", wx.ITEM_CHECK)
        viewSpectrumRuler.Append(ID_viewSpectrumRulerPpm, "ppm", "", wx.ITEM_CHECK)
        viewSpectrumRuler.Append(ID_viewSpectrumRulerZ, "Charge", "", wx.ITEM_CHECK)
        viewSpectrumRuler.Append(ID_viewSpectrumRulerCursorMass, "Neutral Mass (Cursor)", "", wx.ITEM_CHECK)
        viewSpectrumRuler.Append(ID_viewSpectrumRulerParentMass, "Neutral Mass (Parent)", "", wx.ITEM_CHECK)
        viewSpectrumRuler.Append(ID_viewSpectrumRulerArea, "Area", "", wx.ITEM_CHECK)
        view.AppendMenu(-1, "Spectrum Ruler", viewSpectrumRuler)
        
        viewPeaklistColumns = wx.Menu()
        viewPeaklistColumns.Append(ID_viewPeaklistColumnMz, "m/z", "", wx.ITEM_CHECK)
        viewPeaklistColumns.Append(ID_viewPeaklistColumnAi, "a.i.", "", wx.ITEM_CHECK)
        viewPeaklistColumns.Append(ID_viewPeaklistColumnInt, "Intensity", "", wx.ITEM_CHECK)
        viewPeaklistColumns.Append(ID_viewPeaklistColumnBase, "Baseline", "", wx.ITEM_CHECK)
        viewPeaklistColumns.Append(ID_viewPeaklistColumnRel, "Rel. Intensity", "", wx.ITEM_CHECK)
        viewPeaklistColumns.Append(ID_viewPeaklistColumnSn, "s/n", "", wx.ITEM_CHECK)
        viewPeaklistColumns.Append(ID_viewPeaklistColumnZ, "Charge", "", wx.ITEM_CHECK)
        viewPeaklistColumns.Append(ID_viewPeaklistColumnMass, "Mass", "", wx.ITEM_CHECK)
        viewPeaklistColumns.Append(ID_viewPeaklistColumnFwhm, "FWHM", "", wx.ITEM_CHECK)
        viewPeaklistColumns.Append(ID_viewPeaklistColumnResol, "Resolution", "", wx.ITEM_CHECK)
        viewPeaklistColumns.Append(ID_viewPeaklistColumnGroup, "Group", "", wx.ITEM_CHECK)
        view.AppendMenu(-1, "Peak List Columns", viewPeaklistColumns)
        
        view.AppendSeparator()
        view.Append(ID_viewAutoscale, "Autoscale Intensity"+HK_viewAutoscale, "", wx.ITEM_CHECK)
        view.Append(ID_viewNormalize, "Normalize Intensity"+HK_viewNormalize, "", wx.ITEM_CHECK)
        view.AppendSeparator()
        view.Append(ID_viewRange, "Set Mass Range..."+HK_viewRange, "")
        view.AppendSeparator()
        view.Append(ID_documentFlip, "Flip Spectrum"+HK_documentFlip, "")
        view.Append(ID_documentOffset, "Offset Spectrum...", "")
        view.Append(ID_documentClearOffsets, "Clear All Offsets", "")
        view.AppendSeparator()
        view.Append(ID_viewCanvasProperties, "Canvas Properties..."+HK_viewCanvasProperties, "")
        
        self.Bind(wx.EVT_MENU, self.onView, id=ID_viewLegend)
        self.Bind(wx.EVT_MENU, self.onView, id=ID_viewGrid)
        self.Bind(wx.EVT_MENU, self.onView, id=ID_viewMinorTicks)
        self.Bind(wx.EVT_MENU, self.onView, id=ID_viewDataPoints)
        self.Bind(wx.EVT_MENU, self.onView, id=ID_viewPosBars)
        self.Bind(wx.EVT_MENU, self.onView, id=ID_viewGel)
        self.Bind(wx.EVT_MENU, self.onView, id=ID_viewGelLegend)
        self.Bind(wx.EVT_MENU, self.onView, id=ID_viewTracker)
        self.Bind(wx.EVT_MENU, self.onView, id=ID_viewCheckLimits)
        
        self.Bind(wx.EVT_MENU, self.onView, id=ID_viewLabels)
        self.Bind(wx.EVT_MENU, self.onView, id=ID_viewTicks)
        self.Bind(wx.EVT_MENU, self.onView, id=ID_viewLabelCharge)
        self.Bind(wx.EVT_MENU, self.onView, id=ID_viewLabelGroup)
        self.Bind(wx.EVT_MENU, self.onView, id=ID_viewLabelBgr)
        self.Bind(wx.EVT_MENU, self.onView, id=ID_viewLabelAngle)
        self.Bind(wx.EVT_MENU, self.onView, id=ID_viewOverlapLabels)
        self.Bind(wx.EVT_MENU, self.onView, id=ID_viewAllLabels)
        
        self.Bind(wx.EVT_MENU, self.onView, id=ID_viewNotations)
        self.Bind(wx.EVT_MENU, self.onView, id=ID_viewNotationMarks)
        self.Bind(wx.EVT_MENU, self.onView, id=ID_viewNotationLabels)
        self.Bind(wx.EVT_MENU, self.onView, id=ID_viewNotationMz)
        
        self.Bind(wx.EVT_MENU, self.onViewSpectrumRuler, id=ID_viewSpectrumRulerMz)
        self.Bind(wx.EVT_MENU, self.onViewSpectrumRuler, id=ID_viewSpectrumRulerDist)
        self.Bind(wx.EVT_MENU, self.onViewSpectrumRuler, id=ID_viewSpectrumRulerPpm)
        self.Bind(wx.EVT_MENU, self.onViewSpectrumRuler, id=ID_viewSpectrumRulerZ)
        self.Bind(wx.EVT_MENU, self.onViewSpectrumRuler, id=ID_viewSpectrumRulerCursorMass)
        self.Bind(wx.EVT_MENU, self.onViewSpectrumRuler, id=ID_viewSpectrumRulerParentMass)
        self.Bind(wx.EVT_MENU, self.onViewSpectrumRuler, id=ID_viewSpectrumRulerArea)
        
        self.Bind(wx.EVT_MENU, self.onViewPeaklistColumns, id=ID_viewPeaklistColumnMz)
        self.Bind(wx.EVT_MENU, self.onViewPeaklistColumns, id=ID_viewPeaklistColumnAi)
        self.Bind(wx.EVT_MENU, self.onViewPeaklistColumns, id=ID_viewPeaklistColumnInt)
        self.Bind(wx.EVT_MENU, self.onViewPeaklistColumns, id=ID_viewPeaklistColumnBase)
        self.Bind(wx.EVT_MENU, self.onViewPeaklistColumns, id=ID_viewPeaklistColumnRel)
        self.Bind(wx.EVT_MENU, self.onViewPeaklistColumns, id=ID_viewPeaklistColumnSn)
        self.Bind(wx.EVT_MENU, self.onViewPeaklistColumns, id=ID_viewPeaklistColumnZ)
        self.Bind(wx.EVT_MENU, self.onViewPeaklistColumns, id=ID_viewPeaklistColumnMass)
        self.Bind(wx.EVT_MENU, self.onViewPeaklistColumns, id=ID_viewPeaklistColumnFwhm)
        self.Bind(wx.EVT_MENU, self.onViewPeaklistColumns, id=ID_viewPeaklistColumnResol)
        self.Bind(wx.EVT_MENU, self.onViewPeaklistColumns, id=ID_viewPeaklistColumnGroup)
        
        self.Bind(wx.EVT_MENU, self.onView, id=ID_viewAutoscale)
        self.Bind(wx.EVT_MENU, self.onView, id=ID_viewNormalize)
        self.Bind(wx.EVT_MENU, self.onViewRange, id=ID_viewRange)
        self.Bind(wx.EVT_MENU, self.onDocumentFlip, id=ID_documentFlip)
        self.Bind(wx.EVT_MENU, self.onDocumentOffset, id=ID_documentOffset)
        self.Bind(wx.EVT_MENU, self.onDocumentOffset, id=ID_documentClearOffsets)
        self.Bind(wx.EVT_MENU, self.onViewCanvasProperties, id=ID_viewCanvasProperties)
        
        self.menubar.Append(view, "View")
        
        self.menubar.Check(ID_viewLegend, bool(config.spectrum['showLegend']))
        self.menubar.Check(ID_viewGrid, bool(config.spectrum['showGrid']))
        self.menubar.Check(ID_viewMinorTicks, bool(config.spectrum['showMinorTicks']))
        self.menubar.Check(ID_viewDataPoints, bool(config.spectrum['showDataPoints']))
        self.menubar.Check(ID_viewPosBars, bool(config.spectrum['showPosBars']))
        self.menubar.Check(ID_viewGel, bool(config.spectrum['showGel']))
        self.menubar.Check(ID_viewGelLegend, bool(config.spectrum['showGelLegend']))
        self.menubar.Check(ID_viewTracker, bool(config.spectrum['showTracker']))
        self.menubar.Check(ID_viewCheckLimits, bool(config.spectrum['checkLimits']))
        
        self.menubar.Check(ID_viewLabelCharge, bool(config.spectrum['labelCharge']))
        self.menubar.Check(ID_viewLabelGroup, bool(config.spectrum['labelGroup']))
        self.menubar.Check(ID_viewLabelBgr, bool(config.spectrum['labelBgr']))
        self.menubar.Check(ID_viewOverlapLabels, bool(config.spectrum['overlapLabels']))
        self.menubar.Check(ID_viewAllLabels, bool(config.spectrum['showAllLabels']))
        
        self.menubar.Check(ID_viewNotationMarks, bool(config.spectrum['notationMarks']))
        self.menubar.Check(ID_viewNotationLabels, bool(config.spectrum['notationLabels']))
        self.menubar.Check(ID_viewNotationMz, bool(config.spectrum['notationMZ']))
        
        self.menubar.Check(ID_viewSpectrumRulerMz, bool('mz' in config.main['cursorInfo']))
        self.menubar.Check(ID_viewSpectrumRulerDist, bool('dist' in config.main['cursorInfo']))
        self.menubar.Check(ID_viewSpectrumRulerPpm, bool('ppm' in config.main['cursorInfo']))
        self.menubar.Check(ID_viewSpectrumRulerZ, bool('z' in config.main['cursorInfo']))
        self.menubar.Check(ID_viewSpectrumRulerCursorMass, bool('cmass' in config.main['cursorInfo']))
        self.menubar.Check(ID_viewSpectrumRulerParentMass, bool('pmass' in config.main['cursorInfo']))
        self.menubar.Check(ID_viewSpectrumRulerArea, bool('area' in config.main['cursorInfo']))
        
        self.menubar.Check(ID_viewPeaklistColumnMz, bool('mz' in config.main['peaklistColumns']))
        self.menubar.Check(ID_viewPeaklistColumnAi, bool('ai' in config.main['peaklistColumns']))
        self.menubar.Check(ID_viewPeaklistColumnBase, bool('base' in config.main['peaklistColumns']))
        self.menubar.Check(ID_viewPeaklistColumnInt, bool('int' in config.main['peaklistColumns']))
        self.menubar.Check(ID_viewPeaklistColumnRel, bool('rel' in config.main['peaklistColumns']))
        self.menubar.Check(ID_viewPeaklistColumnSn, bool('sn' in config.main['peaklistColumns']))
        self.menubar.Check(ID_viewPeaklistColumnZ, bool('z' in config.main['peaklistColumns']))
        self.menubar.Check(ID_viewPeaklistColumnMass, bool('mass' in config.main['peaklistColumns']))
        self.menubar.Check(ID_viewPeaklistColumnFwhm, bool('fwhm' in config.main['peaklistColumns']))
        self.menubar.Check(ID_viewPeaklistColumnResol, bool('resol' in config.main['peaklistColumns']))
        self.menubar.Check(ID_viewPeaklistColumnGroup, bool('group' in config.main['peaklistColumns']))
        
        self.menubar.Check(ID_viewAutoscale, bool(config.spectrum['autoscale']))
        self.menubar.Check(ID_viewNormalize, bool(config.spectrum['normalize']))


# =================================#
        # Evaluation menu
        evalmenu = wx.Menu()
        evalmenu.Append(ID_evalRes, "Evaluate Results"+HK_evalRes, "")

        self.Bind(wx.EVT_MENU, self.onEvalRes, id=ID_evalRes)
        
        self.menubar.Append(evalmenu, "Evaluation")

#=================================#
     # ----

    def onWindowLayout(self, evt=None, layout=None):
        """Apply selected window layout."""
        
        # documents bottom
        if layout == 'layout2' or (evt and evt.GetId() == ID_windowLayout2):
            config.main['layout'] = 'layout2'
            self.menubar.Check(ID_windowLayout2, True)
            self.AUIManager.GetPane('documents').Show().Bottom().Layer(0).Row(0).Position(0).MinSize((100,195)).BestSize((100,195))
            self.AUIManager.GetPane('peaklist').Show().Right().Layer(0).Row(0).Position(0).MinSize((195,100)).BestSize((195,100))
        
        # peaklist bottom
        elif layout == 'layout3' or (evt and evt.GetId() == ID_windowLayout3):
            config.main['layout'] = 'layout3'
            self.menubar.Check(ID_windowLayout3, True)
            self.AUIManager.GetPane('documents').Show().Left().Layer(0).Row(0).Position(0).MinSize((195,100)).BestSize((195,100))
            self.AUIManager.GetPane('peaklist').Show().Bottom().Layer(0).Row(0).Position(0).MinSize((100,195)).BestSize((100,195))
        
        # documents and peaklist bottom
        elif layout == 'layout4' or (evt and evt.GetId() == ID_windowLayout4):
            config.main['layout'] = 'layout4'
            self.menubar.Check(ID_windowLayout4, True)
            self.AUIManager.GetPane('documents').Show().Bottom().Layer(0).Row(0).Position(0).MinSize((100,195)).BestSize((100,195))
            self.AUIManager.GetPane('peaklist').Show().Bottom().Layer(0).Row(0).Position(1).MinSize((100,195)).BestSize((100,195))
        
        # default
        else:
            config.main['layout'] = 'default'
            self.AUIManager.GetPane('documents').Show().Left().Layer(0).Row(0).Position(0).MinSize((195,100)).BestSize((195,100))
            self.AUIManager.GetPane('peaklist').Show().Right().Layer(0).Row(0).Position(0).MinSize((195,100)).BestSize((195,100))
        
        # set last size
        if layout:
            self.AUIManager.GetPane('documents').BestSize((config.main['documentsWidth'], config.main['documentsHeight']))
            self.AUIManager.GetPane('peaklist').BestSize((config.main['peaklistWidth'], config.main['peaklistHeight']))
        
        # apply changes
        self.AUIManager.Update()


# =========================================================================#

    def makeGUI(self):
        """Init all gui elements."""
        
        # make documents panel
        self.documentsPanel = panelDocuments(self, self.documents)
        
        # Remove add/delete buttons because won't be needing them 
        self.documentsPanel.add_butt.Destroy()
        self.documentsPanel.delete_butt.Destroy()

        # Unbind right click events
        self.documentsPanel.documentTree.Unbind(wx.EVT_RIGHT_DOWN, handler = self.documentsPanel.onRMD)
        self.documentsPanel.documentTree.Unbind(wx.EVT_RIGHT_UP, handler = self.documentsPanel.onRMU)
        
        # make spectrum panel
        self.spectrumPanel = panelSpectrum(self, self.documents)
        
        # make peaklist panel
        self.peaklistPanel = panelPeaklist(self)
        
        # init other tools
        self.documentInfoPanel = None
        
        # manage frames
        self.AUIManager = wx.aui.AuiManager()
        self.AUIManager.SetManagedWindow(self)
        self.AUIManager.SetDockSizeConstraint(0.5, 0.5)
        
        self.AUIManager.AddPane(self.documentsPanel, wx.aui.AuiPaneInfo().Name("documents").
            Left().MinSize((195,100)).Caption("Opened Documents").CaptionVisible(False).
            Gripper(config.main['unlockGUI']).GripperTop(True).
            CloseButton(False).PaneBorder(False))
        
        self.AUIManager.AddPane(self.spectrumPanel, wx.aui.AuiPaneInfo().Name("plot").
            CentrePane().MinSize((300,100)).Caption("Spectrum Viewer").CaptionVisible(False).
            CloseButton(False).PaneBorder(False))
        
        self.AUIManager.AddPane(self.peaklistPanel, wx.aui.AuiPaneInfo().Name("peaklist").
            Right().MinSize((195,100)).Caption("Current Peak List").CaptionVisible(False).
            Gripper(config.main['unlockGUI']).GripperTop(True).
            CloseButton(False).PaneBorder(False))
        
        # show panels
        self.documentsPanel.Show(True)
        self.spectrumPanel.Show(True)
        self.peaklistPanel.Show(True)
        
        # set frame manager properties
        artProvider = self.AUIManager.GetArtProvider()
        artProvider.SetColor(wx.aui.AUI_DOCKART_SASH_COLOUR, self.documentsPanel.GetBackgroundColour())
        artProvider.SetColor(wx.aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR, self.documentsPanel.GetBackgroundColour())
        artProvider.SetMetric(wx.aui.AUI_DOCKART_SASH_SIZE, mwx.SASH_SIZE)
        artProvider.SetMetric(wx.aui.AUI_DOCKART_GRIPPER_SIZE, mwx.GRIPPER_SIZE)
        if mwx.SASH_COLOUR:
            self.SetOwnBackgroundColour(mwx.SASH_COLOUR)
            artProvider.SetColor(wx.aui.AUI_DOCKART_SASH_COLOUR, mwx.SASH_COLOUR)
        
        # set last layout
        self.onWindowLayout(layout=config.main['layout'])   

    # ----
    def updateControls(self):
        """Update menubar and toolbar items state."""
        
        # skip for Mac since it doesn't work correctly... why???
        if wx.Platform == '__WXMAC__':
            return

        # switching between spectrum viewer and evaluator
        if hasattr(self, 'spectrumPanel') == False or self.spectrumPanel.IsShown() == False :
            enableSpect = False
        else:
            enableSpect = True
        
        # view
        self.menubar.Enable(ID_viewLegend, enableSpect)
        self.menubar.Enable(ID_viewGrid, enableSpect)
        self.menubar.Enable(ID_viewDataPoints, enableSpect)
        self.menubar.Enable(ID_viewPosBars, enableSpect)
        self.menubar.Enable(ID_viewGel, enableSpect)
        self.menubar.Enable(ID_viewGelLegend, enableSpect)
        self.menubar.Enable(ID_viewLabels, enableSpect)
        self.menubar.Enable(ID_viewTicks, enableSpect)
        self.menubar.Enable(ID_viewLabelCharge, enableSpect)
        self.menubar.Enable(ID_viewLabelGroup, enableSpect)
        self.menubar.Enable(ID_viewLabelBgr, enableSpect)
        self.menubar.Enable(ID_viewLabelAngle, enableSpect)
        self.menubar.Enable(ID_viewOverlapLabels, enableSpect)
        self.menubar.Enable(ID_viewAllLabels, enableSpect)
        self.menubar.Enable(ID_viewNotations, enableSpect)
        self.menubar.Enable(ID_viewNotationLabels, enableSpect)
        self.menubar.Enable(ID_viewNormalize, enableSpect)
        self.menubar.Enable(ID_viewRange, enableSpect)
        self.menubar.Enable(ID_documentFlip, enableSpect)
        self.menubar.Enable(ID_documentOffset, enableSpect)
        self.menubar.Enable(ID_documentClearOffsets, enableSpect)
        self.menubar.Enable(ID_viewCanvasProperties, enableSpect)
        self.menubar.Enable(ID_viewTracker, enableSpect)
        self.menubar.Enable(ID_viewCheckLimits, enableSpect)
        self.menubar.Enable(ID_viewMinorTicks, enableSpect)
        self.menubar.Enable(ID_viewAutoscale, enableSpect)
        self.menubar.Enable(ID_viewNotationMarks, enableSpect)
        self.menubar.Enable(ID_viewNotationMz, enableSpect)
        self.menubar.Enable(ID_viewSpectrumRulerMz, enableSpect)
        self.menubar.Enable(ID_viewSpectrumRulerDist, enableSpect)
        self.menubar.Enable(ID_viewSpectrumRulerPpm, enableSpect)
        self.menubar.Enable(ID_viewSpectrumRulerZ, enableSpect)
        self.menubar.Enable(ID_viewSpectrumRulerCursorMass, enableSpect)
        self.menubar.Enable(ID_viewSpectrumRulerParentMass, enableSpect)
        self.menubar.Enable(ID_viewSpectrumRulerArea, enableSpect)
        self.menubar.Enable(ID_viewPeaklistColumnMz, enableSpect)
        self.menubar.Enable(ID_viewPeaklistColumnAi, enableSpect)
        self.menubar.Enable(ID_viewPeaklistColumnInt, enableSpect)
        self.menubar.Enable(ID_viewPeaklistColumnBase, enableSpect)
        self.menubar.Enable(ID_viewPeaklistColumnRel, enableSpect)
        self.menubar.Enable(ID_viewPeaklistColumnSn, enableSpect)
        self.menubar.Enable(ID_viewPeaklistColumnZ, enableSpect)
        self.menubar.Enable(ID_viewPeaklistColumnMass, enableSpect)
        self.menubar.Enable(ID_viewPeaklistColumnFwhm, enableSpect)
        self.menubar.Enable(ID_viewPeaklistColumnResol, enableSpect)
        self.menubar.Enable(ID_viewPeaklistColumnGroup, enableSpect)
            
            
        # document
        self.menubar.Enable(ID_documentNew, enableSpect)
        self.menubar.Enable(ID_documentOpen, enableSpect)
        self.menubar.Enable(ID_documentClose, enableSpect)
        self.menubar.Enable(ID_documentCloseAll, enableSpect)
                   
        if self.currentDocument == None:
            enable = False
            document = None
        else:
            enable = True
            document = self.documents[self.currentDocument]
            
        # update menubar
        self.menubar.Enable(ID_documentClose, enable)
        
        
    # ----
    
    
    def onToolsSpectrum(self, evt):
        """Toggle spectrum tools."""
        
        # get ID
        ID = evt.GetId()
        
        # set tool in menubar
        if ID == ID_toolsRuler:
            tool = 'ruler'
        elif ID == ID_toolsLabelPeak:
            tool = 'labelpeak'
        elif ID == ID_toolsLabelPoint:
            tool = 'labelpoint'
        elif ID == ID_toolsLabelEnvelope:
            tool = 'labelenvelope'
        elif ID == ID_toolsDeleteLabel:
            tool = 'deletelabel'
        elif ID == ID_toolsOffset:
            tool = 'offset'
        
        # set tool in spectrum
        self.spectrumPanel.setCurrentTool(tool)
        self.spectrumPanel.spectrumCanvas.SetFocus()
    
    # ----

#==========================================================================================#

    # View events

    def onView(self, evt):
        """Update view parameters in the spectrum."""
        
        # get ID
        ID = evt.GetId()
        
        # set new params
        if ID == ID_viewLegend:
            values = (1,0)
            config.spectrum['showLegend'] = values[bool(config.spectrum['showLegend'])]
            self.menubar.Check(ID_viewLegend, bool(config.spectrum['showLegend']))
        
        elif ID == ID_viewGrid:
            values = (1,0)
            config.spectrum['showGrid'] = values[bool(config.spectrum['showGrid'])]
            self.menubar.Check(ID_viewGrid, bool(config.spectrum['showGrid']))
        
        elif ID == ID_viewMinorTicks:
            values = (1,0)
            config.spectrum['showMinorTicks'] = values[bool(config.spectrum['showMinorTicks'])]
            self.menubar.Check(ID_viewMinorTicks, bool(config.spectrum['showMinorTicks']))
        
        elif ID == ID_viewDataPoints:
            values = (1,0)
            config.spectrum['showDataPoints'] = values[bool(config.spectrum['showDataPoints'])]
            self.menubar.Check(ID_viewDataPoints, bool(config.spectrum['showDataPoints']))
        
        elif ID == ID_viewPosBars:
            values = (1,0)
            config.spectrum['showPosBars'] = values[bool(config.spectrum['showPosBars'])]
            self.menubar.Check(ID_viewPosBars, bool(config.spectrum['showPosBars']))
        
        elif ID == ID_viewGel:
            values = (1,0)
            config.spectrum['showGel'] = values[bool(config.spectrum['showGel'])]
            self.menubar.Check(ID_viewGel, bool(config.spectrum['showGel']))
        
        elif ID == ID_viewGelLegend:
            values = (1,0)
            config.spectrum['showGelLegend'] = values[bool(config.spectrum['showGelLegend'])]
            self.menubar.Check(ID_viewGelLegend, bool(config.spectrum['showGelLegend']))
        
        elif ID == ID_viewTracker:
            values = (1,0)
            config.spectrum['showTracker'] = values[bool(config.spectrum['showTracker'])]
            self.menubar.Check(ID_viewTracker, bool(config.spectrum['showTracker']))
        
        elif ID == ID_viewLabels:
            values = (1,0)
            title = ("Show Labels", "Hide Labels")
            config.spectrum['showLabels'] = values[bool(config.spectrum['showLabels'])]
            self.menubar.SetLabel(ID_viewLabels, title[bool(config.spectrum['showLabels'])]+HK_viewLabels)
        
        elif ID == ID_viewTicks:
            values = (1,0)
            title = ("Show Ticks", "Hide Ticks")
            config.spectrum['showTicks'] = values[bool(config.spectrum['showTicks'])]
            self.menubar.SetLabel(ID_viewTicks, title[bool(config.spectrum['showTicks'])]+HK_viewTicks)
        
        elif ID == ID_viewLabelCharge:
            values = (1,0)
            config.spectrum['labelCharge'] = values[bool(config.spectrum['labelCharge'])]
            self.menubar.Check(ID_viewLabelCharge, bool(config.spectrum['labelCharge']))
        
        elif ID == ID_viewLabelGroup:
            values = (1,0)
            config.spectrum['labelGroup'] = values[bool(config.spectrum['labelGroup'])]
            self.menubar.Check(ID_viewLabelGroup, bool(config.spectrum['labelGroup']))
        
        elif ID == ID_viewLabelBgr:
            values = (1,0)
            config.spectrum['labelBgr'] = values[bool(config.spectrum['labelBgr'])]
            self.menubar.Check(ID_viewLabelBgr, bool(config.spectrum['labelBgr']))
        
        elif ID == ID_viewLabelAngle:
            values = (90,0)
            title = ("Vertical Labels", "Horizontal Labels")
            config.spectrum['labelAngle'] = values[bool(config.spectrum['labelAngle'])]
            self.menubar.SetLabel(ID_viewLabelAngle, title[bool(config.spectrum['labelAngle'])]+HK_viewLabelAngle)
        
        elif ID == ID_viewOverlapLabels:
            values = (1,0)
            config.spectrum['overlapLabels'] = values[bool(config.spectrum['overlapLabels'])]
            self.menubar.Check(ID_viewOverlapLabels, bool(config.spectrum['overlapLabels']))
        
        elif ID == ID_viewCheckLimits:
            values = (1,0)
            config.spectrum['checkLimits'] = values[bool(config.spectrum['checkLimits'])]
            self.menubar.Check(ID_viewCheckLimits, bool(config.spectrum['checkLimits']))
        
        elif ID == ID_viewAllLabels:
            values = (1,0)
            config.spectrum['showAllLabels'] = values[bool(config.spectrum['showAllLabels'])]
            self.menubar.Check(ID_viewAllLabels, bool(config.spectrum['showAllLabels']))
        
        elif ID == ID_viewNotations:
            values = (1,0)
            title = ("Show Notations", "Hide Notations")
            config.spectrum['showNotations'] = values[bool(config.spectrum['showNotations'])]
            self.menubar.SetLabel(ID_viewNotations, title[bool(config.spectrum['showNotations'])])
        
        elif ID == ID_viewNotationMarks:
            values = (1,0)
            config.spectrum['notationMarks'] = values[bool(config.spectrum['notationMarks'])]
            self.menubar.Check(ID_viewNotationMarks, bool(config.spectrum['notationMarks']))
        
        elif ID == ID_viewNotationLabels:
            values = (1,0)
            config.spectrum['notationLabels'] = values[bool(config.spectrum['notationLabels'])]
            self.menubar.Check(ID_viewNotationLabels, bool(config.spectrum['notationLabels']))
        
        elif ID == ID_viewNotationMz:
            values = (1,0)
            config.spectrum['notationMZ'] = values[bool(config.spectrum['notationMZ'])]
            self.menubar.Check(ID_viewNotationMz, bool(config.spectrum['notationMZ']))
        
        elif ID == ID_viewAutoscale:
            values = (1,0)
            config.spectrum['autoscale'] = values[bool(config.spectrum['autoscale'])]
            self.menubar.Check(ID_viewAutoscale, bool(config.spectrum['autoscale']))
        
        elif ID == ID_viewNormalize:
            values = (1,0)
            config.spectrum['normalize'] = values[bool(config.spectrum['normalize'])]
            self.menubar.Check(ID_viewNormalize, bool(config.spectrum['normalize']))
        
        # update spectrum
        self.spectrumPanel.updateCanvasProperties(ID)
        self.spectrumPanel.spectrumCanvas.SetFocus()

    # ----


    def onViewSpectrumRuler(self, evt):
        """Show / hide cursor info values."""
        
        # get ID
        ID = evt.GetId()
        
        # set items
        items = {
            ID_viewSpectrumRulerMz: 'mz',
            ID_viewSpectrumRulerDist: 'dist',
            ID_viewSpectrumRulerPpm: 'ppm',
            ID_viewSpectrumRulerZ: 'z',
            ID_viewSpectrumRulerCursorMass: 'cmass',
            ID_viewSpectrumRulerParentMass: 'pmass',
            ID_viewSpectrumRulerArea: 'area'
        }
        
        # change config
        item = items[ID]
        if item in config.main['cursorInfo']:
            del config.main['cursorInfo'][config.main['cursorInfo'].index(item)]
        else:
            config.main['cursorInfo'].append(item)
        
        # update menubar
        self.menubar.Check(ID, bool(item in config.main['cursorInfo']))

    # ----
    
    
    def onViewPeaklistColumns(self, evt):
        """Show / hide peaklist columns."""
        
        # get ID
        ID = evt.GetId()
        
        # set items
        items = {
            ID_viewPeaklistColumnMz: 'mz',
            ID_viewPeaklistColumnAi: 'ai',
            ID_viewPeaklistColumnInt: 'int',
            ID_viewPeaklistColumnBase: 'base',
            ID_viewPeaklistColumnRel: 'rel',
            ID_viewPeaklistColumnSn: 'sn',
            ID_viewPeaklistColumnZ: 'z',
            ID_viewPeaklistColumnMass: 'mass',
            ID_viewPeaklistColumnFwhm: 'fwhm',
            ID_viewPeaklistColumnResol: 'resol',
            ID_viewPeaklistColumnGroup: 'group',
        }
        
        # change config
        item = items[ID]
        columns = config.main['peaklistColumns'][:]
        if item in columns:
            del columns[columns.index(item)]
        else:
            columns.append(item)
        
        # ensure at least one item is present and right order
        if len(columns) > 0:
            config.main['peaklistColumns'] = []
            if 'mz' in columns:
                config.main['peaklistColumns'].append('mz')
            if 'ai' in columns:
                config.main['peaklistColumns'].append('ai')
            if 'int' in columns:
                config.main['peaklistColumns'].append('int')
            if 'base' in columns:
                config.main['peaklistColumns'].append('base')
            if 'rel' in columns:
                config.main['peaklistColumns'].append('rel')
            if 'sn' in columns:
                config.main['peaklistColumns'].append('sn')
            if 'z' in columns:
                config.main['peaklistColumns'].append('z')
            if 'mass' in columns:
                config.main['peaklistColumns'].append('mass')
            if 'fwhm' in columns:
                config.main['peaklistColumns'].append('fwhm')
            if 'resol' in columns:
                config.main['peaklistColumns'].append('resol')
            if 'group' in columns:
                config.main['peaklistColumns'].append('group')
        else:
            wx.Bell()
        
        # update menubar
        self.menubar.Check(ID, bool(item in config.main['peaklistColumns']))
        
        # update peaklist
        self.peaklistPanel.updatePeaklistColumns()

    # ----
    
    
    def onViewCanvasProperties(self, evt):
        """Show spectrum canvas properties dialog."""
        self.spectrumPanel.onCanvasProperties()

    # ----

    def onViewRange(self, evt):
        """Set current ranges for spectrum canvas."""
        
        # get current range
        if not config.internal['canvasXrange']:
            massRange = self.spectrumPanel.getCurrentRange()
            minX = '%.0f' % massRange[0]
            maxX = '%.0f' % massRange[1]
            massRange = (minX, maxX)
        else:
            massRange = config.internal['canvasXrange']
        
        # show range dialog
        dlg = dlgViewRange(self, massRange)
        if dlg.ShowModal() == wx.ID_OK:
            massRange = dlg.data
            dlg.Destroy()
        else:
            dlg.Destroy()
            return
        
        # set new range
        self.spectrumPanel.setCanvasRange(xAxis=massRange)
        config.internal['canvasXrange'] = massRange

    # ----

    def updateMassPoints(self, points):
        """Highlight specified points in the spectrum."""
        self.spectrumPanel.highlightPoints(points)
    # ----

#===============================================================================#
   
    # File events helper

    def updateNotationMarks(self, refresh=True):
        """Highlight annotations and sequence matches in canvas."""
        
        # get current selection
        selected = self.documentsPanel.getSelectedItemType()
        
        # hide annotation marks
        if not selected or self.currentDocument == None:
            self.spectrumPanel.updateNotationMarks(None, refresh=refresh)
            return
        
        points = []
        
        # get all
        if selected == 'document':
            document = self.documents[self.currentDocument]
            points += [[a.mz, a.ai, a.label] for a in document.annotations]
            for sequence in document.sequences:
                points += [[m.mz, m.ai, m.label] for m in sequence.matches]
        
        # get annotations
        elif selected in ('annotations', 'annotation'):
            document = self.documents[self.currentDocument]
            points += [[a.mz, a.ai, a.label] for a in document.annotations]
        
        # get sequence matches
        elif selected in ('sequence', 'match') and self.currentSequence != None:
            sequence = self.documents[self.currentDocument].sequences[self.currentSequence]
            points += [[m.mz, m.ai, m.label] for m in sequence.matches]
        
        # sort points
        points.sort()
        
        # update spectrum panel
        self.spectrumPanel.updateNotationMarks(points, refresh=refresh)
    

    # ----

    def onSequenceSelected(self, seqIndex):
        """Set current sequence."""
        
        # get sequence
        if seqIndex != None:
            seqData = self.documents[self.currentDocument].sequences[seqIndex]
        else:
            seqData = None
        
        # update panels
        if seqIndex != self.currentSequence:
            
            # set current sequence
            self.currentSequence = seqIndex
            
            # update menubar and toolbar
            self.updateControls()
    
    # ----

    def getFreeColour(self):
        """Get free colour from config or generate random."""
        
        # get colour from config
        for colour in config.colours:
            if not colour in self.usedColours:
                self.usedColours.append(colour)
                return colour
        
        # generate random colour
        i = 0
        while True:
            i += 1
            colour = [random.randrange(0,255), random.randrange(0,255), random.randrange(0,255)]
            if colour not in self.usedColours or i==10000:
                self.usedColours.append(colour)
                return colour

    # ----


#=====================================================================================================#
    # File events

    def onDocumentNew(self, evt=None, document=None, select=True):
        """Create blank document."""
        
        # make document
        if document == None:
            document = doc.document()
            document.title = 'Blank Document'
        
        # set colour
        document.colour = self.getFreeColour()
        
        # append document
        self.documents.append(document)
        
        # update gui
        self.onDocumentLoaded(select)
 
    # ----
    
    def onDocumentOpen(self, evt=None, path=None):
        """Open document."""
        
        # add path to queue
        if path:
            self.tmpDocumentQueue.append(path)
        
        # open dialog if no path specified
        else:
            lastDir = ''
            if os.path.exists(config.main['lastDir']):
                lastDir = config.main['lastDir']
            wildcard =  "All supported formats|fid;*.msd;*.baf;*.yep;*.mzData;*.mzdata*;*.mzXML;*.mzxml;*.mzML;*.mzml;*.xml;*.XML;*.mgf;*.MGF;*.txt;*.xy;*.asc|All files|*.*"
            dlg = wx.FileDialog(self, "Open Document", lastDir, "", wildcard=wildcard, style=wx.FD_OPEN|wx.FD_MULTIPLE|wx.FD_FILE_MUST_EXIST)
            if dlg.ShowModal() == wx.ID_OK:
                paths = dlg.GetPaths()
                dlg.Destroy()
                self.tmpDocumentQueue += list(paths)
            else:
                dlg.Destroy()
                return
        
        # import documents in queue
        self.importDocumentQueue()

    # ----

    def onDocumentClose(self, evt=None, docIndex=None, review=False, selectPrevious=True):
        """Close current document."""
        
        # check document
        if docIndex == None:
            docIndex = self.currentDocument
        if docIndex == None:
            wx.Bell()
            return False
        
        # unblock colour
        colour = self.documents[docIndex].colour
        if colour in self.usedColours:
            del self.usedColours[self.usedColours.index(colour)]
        
        # clear visibility history
        self.documentsSoloCurrent = None
        self.documentsSoloPrevious = {}
        
        # delete document
        self.documentsPanel.selectDocument(None)
        self.documentsPanel.deleteDocument(docIndex)
        self.spectrumPanel.deleteSpectrum(docIndex)
        del self.documents[docIndex]
        
        # select previous visible document
        if selectPrevious:
            while docIndex > 0:
                docIndex -= 1
                if self.documents[docIndex].visible:
                    self.documentsPanel.selectDocument(docIndex)
                    break
        
        # update menubar and toolbar
        self.updateControls()
        
        # unchanged or saved document
        return True

    # ----
    
    def onDocumentCloseAll(self, evt=None):
        """Close all documents."""
        
        # close panels
        if self.documentInfoPanel:
            self.documentInfoPanel.Close()
        
            
        # close documents
        while self.documents:
            docIndex = len(self.documents)-1
            if not self.onDocumentClose(docIndex=docIndex, review=False, selectPrevious=False):
                return False
        
        return True
   
    # ----


    def onQuit(self, evt):
        """Close all documents and quit application."""

        evt.Skip()
        self.Destroy()
    
    # ----

    # DOCUMENT IMPORT
    
    def importDocumentQueue(self):
        """Open dropped documents."""
        
        # queue is already running
        if self.processingDocumentQueue:
            return
        
        # process all files in queue
        self.processingDocumentQueue = True
        while self.tmpDocumentQueue:
            self.importDocument(path=self.tmpDocumentQueue[0])
        
        # release processing flag
        self.processingDocumentQueue = False
    
    # ----

    def importDocument(self, path):
        """Open document."""
        
        # remove path from queue
        if path in self.tmpDocumentQueue:
            i = self.tmpDocumentQueue.index(path)
            del self.tmpDocumentQueue[i]
        
        # check path
        if os.path.exists(path):
            config.main['lastDir'] = os.path.split(path)[0]
        else:
            wx.Bell()
            dlg = mwx.dlgMessage(self, title="Document doesn't exists.", message="Specified document path cannot be found or is temporarily\nunavailable.")
            dlg.ShowModal()
            dlg.Destroy()
            return
        
        # get document type
        docType = self.getDocumentType(path)
        if not docType:
            wx.Bell()
            dlg = mwx.dlgMessage(self, title="Unable to open the document.", message="Document type or structure can't be recognized. Selected format\nis probably unsupported.")
            dlg.ShowModal()
            dlg.Destroy()
            return
        
        # import sequences from FASTA
        if docType == 'FASTA':
            self.onSequenceImport(path=path)
            return
        
        # convert Bruker format
        compassUsed = False
        if docType == 'bruker':
            compassUsed = True
            docType = config.main['compassFormat']
            path = self.convertBrukerData(path)
            if not path:
                return
        
        # select scans from multiscan documents
        scans = [None]
        if docType in ('mzXML', 'mzData', 'mzML', 'MGF'):
            scans = self.askForScans(path, docType)
            if not scans:
                return
        
        # open document
        status = True
        for scan in scans:
            before = len(self.documents)
            
            # init processing gauge
            gauge = mwx.gaugePanel(self, 'Reading data...')
            gauge.show()
            
            # load document
            process = threading.Thread(target=self.runDocumentParser, kwargs={'path':path, 'docType':docType, 'scan':scan})
            process.start()
            while process.isAlive():
                gauge.pulse()
            
            # append document
            if before < len(self.documents):
                self.onDocumentLoaded(select=True)
                status *= True
            else:
                status *= False
            
            # close processing gauge
            gauge.close()
        
        # delete compass file
        if compassUsed and config.main['compassDeleteFile']:
            try: os.unlink(path)
            except: pass
        
        
        # processing failed
        if not status:
            wx.Bell()
            dlg = mwx.dlgMessage(self, title="Unable to open the document.", message="There were some errors while reading selected document\nor it contains no data.")
            dlg.ShowModal()
            dlg.Destroy()
    
    # ----
    
    def getDocumentType(self, path):
        """Get document type."""
        
        # get filename and extension
        dirName, fileName = os.path.split(path)
        baseName, extension = os.path.splitext(fileName)
        fileName = fileName.lower()
        baseName = baseName.lower()
        extension = extension.lower()
        
        # get document type by filename or extension
        if extension == '.msd':
            return 'mSD'
        elif fileName == 'fid' or extension in ('.baf', '.yep'):
            return 'bruker'
        elif extension == '.mzdata':
            return 'mzData'
        elif extension == '.mzxml':
            return 'mzXML'
        elif extension == '.mzml':
            return 'mzML'
        elif extension == '.mgf':
            return 'MGF'
        elif extension in ('.xy', '.txt', '.asc'):
            return 'XY'
        elif extension in ('.fa', '.fsa', '.faa', '.fasta'):
            return 'FASTA'
        elif os.path.isdir(path):
            for dirpath, dirnames, filenames in os.walk(path):
                names = [i.lower() for i in filenames]
                if 'fid' in names or 'analysis.baf' in names or 'analysis.yep' in names:
                    return 'bruker'
        
        # get document type for xml files
        if extension == '.xml':
            document = open(path, 'r')
            data = document.read(500)
            if '<mzData' in data:
                return 'mzData'
            elif '<mzXML' in data:
                return 'mzXML'
            elif '<mzML' in data:
                return 'mzML'
            document.close()
        
        # unknown document type
        return False
   
    # ----

    def askForScans(self, path, docType):
        """Select scans to import."""
        
        self.tmpScanlist = None
        
        # get scan list
        gauge = mwx.gaugePanel(self, 'Gathering scan list...')
        gauge.show()
        process = threading.Thread(target=self.getDocumentScanList, kwargs={'path':path, 'docType':docType})
        process.start()
        while process.isAlive():
            gauge.pulse()
        gauge.close()
        
        # unable to load scan list
        if not self.tmpScanlist:
            wx.Bell()
            dlg = mwx.dlgMessage(self, title="Unable to open the document.", message="Selected document is damaged or contains no data.")
            dlg.ShowModal()
            dlg.Destroy()
            return False
        
        # select scans to open
        if len(self.tmpScanlist) > 1:
            dlg = dlgSelectScans(self, self.tmpScanlist)
            if dlg.ShowModal() == wx.ID_OK:
                selected = dlg.selected
                dlg.Destroy()
                return selected
            else:
                dlg.Destroy()
                return None
        else:
            return [None]
    # ----
    def getDocumentScanList(self, path, docType):
        """Get scans from document."""
        
        modified = os.path.getmtime(path)
        
        # try to load from buffer
        if path in self.bufferedScanlists and modified == self.bufferedScanlists[path][0]:
            self.tmpScanlist = self.bufferedScanlists[path][1]
            return
        
        # set parser
        if docType == 'mzData':
            parser = mspy.parseMZDATA(path)
        elif docType == 'mzXML':
            parser = mspy.parseMZXML(path)
        elif docType == 'mzML':
            parser = mspy.parseMZML(path)
        elif docType == 'MGF':
            parser = mspy.parseMGF(path)
        else:
            return
        
        # load scans
        self.tmpScanlist = parser.scanlist()
        
        # remember scan list
        if self.tmpScanlist:
            self.bufferedScanlists[path] = (modified, self.tmpScanlist)
    # ----
    
    def runDocumentParser(self, path, docType, scan=None):
        """Load spectrum document."""
        
        document = False
        spectrum = False
        
        # get data data
        if docType == 'mSD':
            parser = doc.parseMSD(path)
            document = parser.getDocument()
        elif docType == 'mzData':
            parser = mspy.parseMZDATA(path)
            spectrum = parser.scan(scan)
        elif docType == 'mzXML':
            parser = mspy.parseMZXML(path)
            spectrum = parser.scan(scan)
        elif docType == 'mzML':
            parser = mspy.parseMZML(path)
            spectrum = parser.scan(scan)
        elif docType == 'MGF':
            parser = mspy.parseMGF(path)
            spectrum = parser.scan(scan)
        elif docType == 'XY':
            parser = mspy.parseXY(path)
            spectrum = parser.scan()
        else:
            return
        
        # make document for non-mSD formats
        if spectrum != False:
            
            # init document
            document = doc.document()
            document.format = docType
            document.path = path
            document.spectrum = spectrum
            
            # get info
            info = parser.info()
            if info:
                document.title = info['title']
                document.operator = info['operator']
                document.contact = info['contact']
                document.institution = info['institution']
                document.date = info['date']
                document.instrument = info['instrument']
                document.notes = info['notes']
            
            # set date if empty
            if not document.date and docType != 'mSD':
                document.date = time.ctime(os.path.getctime(path))
            
            # set title if empty
            if not document.title:
                if document.spectrum.title != '':
                    document.title = document.spectrum.title
                else:
                    dirName, fileName = os.path.split(path)
                    baseName, extension = os.path.splitext(fileName)
                    if baseName.lower() == "analysis":
                        document.title = os.path.split(dirName)[1]
                    else:
                        document.title = baseName
            
            # add scan number to title
            if scan:
                document.title += ' [%s]' % scan
            
        # finalize and append document
        if document:
            document.colour = self.getFreeColour()
            document.sortAnnotations()
            document.sortSequenceMatches()
            self.documents.append(document)
            
            # precalculate baseline
            if document.spectrum.hasprofile():
                document.spectrum.baseline(
                    window = (1./config.processing['baseline']['precision']),
                    offset = config.processing['baseline']['offset']
                )
   
    # ----

    def onDocumentLoaded(self, select=True):
        """Update GUI after document loaded."""
        
        # clear visibility history
        self.documentsSoloCurrent = None
        self.documentsSoloPrevious = {}
        
        # append document
        self.spectrumPanel.appendLastSpectrum()
        self.documentsPanel.appendLastDocument()
        
        # select document
        if select:
            self.documentsPanel.selectDocument(-1)
        
    # ----

    def onDocumentSelected(self, docIndex):
        """Set current document."""
        
        # get document and application title
        if docIndex != None:
            docData = self.documents[docIndex]
            title = 'PSME - %s' % (docData.title)
            if docData.dirty:
                title += ' *'
        else:
            docData = None
            title = 'PSME'
        
        # update app title
        self.SetTitle(title)
        
        # update panels
        if docIndex != self.currentDocument:
            
            # set current document
            self.currentDocument = docIndex
            self.currentSequence = None
            
            # update spectrum panel
            self.spectrumPanel.selectSpectrum(docIndex, refresh=False)
            
            # update peaklist panel
            self.peaklistPanel.setData(docData)
            
            # update document info panel
            if self.documentInfoPanel:
                self.documentInfoPanel.setData(docData)
            
            # update menubar and toolbar
            self.updateControls()

    # ----
        
    def onDocumentChanged(self, items=()):
        """Document content has changed."""
        
        # check selection
        if self.currentDocument == None:
            return
        
        # update spectrum panel
        if 'spectrum' in items:
            self.spectrumPanel.updateSpectrum(self.currentDocument)
        
        # update peaklist panel
        if 'spectrum' in items:
            self.peaklistPanel.updatePeakList()
        
        # update title-dependent panels
        if 'doctitle' in items:
            self.spectrumPanel.updateSpectrumProperties(self.currentDocument)
        
        # update documents panel
        if 'notations' in items:
            self.documentsPanel.updateAnnotations(self.currentDocument)
            for seqIndex in range(len(self.documents[self.currentDocument].sequences)):
                self.documentsPanel.updateSequenceMatches(self.currentDocument, seqIndex)
        if 'annotations' in items:
            self.documentsPanel.updateAnnotations(self.currentDocument, expand=True)
        if 'sequences' in items:
            self.documentsPanel.updateSequences(self.currentDocument)
        if 'seqtitle' in items:
            self.documentsPanel.updateSequenceTitle(self.currentDocument, self.currentSequence)
        if 'matches' in items:
            self.documentsPanel.updateSequenceMatches(self.currentDocument, self.currentSequence, expand=True)
        
        # update notation marks
        if 'notations' in items \
        or 'annotations' in items \
        or 'sequences' in items \
        or 'matches' in items:
            self.updateNotationMarks()
        
        # update data-dependent panels
        if 'spectrum' in items:
            
            docData = self.documents[self.currentDocument]
            
            # update document info panel
            if self.documentInfoPanel:
                self.documentInfoPanel.setData(docData)
        
        # disable undo
        if 'sequence' in items:
            self.documents[self.currentDocument].backup(None)
        
        # set document status
        self.documents[self.currentDocument].dirty = True
        self.documentsPanel.updateDocumentTitle(self.currentDocument)
        
        # update app title
        title = 'PSME - %s *' % (self.documents[self.currentDocument].title)
        self.SetTitle(title)
        
        # update controls
        self.updateControls()

    # ----
    
    def onDocumentInfo(self, evt=None):
        """Show document information panel."""
        
        # check document
        if not self.documentInfoPanel and self.currentDocument == None:
            wx.Bell()
            return
        
        # destroy panel
        if self.documentInfoPanel and evt:
            self.documentInfoPanel.Close()
            return
        
        # show panel
        if not self.documentInfoPanel:
            self.documentInfoPanel = panelDocumentInfo(self)
            self.documentInfoPanel.Centre()
            self.documentInfoPanel.Show(True)
        
        # set current document
        if self.currentDocument != None:
            self.documentInfoPanel.setData(self.documents[self.currentDocument])
            self.documentInfoPanel.Raise()
        else:
            self.documentInfoPanel.setData(None)
            self.documentInfoPanel.Raise()
    
    # ----

    def onDocumentFlip(self, evt):
        """Flip spectrum vertically."""
        
        # check document
        if self.currentDocument == None:
            wx.Bell()
            return
        
        # set document flipping
        self.documents[self.currentDocument].flipped = not self.documents[self.currentDocument].flipped
        
        # update spectrum panel
        self.spectrumPanel.updateSpectrumProperties(self.currentDocument)
   
    # ----
    
    def onDocumentOffset(self, evt):
        """Offset spectrum."""
        
        # set offset for current document
        if evt.GetId() == ID_documentOffset and self.currentDocument != None:
            if config.spectrum['normalize']:
                wx.Bell()
                return
            dlg = dlgSpectrumOffset(self, self.documents[self.currentDocument].offset)
            if dlg.ShowModal() == wx.ID_OK:
                offset = dlg.getData()
                dlg.Destroy()
                self.documents[self.currentDocument].offset = offset
                self.spectrumPanel.updateSpectrumProperties(self.currentDocument)
            else:
                dlg.Destroy()
        
        # clear offset for current document
        elif evt.GetId() == ID_documentClearOffset and self.currentDocument != None:
            self.documents[self.currentDocument].offset = [0,0]
            self.spectrumPanel.updateSpectrumProperties(self.currentDocument)
        
        # clear offset for all documents
        elif evt.GetId() == ID_documentClearOffsets:
            for x, document in enumerate(self.documents):
                document.offset = [0,0]
                self.spectrumPanel.updateSpectrumProperties(x, refresh=False)
            self.spectrumPanel.refresh()
        
        # no document
        else:
            wx.Bell()
            return
   
    # ----

    def onDocumentDropped(self, evt=None, paths=None):
        """Open dropped documents."""
        
        # get paths
        if evt != None:
            paths = evt.GetFiles()
        
        # open documents
        if paths:
            self.tmpDocumentQueue += list(paths)
            wx.CallAfter(self.importDocumentQueue)
   
    # ----
    
    def onDocumentAnnotationsDelete(self, evt=None, annotIndex=None):
        """Delete annotations."""
        
        # check selection
        if self.currentDocument == None:
            return
        
        # delete annotations
        self.documents[self.currentDocument].backup(('annotations'))
        if annotIndex != None:
            del self.documents[self.currentDocument].annotations[annotIndex]
        else:
            del self.documents[self.currentDocument].annotations[:]
        
        # update GUI
        self.onDocumentChanged(items=('annotations'))
   
    # ----

    def onDocumentNotationsDelete(self, evt=None):
        """Delete all annotations and sequence matches."""
        
        # check selection
        if self.currentDocument == None:
            return
        
        # backup annotations and matches
        self.documents[self.currentDocument].backup(('notations'))
        
        # delete annotations
        del self.documents[self.currentDocument].annotations[:]
        
        # delete sequence matches
        for seqIndex in range(len(self.documents[self.currentDocument].sequences)):
            del self.documents[self.currentDocument].sequences[seqIndex].matches[:]
        
        # update GUI
        self.onDocumentChanged(items=('notations'))
   
    # ----


#================================================================================#    
   
    # Switch between windows for spectrum viewer and PSME

    def onSpectViewer(self, event=None):
        if hasattr(self, 'spectrumPanel') == False:
            self.makeGUI()
            self.updateControls()
        
        elif self.documentsPanel.IsShown():
            pass
        
        else:
            self.documentsPanel.Show(True)
            self.spectrumPanel.Show(True)
            self.peaklistPanel.Show(True)
            self.updateControls()
            
    # ----

    def onEvalRes(self, event=None):
        if hasattr(self, 'spectrumPanel') and self.spectrumPanel.IsShown():
            self.documentsPanel.Show(False)
            self.spectrumPanel.Show(False)
            self.peaklistPanel.Show(False)

        self.updateControls()
        self.evalNum += 1
        curPage = self.nb.AddPage(mainPanel(self.nb, -1, "Evaluation", self.evalNum), "Evaluation %d" % self.evalNum, select = True)
    
    

# Run
app = wx.App(False)
frame = mainFrame(None, -1, 'Peptide-Spectrum-Matches (PSMs) Evaluation (version 0.1.0) ')
frame.Show()
app.MainLoop()
