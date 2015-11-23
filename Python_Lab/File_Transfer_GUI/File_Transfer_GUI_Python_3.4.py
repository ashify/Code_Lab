__author__ = 'Carlin Aylsworth'
import wx
import wx.lib.filebrowsebutton as filebrowse
import os
import time
import shutil
import sqlite3
import datetime

try:
    from agw import buttonpanel as bp
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.buttonpanel as bp
try:
    from agw import cubecolourdialog as CCD
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.cubecolourdialog as CCD

#establish database connection and cursor
conn = sqlite3.connect('filecheck.db')
c = conn.cursor()


def create(parent):
    return Frame(parent)

[wxID_FRAME1] = [wx.NewId() for _init_ctrls in range(1)]


class Frame(wx.Frame):
    
    def __init__(self, parent):
        self._init_ctrls(parent)
        self.lastMousePos = wx.Point(0, 0)
    
    def _init_ctrls(self, parent):
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=parent, size=(680, 470), title='Frame1')
        self.created = False
        self.useredited = False
        self.hassettingpanel = False
        self.mainPanel = wx.Panel(self, -1)
        self.starttext = wx.StaticText(self.mainPanel, -1,
            """1. Choose a source directory to search for new/modified files.\n2. Choose directory to copy files to, if any are found.""", pos=(100,60))
        self.dbb = filebrowse.DirBrowseButton(
            self.mainPanel, -1, size=(450, -1), pos=(100,100), buttonText="Source", labelText = 'Choose Directory:'
            )
        self.dbb2 = filebrowse.DirBrowseButton(
            self.mainPanel, -1, size=(450, -1), pos=(100,150), buttonText="Destination", labelText = 'Choose Directory:'
            )
        self.btn = wx.Button(self.mainPanel, -1, label="Run", pos=(458,200), size=(90,40))
        self.console = wx.TextCtrl(self.mainPanel, -1, pos=(100,250), size=(450,150), style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_WORDWRAP)
        self.agwStyle = bp.BP_USE_GRADIENT
        # self.CreateMenuBar()
        self.agwStyle = bp.BP_USE_GRADIENT
        self.titleBar = bp.ButtonPanel(self.mainPanel, -1, "Backup New/Modified Files",
                                       agwStyle=self.agwStyle, alignment=bp.BP_ALIGN_LEFT)
        self.CreateButtons()
        self.SetProperties()

        # Bind Event Handlers to controls
        self.btn.Bind(wx.EVT_BUTTON, self.onCopy)
        self.Bind(wx.EVT_KEY_UP, self.on_key_press)
        self.Bind(wx.EVT_MOTION, self.OnFrame1Motion)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnFrame1LeftDown)
        self.Centre()
        self.initialQuery()

    ############################################
    ############# GUI Init Methods #############
    ############################################
        
    def SetProperties(self):
        if self.useredited:
            return
        
        bpArt = self.titleBar.GetBPArt()

        if self.agwStyle & bp.BP_USE_GRADIENT:
            bpArt.SetColour(bp.BP_TEXT_COLOUR, wx.WHITE)
            bpArt.SetColour(bp.BP_BORDER_COLOUR, wx.Colour(83, 148, 159))
            bpArt.SetColour(bp.BP_GRADIENT_COLOUR_FROM, wx.Colour(83, 148, 159))
            bpArt.SetColour(bp.BP_GRADIENT_COLOUR_TO, wx.Colour(83, 148, 159))
            bpArt.SetColour(bp.BP_BUTTONTEXT_COLOUR, wx.Colour(70,143,255))
            bpArt.SetColour(bp.BP_SEPARATOR_COLOUR,
                            bp.BrightenColour(wx.Colour(60, 11, 112), 0.85))
            bpArt.SetColour(bp.BP_SELECTION_BRUSH_COLOUR, wx.Colour(225, 225, 255))
            bpArt.SetColour(bp.BP_SELECTION_PEN_COLOUR, wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION))

        else:

            background = self.titleBar.GetBackgroundColour()
            bpArt.SetColour(bp.BP_TEXT_COLOUR, wx.Colour(120, 185, 197))
            bpArt.SetColour(bp.BP_BORDER_COLOUR,
                            bp.BrightenColour(background, 0.85))
            bpArt.SetColour(bp.BP_SEPARATOR_COLOUR,
                            bp.BrightenColour(background, 0.85))
            bpArt.SetColour(bp.BP_BUTTONTEXT_COLOUR, wx.BLACK)
            bpArt.SetColour(bp.BP_SELECTION_BRUSH_COLOUR, wx.Colour(242, 242, 235))
            bpArt.SetColour(bp.BP_SELECTION_PEN_COLOUR, wx.Colour(206, 206, 195))

        self.titleBar.SetStyle(self.agwStyle)

    def CreateButtons(self):
        self.Freeze()

        if self.created:
            sizer = self.mainPanel.GetSizer()
            sizer.Detach(0)
            self.titleBar.Hide()
            wx.CallAfter(self.titleBar.Destroy)
            self.titleBar = bp.ButtonPanel(self.mainPanel, -1, "Modern GUI")
            self.SetProperties()

        self.indices = []
        kind = wx.ITEM_NORMAL

        btn = bp.ButtonInfo(self.titleBar, wx.NewId(),wx.ArtProvider.GetBitmap(wx.ART_HELP, wx.ART_TOOLBAR, (32,32)), kind=kind)
        self.titleBar.AddButton(btn)
        self.Bind(wx.EVT_BUTTON, self.OnAbout, btn)

        btn = bp.ButtonInfo(self.titleBar, wx.NewId(),wx.ArtProvider.GetBitmap(wx.ART_ERROR, wx.ART_TOOLBAR, (32,32)), kind=kind)
        self.titleBar.AddButton(btn)
        self.Bind(wx.EVT_BUTTON, self.OnClose, btn)
        self.ChangeLayout()
        self.Thaw()
        self.titleBar.DoLayout()

        self.created = True
            
    def ChangeLayout(self):
        # Change the layout after a switch in ButtonPanel alignment
        self.Freeze()
        vSizer = wx.BoxSizer(wx.VERTICAL)

        self.mainPanel.SetSizer(vSizer)

        vSizer.Add(self.titleBar, 0, wx.EXPAND)
        vSizer.Add((20, 20))

        vSizer.Layout()
        self.mainPanel.Layout()
        self.Thaw()

    ############################################
    ############### Event Handlers #############
    ############################################
    
    def onCopy(self, evt):
        src_dir = self.dbb.GetValue().replace('\\','/')
        dest_dir = self.dbb2.GetValue().replace('\\','/')
        src_files = os.listdir(src_dir)
        lasttime = c.execute('SELECT time FROM lastcheck ORDER BY ROWID DESC LIMIT 1')
        day_ago = time.time() - (24*60*60)
        for row in lasttime:
            day_ago = row[0]
        count = 0
        
        for file in src_files:
            if os.path.getmtime(src_dir+'/'+file) > day_ago:
                count += 1
                shutil.copy(src_dir+'/'+file, dest_dir)
                self.console.AppendText(str(count)+'.'+file+' copied to '+ dest_dir+'\n')           
        if count == 0:
            self.console.AppendText('No newly modified files in that directory.\n')

        date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute("INSERT INTO lastcheck(datetime,time) VALUES(?,?)",(date_time,time.time()))
        conn.commit()    
        
    def on_key_press(self, event):
        '''
        quit if user presses Esc key (27)
        '''
        if event.GetKeyCode() == 27:
            self.Close(force=True)
        else:
            event.Skip()
    def OnAlignment(self, event):

        # Here we change the alignment property of ButtonPanel
        current = event.GetId()
        item = self.GetMenuBar().FindItemById(current)
        alignment = getattr(bp, item.GetLabel())
        self.alignment = alignment

        self.ChangeLayout()
        self.titleBar.SetAlignment(alignment)
        self.mainPanel.Layout()

        event.Skip()

    def OnFrame1Motion(self, event):
        if not event.Dragging():
            self._dragPos = None
            return
        # important! the next 2 lines fix draggable bug
        if self.HasCapture():
            self.ReleaseMouse()
        self.CaptureMouse()
        if not self._dragPos:
            self._dragPos = event.GetPosition()
        else:
            pos = event.GetPosition()
            displacement = self._dragPos - pos
            self.SetPosition( self.GetPosition() - displacement )        
        
    def OnFrame1LeftDown(self, event):
        self.lastMousePos = event.GetPosition()
        event.Skip()
        
    def OnAbout(self, event):

        msg = "This is an app that will backup files from a given\n" + \
              "folder if they have been created/modified within 24 hours.\n\n" + \
              "Author: Carlin Aylsworth @ 09 Sep 2015\n\n" + \
              "Please Report Any Bugs/Requests To:\n" + \
              "carlinaylsworth@hotmail.com\n\n"

        dlg = wx.MessageDialog(self, msg, "About",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        
    def OnClose(self, event):
        self.Destroy()
        event.Skip()

    #queries db for last check for updated files, or creates table
    def initialQuery(self):
        c.execute("CREATE TABLE IF NOT EXISTS lastcheck(datetime TEXT, time REAL)")
        lastcheck = c.execute('SELECT datetime FROM lastcheck ORDER BY ROWID DESC LIMIT 1')
        for row in lastcheck:
            self.console.AppendText('Last check occurred on: '+ str(row).replace('(','').replace(')','').replace('u\'','').replace("'","")+'\n')
                   
if __name__ == "__main__":
    app = wx.App()
    frame = create(None)
    frame.Show()
    app.MainLoop()
    

    
    



    
