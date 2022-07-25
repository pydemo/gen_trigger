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
        {page_load}