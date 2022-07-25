import wx
#import wx.lib.mixins.listctrl as listmix
#from wx.lib.agw import ultimatelistctrl as ULC

import wx
import os, sys, time, json
from os.path import isfile, dirname, join, isdir
#import subprocess
from pprint import pprint as pp
from ui_layer.log_init import log, info, debug
from ui_layer.Base import Base


from ui_layer.utils import exception, load_pipeline_module
from pathlib import Path

from ui_layer.common import open_editor
#from ui_layer.module.controller.Searcheable_ListCtrl_Controller import Controller
#from ui_layer.module.Sortable_ListCtrl import Sortable_ListCtrl

import cli_layer.aws_pipeline_utils  as APU
import cli_layer.s3_utils  as S3U
import ui_layer.config.ui_config as ui_config
uic = ui_config.uic
Sortable_ListCtrl= load_pipeline_module(uic, 'Sortable_ListCtrl')
#from ui_layer.module.Sortable_Searcheable_ListCtrl import Sortable_Searcheable_ListCtrl
MAIN_WIDTH=300
MAIN_HEIGHT=300

class Sortable_ListPanel(wx.Panel, Base):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS, size=(MAIN_WIDTH,MAIN_HEIGHT))
        self.b_first = b_first=wx.Button(self, wx.ID_OK, label="First", size=(50, 30))
        b_first.Bind(wx.EVT_BUTTON, self.onFirstPage)
        self.b_prev = b_prev=wx.Button(self, wx.ID_OK, label="Prev", size=(50, 30))
        b_prev.Bind(wx.EVT_BUTTON, self.onPrevPage)
        self.b_next = b_next=wx.Button(self, wx.ID_OK, label="Next", size=(50, 30))
        b_next.Bind(wx.EVT_BUTTON, self.onNextPage)
        self.b_last = b_last=wx.Button(self, wx.ID_OK, label="Last", size=(50, 30))
        b_last.Bind(wx.EVT_BUTTON, self.onLastPage)

        self.b_order = b_order=wx.Button(self, wx.ID_OK, label="Order", size=(50, 30))
        b_order.Bind(wx.EVT_BUTTON, self.onOrder)
        self.b_download = b_download=wx.Button(self, wx.ID_OK, label="Download", size=(50, 30))
        b_download.Bind(wx.EVT_BUTTON, self.onDownload)
        self.list_ctrl = Sortable_ListCtrl(self)


        sizer = wx.BoxSizer(wx.VERTICAL)
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        h_sizer.Add(self.b_first, 0,0,3)
        h_sizer.Add(self.b_prev, 0,0,3)
        h_sizer.Add(self.b_next, 0,0,3)
        h_sizer.Add(self.b_last, 0,0,3)
        h_sizer.Add((25,5), 0,0,3)
        h_sizer.Add(self.b_order, 0,0,3)
        h_sizer.Add((25,5), 0,0,3)
        h_sizer.Add(self.b_download, 0,0,3)        
        h_sizer.Add((5,5), 1, wx.ALL|wx.EXPAND,1)
        sizer.Add(h_sizer, 0,0,1)
        sizer.Add(self.list_ctrl, 1, wx.ALL|wx.EXPAND, 1)
        self.SetSizer(sizer)
    def onDownload(self,event):
        print('onDownload')
        self.send('downloadChunk',())        
    def onFirstPage(self,event):
        print('First')
        self.send('firstPage',())
    def onOrder(self,event):
        print('Order')
        self.send('onOrder',())
        
    def onPrevPage(self,event):
        print('Prev')
        self.send('prevPage',())
    def onNextPage(self,event):
        print('Next')
        self.send('nextPage',())
        
    def onLastPage(self,event):
        print('Last')
        r = wx.MessageDialog(
            None,
            'Fetch full file list?' ,
            'Confirm last page retrieval',
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
        ).ShowModal()

        if r != wx.ID_YES:
            return
            
        self.send('lastPage',())        
        