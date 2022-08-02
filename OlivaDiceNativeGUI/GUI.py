# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   GUI.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import OlivaDiceNativeGUI
import OlivaDiceCore

import base64
import os
import tkinter
from tkinter import ttk
import webbrowser

from PIL import Image
from PIL import ImageTk

dictColorContext = {
    'color_001': '#00A0EA',
    'color_002': '#BBE9FF',
    'color_003': '#40C3FF',
    'color_004': '#FFFFFF',
    'color_005': '#000000',
    'color_006': '#80D7FF'
}

def releaseBase64Data(dir_path, file_name, base64_data):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path) 
    with open(dir_path + '/' + file_name, 'wb+') as tmp:
        tmp.write(base64.b64decode(base64_data))

def get_tree_force(tree_obj):
    return tree_obj.item(tree_obj.focus())

class ConfigUI(object):
    def __init__(self, Model_name, logger_proc = None):
        self.Model_name = Model_name
        self.UIObject = {}
        self.UIData = {}
        self.UIConfig = {}
        self.logger_proc = logger_proc
        self.UIData['flag_open'] = False
        self.UIData['click_record'] = {}
        self.UIConfig.update(dictColorContext)

    def start(self):
        self.UIObject['root'] = tkinter.Tk()
        self.UIObject['root'].title('OlivaDice 设置面板')
        self.UIObject['root'].geometry('800x600')
        self.UIObject['root'].minsize(800, 600)
        self.UIObject['root'].resizable(
            width = True,
            height = True
        )
        self.UIObject['root'].grid_rowconfigure(0, weight = 0)
        self.UIObject['root'].grid_rowconfigure(1, weight = 15)
        self.UIObject['root'].grid_columnconfigure(0, weight = 15)
        self.UIObject['root'].configure(bg = self.UIConfig['color_001'])

        self.UIData['hash_now'] = 'unity'

        self.init_hash_Combobox()

        self.init_notebook()

        # 主页
        self.init_frame_main()

        # 回复词
        self.init_frame_str()

        # 配置项
        self.init_frame_console()

        # 骰主列表
        # 还没写
        self.init_frame_master()

        self.UIObject['Notebook_root'].add(self.UIObject['frame_main_root'], text="首页")
        self.UIObject['Notebook_root'].add(self.UIObject['frame_str_root'], text="回复词")
        self.UIObject['Notebook_root'].add(self.UIObject['frame_console_root'], text="配置项")
        self.UIObject['Notebook_root'].add(self.UIObject['frame_master_root'], text="骰主列表")

        self.init_data_total()

        self.UIObject['root'].iconbitmap('./resource/tmp_favoricon.ico')
        self.UIObject['root'].mainloop()
        OlivaDiceNativeGUI.load.flag_open = False

    def init_hash_Combobox(self):
        self.UIData['hash_Combobox_root_StringVar'] = tkinter.StringVar()
        self.UIObject['hash_Combobox_root'] = ttk.Combobox(
            self.UIObject['root'],
            textvariable = self.UIData['hash_Combobox_root_StringVar']
        )
        self.UIObject['hash_Combobox_root'].grid(
            row = 0,
            column = 0,
            sticky = "nsw",
            rowspan = 1,
            columnspan = 1,
            padx = (15, 0),
            pady = (15, 0),
            ipadx = 0,
            ipady = 0
        )
        self.UIObject['hash_Combobox_root'].configure(state='readonly')
        #self.UIObject['hash_Combobox_root'].bind('<<ComboboxSelected>>', lambda x : self.tree_edit_UI_Combobox_ComboboxSelected(x, action, obj_name))
        self.UIData['hash_default'] = 'unity'
        self.UIData['hash_default_key'] = '全局 (不推荐)'
        self.UIData['hash_find'] = {
            self.UIData['hash_default_key']: self.UIData['hash_default']
        }
        self.UIData['hash_list'] = [self.UIData['hash_default_key']]
        for hash_this in OlivaDiceNativeGUI.load.dictBotInfo:
            key_info = '%s | %s' % (
                OlivaDiceNativeGUI.load.dictBotInfo[hash_this].platform['platform'],
                OlivaDiceNativeGUI.load.dictBotInfo[hash_this].id
            )
            self.UIData['hash_list'].append(key_info)
            self.UIData['hash_find'][key_info] = hash_this
            if self.UIData['hash_default'] == 'unity':
                self.UIData['hash_default_key'] = key_info
                self.UIData['hash_default'] = hash_this
        self.UIData['hash_now'] = self.UIData['hash_default']
        self.UIObject['hash_Combobox_root']['value'] = tuple(self.UIData['hash_list'])
        self.UIObject['hash_Combobox_root'].current(
            self.UIData['hash_list'].index(
                self.UIData['hash_default_key']
            )
        )
        self.UIObject['hash_Combobox_root'].bind('<<ComboboxSelected>>', lambda x : self.Combobox_ComboboxSelected(x, 'set', 'hash_Combobox_root'))

    def Combobox_ComboboxSelected(self, action, event, target):
        if target == 'hash_Combobox_root':
            self.UIData['hash_now'] = self.UIData['hash_find'][self.UIData['hash_Combobox_root_StringVar'].get()]
            self.init_data_total()

    def init_notebook(self):
        self.UIData['style'] = ttk.Style()
        self.UIData['style'].element_create('Plain.Notebook.tab', "from", 'default')
        self.UIData['style'].layout(
            "TNotebook.Tab",
            [('Plain.Notebook.tab', {'children':
                [('Notebook.padding', {'side': 'top', 'children':
                    [('Notebook.focus', {'side': 'top', 'children':
                        [('Notebook.label', {'side': 'top', 'sticky': ''})],
                    'sticky': 'nswe'})],
                'sticky': 'nswe'})],
            'sticky': 'nswe'})])
        self.UIData['style'].configure(
            "TNotebook",
            background = self.UIConfig['color_001'],
            borderwidth = 0,
            relief = tkinter.FLAT,
            padding = [-1, 1, -3, -3],
            tabmargins = [5, 5, 0, 0]
        )
        self.UIData['style'].configure(
            "TNotebook.Tab",
            background = self.UIConfig['color_006'],
            foreground = self.UIConfig['color_001'],
            padding = 4,
            borderwidth = 0,
            font = ('等线', 12, 'bold')
        )
        self.UIData['style'].map(
            "TNotebook.Tab",
            background = [
                ('selected', self.UIConfig['color_004']),
                ('!selected', self.UIConfig['color_003'])
            ],
            foreground = [
                ('selected', self.UIConfig['color_003']),
                ('!selected', self.UIConfig['color_004'])
            ]
        )

        self.UIObject['Notebook_root'] = ttk.Notebook(self.UIObject['root'], style = 'TNotebook')
        self.UIObject['Notebook_root'].grid(
            row = 1,
            column = 0,
            sticky = "nsew",
            rowspan = 1,
            columnspan = 1,
            padx = (15, 15),
            pady = (8, 15),
            ipadx = 0,
            ipady = 0
        )
        self.UIObject['Notebook_root'].grid_rowconfigure(0, weight = 0)
        self.UIObject['Notebook_root'].grid_rowconfigure(1, weight = 15)
        self.UIObject['Notebook_root'].grid_columnconfigure(0, weight = 15)

    def init_frame_main(self):
        self.UIObject['frame_main_root'] = tkinter.Frame(self.UIObject['Notebook_root'])
        self.UIObject['frame_main_root'].configure(relief = tkinter.FLAT)
        self.UIObject['frame_main_root'].grid(
            row = 1,
            column = 0,
            sticky = "nsew",
            rowspan = 1,
            columnspan = 1,
            padx = (0, 0),
            pady = (0, 0),
            ipadx = 0,
            ipady = 0
        )
        self.UIObject['frame_main_root'].grid_rowconfigure(0, weight = 0)
        self.UIObject['frame_main_root'].grid_rowconfigure(1, weight = 0)
        self.UIObject['frame_main_root'].grid_rowconfigure(2, weight = 0)
        self.UIObject['frame_main_root'].grid_rowconfigure(3, weight = 15)
        self.UIObject['frame_main_root'].grid_rowconfigure(4, weight = 0)
        self.UIObject['frame_main_root'].grid_columnconfigure(0, weight = 15)
        self.UIObject['frame_main_root'].grid_columnconfigure(1, weight = 15)
        self.UIObject['frame_main_root'].grid_columnconfigure(2, weight = 15)
        self.UIObject['frame_main_root'].grid_columnconfigure(3, weight = 15)
        self.UIObject['frame_main_root'].grid_columnconfigure(4, weight = 15)
        self.UIObject['frame_main_root'].grid_columnconfigure(5, weight = 15)
        self.UIObject['frame_main_root'].grid_columnconfigure(6, weight = 15)
        self.UIObject['frame_main_root'].grid_columnconfigure(7, weight = 15)
        self.UIObject['frame_main_root'].grid_columnconfigure(8, weight = 15)
        self.UIObject['frame_main_root'].configure(bg = self.UIConfig['color_001'], borderwidth = 0)

        self.UIObject['label_master_token'] = tkinter.Label(
            self.UIObject['frame_main_root'],
            text = '点击以下按钮复制指令，并在聊天窗口中发送给骰子，即可成为骰主！'
        )
        self.UIObject['label_master_token'].configure(
            bg = self.UIConfig['color_001'],
            fg = self.UIConfig['color_004'],
            font = ('等线', 18, 'bold')
        )
        self.UIObject['label_master_token'].grid(
            row = 0,
            column = 0,
            sticky = "nwe",
            rowspan = 1,
            columnspan = 9,
            padx = (0, 0),
            pady = (15, 0),
            ipadx = 0,
            ipady = 0
        )

        self.UIData['buttom_master_token_copy_StringVar'] = tkinter.StringVar()
        self.process_msg()
        self.UIObject['buttom_master_token_copy'] = tkinter.Button(
            self.UIObject['frame_main_root'],
            textvariable = self.UIData['buttom_master_token_copy_StringVar'],
            command = lambda : self.master_token_copy_action(),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            font = ('等线', 16, 'bold')
        )
        self.UIObject['buttom_master_token_copy'].bind('<Enter>', lambda x : self.buttom_action('buttom_master_token_copy', '<Enter>'))
        self.UIObject['buttom_master_token_copy'].bind('<Leave>', lambda x : self.buttom_action('buttom_master_token_copy', '<Leave>'))
        self.UIObject['buttom_master_token_copy'].grid(
            row = 1,
            column = 0,
            sticky = "nwe",
            rowspan = 1,
            columnspan = 9,
            padx = (60, 60),
            pady = (15, 8),
            ipadx = 0,
            ipady = 0
        )

        releaseBase64Data('./resource', 'tmp_icon.png', OlivaDiceNativeGUI.imageData.icon)
        self.UIObject['icon_img_data'] = Image.open('./resource/tmp_icon.png')
        self.UIObject['icon_img_data'] = self.UIObject['icon_img_data'].resize((192 * 2, 108 * 2), Image.ANTIALIAS)
        self.UIObject['icon_img'] = ImageTk.PhotoImage(self.UIObject['icon_img_data'])
        self.UIObject['icon_label'] = tkinter.Label(self.UIObject['frame_main_root'])
        self.UIObject['icon_label'].config(image = self.UIObject['icon_img'])
        self.UIObject['icon_label'].image = self.UIObject['icon_img']
        self.UIObject['icon_label'].configure(
            bg = self.UIConfig['color_001']
        )
        self.UIObject['icon_label'].grid(
            row = 2,
            column = 0,
            sticky = "nwe",
            rowspan = 1,
            columnspan = 9,
            padx = (15, 15),
            pady = (0, 0),
            ipadx = 0,
            ipady = 0
        )

        self.UIObject['label_bot_info'] = tkinter.Label(
            self.UIObject['frame_main_root'],
            text = '\n'.join(
                [
                    OlivaDiceCore.data.bot_info,
                    '',
                    '世界是属于每一个人的。要创造一个充满逻辑并尊重每一个人的世界。',
                    '                                        ——《Новый Элемент Расселения》A.D.1960 Москва'
                ]
            )
        )
        self.UIObject['label_bot_info'].configure(
            bg = self.UIConfig['color_001'],
            fg = self.UIConfig['color_004'],
            font = ('等线', 14, 'bold')
        )
        self.UIObject['label_bot_info'].grid(
            row = 3,
            column = 0,
            sticky = "nwe",
            rowspan = 1,
            columnspan = 9,
            padx = (0, 0),
            pady = (15, 0),
            ipadx = 0,
            ipady = 0
        )

        self.UIObject['buttom_share_1'] = tkinter.Button(
            self.UIObject['frame_main_root'],
            text = '论坛地址',
            command = lambda : self.show_project_site('https://forum.olivos.run/'),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
            width = 12
        )
        self.UIObject['buttom_share_1'].bind('<Enter>', lambda x : self.buttom_action('buttom_share_1', '<Enter>'))
        self.UIObject['buttom_share_1'].bind('<Leave>', lambda x : self.buttom_action('buttom_share_1', '<Leave>'))
        self.UIObject['buttom_share_1'].grid(
            row = 4,
            column = 0,
            sticky = "nwe",
            rowspan = 1,
            columnspan = 2,
            padx = (15, 0),
            pady = (15, 0),
            ipadx = 0,
            ipady = 0
        )

        self.UIObject['buttom_share_2'] = tkinter.Button(
            self.UIObject['frame_main_root'],
            text = '使用手册',
            command = lambda : self.show_project_site('https://wiki.dice.center/'),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
            width = 12
        )
        self.UIObject['buttom_share_2'].bind('<Enter>', lambda x : self.buttom_action('buttom_share_2', '<Enter>'))
        self.UIObject['buttom_share_2'].bind('<Leave>', lambda x : self.buttom_action('buttom_share_2', '<Leave>'))
        self.UIObject['buttom_share_2'].grid(
            row = 4,
            column = 2,
            sticky = "nwe",
            rowspan = 1,
            columnspan = 2,
            padx = (15, 0),
            pady = (15, 0),
            ipadx = 0,
            ipady = 0
        )

        self.UIObject['buttom_share_3'] = tkinter.Button(
            self.UIObject['frame_main_root'],
            text = '项目源码',
            command = lambda : self.show_project_site('https://github.com/OlivOS-Team/OlivaDiceCore'),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
            width = 12
        )
        self.UIObject['buttom_share_3'].bind('<Enter>', lambda x : self.buttom_action('buttom_share_3', '<Enter>'))
        self.UIObject['buttom_share_3'].bind('<Leave>', lambda x : self.buttom_action('buttom_share_3', '<Leave>'))
        self.UIObject['buttom_share_3'].grid(
            row = 4,
            column = 5,
            sticky = "nwe",
            rowspan = 1,
            columnspan = 2,
            padx = (15, 0),
            pady = (15, 0),
            ipadx = 0,
            ipady = 0
        )

        self.UIObject['buttom_share_4'] = tkinter.Button(
            self.UIObject['frame_main_root'],
            text = '赞助项目',
            command = lambda : self.show_project_site('https://afdian.net/@OlivOS'),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
            width = 12
        )
        self.UIObject['buttom_share_4'].bind('<Enter>', lambda x : self.buttom_action('buttom_share_4', '<Enter>'))
        self.UIObject['buttom_share_4'].bind('<Leave>', lambda x : self.buttom_action('buttom_share_4', '<Leave>'))
        self.UIObject['buttom_share_4'].grid(
            row = 4,
            column = 7,
            sticky = "nwe",
            rowspan = 1,
            columnspan = 2,
            padx = (15, 0),
            pady = (15, 0),
            ipadx = 0,
            ipady = 0
        )

    def master_token_copy_action(self):
        self.UIObject['root'].clipboard_clear()
        self.UIObject['root'].clipboard_append(self.UIData['buttom_master_token_copy_StringVar'].get())
        self.UIObject['root'].update()
        tkinter.messagebox.showinfo('已完成复制', '在聊天窗口中发送给骰子，即可成为骰主！')

    def process_msg(self):
        self.UIObject['root'].after(1000,self.process_msg)
        self.UIData['buttom_master_token_copy_StringVar'].set('.master %s' % OlivaDiceCore.data.bot_content['masterKey'])

    def show_project_site(self, url):
        tkinter.messagebox.showinfo("提示", "将通过浏览器访问 " + url)
        try:
            webbrowser.open(url)
        except webbrowser.Error as error_info:
            tkinter.messagebox.showerror("webbrowser.Error", error_info)

    def buttom_action(self, name, action):
        if name in self.UIObject:
            if action == '<Enter>':
                self.UIObject[name].configure(bg = self.UIConfig['color_006'])
            if action == '<Leave>':
                self.UIObject[name].configure(bg = self.UIConfig['color_003'])

    def init_frame_str(self):
        self.UIObject['frame_str_root'] = tkinter.Frame(self.UIObject['Notebook_root'])
        self.UIObject['frame_str_root'].configure(relief = tkinter.FLAT)
        self.UIObject['frame_str_root'].grid(
            row = 1,
            column = 0,
            sticky = "nsew",
            rowspan = 1,
            columnspan = 1,
            padx = (0, 0),
            pady = (0, 0),
            ipadx = 0,
            ipady = 0
        )
        self.UIObject['frame_str_root'].grid_rowconfigure(0, weight = 0)
        self.UIObject['frame_str_root'].grid_rowconfigure(1, weight = 15)
        self.UIObject['frame_str_root'].grid_columnconfigure(0, weight = 15)
        self.UIObject['frame_str_root'].grid_columnconfigure(1, weight = 0)
        self.UIObject['frame_str_root'].configure(bg = self.UIConfig['color_001'], borderwidth = 0)

        self.UIObject['tree_str'] = ttk.Treeview(self.UIObject['frame_str_root'])
        self.UIObject['tree_str']['show'] = 'headings'
        self.UIObject['tree_str']['columns'] = ('KEY', 'NOTE', 'DATA')
        self.UIObject['tree_str'].column('KEY', width = 140)
        self.UIObject['tree_str'].column('NOTE', width = 275)
        self.UIObject['tree_str'].column('DATA', width = 275)
        self.UIObject['tree_str'].heading('KEY', text = '条目')
        self.UIObject['tree_str'].heading('NOTE', text = '说明')
        self.UIObject['tree_str'].heading('DATA', text = '内容')
        self.UIObject['tree_str'].grid(
            row = 1,
            column = 0,
            sticky = "nsew",
            rowspan = 1,
            columnspan = 1,
            padx = (0, 0),
            pady = (0, 0),
            ipadx = 0,
            ipady = 0
        )
        self.UIObject['tree_rightkey_menu'] = tkinter.Menu(self.UIObject['root'], tearoff = False)
        self.UIObject['tree_str'].bind('<Button-3>', lambda x : self.tree_str_rightKey(x))
        self.UIObject['tree_str_yscroll'] = ttk.Scrollbar(
            self.UIObject['frame_str_root'],
            orient = "vertical",
            command = self.UIObject['tree_str'].yview
        )
        self.UIObject['tree_str'].configure(
            yscrollcommand = self.UIObject['tree_str_yscroll'].set
        )
        self.UIObject['tree_str_yscroll'].grid(
            row = 1,
            column = 1,
            sticky = "nsw",
            rowspan = 1,
            columnspan = 1,
            padx = (0, 0),
            pady = (0, 0),
            ipadx = 0,
            ipady = 0
        )

        self.UIObject['buttom_edit'] = tkinter.Button(
            self.UIObject['frame_str_root'],
            text = '编辑',
            command = lambda : self.tree_str_edit(),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
            width = 12
        )
        self.UIObject['buttom_edit'].bind('<Enter>', lambda x : self.buttom_action('buttom_edit', '<Enter>'))
        self.UIObject['buttom_edit'].bind('<Leave>', lambda x : self.buttom_action('buttom_edit', '<Leave>'))
        self.UIObject['buttom_edit'].grid(
            row = 2,
            column = 0,
            sticky = "ne",
            rowspan = 1,
            columnspan = 2,
            padx = (15, 0),
            pady = (8, 0),
            ipadx = 0,
            ipady = 0
        )

    def init_frame_console(self):
        self.UIObject['frame_console_root'] = tkinter.Frame(self.UIObject['Notebook_root'])
        self.UIObject['frame_console_root'].configure(relief = tkinter.FLAT)
        self.UIObject['frame_console_root'].grid(
            row = 1,
            column = 0,
            sticky = "nsew",
            rowspan = 1,
            columnspan = 1,
            padx = (0, 0),
            pady = (0, 0),
            ipadx = 0,
            ipady = 0
        )
        self.UIObject['frame_console_root'].grid_rowconfigure(0, weight = 0)
        self.UIObject['frame_console_root'].grid_rowconfigure(1, weight = 15)
        self.UIObject['frame_console_root'].grid_rowconfigure(2, weight = 0)
        self.UIObject['frame_console_root'].grid_columnconfigure(0, weight = 15)
        self.UIObject['frame_console_root'].configure(bg = self.UIConfig['color_001'], borderwidth = 0)

        self.UIObject['tree_console'] = ttk.Treeview(self.UIObject['frame_console_root'])
        self.UIObject['tree_console']['show'] = 'headings'
        self.UIObject['tree_console']['columns'] = ('KEY', 'NOTE', 'DATA')
        self.UIObject['tree_console'].column('KEY', width = 140)
        self.UIObject['tree_console'].column('NOTE', width = 500)
        self.UIObject['tree_console'].column('DATA', width = 50)
        self.UIObject['tree_console'].heading('KEY', text = '条目')
        self.UIObject['tree_console'].heading('NOTE', text = '说明')
        self.UIObject['tree_console'].heading('DATA', text = '内容')
        self.UIObject['tree_console'].grid(
            row = 1,
            column = 0,
            sticky = "nsew",
            rowspan = 1,
            columnspan = 1,
            padx = (0, 0),
            pady = (0, 0),
            ipadx = 0,
            ipady = 0
        )
        self.UIObject['tree_rightkey_menu'] = tkinter.Menu(self.UIObject['root'], tearoff = False)
        self.UIObject['tree_console'].bind('<Button-3>', lambda x : self.tree_console_rightKey(x))
        self.UIObject['tree_console_yscroll'] = ttk.Scrollbar(
            self.UIObject['frame_console_root'],
            orient = "vertical",
            command = self.UIObject['tree_console'].yview
        )
        self.UIObject['tree_console'].configure(
            yscrollcommand = self.UIObject['tree_console_yscroll'].set
        )
        self.UIObject['tree_console_yscroll'].grid(
            row = 1,
            column = 1,
            sticky = "nsw",
            rowspan = 1,
            columnspan = 1,
            padx = (0, 0),
            pady = (0, 0),
            ipadx = 0,
            ipady = 0
        )

        self.UIObject['buttom_edit'] = tkinter.Button(
            self.UIObject['frame_console_root'],
            text = '编辑',
            command = lambda : self.tree_console_edit(),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
            width = 12
        )
        self.UIObject['buttom_edit'].bind('<Enter>', lambda x : self.buttom_action('buttom_edit', '<Enter>'))
        self.UIObject['buttom_edit'].bind('<Leave>', lambda x : self.buttom_action('buttom_edit', '<Leave>'))
        self.UIObject['buttom_edit'].grid(
            row = 2,
            column = 0,
            sticky = "ne",
            rowspan = 1,
            columnspan = 2,
            padx = (15, 0),
            pady = (8, 0),
            ipadx = 0,
            ipady = 0
        )

    def init_frame_master(self):
        self.UIObject['frame_master_root'] = tkinter.Frame(self.UIObject['Notebook_root'])
        self.UIObject['frame_master_root'].configure(relief = tkinter.FLAT)
        self.UIObject['frame_master_root'].grid(
            row = 1,
            column = 0,
            sticky = "nsew",
            rowspan = 1,
            columnspan = 1,
            padx = (0, 0),
            pady = (0, 0),
            ipadx = 0,
            ipady = 0
        )
        self.UIObject['frame_master_root'].grid_rowconfigure(0, weight = 0)
        self.UIObject['frame_master_root'].grid_rowconfigure(1, weight = 0)
        self.UIObject['frame_master_root'].grid_rowconfigure(2, weight = 0)
        self.UIObject['frame_master_root'].grid_rowconfigure(3, weight = 15)
        self.UIObject['frame_master_root'].grid_columnconfigure(0, weight = 5)
        self.UIObject['frame_master_root'].grid_columnconfigure(1, weight = 5)
        self.UIObject['frame_master_root'].grid_columnconfigure(2, weight = 5)
        self.UIObject['frame_master_root'].grid_columnconfigure(3, weight = 5)
        self.UIObject['frame_master_root'].grid_columnconfigure(4, weight = 5)
        self.UIObject['frame_master_root'].grid_columnconfigure(5, weight = 0)
        self.UIObject['frame_master_root'].grid_columnconfigure(6, weight = 15)
        self.UIObject['frame_master_root'].grid_columnconfigure(7, weight = 0)
        self.UIObject['frame_master_root'].configure(bg = self.UIConfig['color_001'], borderwidth = 0)

        self.UIObject['tree_master'] = ttk.Treeview(self.UIObject['frame_master_root'])
        self.UIObject['tree_master']['show'] = 'headings'
        self.UIObject['tree_master']['columns'] = ('KEY', 'NAME')
        self.UIObject['tree_master'].column('KEY', width = 50)
        self.UIObject['tree_master'].column('NAME', width = 50)
        self.UIObject['tree_master'].heading('KEY', text = '账号')
        self.UIObject['tree_master'].heading('NAME', text = '昵称')
        self.UIObject['tree_master'].grid(
            row = 0,
            column = 6,
            sticky = "nsew",
            rowspan = 4,
            columnspan = 1,
            padx = (0, 0),
            pady = (0, 0),
            ipadx = 0,
            ipady = 0
        )
        self.UIObject['tree_rightkey_menu'] = tkinter.Menu(self.UIObject['root'], tearoff = False)
        #self.UIObject['tree_master'].bind('<Button-3>', lambda x : self.tree_master_rightKey(x))
        self.UIObject['tree_master'].bind('<<TreeviewSelect>>', lambda x : self.treeSelect('tree_master', x))
        self.UIObject['tree_master_yscroll'] = ttk.Scrollbar(
            self.UIObject['frame_master_root'],
            orient = "vertical",
            command = self.UIObject['tree_master'].yview
        )
        self.UIObject['tree_master'].configure(
            yscrollcommand = self.UIObject['tree_master_yscroll'].set
        )
        self.UIObject['tree_master_yscroll'].grid(
            row = 0,
            column = 7,
            sticky = "nsw",
            rowspan = 4,
            columnspan = 1,
            padx = (0, 0),
            pady = (0, 0),
            ipadx = 0,
            ipady = 0
        )

        self.UIData['entry_master_StringVar'] = tkinter.StringVar()
        self.UIObject['entry_master'] = tkinter.Entry(
            self.UIObject['frame_master_root'],
            textvariable = self.UIData['entry_master_StringVar']
        )
        self.UIObject['entry_master'].configure(
            bg = self.UIConfig['color_006'],
            fg = self.UIConfig['color_001'],
            font = ('等线', 12, 'bold'),
            bd = 0,
            justify = 'center'
        )
        self.UIObject['entry_master'].grid(
            row = 0,
            column = 1,
            sticky = "nwe",
            rowspan = 1,
            columnspan = 3,
            padx = (0, 0),
            pady = (180, 0),
            ipadx = 4,
            ipady = 8
        )

        self.UIObject['buttom_master_add'] = tkinter.Button(
            self.UIObject['frame_master_root'],
            text = '添加',
            command = lambda : self.tree_master_config('add'),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
        )
        self.UIObject['buttom_master_add'].bind('<Enter>', lambda x : self.buttom_action('buttom_master_add', '<Enter>'))
        self.UIObject['buttom_master_add'].bind('<Leave>', lambda x : self.buttom_action('buttom_master_add', '<Leave>'))
        self.UIObject['buttom_master_add'].grid(
            row = 1,
            column = 1,
            sticky = "new",
            rowspan = 1,
            columnspan = 1,
            padx = (0, 0),
            pady = (45, 0),
            ipadx = 0,
            ipady = 0
        )

        self.UIObject['buttom_master_del'] = tkinter.Button(
            self.UIObject['frame_master_root'],
            text = '删除',
            command = lambda : self.tree_master_config('del'),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
        )
        self.UIObject['buttom_master_del'].bind('<Enter>', lambda x : self.buttom_action('buttom_master_del', '<Enter>'))
        self.UIObject['buttom_master_del'].bind('<Leave>', lambda x : self.buttom_action('buttom_master_del', '<Leave>'))
        self.UIObject['buttom_master_del'].grid(
            row = 1,
            column = 3,
            sticky = "new",
            rowspan = 1,
            columnspan = 1,
            padx = (0, 0),
            pady = (45, 0),
            ipadx = 0,
            ipady = 0
        )

    def treeSelect(self, name, x):
        if name == 'tree_master':
            force = get_tree_force(self.UIObject['tree_master'])
            self.UIData['entry_master_StringVar'].set(str(force['text']))

    def tree_str_rightKey(self, event):
        self.UIObject['tree_rightkey_menu'].delete(0, tkinter.END)
        self.UIObject['tree_rightkey_menu'].add_command(label = '编辑', command = lambda : self.tree_str_edit())
        self.UIObject['tree_rightkey_menu'].post(event.x_root, event.y_root)

    def tree_console_rightKey(self, event):
        self.UIObject['tree_rightkey_menu'].delete(0, tkinter.END)
        self.UIObject['tree_rightkey_menu'].add_command(label = '编辑', command = lambda : self.tree_console_edit())
        self.UIObject['tree_rightkey_menu'].post(event.x_root, event.y_root)

    def tree_str_edit(self):
        tmp_key = get_tree_force(self.UIObject['tree_str'])['text']
        if len(tmp_key) > 0:
            self.edit_str_UI(
                root_obj = self.UIObject['root'],
                root_class = self,
                key = tmp_key,
                hash = self.UIData['hash_now']
            ).start()

    def tree_console_edit(self):
        tmp_key = get_tree_force(self.UIObject['tree_console'])['text']
        if len(tmp_key) > 0:
            self.edit_console_UI(
                root_obj = self.UIObject['root'],
                root_class = self,
                key = tmp_key,
                hash = self.UIData['hash_now']
            ).start()

    def tree_master_config(self, action:str):
        tmp_hashSelection = self.UIData['hash_now']
        tmp_platform = None
        if tmp_hashSelection in OlivaDiceNativeGUI.load.dictBotInfo:
            tmp_platform = OlivaDiceNativeGUI.load.dictBotInfo[tmp_hashSelection].platform['platform']
        tmp_master_target = self.UIData['entry_master_StringVar'].get()
        try:
            tmp_master_target = int(tmp_master_target)
        except:
            tmp_master_target = None
        if tmp_platform != None and tmp_master_target != None:
            tmp_master_target = str(tmp_master_target)
            if action == 'add':
                tmp_dataList_new = []
                tmp_dataList = OlivaDiceCore.console.getConsoleSwitchByHash(
                    'masterList',
                    tmp_hashSelection
                )
                flag_done = False
                for tmp_dataList_this in tmp_dataList:
                    if len(tmp_dataList_this) == 2:
                        if str(tmp_dataList_this[0]) == tmp_master_target:
                            flag_done = True
                        tmp_dataList_new.append(tmp_dataList_this)
                if not flag_done:
                    tmp_dataList_new.append(
                        [
                            tmp_master_target,
                            tmp_platform
                        ]
                    )
                    OlivaDiceCore.console.setConsoleSwitchByHash(
                        'masterList',
                        tmp_dataList_new,
                        tmp_hashSelection
                    )
                    OlivaDiceCore.console.saveConsoleSwitch()
                    self.init_data_total()
            elif action == 'del':
                tmp_dataList_new = []
                tmp_dataList = OlivaDiceCore.console.getConsoleSwitchByHash(
                    'masterList',
                    tmp_hashSelection
                )
                flag_done = False
                for tmp_dataList_this in tmp_dataList:
                    if len(tmp_dataList_this) == 2:
                        if str(tmp_dataList_this[0]) == tmp_master_target:
                            flag_done = True
                        else:
                            tmp_dataList_new.append(tmp_dataList_this)
                if flag_done:
                    OlivaDiceCore.console.setConsoleSwitchByHash(
                        'masterList',
                        tmp_dataList_new,
                        tmp_hashSelection
                    )
                    OlivaDiceCore.console.saveConsoleSwitch()
                    self.init_data_total()

    class edit_str_UI(object):
        def __init__(self, root_obj, root_class, key, hash):
            self.root = root_obj
            self.root_class = root_class
            self.key = key
            self.hash = hash
            self.data = None
            self.UIObject = {}
            self.UIData = {}
            self.UIConfig = {}
            self.UIConfig.update(dictColorContext)
            
        def start(self):
            self.UIObject['root'] = tkinter.Toplevel(self.root)
            self.UIObject['root'].title('修改设置 - %s' % self.key)
            self.UIObject['root'].geometry('400x300')
            self.UIObject['root'].minsize(400, 300)
            self.UIObject['root'].resizable(
                width = True,
                height = True
            )
            self.UIObject['root'].grid_rowconfigure(0, weight = 0)
            self.UIObject['root'].grid_rowconfigure(1, weight = 15)
            self.UIObject['root'].grid_columnconfigure(0, weight = 15)
            self.UIObject['root'].configure(bg = self.UIConfig['color_001'])

            dictStrCustomDict = OlivaDiceCore.msgCustom.dictStrCustomDict
            dictStrCustomNote = OlivaDiceNativeGUI.msgCustom.dictStrCustomNote

            tmp_info = '无说明'
            tmp_data = ''
            if self.key in dictStrCustomNote:
                tmp_info = dictStrCustomNote[self.key]
            if self.hash in dictStrCustomDict:
                if self.key in dictStrCustomDict[self.hash]:
                    tmp_data = dictStrCustomDict[self.hash][self.key]
            self.data = tmp_data

            self.UIObject['label_note'] = tkinter.Label(
                self.UIObject['root'],
                text = tmp_info,
                font = ('等线', 12, 'bold')
            )
            self.UIObject['label_note'].configure(
                bg = self.UIConfig['color_001'],
                fg = self.UIConfig['color_004'],
                justify = 'left',
                anchor = 'nw'
            )
            self.UIObject['label_note'].grid(
                row = 0,
                column = 0,
                sticky = "nsew",
                rowspan = 1,
                columnspan = 1,
                padx = (15, 15),
                pady = (15, 0),
                ipadx = 0,
                ipady = 0
            )
            self.UIData['entry_edit_StringVar'] = tkinter.StringVar()
            self.UIObject['entry_edit'] = tkinter.Text(
                self.UIObject['root'],
                wrap = tkinter.WORD
            )
            self.UIObject['entry_edit'].configure(
                bg = self.UIConfig['color_004'],
                fg = self.UIConfig['color_005'],
                bd = 0,
                font = (None, 10),
                padx = 4,
                pady = 8
            )
            self.UIObject['entry_edit'].grid(
                row = 1,
                column = 0,
                sticky = "nsew",
                rowspan = 1,
                columnspan = 1,
                padx = (15, 15),
                pady = (8, 15),
                ipadx = 4,
                ipady = 8
            )
            self.UIObject['entry_edit'].insert('1.0', tmp_data)

            self.UIObject['root'].iconbitmap('./resource/tmp_favoricon.ico')

            self.UIObject['root'].protocol("WM_DELETE_WINDOW", self.quit)

            self.UIObject['root'].mainloop()

        def quit(self):
            self.save()
            if self.root_class != None:
                self.root_class.init_data_total()
            self.UIObject['root'].destroy()

        def save(self):
            tmp_new_str = self.UIObject['entry_edit'].get('1.0', tkinter.END)[:-1]
            if self.data != None and tmp_new_str != self.data:
                OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[self.hash][self.key] = tmp_new_str
                OlivaDiceCore.msgCustom.dictStrCustomDict[self.hash][self.key] = tmp_new_str
                OlivaDiceCore.msgCustomManager.saveMsgCustomByBotHash(self.hash)


    class edit_console_UI(object):
        def __init__(self, root_obj, root_class, key, hash):
            self.root = root_obj
            self.root_class = root_class
            self.key = key
            self.hash = hash
            self.data = None
            self.UIObject = {}
            self.UIData = {}
            self.UIConfig = {}
            self.UIConfig.update(dictColorContext)
            
        def start(self):
            self.UIObject['root'] = tkinter.Toplevel(self.root)
            self.UIObject['root'].title('修改设置 - %s' % self.key)
            #self.UIObject['root'].geometry('400x100')
            self.UIObject['root'].minsize(400, 10)
            self.UIObject['root'].resizable(
                width = True,
                height = False
            )
            self.UIObject['root'].grid_rowconfigure(0, weight = 0)
            self.UIObject['root'].grid_rowconfigure(1, weight = 15)
            self.UIObject['root'].grid_columnconfigure(0, weight = 15)
            self.UIObject['root'].configure(bg = self.UIConfig['color_001'])

            dictConsoleSwitch = OlivaDiceCore.console.dictConsoleSwitch
            dictConsoleSwitchNote = OlivaDiceNativeGUI.msgCustom.dictConsoleSwitchNote

            tmp_info = '无说明'
            tmp_data = ''
            if self.key in dictConsoleSwitchNote:
                tmp_info = dictConsoleSwitchNote[self.key]
            if self.hash in dictConsoleSwitch:
                if self.key in dictConsoleSwitch[self.hash]:
                    tmp_data = dictConsoleSwitch[self.hash][self.key]
            self.data = tmp_data

            self.UIObject['label_note'] = tkinter.Label(
                self.UIObject['root'],
                text = tmp_info,
                font = ('等线', 12, 'bold')
            )
            self.UIObject['label_note'].configure(
                bg = self.UIConfig['color_001'],
                fg = self.UIConfig['color_004'],
                justify = 'left',
                anchor = 'nw'
            )
            self.UIObject['label_note'].grid(
                row = 0,
                column = 0,
                sticky = "nsew",
                rowspan = 1,
                columnspan = 1,
                padx = (15, 15),
                pady = (15, 0),
                ipadx = 0,
                ipady = 0
            )
            self.UIData['entry_edit_StringVar'] = tkinter.StringVar()
            self.UIObject['entry_edit'] = tkinter.Entry(
                self.UIObject['root'],
                textvariable = self.UIData['entry_edit_StringVar']
            )
            self.UIObject['entry_edit'].configure(
                bg = self.UIConfig['color_006'],
                fg = self.UIConfig['color_001'],
                bd = 0,
                font = ('等线', 12, 'bold'),
                justify = 'center'
                #width = width
            )
            self.UIObject['entry_edit'].grid(
                row = 1,
                column = 0,
                sticky = "n",
                rowspan = 1,
                columnspan = 1,
                padx = (15, 15),
                pady = (8, 15),
                ipadx = 0,
                ipady = 8
            )
            self.UIData['entry_edit_StringVar'].set(tmp_data)

            self.UIObject['root'].iconbitmap('./resource/tmp_favoricon.ico')

            self.UIObject['root'].protocol("WM_DELETE_WINDOW", self.quit)

            self.UIObject['root'].mainloop()

        def quit(self):
            self.save()
            if self.root_class != None:
                self.root_class.init_data_total()
            self.UIObject['root'].destroy()

        def save(self):
            tmp_new_str = self.UIData['entry_edit_StringVar'].get()
            if self.data != None and tmp_new_str != self.data:
                try:
                    OlivaDiceCore.console.dictConsoleSwitch[self.hash][self.key] = int(tmp_new_str)
                    OlivaDiceCore.console.saveConsoleSwitch()
                except:
                    pass

    def init_data_total(self):
        tmp_hashSelection = self.UIData['hash_now']

        tmp_tree_item_children = self.UIObject['tree_str'].get_children()
        for tmp_tree_item_this in tmp_tree_item_children:
            self.UIObject['tree_str'].delete(tmp_tree_item_this)
        if tmp_hashSelection in OlivaDiceCore.msgCustom.dictStrCustomDict:
            tmp_dictStrCustomDict = OlivaDiceCore.msgCustom.dictStrCustomDict[tmp_hashSelection]
            for tmp_dictCustomData_this in OlivaDiceCore.msgCustom.dictStrCustomDict[tmp_hashSelection]:
                try:
                    tmp_value = tmp_dictStrCustomDict[tmp_dictCustomData_this]
                    tmp_value = tmp_value.replace('\r\n', r'\r\n')
                    tmp_value = tmp_value.replace('\n', r'\n')
                    tmp_value = tmp_value.replace('\r', r'\r')
                    tmp_note = ''
                    if tmp_dictCustomData_this in OlivaDiceNativeGUI.msgCustom.dictStrCustomNote:
                        tmp_note = OlivaDiceNativeGUI.msgCustom.dictStrCustomNote[tmp_dictCustomData_this]
                    tmp_note = tmp_note.replace('\n', ' ')
                    tmp_note = tmp_note.replace('\r', ' ')
                    self.UIObject['tree_str'].insert(
                        '',
                        tkinter.END,
                        text = tmp_dictCustomData_this,
                        values=(
                            tmp_dictCustomData_this,
                            tmp_note,
                            tmp_value
                        )
                    )
                except:
                    pass

        tmp_tree_item_children = self.UIObject['tree_console'].get_children()
        for tmp_tree_item_this in tmp_tree_item_children:
            self.UIObject['tree_console'].delete(tmp_tree_item_this)
        if tmp_hashSelection in OlivaDiceCore.console.dictConsoleSwitch:
            tmp_dictConsoleSwitch = OlivaDiceCore.console.dictConsoleSwitch[tmp_hashSelection]
            for tmp_dictConsoleSwitch_this in tmp_dictConsoleSwitch:
                try:
                    if type(tmp_dictConsoleSwitch[tmp_dictConsoleSwitch_this]) == int:
                        tmp_value = str(tmp_dictConsoleSwitch[tmp_dictConsoleSwitch_this])
                        tmp_value = tmp_value.replace('\r\n', r'\r\n')
                        tmp_value = tmp_value.replace('\n', r'\n')
                        tmp_value = tmp_value.replace('\r', r'\r')
                        tmp_note = ''
                        if tmp_dictConsoleSwitch_this in OlivaDiceNativeGUI.msgCustom.dictConsoleSwitchNote:
                            tmp_note = OlivaDiceNativeGUI.msgCustom.dictConsoleSwitchNote[tmp_dictConsoleSwitch_this]
                        tmp_note = tmp_note.replace('\n', ' ')
                        tmp_note = tmp_note.replace('\r', ' ')
                        self.UIObject['tree_console'].insert(
                            '',
                            tkinter.END,
                            text = tmp_dictConsoleSwitch_this,
                            values=(
                                tmp_dictConsoleSwitch_this,
                                tmp_note,
                                tmp_value
                            )
                        )
                except:
                    pass

        tmp_tree_item_children = self.UIObject['tree_master'].get_children()
        for tmp_tree_item_this in tmp_tree_item_children:
            self.UIObject['tree_master'].delete(tmp_tree_item_this)
        tmp_dataList = OlivaDiceCore.console.getConsoleSwitchByHash(
            'masterList',
            tmp_hashSelection
        )
        for tmp_dataList_this in tmp_dataList:
            if len(tmp_dataList_this) == 2:
                tmp_userName = '骰主'
                tmp_userRawId = tmp_dataList_this[0]
                tmp_userPlatform = tmp_dataList_this[1]
                tmp_botHash = tmp_hashSelection
                tmp_userHash = OlivaDiceCore.userConfig.getUserHash(
                    userId = tmp_userRawId,
                    userType = 'user',
                    platform = tmp_userPlatform
                )
                tmp_userId = OlivaDiceCore.userConfig.getUserDataByKeyWithHash(
                    userHash = tmp_userHash,
                    userDataKey = 'userId',
                    botHash = tmp_botHash
                )
                if tmp_userId != None:
                    tmp_userName = OlivaDiceCore.userConfig.getUserConfigByKeyWithHash(
                        userHash = tmp_userHash,
                        userConfigKey = 'userName',
                        botHash = tmp_botHash
                    )
                try:
                    self.UIObject['tree_master'].insert(
                        '',
                        tkinter.END,
                        text = str(tmp_dataList_this[0]),
                        values=(
                            str(tmp_dataList_this[0]),
                            str(tmp_userName)
                        )
                    )
                except:
                    pass
