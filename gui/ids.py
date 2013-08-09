# -------------------------------------------------------------------------
#     Copyright (C) 2005-2013 Martin Strohalm <www.mmass.org>

#     This program is free software; you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation; either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#     GNU General Public License for more details.

#     Complete text of GNU GPL can be found in the file LICENSE.TXT in the
#     main directory of the program.
# -------------------------------------------------------------------------

# load libs
import wx

# common
ID_quit = wx.ID_EXIT

HK_quit = '\tCtrl+Q'
if wx.Platform == '__WXMAC__':
    HK_preferences = '\tCtrl+,'

# file
ID_documentNew = wx.NewId()
ID_documentOpen = wx.NewId()
ID_documentClose = wx.NewId()
ID_documentCloseAll = wx.NewId()

ID_documentAnnotationEdit = wx.NewId()
ID_documentAnnotationDelete = wx.NewId()
ID_documentAnnotationSendToMassCalculator = wx.NewId()
ID_documentAnnotationSendToMassToFormula = wx.NewId()
ID_documentAnnotationSendToEnvelopeFit = wx.NewId()
ID_documentAnnotationsDelete = wx.NewId()
ID_documentAnnotationsCalibrateBy = wx.NewId()
ID_documentNotationsDelete = wx.NewId()

HK_documentNew = '\tCtrl+N'
HK_documentOpen = '\tCtrl+O'
HK_documentClose = '\tCtrl+W'
HK_documentCloseAll = '\tShift+Ctrl+W'

# view
ID_viewGrid = wx.NewId()
ID_viewMinorTicks = wx.NewId()
ID_viewLegend = wx.NewId()
ID_viewPosBars = wx.NewId()
ID_viewGel = wx.NewId()
ID_viewGelLegend = wx.NewId()
ID_viewTracker = wx.NewId()
ID_viewDataPoints = wx.NewId()
ID_viewLabels = wx.NewId()
ID_viewTicks = wx.NewId()
ID_viewLabelCharge = wx.NewId()
ID_viewLabelGroup = wx.NewId()
ID_viewLabelBgr = wx.NewId()
ID_viewLabelAngle = wx.NewId()
ID_viewAllLabels = wx.NewId()
ID_viewOverlapLabels = wx.NewId()
ID_viewCheckLimits = wx.NewId()
ID_viewNotations = wx.NewId()
ID_viewNotationMarks = wx.NewId()
ID_viewNotationLabels = wx.NewId()
ID_viewNotationMz = wx.NewId()
ID_viewAutoscale = wx.NewId()
ID_viewNormalize = wx.NewId()
ID_viewRange = wx.NewId()
ID_viewCanvasProperties = wx.NewId()

ID_viewSpectrum = wx.NewId()
ID_viewSpectrumRulerMz = wx.NewId()
ID_viewSpectrumRulerDist = wx.NewId()
ID_viewSpectrumRulerPpm = wx.NewId()
ID_viewSpectrumRulerZ = wx.NewId()
ID_viewSpectrumRulerCursorMass = wx.NewId()
ID_viewSpectrumRulerParentMass = wx.NewId()
ID_viewSpectrumRulerArea = wx.NewId()

ID_viewPeaklistColumnMz = wx.NewId()
ID_viewPeaklistColumnAi = wx.NewId()
ID_viewPeaklistColumnInt = wx.NewId()
ID_viewPeaklistColumnBase = wx.NewId()
ID_viewPeaklistColumnRel = wx.NewId()
ID_viewPeaklistColumnSn = wx.NewId()
ID_viewPeaklistColumnZ = wx.NewId()
ID_viewPeaklistColumnMass = wx.NewId()
ID_viewPeaklistColumnFwhm = wx.NewId()
ID_viewPeaklistColumnResol = wx.NewId()
ID_viewPeaklistColumnGroup = wx.NewId()

HK_viewPosBars = '\tAlt+Ctrl+P'
HK_viewGel = '\tAlt+Ctrl+G'
HK_viewLabels = '\tAlt+Ctrl+L'
HK_viewTicks = '\tAlt+Ctrl+T'
HK_viewLabelAngle = '\tAlt+Ctrl+H'
HK_viewAllLabels = '\tAlt+Ctrl+Shift+L'
HK_viewOverlapLabels = '\tAlt+Ctrl+O'
HK_viewAutoscale = '\tAlt+Ctrl+A'
HK_viewNormalize = '\tAlt+Ctrl+N'
HK_viewRange = '\tAlt+Ctrl+R'
HK_viewCanvasProperties = '\tCtrl+J'

# processing
ID_processingUndo = wx.NewId()
ID_processingPeakpicking = wx.NewId()
ID_processingDeisotoping = wx.NewId()
ID_processingDeconvolution = wx.NewId()
ID_processingBaseline = wx.NewId()
ID_processingSmoothing = wx.NewId()
ID_processingCrop = wx.NewId()
ID_processingMath = wx.NewId()
ID_processingBatch = wx.NewId()
ID_toolsSwapData = wx.NewId()

HK_processingUndo = '\tCtrl+Z'
HK_processingPeakpicking = '\tCtrl+F'
HK_processingDeisotoping = '\tCtrl+D'
HK_processingDeconvolution = ''
HK_processingSmoothing = '\tCtrl+G'
HK_processingBaseline = '\tCtrl+B'

# evaluation
ID_evalRes = wx.NewId()
ID_toRes = wx.NewId()

HK_evalRes = '\tCtrl+E'
HK_toRes  = '\tCtrl+R'

# sequence
ID_sequenceNew = wx.NewId()
ID_sequenceImport = wx.NewId()
ID_sequenceEditor = wx.NewId()
ID_sequenceModifications = wx.NewId()
ID_sequenceDigest = wx.NewId()
ID_sequenceFragment = wx.NewId()
ID_sequenceSearch = wx.NewId()
ID_sequenceSendToMassCalculator = wx.NewId()
ID_sequenceSendToEnvelopeFit = wx.NewId()
ID_sequenceDelete = wx.NewId()
ID_sequenceSort = wx.NewId()
ID_sequenceMatchEdit = wx.NewId()
ID_sequenceMatchDelete = wx.NewId()
ID_sequenceMatchSendToMassCalculator = wx.NewId()
ID_sequenceMatchSendToEnvelopeFit = wx.NewId()
ID_sequenceMatchesDelete = wx.NewId()
ID_sequenceMatchesCalibrateBy = wx.NewId()

# tools
ID_toolsProcessing = wx.NewId()
ID_toolsCalibration = wx.NewId()
ID_toolsSequence = wx.NewId()
ID_toolsRuler = wx.NewId()
ID_toolsLabelPeak = wx.NewId()
ID_toolsLabelPoint = wx.NewId()
ID_toolsLabelEnvelope = wx.NewId()
ID_toolsDeleteLabel = wx.NewId()
ID_toolsOffset = wx.NewId()
ID_toolsPeriodicTable = wx.NewId()
ID_toolsMassCalculator = wx.NewId()
ID_toolsMassToFormula = wx.NewId()
ID_toolsMassDefectPlot = wx.NewId()
ID_toolsMassFilter = wx.NewId()
ID_toolsCompoundsSearch = wx.NewId()
ID_toolsPeakDifferences = wx.NewId()
ID_toolsComparePeaklists = wx.NewId()
ID_toolsSpectrumGenerator = wx.NewId()
ID_toolsEnvelopeFit = wx.NewId()
ID_toolsMascot = wx.NewId()
ID_toolsProfound = wx.NewId()
ID_toolsProspector = wx.NewId()
ID_toolsDocumentInfo = wx.NewId()
ID_toolsDocumentReport = wx.NewId()
ID_toolsDocumentExport = wx.NewId()

HK_toolsCalibration = '\tCtrl+R'
HK_toolsRuler = '\tShift+Ctrl+H'
HK_toolsLabelPeak = '\tShift+Ctrl+P'
HK_toolsLabelPoint = '\tShift+Ctrl+I'
HK_toolsLabelEnvelope = '\tShift+Ctrl+E'
HK_toolsDeleteLabel = '\tShift+Ctrl+X'
HK_toolsPeriodicTable = '\tShift+Ctrl+T'
HK_toolsMassCalculator = '\tShift+Ctrl+M'
HK_toolsMassToFormula = '\tShift+Ctrl+B'
HK_toolsMassDefectPlot = '\tShift+Ctrl+O'
HK_toolsMassFilter = '\tShift+Ctrl+F'
HK_toolsCompoundsSearch = '\tShift+Ctrl+U'
HK_toolsPeakDifferences = '\tShift+Ctrl+D'
HK_toolsComparePeaklists = '\tShift+Ctrl+C'
HK_toolsSpectrumGenerator = '\tShift+Ctrl+G'
HK_toolsEnvelopeFit = '\tShift+Ctrl+V'

# peaklist panel
ID_peaklistAnnotate = wx.NewId()
ID_peaklistSendToMassToFormula = wx.NewId()

# match panel
ID_matchErrors = wx.NewId()
ID_matchSummary = wx.NewId()

# calibration panel
ID_calibrationReferences = wx.NewId()
ID_calibrationErrors = wx.NewId()

# mass calculator panel
ID_massCalculatorSummary = wx.NewId()
ID_massCalculatorIonSeries = wx.NewId()
ID_massCalculatorPattern = wx.NewId()
ID_massCalculatorCollapse = wx.NewId()

# mass to formula panel
ID_massToFormulaSearchPubChem = wx.NewId()
ID_massToFormulaSearchChemSpider = wx.NewId()
ID_massToFormulaSearchMETLIN = wx.NewId()
ID_massToFormulaSearchHMDB = wx.NewId()
ID_massToFormulaSearchLipidMaps = wx.NewId()

# coumpounds search panel
ID_compoundsSearchCompounds = wx.NewId()
ID_compoundsSearchFormula = wx.NewId()

# info panel
ID_documentInfoSummary = wx.NewId()
ID_documentInfoSpectrum = wx.NewId()
ID_documentInfoNotes = wx.NewId()

# export panel
ID_documentExportImage = wx.NewId()
ID_documentExportPeaklist = wx.NewId()
ID_documentExportSpectrum = wx.NewId()

# dialog buttons
ID_dlgDontSave = wx.NewId()
ID_dlgSave = wx.NewId()
ID_dlgCancel = wx.NewId()
ID_dlgDiscard = wx.NewId()
ID_dlgReview = wx.NewId()
ID_dlgReplace = wx.NewId()
ID_dlgReplaceAll = wx.NewId()
ID_dlgSkip = wx.NewId()
ID_dlgAppend = wx.NewId()

# list pop-up menu
ID_listViewAll = wx.NewId()
ID_listViewMatched = wx.NewId()
ID_listViewUnmatched = wx.NewId()
ID_listCopy = wx.NewId()
ID_listCopySequence = wx.NewId()
ID_listCopyFormula = wx.NewId()
ID_listSendToMassCalculator = wx.NewId()
ID_listSendToEnvelopeFit = wx.NewId()
