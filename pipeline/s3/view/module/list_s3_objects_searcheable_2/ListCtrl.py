#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
"""Sorted ListCtrl
OnClick 132060
(132060, 'k9-filestore/k9-feed-doc-lims/', 'A0361447 PABF.pdf', 46112502)
OnClick 136392
(136392, 'k9-filestore/k9-feed-doc-lims/', 'A0369628_PABF.pdf', 39667914)
OnClick 115657
(115657, 'k9-filestore/k9-feed-doc-lims/', 'A0331486_PABF.pdf', 34889047)
OnClick 46977
(46977, 'k9-filestore/k9-feed-doc-lims/', 'A0201883_TRF_1.pdf', 25353205)
OnClick 54409
(54409, 'k9-filestore/k9-feed-doc-lims/', 'A0217825_TRF_1.pdf', 23037220)
OnClick 203619
(203619, 'k9-filestore/k9-feed-doc-lims/', 'A77632_TRF_1.pdf', 22684558)
"""
import os, sys
from pprint import pprint as pp
e=sys.exit
from os.path import join, split, dirname, abspath
try:
    dirName = dirname(abspath(__file__))
except:
    dirName = dirname(abspath(sys.argv[0]))

sys.path.append(split(dirName)[0])
sys.path.append(split(split(dirName)[0])[0])
sys.path.append(split(split(split(dirName)[0])[0])[0])
sys.path.append(split(split(split(split(dirName)[0])[0])[0])[0])
sys.path.append(split(split(split(split(split(dirName)[0])[0])[0])[0])[0])
import platform
import tempfile

import wx
import wx.lib.mixins.listctrl as listmix
import datetime
import sys
import boto3
import os, sys, time, json
from os.path import isfile, dirname, join, isdir
import subprocess
from tempfile import gettempdir
from ui_layer.log_init import log, info, debug
from ui_layer.Base import reciever, Base

from collections import OrderedDict

from ui_layer.utils import exception
from pathlib import Path

from ui_layer.common import open_editor





import cli_layer.aws_pipeline_utils  as APU
import cli_layer.s3_utils  as S3U
import ui_layer.config.ui_config as ui_config
uic = ui_config.uic




from wxasync import AsyncBind, WxAsyncApp, StartCoroutine
if 0:
    import wx.lib.sized_controls as sc

    from wx.lib.pdfviewer import pdfViewer, pdfButtonPanel

    class PDFViewer(sc.SizedFrame):
        def __init__(self, parent, **kwds):
            super(PDFViewer, self).__init__(parent, **kwds)

            paneCont = self.GetContentsPane()
            self.buttonpanel = pdfButtonPanel(paneCont, wx.NewId(),
                                    wx.DefaultPosition, wx.DefaultSize, 0)
            self.buttonpanel.SetSizerProps(expand=True)
            self.viewer = pdfViewer(paneCont, wx.NewId(), wx.DefaultPosition,
                                    wx.DefaultSize,
                                    wx.HSCROLL|wx.VSCROLL|wx.SUNKEN_BORDER)
            self.viewer.UsePrintDirect = False
            self.viewer.SetSizerProps(expand=True, proportion=1)

            # introduce buttonpanel and viewer to each other
            self.buttonpanel.viewer = self.viewer
            self.viewer.buttonpanel = self.buttonpanel




MAXINT = 99999999
CHUNK_SIZE = 30 


def get_S3_File_List():
    bucket_name= 'gh-package-pdf'
    bucket_name= 'k9-filestore'
    prefix='k9-feed-doc-lims/'
    chunk = S3U.list_s3_files_gen(bucket_name, prefix, 1000, 100)
    #header
    #print('source,pipeline_name')
    rows={}
    for cid, pd in enumerate(chunk):
        for pid, ppl in enumerate(pd):
            #pp(ppl)
            #e()
            rows[pid] =(pid, f'{bucket_name}/{prefix}',pd[ppl]['Key'].lstrip(prefix),pd[ppl]['Size'])
    header = ['Id', 'Bucket','Key', 'Size']
    print('Got ', len(rows))
    return header, rows

def get_S3_File_List_gen():
    bucket_name= 'gh-package-pdf'
    bucket_name= 'k9-filestore'
    prefix='k9-feed-doc-lims/'
    #chunk = S3U.list_s3_files_gen_start_after(bucket_name, prefix, start_after='A010281301.FINAL_v1_report.pdf')
    chunk = S3U.list_s3_files_gen_v2(bucket_name, prefix, MaxKeys=CHUNK_SIZE, plimit= 1_000_000)
    
    #header
    #print('source,pipeline_name')
    header = ['Id', 'Bucket','Key', 'Size']
    gid=0
    for cid, pd in enumerate(chunk):
        rows={}
        print(cid,len(pd))
        for pid, ppl in enumerate(pd):
            #pp(ppl)
            #e()
            rows[gid] =(gid, f'{bucket_name}/{prefix}',pd[ppl]['Key'].lstrip(prefix),pd[ppl]['Size'])
            gid +=1
        #print('Got ', len(rows))
        yield header, rows

    return header, rows
    


import sqlite3
from subprocess import Popen, PIPE

from pathlib import Path

from cli_layer.common import  SLITE_LOC


import sqlite3
DB_NAME     = "s3_files.db"
MAXINT = 99999999
PAGE_SIZE = 30 


BUCKET_NAME= 'k9-filestore'
PREFIX='k9-feed-doc-lims'
        
        
con = sqlite3.connect(DB_NAME)
e=sys.exit


async def dump_S3ChunkToFile():
    print('dump_S3ChunkToFile')
    
    if 0:
        bucket_name= 'gh-package-pdf'
        bucket_name= 'k9-filestore'
        prefix='k9-feed-doc-lims/'
        #chunk = S3U.list_s3_files_gen_start_after(bucket_name, prefix, start_after='A010281301.FINAL_v1_report.pdf')
        chunk = S3U.list_s3_files_gen_v2(bucket_name, prefix, MaxKeys=CHUNK_SIZE, plimit= 1_000_000)
        from csv import writer
        
        from pathlib import Path
        import platform
        import tempfile
        from random import sample
        from string import digits, ascii_letters
        cid=0
        temp_dir = Path("/tmp" if platform.system() == "Darwin" else tempfile.gettempdir())
        ext_dir  = join(temp_dir, 's3_extract_%s' % ''.join(sample(ascii_letters + digits, 10)))
        if not isdir(ext_dir):
            os.makedirs(ext_dir)
        
        #Download from S3
        gid=0
        for cid, pd in enumerate(chunk):
            rows={}
            print('dump_S3ChunkToFile:', cid,len(pd))
            fname= join(ext_dir, f'{cid}.csv')
            with open(fname, 'a', newline='') as fh:
                writer_object = writer(fh)
                header = ['Id', 'Bucket','Key', 'Size']
                writer_object.writerow(header)
                
                for pid, ppl in enumerate(pd):
                    #pp(ppl)
                    #e()
                    #row = (gid, f'{bucket_name}/{prefix}',pd[ppl]['Key'].lstrip(prefix),pd[ppl]['Size'])
                    writer_object.writerow((cid, f'{bucket_name}/{prefix}',pd[ppl]['Key'].lstrip(prefix),pd[ppl]['Size']))
                    gid +=1
            print(f'Extracted to {fname}')
            yield header, fname
            cid +=1

AsyncDownload, EVT_ASYNC_DOWNLOAD = wx.lib.newevent.NewEvent()


def get_S3_File_Chunk_gen():
    bucket_name= 'gh-package-pdf'
    bucket_name= 'k9-filestore'
    prefix='k9-feed-doc-lims/'
    #chunk = S3U.list_s3_files_gen_start_after(bucket_name, prefix, start_after='A010281301.FINAL_v1_report.pdf')
    chunk = S3U.list_s3_files_gen_v2(bucket_name, prefix, MaxKeys=CHUNK_SIZE, plimit= 1_000_000)
    
    #header
    #print('source,pipeline_name')
    header = ['Id', 'Bucket','Key', 'Size']
    gid=0
    for cid, pd in enumerate(chunk):
        rows={}
        print(cid,len(pd))
        for pid, ppl in enumerate(pd):
            #pp(ppl)
            #e()
            rows[gid] =(gid, f'{bucket_name}/{prefix}',pd[ppl]['Key'].lstrip(prefix),pd[ppl]['Size'])
            gid +=1
        #print('Got ', len(rows))
        yield header, rows

    return header, rows
    
Controller        = load_pipeline_module(uic, 'Controller/ListCtrl_Controller')
    
class ListCtrl(wx.ListCtrl, listmix.ColumnSorterMixin, Controller):
    
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, style = wx.LC_REPORT)
        self.row_gen=get_S3_File_Chunk_gen()
        #self.file_gen=dump_S3ChunkToFile()
        self.data={}
        self.cid=0
        self.pid=0
        self.last_pid=0
        self.is_full=False
        self.ctrl_down = False
        self.setData()
        if 0:
            for header, rows in row_gen:
                self.data.update(rows)
            self.itemDataMap = self.data
        

        for col in self.header:
            self.InsertColumn(MAXINT, col)
        #self.InsertColumn(maxint, "Zahl")
        #self.InsertColumn(maxint, "Datum")
        if 0:
            # Daten in ListCtrl schreiben
            for key in sorted(self.data.keys()):
                char_value, number_value, date_value = self.data[key]
                index = self.InsertStringItem(MAXINT, char_value)
                self.SetItemData(index, key) #muss sein
                self.SetStringItem(index, 1, str(number_value))
                self.SetStringItem(index, 2, date_value.strftime("%d.%m.%Y"))
                self.SetColumnWidth(2, wx.LIST_AUTOSIZE)

        self.Refresh()
        print('Done.')
        listmix.ColumnSorterMixin.__init__(self, numColumns = self.GetColumnCount())
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnClick)
        self.sub('nextPage')
        self.sub('lastPage')
        self.sub('prevPage')
        self.sub('firstPage')
        self.sub('onOrder')
        self.sub('downloadChunk')
        
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick, self)
        self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPress)
        self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)

    #CREATE TABLE s3_files AS select Id, Bucket, Key, CAST(Size AS INTEGER) AS Size from t_table;
    @reciever
    def __downloadChunk(self, message, arg2=None, **kwargs):
        for self.header, fname in dump_S3ChunkToFile():
            if 1: #Insert into SqLite
                tname='s3_table'
                print('Loading file', fname)
                load_table(tname, fname)
            time.sleep(1)
    @reciever
    def downloadChunk(self, message, arg2=None, **kwargs):
        print('Started dc')
        if 0:
            StartCoroutine(self.async_download, self)
        if 1:
            #AsyncDownload, EVT_ASYNC_DOWNLOAD
            evt = AsyncDownload()
            wx.PostEvent(self, evt)
    async def update_clock(self):
        print('test update_clock')

    async def async_download(self, event):
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
        if 0:
            bucket_name= 'gh-package-pdf'
            bucket_name= 'k9-filestore'
            prefix='k9-feed-doc-lims/'
            #chunk = S3U.list_s3_files_gen_start_after(bucket_name, prefix, start_after='A010281301.FINAL_v1_report.pdf')
            chunk = S3U.list_s3_files_gen_v2(bucket_name, prefix, MaxKeys=CHUNK_SIZE, plimit= 1_000_000)
            from csv import writer
            
            from pathlib import Path
            import platform
            import tempfile
            from random import sample
            from string import digits, ascii_letters
            cid=0
            temp_dir = Path("/tmp" if platform.system() == "Darwin" else tempfile.gettempdir())
            ext_dir  = join(temp_dir, 's3_extract_%s' % ''.join(sample(ascii_letters + digits, 10)))
            if not isdir(ext_dir):
                os.makedirs(ext_dir)
            
            #Download from S3
            gid=0
            for cid, pd in enumerate(chunk):
                rows={}
                print('dump_S3ChunkToFile:', cid,len(pd))
                fname= join(ext_dir, f'{cid}.csv')
                with open(fname, 'a', newline='') as fh:
                    writer_object = writer(fh)
                    header = ['Id', 'Bucket','Key', 'Size']
                    writer_object.writerow(header)
                    
                    for pid, ppl in enumerate(pd):
                        #pp(ppl)
                        #e()
                        #row = (gid, f'{bucket_name}/{prefix}',pd[ppl]['Key'].lstrip(prefix),pd[ppl]['Size'])
                        writer_object.writerow((cid, f'{bucket_name}/{prefix}',pd[ppl]['Key'].lstrip(prefix),pd[ppl]['Size']))
                        gid +=1
                print(f'Extracted to {fname}')
                #yield header, fname
                cid +=1
                await asyncio.sleep(0.001)
        if 0:
            for self.header, fname in dump_S3ChunkToFile():
                if 1: #Insert into SqLite
                    tname='s3_table'
                    print('Loading file', fname)
                    load_table(tname, fname)
                await asyncio.sleep(1)

    @reciever
    def _downloadChunk(self, message, arg2=None, **kwargs):
        self.header, fname = next(dump_S3ChunkToFile())
        print(fname)
        if 0:
            pstart=CHUNK_SIZE*self.pid
            rcnt=len(rows)
            self.itemDataMap = {x:self.data[x] for x in range(pstart, pstart+rcnt)}
            self.Refresh()
        if 1: #Insert into SqLite
            tname='s3_table'
            print('Loading file', fname)
            load_table(tname, fname)
            
    def setSqliteData(self):
        self.header, rows = next(self.row_gen)
        #self.data.update(rows)
        pstart=CHUNK_SIZE*self.pid
        rcnt=len(rows)        
        self.itemDataMap = {x:self.data[x] for x in range(pstart, pstart+rcnt)}
        
        #return header, rows
    def setData(self):
        self.header, rows = next(self.row_gen)
        self.data.update(rows)
        pstart=CHUNK_SIZE*self.pid
        rcnt=len(rows)        
        self.itemDataMap = {x:self.data[x] for x in range(pstart, pstart+rcnt)}
        #pp(self.itemDataMap)

    @reciever
    def onOrder(self, message, arg2=None, **kwargs):

        print('onOrder')
        #pp(self.data)
        if 1:
            lst=sorted(self.data.items(), key=lambda kv: kv[1][3])
            print('*'*80)
            #pp(lst)
            self.data={i:x[1] for i,x in enumerate(sorted(self.data.items(), key=lambda kv: kv[1][3]))}
            self.setPage()
            #self.itemDataMap = self.data
            print('-'*80)
            #pp(self.data)
            self.Refresh()
    @reciever
    def firstPage(self, message, arg2=None, **kwargs):
        
        self.pid =0
        print('first page:', self.pid)
        self.setPage()
        self.Refresh()
        
    def setPage(self):
        eid = CHUNK_SIZE*(self.pid+1)
        if len(self.data) < eid:
            eid = len(self.data)
        self.itemDataMap = {x:self.data[x] for x in range(CHUNK_SIZE*self.pid, eid)}
        
    @reciever
    def prevPage(self, message, arg2=None, **kwargs):
        
        self.pid -=1
        print('prev page:', self.pid)
        self.setPage()
        self.Refresh()
        
    def getAllData(self):
        for header, rows in self.row_gen:
            self.data.update(rows)
            assert rows
            self.pid +=1
            print('getAllData:', self.pid,'data:', len(self.data),len(rows), len(header))
            
        print(CHUNK_SIZE*self.pid, CHUNK_SIZE*(self.pid+1))
        
        #pp(self.itemDataMap)
    @reciever
    def lastPage(self, message, arg2=None, **kwargs):
        
        #self.pid +=1
        print('last page:', self.pid)
        if not self.is_full:
            
            self.getAllData()
            self.itemDataMap = {x:self.data[x] for x in range(CHUNK_SIZE*(self.pid), len(self.data))}
            self.Refresh()
            self.is_full=True
            self.last_pid=self.pid
        else:
            self.pid = self.last_pid
            self.Refresh()
        
    def OnKeyUp(self, evt=None):

        self.ctrl_down = evt.controlDown
    def OnColClick(self, event):

        print(self.ctrl_down)
        
        if self.ctrl_down:
            self.ctrl_down=False
            r = wx.MessageDialog(
                None,
                'Fetch full file list?' ,
                'Confirm global sort',
                wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
            ).ShowModal()
            
            if r != wx.ID_YES:
                
                return
        else:
            if 0:
                self.pid -=1
                self.setData()
                self.Refresh()
            event.Skip()

    def onKeyPress(self, evt):

        self.ctrl_down = evt.controlDown

        evt.Skip()
            
    def GetListCtrl(self):
        return self.slist        
    @reciever
    def nextPage(self, message, arg2=None, **kwargs):
        
        self.pid +=1
        print('next page:', self.pid)
        self.setData()
        self.Refresh()
    def Refresh(self):
        self.Freeze()
        self.DeleteAllItems()
        data=self.itemDataMap
        if 1:
            # Daten in ListCtrl schreiben
            for key in list(data.keys()):
                
                pid, char_value, number_value, date_value = data[key]
                index = self.InsertStringItem(MAXINT, str(pid))
                self.SetItemData(index, key) #muss sein
                self.SetStringItem(index, 1, char_value)
                self.SetStringItem(index, 2, number_value)
                #self.SetStringItem(index, 2, date_value.strftime("%d.%m.%Y"))
                self.SetStringItem(index, 3, "{:,} B".format(date_value))

        self.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.SetColumnWidth(2, wx.LIST_AUTOSIZE)
        self.SetColumnWidth(3, wx.LIST_AUTOSIZE)
        self.Thaw()

    def GetListCtrl(self):
        return self

    def OnClick(self, event):
        item=int(event.GetText())
        print ('OnClick', item)
        print(self.itemDataMap[item])
        _,_, fn,_ =self.itemDataMap[item]
        s3_key = '/'.join([PREFIX,fn])
        print('Opening', s3_key)
        #e()
        temp_dir = Path("/tmp" if platform.system() == "Darwin" else tempfile.gettempdir())
        local_fn= join(temp_dir, fn)
        self.download_file(BUCKET_NAME, s3_key, local_fn)
        if 0:
            self.view_pdf(local_fn)
        else:
            self.open_pdf(local_fn)
            if 0:
                import subprocess
                doc = subprocess.Popen(["start", local_fn], shell=True)
        
    def open_pdf(self, local_fn):
        assert isfile(local_fn)
        status=os.startfile(local_fn)
        print(status)
    def linux(self):
        from webbrowser import BackgroundBrowser
        browser = BackgroundBrowser('/usr/bin/okular')
        browser.args.extend(
            ['--icon', 'okular', '-caption', 'Okular']
        )
        browser.open("/path/to/file.pdf")  
        
    def view_pdf(self, local_fn):
        import wx.lib.mixins.inspection as WIT
        


        pdfV = PDFViewer(None, size=(800, 600))
        pdfV.viewer.UsePrintDirect = False
        pdfV.viewer.LoadFile(local_fn)
        pdfV.Show()
    
    def getS3Client(self):

        session = boto3.Session()
              
        s3 = session.client('s3')
        return s3
    def download_file(self, bucket_name, s3_key, local_fn):

        s3= self.getS3Client()
        
        
        status=s3.download_file(bucket_name,s3_key, local_fn)
        print('Downloaded to ', local_fn, status)
        #pfmtd([dict(From=fc.key_to, To=fc.down_to, Status='Downloaded')], 'Download status')
        return status
    

class MyFrame(wx.Frame):
    
    def __init__(
        self, parent = None, title = "Example", size = wx.Size(550, 420)
    ):
        wx.Frame.__init__(self, parent, -1, title, size = size)
        
        panel = wx.Panel(self)
        
        vbox_main = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(vbox_main)
        
        my_list = SortedListCtrl(panel)
        vbox_main.Add(my_list, 1, wx.EXPAND | wx.ALL, 10)


def main():
    """Testing"""
    app = wx.PySimpleApp()
    f = MyFrame()
    f.Center()
    f.Show()
    app.MainLoop()


if __name__ == "__main__":

        
        
    main()