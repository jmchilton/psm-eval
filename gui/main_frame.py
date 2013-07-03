import wx
from ids import *
import os
from main_panel import *

# Main Frame

class mainFrame(wx.Frame):
    
    def __init__(self, parent, id, title):
        # global counter for the sequence of files being evaluated
        self.evalNum = 0
        wx.Frame.__init__(self, parent, -1, title, size=(1000,800))
        self.nb = wx.Notebook(self)
        self.makeMenuBar()
        self.SetMenuBar(self.menubar)
        
        # init basics
        self.processingDocumentQueue = False
        self.tmpDocumentQueue = []

    def makeMenuBar(self):
        # init menubar
        # HK_ indicates hotkeys
        self.menubar = wx.MenuBar()

        # file menu
        filemenu = wx.Menu()
        filemenu.Append(ID_docOpen, "Open"+HK_docOpen, "Open a Peptide Report")
        filemenu.AppendSeparator()
        filemenu.Append(ID_docClose, "Close"+HK_docClose, "Close the current report document")
        filemenu.Append(ID_docCloseAll, "Close All"+HK_docCloseAll, "Close all report documents")
        filemenu.AppendSeparator()
        filemenu.Append(ID_docPrintSpectrum, "Print Spectrum"+HK_docPrintSpectrum, "")
        filemenu.Append(ID_docReport, "Analysis Report"+HK_docReport, "")
        filemenu.AppendSeparator()
        filemenu.Append(ID_quit, "Quit"+HK_quit, "Quit PSME")
        
        # Bind events with objects
        
        self.Bind(wx.EVT_MENU, self.onDocOpen, id=ID_docOpen)
        # self.Bind(wx.EVT_MENU, self.onDocClose, id=ID_docClose)
        # self.Bind(wx.EVT_MENU, self.onDocCloseAll, id=ID_docCloseAll)
        # self.Bind(wx.EVT_MENU, self.onDocPrintSpectrum, id=ID_docPrintSpectrum)
        # self.Bind(wx.EVT_MENU, self.onDocReport, id=ID_docReport)
        self.Bind(wx.EVT_MENU, self.onQuit, id=ID_quit)

        self.menubar.Append(filemenu, "File")

        # view menu
        viewmenu = wx.Menu()
        
        viewPeakListColumns = wx.Menu()
        # fill in details of the viewPeakListColumns submenu
        viewmenu.AppendMenu(-1, "Peak List Columns", viewPeakListColumns)
        '''
        self.Bind(wx.EVT_MENU, self.onView, id=ID_view)
        self.Bind(wx.EVT_MENU, self.onViewPeakListColumns, id=ID_viewPeakListColumn)
        '''
        
        self.menubar.Append(viewmenu, "View")

    
        # Evaluation menu
        evalmenu = wx.Menu()
        evalmenu.Append(ID_evalRes, "Evaluate Results"+HK_evalRes, "")

        self.Bind(wx.EVT_MENU, self.onEvalRes, id=ID_evalRes)
        
        self.menubar.Append(evalmenu, "Evaluation")
        
    # Default events
    def onQuit(self, event):

        # close all documents
        if not self.onDocCloseAll():
            return
        
        event.Skip()
        self.Destroy()


    
    # File events
    # ---
    def onDocOpen(self, event=None):
        """Open document."""

        dirname = ''
        wildcard =  "All supported formats|fid;*.msd;*.baf;*.yep;*.mzData;*.mzdata*;*.mzXML;*.mzxml;*.mzML;*.mzml;*.xml;*.XML;*.mgf;*.MGF;*.txt;*.xy;*.asc|All files|*.*"
        dlg = wx.FileDialog(self, "Open Document", dirname, "", wildcard=wildcard, style=wx.FD_OPEN|wx.FD_MULTIPLE|wx.FD_FILE_MUST_EXIST)
            
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            dlg.Destroy()
            # Add the document to the queue of docs ready to be processed
            self.tmpDocumentQueue += list(paths)
            
            '''
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            self.control.SetValue(f.read())
            f.close()
            '''
        else:
            dlg.Destroy()
    #---
    
    def onDocCloseAll(self, event=None):
        return True
    #---
    
    def onEvalRes(self, event=None):
        self.evalNum += 1
        curPage = self.nb.AddPage(mainPanel(self.nb, -1, "Evaluation"), "Evaluation %d" % self.evalNum)
    
    

app = wx.App(False)
frame = mainFrame(None, -1, 'Peptide-Spectrum-Matches (PSMs) Evaluation (version 0.1.0) ')
frame.Show()
app.MainLoop()
