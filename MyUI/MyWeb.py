# coding:utf-8

import wx
from Utils import gl, new_wordcloud
import  cStringIO
import os


__author__ = 'Tacey Wong'
__date__   = "2016年元月"


###########################################################################
## Web文本抽取生成词云
###########################################################################

class MyWeb(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
                          style=wx.TAB_TRAVERSAL)

        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK))
        self.stop_word_file =None
        self.goal_file = None
        self.final_pic = None
        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        sbSizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"词云配置"), wx.HORIZONTAL)

        sbSizer4 = wx.StaticBoxSizer(wx.StaticBox(sbSizer1.GetStaticBox(), wx.ID_ANY, u"目标文件"), wx.VERTICAL)

        fgSizer4 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer4.SetFlexibleDirection(wx.BOTH)
        fgSizer4.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.StopWords_Button = wx.Button(sbSizer4.GetStaticBox(), wx.ID_ANY, u"打开停词表", wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        fgSizer4.Add(self.StopWords_Button, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        self.StopWords_staticText = wx.StaticText(sbSizer4.GetStaticBox(), wx.ID_ANY, u"当前：无", wx.DefaultPosition,
                                                  wx.DefaultSize, 0)
        self.StopWords_staticText.Wrap(-1)
        self.StopWords_staticText.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        fgSizer4.Add(self.StopWords_staticText, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.GoalFile_Button = wx.Button(sbSizer4.GetStaticBox(), wx.ID_ANY, u"打开Web文件", wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        fgSizer4.Add(self.GoalFile_Button, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        self.GoalFile_staticText = wx.StaticText(sbSizer4.GetStaticBox(), wx.ID_ANY, u"当前：无", wx.DefaultPosition,
                                                 wx.DefaultSize, 0)
        self.GoalFile_staticText.Wrap(-1)
        self.GoalFile_staticText.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))

        fgSizer4.Add(self.GoalFile_staticText, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        sbSizer4.Add(fgSizer4, 1, wx.EXPAND, 5)

        sbSizer1.Add(sbSizer4, 1, wx.EXPAND, 5)

        sbSizer5 = wx.StaticBoxSizer(wx.StaticBox(sbSizer1.GetStaticBox(), wx.ID_ANY, u"尺寸设置"), wx.VERTICAL)

        fgSizer2 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer2.SetFlexibleDirection(wx.BOTH)
        fgSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.Margin_staticText = wx.StaticText(sbSizer5.GetStaticBox(), wx.ID_ANY, u"边距", wx.DefaultPosition,
                                               wx.DefaultSize, 0)
        self.Margin_staticText.Wrap(-1)
        fgSizer2.Add(self.Margin_staticText, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.Margin_spinCtrl = wx.SpinCtrl(sbSizer5.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                           wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 50, 0)
        fgSizer2.Add(self.Margin_spinCtrl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.Width_staticText = wx.StaticText(sbSizer5.GetStaticBox(), wx.ID_ANY, u"宽度", wx.DefaultPosition,
                                              wx.DefaultSize, 0)
        self.Width_staticText.Wrap(-1)
        fgSizer2.Add(self.Width_staticText, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.Width_spinCtrl = wx.SpinCtrl(sbSizer5.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                          wx.DefaultSize, wx.SP_ARROW_KEYS, 100, 10000, 800)
        fgSizer2.Add(self.Width_spinCtrl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.Height_staticText = wx.StaticText(sbSizer5.GetStaticBox(), wx.ID_ANY, u"高度", wx.DefaultPosition,
                                               wx.DefaultSize, 0)
        self.Height_staticText.Wrap(-1)
        fgSizer2.Add(self.Height_staticText, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.Height_spinCtrl = wx.SpinCtrl(sbSizer5.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                           wx.DefaultSize, wx.SP_ARROW_KEYS, 80, 10000, 600)
        fgSizer2.Add(self.Height_spinCtrl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        sbSizer5.Add(fgSizer2, 1, wx.EXPAND, 5)

        sbSizer1.Add(sbSizer5, 1, wx.EXPAND, 5)

        sbSizer6 = wx.StaticBoxSizer(wx.StaticBox(sbSizer1.GetStaticBox(), wx.ID_ANY, u"字体设置"), wx.VERTICAL)

        fgSizer3 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer3.SetFlexibleDirection(wx.BOTH)
        fgSizer3.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.Font_staticText = wx.StaticText(sbSizer6.GetStaticBox(), wx.ID_ANY, u"选择字体", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        self.Font_staticText.Wrap(-1)
        fgSizer3.Add(self.Font_staticText, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)

        Font_ChoiceChoices = []
        self.Font_Choice = wx.Choice(sbSizer6.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                   Font_ChoiceChoices, 0)
        self.update_Choice()
        fgSizer3.Add(self.Font_Choice, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.MaxFont_staticText = wx.StaticText(sbSizer6.GetStaticBox(), wx.ID_ANY, u"最大字体", wx.DefaultPosition,
                                                wx.DefaultSize, 0)
        self.MaxFont_staticText.Wrap(-1)
        fgSizer3.Add(self.MaxFont_staticText, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)

        self.MaxFont_spinCtrl = wx.SpinCtrl(sbSizer6.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                            wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 40, 10)
        fgSizer3.Add(self.MaxFont_spinCtrl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.MinFont_staticText = wx.StaticText(sbSizer6.GetStaticBox(), wx.ID_ANY, u"最小字体", wx.DefaultPosition,
                                                wx.DefaultSize, 0)
        self.MinFont_staticText.Wrap(-1)
        fgSizer3.Add(self.MinFont_staticText, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)

        self.MinFont_spinCtrl = wx.SpinCtrl(sbSizer6.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                            wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 40, 5)
        fgSizer3.Add(self.MinFont_spinCtrl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        sbSizer6.Add(fgSizer3, 1, wx.EXPAND, 5)

        sbSizer1.Add(sbSizer6, 1, wx.EXPAND, 5)

        sbSizer7 = wx.StaticBoxSizer(wx.StaticBox(sbSizer1.GetStaticBox(), wx.ID_ANY, u"颜色设置"), wx.VERTICAL)

        self.BG_Color_staticText = wx.StaticText(sbSizer7.GetStaticBox(), wx.ID_ANY, u"选择背景颜色", wx.DefaultPosition,
                                                 wx.DefaultSize, 0)
        self.BG_Color_staticText.Wrap(-1)
        sbSizer7.Add(self.BG_Color_staticText, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.BG_Color_colourPicker = wx.ColourPickerCtrl(sbSizer7.GetStaticBox(), wx.ID_ANY, wx.BLACK,
                                                         wx.DefaultPosition,
                                                         wx.DefaultSize, wx.CLRP_DEFAULT_STYLE)
        sbSizer7.Add(self.BG_Color_colourPicker, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        sbSizer1.Add(sbSizer7, 1, wx.EXPAND, 5)

        bSizer1.Add(sbSizer1, 1, wx.EXPAND, 5)

        sbSizer3 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, u"词云生成"), wx.VERTICAL)

        fgSizer1 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.GenWordCloud_Button = wx.Button(sbSizer3.GetStaticBox(), wx.ID_ANY, u"词云生成", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        bSizer2.Add(self.GenWordCloud_Button, 0, wx.ALL, 5)

        self.Save_Button = wx.Button(sbSizer3.GetStaticBox(), wx.ID_ANY, u"保存词云", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.Save_Button, 0, wx.ALL, 5)

        fgSizer1.Add(bSizer2, 1, wx.EXPAND, 5)

        sbSizer9 = wx.StaticBoxSizer(wx.StaticBox(sbSizer3.GetStaticBox(), wx.ID_ANY, u"词云预览"), wx.VERTICAL)

        self.PicShow_Bitmap = wx.StaticBitmap(sbSizer9.GetStaticBox(), wx.ID_ANY,
                                              wx.Bitmap(u"C:\\Users\\Administrator\\Desktop\\论文资料\\test.png",
                                                        wx.BITMAP_TYPE_ANY), wx.DefaultPosition, wx.DefaultSize, 0)
        sbSizer9.Add(self.PicShow_Bitmap, 1, wx.ALL | wx.EXPAND, 5)

        fgSizer1.Add(sbSizer9, 1, wx.EXPAND, 5)

        sbSizer3.Add(fgSizer1, 1, wx.EXPAND, 5)

        bSizer1.Add(sbSizer3, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        # Connect Events
        self.StopWords_Button.Bind(wx.EVT_BUTTON, self.StopWords_ButtonOnButtonClick)
        self.GoalFile_Button.Bind(wx.EVT_BUTTON, self.GoalFile_ButtonOnButtonClick)
        self.GenWordCloud_Button.Bind(wx.EVT_BUTTON, self.GenWordCloud_ButtonOnButtonClick)
        self.Save_Button.Bind(wx.EVT_BUTTON, self.Save_ButtonOnButtonClick)

    def __del__(self):
        pass


    # Virtual event handlers, overide them in your derived class
    def StopWords_ButtonOnButtonClick(self, event):
        event.Skip()
        wildcard = u"TXT纯文本 (*.txt)|*.txt"

        dlg = wx.FileDialog(
            self, message=u"选取停词表文档",
            defaultDir=gl.CWD+u"\\data\\stopwords",
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.CHANGE_DIR  # | wx.MULTIPLE
        )

        # Show the dialog and retrieve the user response. If it is the OK response,
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            path = dlg.GetPath()  # GetPaths()
            self.stop_word_file = path
            self.StopWords_staticText.SetLabelText(path.split("\\")[-1])
        dlg.Destroy()


    def GoalFile_ButtonOnButtonClick(self, event):
        event.Skip()
        wildcard = u"HTML文本 (*.html)|*.html"

        dlg = wx.FileDialog(
            self, message=u"选取词云生成目标文档",
            defaultDir=gl.CWD,
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.CHANGE_DIR  # | wx.MULTIPLE
        )

        # Show the dialog and retrieve the user response. If it is the OK response,
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            path = dlg.GetPath()  # GetPaths()
            self.goal_file = path
            self.GoalFile_staticText.SetLabelText(path.split("\\")[-1])

        #
        dlg.Destroy()


    def GenWordCloud_ButtonOnButtonClick(self, event):
        event.Skip()
        stop_word_file, goal_file, margin, width, height, font, font_max, font_min, bg_color = self.GetConf()
        print stop_word_file, goal_file, margin, width, height, font, font_max, font_min, bg_color

        if stop_word_file == None or goal_file == None :
            dlg = wx.MessageDialog(self,u"请先选取停词表和目标文档",
                                u"文件缺失",
                               wx.OK | wx.ICON_INFORMATION#wx.ICON_ERROR
                               #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                               )
            dlg.ShowModal()
            dlg.Destroy()
            return 1
        wc = new_wordcloud.MyWordCloud()
        from Utils import cleaner
        html_text = cleaner.clean_html(open(goal_file).read())
        output_file_name = gl.CWD+"\\data\\.catch\\tmp_file.txt"
        goal_file = output_file_name
        output_file_id = open(output_file_name,'w')
        try:
            output_file_id.write(html_text.strip())
        except Exception,e:
            print e
        output_file_id.close()
        stop_word_file = output_file_name
        stopwords = wc.StopWord(filename=stop_word_file)
        seg_list = wc.WordCut(stopwords, goal_file)
        self.final_pic = wc.GenWordCloud(
                                      seg_list=seg_list,
                                      font_path=gl.CWD+u"//data//font//"+font+".ttf",
                                      background_color=bg_color,
                                      margin=margin,
                                      width=width, height=height)

        self.final_pic.to_file(gl.CWD+"\\data\\.catch\\"+"book_to_file.png")
        try:

            imageFile = gl.CWD+"\\data\\.catch\\"+'book_to_file.png'
            data = open(imageFile, "rb").read()
            # convert to a data stream
            stream = cStringIO.StringIO(data)
            # convert to a bitmap
            bmp = wx.BitmapFromImage(wx.ImageFromStream(stream))
            # show the bitmap, (5, 5) are upper left corner coordinates
            # wx.StaticBitmap(self, -1, bmp, (5, 5))

            # alternate (simpler) way to load and display a jpg image from a file
            # actually you can load .jpg  .png  .bmp  or .gif files
            # jpg1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            # bitmap upper left corner is in the position tuple (x, y) = (5, 5)
            self.PicShow_Bitmap.SetBitmap(bmp)
            # self.PicShow_Bitmap(self, -1, bmp, (10 + bmp.GetWidth(), 5), (bmp.GetWidth(), bmp.GetHeight()))
        except IOError:
            print "Image file %s not found" % imageFile
            raise SystemExit

        # self.PicShow_Bitmap.SetBitmap()

        dlg = wx.MessageDialog(self, u'生成成功！',
                               u'处理结果!',
                               wx.OK | wx.ICON_INFORMATION  # wx.ICON_ERROR
                               # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
        )
        dlg.ShowModal()
        dlg.Destroy()

    def Save_ButtonOnButtonClick(self, event):
        event.Skip()
        if self.final_pic == None:
            dlg = wx.MessageDialog(self, u'您尚未生成词云！',
                               u'错误信息!',
                               wx.OK | wx.ICON_INFORMATION  # wx.ICON_ERROR
                               # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                )
            dlg.ShowModal()
            dlg.Destroy()
            return 1
        dlg = wx.FileDialog(
            self, message=u"保存单词云，请选择合适的格式", defaultDir=gl.CWD,
            defaultFile=u"MyWordCloud", wildcard=u"PNG图片 (*.png)|*.png", style=wx.SAVE
        )

        # dlg.SetFilterIndex(2)

        # Show the dialog and retrieve the user response. If it is the OK response,
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.final_pic.to_file(path)
        else:
            return 0

        #
        dlg.Destroy()
        dlg = wx.MessageDialog(self, u'保存完成！',
                               u'处理结果!',
                               wx.OK | wx.ICON_INFORMATION  # wx.ICON_ERROR
                               # wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
        )
        dlg.ShowModal()
        dlg.Destroy()

    def GetConf(self):
        pass
        stop_word_file = self.stop_word_file
        goal_file = self.goal_file
        margin = self.Margin_spinCtrl.GetValue()
        width = self.Width_spinCtrl.GetValue()
        height = self.Height_spinCtrl.GetValue()
        # font = self.Font_fontPicker.GetSelectedFont()
        font = self.Font_Choice.GetString(self.Font_Choice.GetCurrentSelection())
        print "font:",str(font)
        font_max = self.MaxFont_spinCtrl.GetValue()
        font_min = self.MinFont_spinCtrl.GetValue()
        bg_color = tuple(self.BG_Color_colourPicker.GetColour())
        return stop_word_file, goal_file, margin, width, height, font, font_max, font_min, bg_color
    def update_Choice(self):
        pass

        folder_list = os.listdir(gl.CWD+"\\data\\font\\")
        font_Choices=[]
        for i in folder_list:
            if i.endswith(".ttf"):
                font_Choices.append(i[:-4])
        self.Font_Choice.Clear()

        self.Font_Choice.AppendItems([i for i in font_Choices])
        self.Font_Choice.SetSelection(0)
        print "font update"
        return font_Choices
