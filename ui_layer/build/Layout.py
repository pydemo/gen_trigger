# -*- coding: utf-8 -*-
import wx
import wx.lib.agw.aui as aui
from ui_layer.utils import dict2
class Page(object):
    def __init__(self, parent, mgr, refs):
        self.parent=parent
        self.mgr=mgr
        self.refs= refs

    def detachWin(self, winkey, winname):
        mgr=self.mgr
        ref= self.refs[winkey][winname]
        pane= mgr.GetPane(ref)
        
        if pane.IsOk():
            pane.Show(False)
            mgr.DetachPane(ref)

        if 1: 
            ref.Show(False)

    def attachWin(self,win, winkey,winname):
        
        if winkey not in self.refs:  self.refs[winkey] = {}
        
        if 1:
            if winname not in self.refs[winkey] :
                self.refs[winkey][winname] = win
            else: 
                win = self.refs[winkey][winname]
                win.Show(True)
            
    def load_page(self):
        
        #
        #PipelineList | ui_layer\module\ListCtrl_Frame.py.ListCtrl_Frame	
        #ui_layer\module\ListCtrl_Frame.py
        # ui_layer.module.ListCtrl_Frame
        from ui_layer.module.ListCtrl_Frame import ListCtrl_Frame
            
        winname   = 'PipelineList'
        winkey    = r'ui_layer\module\ListCtrl_Frame.py.ListCtrl_Frame'
        win = parent=ListCtrl_Frame(parent=self.parent, name=winname, lineno=0, layout_fn = r'C:\Users\alex_\gh\ui_demo\pipeline\s3\view\ui_layout\list_s3_objects_sortable_paginated_sqlite.json' )
        self.attachWin(win, winkey,winname)

        self.mgr.AddPane(win,aui.AuiPaneInfo().Center().Layer(1).
        BestSize(wx.Size(200,150)).MinSize(wx.Size(200,150)).Caption("PipelineList").
        CloseButton(False).Name("PipelineList").CaptionVisible(False))