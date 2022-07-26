import wx
from wxasync import AsyncBind, WxAsyncApp, StartCoroutine
import asyncio
from asyncio.events import get_event_loop
import time
import wx.lib.newevent
SomeNewEvent, EVT_SOME_NEW_EVENT = wx.lib.newevent.NewEvent()
SomeNewEventAsync, EVT_SOME_NEW_EVENT_ASYNC = wx.lib.newevent.NewEvent()

import ui_layer.config.ui_config as ui_config
uic = ui_config.uic


from pipeline.s3.view.module.list_s3_objects_sortable_paginated_sqlite.Sortable_ListCtrl import Sortable_ListCtrl



class TestSubPanel(wx.Panel):
    def __init__(self, parent=None):
        super(TestSubPanel, self).__init__(parent)
        vbox = wx.BoxSizer(wx.VERTICAL)
        button11 =  wx.Button(self, label="AsyncBind- SUB level")
        
        panel = Sortable_ListCtrl(self)
        vbox.Add(button11, 0)
        vbox.Add(panel, 1, wx.EXPAND|wx.ALL)
        self.SetSizer(vbox)
        self.Layout()
        self.clock_on = False

        """Binding of button event to async method"""
        AsyncBind(wx.EVT_BUTTON, self.async_test, button11)

    async def async_test(self, event):
        print ('async_download')
        await asyncio.sleep(1)
        print ('async_download')
        await asyncio.sleep(1)
        print ('async_download')
        await asyncio.sleep(1)
        print ('async_download')
        await asyncio.sleep(1)
        print ('async_download')
        await asyncio.sleep(1)
        print ('async_download')
        await asyncio.sleep(1)
        print ('async_download')
        await asyncio.sleep(1)
        print ('async_download')
