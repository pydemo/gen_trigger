import wx
from pprint import pprint as pp
import ui_layer.module.images as images

_demoPngs = ["overview", "recent", "frame", "dialog", "moredialog", "core",
             "book", "customcontrol", "morecontrols", "layout", "process",
             "clipboard", "images", "miscellaneous"]
             
             
USE_CUSTOMTREECTRL = False
DEFAULT_PERSPECTIVE = "Default Perspective"
from wx.lib.mixins.treemixin import ExpansionState
if USE_CUSTOMTREECTRL:
    import wx.lib.agw.customtreectrl as CT
    TreeBaseClass = CT.CustomTreeCtrl
else:
    TreeBaseClass = wx.TreeCtrl


class Searcheable_TreeCtrl2(ExpansionState, TreeBaseClass):
    def __init__(self, parent):
        TreeBaseClass.__init__(self, parent, style=wx.TR_DEFAULT_STYLE|
                               wx.TR_HAS_VARIABLE_ROW_HEIGHT)
        self.BuildTreeImageList()
        if USE_CUSTOMTREECTRL:
            self.SetSpacing(10)
            self.SetWindowStyle(self.GetWindowStyle() & ~wx.TR_LINES_AT_ROOT)

        self.SetInitialSize((100,80))
        randomId = wx.NewId()
        self.Bind(wx.EVT_MENU, self.onKeyCombo, id=randomId)
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL,  ord('C'), randomId )])
        self.SetAcceleratorTable(accel_tbl)
    def onKeyCombo(self, event):
        """"""
        print ("You pressed CTRL+C!")

        txt=self.GetItemText(self.GetSelection())
        dataObj = wx.TextDataObject()
        dataObj.SetText(txt)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(dataObj)
            wx.TheClipboard.Close()
        print(txt)

    def AppendItem(self, parent, text, image=-1, wnd=None):
        if USE_CUSTOMTREECTRL:
            item = TreeBaseClass.AppendItem(self, parent, text, image=image, wnd=wnd)
        else:
            item = TreeBaseClass.AppendItem(self, parent, text, image=image)
        return item

    def BuildTreeImageList(self):
        imgList = wx.ImageList(16, 16)
        for png in _demoPngs:
            imgList.Add(images.catalog[png].GetBitmap())

        # add the image for modified demos.
        imgList.Add(images.catalog["custom"].GetBitmap())

        self.AssignImageList(imgList)


    def GetItemIdentity(self, item):
        return self.GetItemData(item)
        
        
        