import wx
#import wx.lib.mixins.listctrl as listmix
#from wx.lib.agw import ultimatelistctrl as ULC

import wx
import os, sys, time, json
from os.path import isfile, dirname, join, isdir
#import subprocess
from pprint import pprint as pp
from ui_layer.log_init import log, info, debug
from ui_layer.Base import reciever


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

class Sortable_ListPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS, size=(MAIN_WIDTH,MAIN_HEIGHT))

        self.list_ctrl = Sortable_ListCtrl(self)


        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list_ctrl, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(sizer)
