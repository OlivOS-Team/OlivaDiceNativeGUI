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
import OlivaDiceOdyssey
try:
    import OlivaDiceMaster
except:
    pass
import base64
import os
import tkinter
from tkinter import ttk, filedialog, messagebox
import webbrowser
import traceback
import threading
import json
import importlib
import re

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

    def get_recover_modules_path(self, hash_selection):
        return os.path.join(OlivaDiceCore.data.dataDirRoot, hash_selection, 'console', 'recover_model.json')

    def get_default_modules(self):
        return ['OlivaDiceCore', 'OlivaDiceJoy', 'OlivaDiceMaster', 'OlivaDiceLogger', 'OlivaDiceOdyssey', 'OlivaStoryCore']

    def load_recover_modules(self, hash_selection):
        path = self.get_recover_modules_path(hash_selection)
        if not os.path.exists(path):
            default_modules = self.get_default_modules()
            dir_path = os.path.dirname(path)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump({"modules": default_modules}, f, ensure_ascii=False, indent=4)
            return default_modules
        else:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if not content.strip():
                        default_modules = self.get_default_modules()
                        self.save_recover_modules(hash_selection, default_modules)
                        return default_modules
                    f.seek(0)
                    data = json.load(f)
                    modules_list = data.get("modules")
                    if not isinstance(modules_list, list) or not modules_list:
                        default_modules = self.get_default_modules()
                        self.save_recover_modules(hash_selection, default_modules)
                        return default_modules
                    return modules_list
            except (json.JSONDecodeError, IOError):
                default_modules = self.get_default_modules()
                self.save_recover_modules(hash_selection, default_modules)
                return default_modules

    def save_recover_modules(self, hash_selection, modules_list):
        path = self.get_recover_modules_path(hash_selection)
        dir_path = os.path.dirname(path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({"modules": modules_list}, f, ensure_ascii=False, indent=4)

    def start(self):
        self.UIObject['root'] = tkinter.Toplevel()
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
        self.UIObject['root'].grid_columnconfigure(1, weight = 15)
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

        # 备份
        if OlivaDiceNativeGUI.load.masterModelFlag:
            self.init_frame_backup()

        # 账号管理
        if OlivaDiceNativeGUI.load.masterModelFlag:
            self.init_frame_account()

        # 骰主列表
        self.init_frame_master()

        # 牌堆管理
        self.UIData['deck_remote_loaded_flag'] = False
        self.init_frame_deck()

        self.UIObject['Notebook_root'].add(self.UIObject['frame_main_root'], text="首页")
        self.UIObject['Notebook_root'].add(self.UIObject['frame_deck_root'], text="牌堆管理")
        self.UIObject['Notebook_root'].add(self.UIObject['frame_str_root'], text="回复词")
        self.UIObject['Notebook_root'].add(self.UIObject['frame_console_root'], text="配置项")
        
        # 只有在有 OlivaDiceMaster 模块时才显示备份选项卡
        if OlivaDiceNativeGUI.load.masterModelFlag:
            self.UIObject['Notebook_root'].add(self.UIObject['frame_backup_root'], text="备份")
        
        # 只有在有 OlivaDiceMaster 模块时才显示账号管理选项卡
        if OlivaDiceNativeGUI.load.masterModelFlag:
            self.UIObject['Notebook_root'].add(self.UIObject['frame_account_root'], text="账号管理")
        
        self.UIObject['Notebook_root'].add(self.UIObject['frame_master_root'], text="骰主列表")

        # 只有在有 OlivaDiceMaster 模块时才加载备份配置
        if OlivaDiceNativeGUI.load.masterModelFlag:
            try:
                self.load_backup_config()
            except Exception as e:
                print(f"警告: 加载备份配置失败: {str(e)}")

        self.init_data_total()

        self.UIObject['root'].iconbitmap('./resource/tmp_favoricon.ico')
        self.UIObject['root'].mainloop()
        #OlivaDiceNativeGUI.load.flag_open = False

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

        self.UIData['onlineStatus_Label_root_StringVar'] = tkinter.StringVar()
        self.UIObject['onlineStatus_Label_root'] = tkinter.Label(
            self.UIObject['root'],
            textvariable = self.UIData['onlineStatus_Label_root_StringVar']
        )
        self.UIObject['onlineStatus_Label_root'].configure(
            bg = self.UIConfig['color_001'],
            fg = self.UIConfig['color_004']
        )
        self.UIObject['onlineStatus_Label_root'].grid(
            row = 0,
            column = 1,
            sticky = "nse",
            rowspan = 1,
            columnspan = 1,
            padx = (0, 15),
            pady = (15, 0),
            ipadx = 0,
            ipady = 0
        )

    def Combobox_ComboboxSelected(self, action, event, target):
        if target == 'hash_Combobox_root':
            self.UIData['hash_now'] = self.UIData['hash_find'][self.UIData['hash_Combobox_root_StringVar'].get()]
            self.init_data_total()

    def init_notebook(self):
        self.UIData['style'] = ttk.Style(self.UIObject['root'])
        try:
            self.UIData['style'].element_create('Plain.Notebook.tab', "from", 'default')
        except:
            pass
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
            columnspan = 2,
            padx = (15, 15),
            pady = (8, 15),
            ipadx = 0,
            ipady = 0
        )
        self.UIObject['Notebook_root'].grid_rowconfigure(0, weight = 0)
        self.UIObject['Notebook_root'].grid_rowconfigure(1, weight = 15)
        self.UIObject['Notebook_root'].grid_columnconfigure(0, weight = 15)
        self.UIObject['Notebook_root'].bind('<<NotebookTabChanged>>', lambda x : self.onNotebookTabChanged(x))

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
        try:
            self.UIObject['icon_img_data'] = self.UIObject['icon_img_data'].resize((192 * 2, 108 * 2), Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.LANCZOS)
        except AttributeError:
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
        messagebox.showinfo('已完成复制', '在聊天窗口中发送给骰子，即可成为骰主！')

    def process_msg(self):
        self.UIObject['root'].after(1000,self.process_msg)
        self.UIData['buttom_master_token_copy_StringVar'].set('.master %s' % OlivaDiceCore.data.bot_content['masterKey'])

    def show_project_site(self, url):
        messagebox.showinfo("提示", "将通过浏览器访问 " + url)
        try:
            webbrowser.open(url)
        except webbrowser.Error as error_info:
            messagebox.showerror("webbrowser.Error", error_info)

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

        self.UIObject['button_frame_str'] = tkinter.Frame(self.UIObject['frame_str_root'])
        self.UIObject['button_frame_str'].configure(bg = self.UIConfig['color_001'])
        self.UIObject['button_frame_str'].grid(
            row = 2,
            column = 0,
            sticky = "nsew",
            rowspan = 1,
            columnspan = 2,
            padx = (15, 15),
            pady = (8, 0)
        )
        
        self.UIObject['buttom_config_restore'] = tkinter.Button(
            self.UIObject['button_frame_str'],
            text='配置恢复模块',
            command=self.edit_restore_modules,
            bd=0,
            activebackground=self.UIConfig['color_002'],
            activeforeground=self.UIConfig['color_001'],
            bg=self.UIConfig['color_003'],
            fg=self.UIConfig['color_004'],
            relief='groove',
            height=2,
            width=12
        )
        self.UIObject['buttom_config_restore'].bind('<Enter>', lambda x: self.buttom_action('buttom_config_restore', '<Enter>'))
        self.UIObject['buttom_config_restore'].bind('<Leave>', lambda x: self.buttom_action('buttom_config_restore', '<Leave>'))
        self.UIObject['buttom_config_restore'].pack(side=tkinter.LEFT, padx=(0, 5))
    
        self.UIObject['buttom_reset_str'] = tkinter.Button(
            self.UIObject['button_frame_str'],
            text = '恢复默认回复',
            command = lambda : self.reset_str_confirm(),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
            width = 12
        )
        self.UIObject['buttom_reset_str'].bind('<Enter>', lambda x : self.buttom_action('buttom_reset_str', '<Enter>'))
        self.UIObject['buttom_reset_str'].bind('<Leave>', lambda x : self.buttom_action('buttom_reset_str', '<Leave>'))
        self.UIObject['buttom_reset_str'].pack(side = tkinter.LEFT, padx = (0, 5))

        self.UIObject['buttom_import_str'] = tkinter.Button(
            self.UIObject['button_frame_str'],
            text = '导入回复',
            command = lambda : self.import_str_config(),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
            width = 12
        )
        self.UIObject['buttom_import_str'].bind('<Enter>', lambda x : self.buttom_action('buttom_import_str', '<Enter>'))
        self.UIObject['buttom_import_str'].bind('<Leave>', lambda x : self.buttom_action('buttom_import_str', '<Leave>'))
        self.UIObject['buttom_import_str'].pack(side = tkinter.LEFT, padx = (0, 5))

        self.UIObject['buttom_export_str'] = tkinter.Button(
            self.UIObject['button_frame_str'],
            text = '导出回复',
            command = lambda : self.export_str_config(),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
            width = 12
        )
        self.UIObject['buttom_export_str'].bind('<Enter>', lambda x : self.buttom_action('buttom_export_str', '<Enter>'))
        self.UIObject['buttom_export_str'].bind('<Leave>', lambda x : self.buttom_action('buttom_export_str', '<Leave>'))
        self.UIObject['buttom_export_str'].pack(side = tkinter.LEFT, padx = (0, 5))

        self.UIObject['buttom_refresh_str'] = tkinter.Button(
            self.UIObject['button_frame_str'],
            text = '刷新回复',
            command = lambda : self.refresh_str_config(),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
            width = 12
        )
        self.UIObject['buttom_refresh_str'].bind('<Enter>', lambda x : self.buttom_action('buttom_refresh_str', '<Enter>'))
        self.UIObject['buttom_refresh_str'].bind('<Leave>', lambda x : self.buttom_action('buttom_refresh_str', '<Leave>'))
        self.UIObject['buttom_refresh_str'].pack(side = tkinter.LEFT, padx = (0, 5))

        self.UIObject['buttom_edit_str'] = tkinter.Button(
            self.UIObject['button_frame_str'],
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
        self.UIObject['buttom_edit_str'].bind('<Enter>', lambda x : self.buttom_action('buttom_edit_str', '<Enter>'))
        self.UIObject['buttom_edit_str'].bind('<Leave>', lambda x : self.buttom_action('buttom_edit_str', '<Leave>'))
        self.UIObject['buttom_edit_str'].pack(side = tkinter.RIGHT)
        
        self.UIObject['buttom_reset_delete_str'] = tkinter.Button(
            self.UIObject['button_frame_str'],
            text = '恢复/删除',
            command = lambda : self.reset_selected_str(),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
            width = 12
        )
        self.UIObject['buttom_reset_delete_str'].bind('<Enter>', lambda x : self.buttom_action('buttom_reset_delete_str', '<Enter>'))
        self.UIObject['buttom_reset_delete_str'].bind('<Leave>', lambda x : self.buttom_action('buttom_reset_delete_str', '<Leave>'))
        self.UIObject['buttom_reset_delete_str'].pack(side = tkinter.RIGHT, padx = (0, 5))

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

        self.UIObject['button_frame_console'] = tkinter.Frame(self.UIObject['frame_console_root'])
        self.UIObject['button_frame_console'].configure(bg = self.UIConfig['color_001'])
        self.UIObject['button_frame_console'].grid(
            row = 2,
            column = 0,
            sticky = "nsew",
            rowspan = 1,
            columnspan = 2,
            padx = (15, 15),
            pady = (8, 0)
        )

        self.UIObject['buttom_reset_console'] = tkinter.Button(
            self.UIObject['button_frame_console'],
            text = '恢复默认配置',
            command = lambda : self.reset_console_confirm(),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
            width = 12
        )
        self.UIObject['buttom_reset_console'].bind('<Enter>', lambda x : self.buttom_action('buttom_reset_console', '<Enter>'))
        self.UIObject['buttom_reset_console'].bind('<Leave>', lambda x : self.buttom_action('buttom_reset_console', '<Leave>'))
        self.UIObject['buttom_reset_console'].pack(side = tkinter.LEFT, padx = (0, 5))

        self.UIObject['buttom_import_console'] = tkinter.Button(
            self.UIObject['button_frame_console'],
            text = '导入配置',
            command = lambda : self.import_console_config(),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
            width = 12
        )
        self.UIObject['buttom_import_console'].bind('<Enter>', lambda x : self.buttom_action('buttom_import_console', '<Enter>'))
        self.UIObject['buttom_import_console'].bind('<Leave>', lambda x : self.buttom_action('buttom_import_console', '<Leave>'))
        self.UIObject['buttom_import_console'].pack(side = tkinter.LEFT, padx = (0, 5))

        self.UIObject['buttom_export_console'] = tkinter.Button(
            self.UIObject['button_frame_console'],
            text = '导出配置',
            command = lambda : self.export_console_config(),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
            width = 12
        )
        self.UIObject['buttom_export_console'].bind('<Enter>', lambda x : self.buttom_action('buttom_export_console', '<Enter>'))
        self.UIObject['buttom_export_console'].bind('<Leave>', lambda x : self.buttom_action('buttom_export_console', '<Leave>'))
        self.UIObject['buttom_export_console'].pack(side = tkinter.LEFT, padx = (0, 5))

        self.UIObject['buttom_refresh_console'] = tkinter.Button(
            self.UIObject['button_frame_console'],
            text = '刷新配置',
            command = lambda : self.refresh_console_config(),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
            width = 12
        )
        self.UIObject['buttom_refresh_console'].bind('<Enter>', lambda x : self.buttom_action('buttom_refresh_console', '<Enter>'))
        self.UIObject['buttom_refresh_console'].bind('<Leave>', lambda x : self.buttom_action('buttom_refresh_console', '<Leave>'))
        self.UIObject['buttom_refresh_console'].pack(side = tkinter.LEFT, padx = (0, 5))

        self.UIObject['buttom_edit_console'] = tkinter.Button(
            self.UIObject['button_frame_console'],
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
        self.UIObject['buttom_edit_console'].bind('<Enter>', lambda x : self.buttom_action('buttom_edit_console', '<Enter>'))
        self.UIObject['buttom_edit_console'].bind('<Leave>', lambda x : self.buttom_action('buttom_edit_console', '<Leave>'))
        self.UIObject['buttom_edit_console'].pack(side = tkinter.RIGHT)

        self.UIObject['buttom_reset_delete_console'] = tkinter.Button(
            self.UIObject['button_frame_console'],
            text = '恢复/删除',
            command = lambda : self.reset_selected_console(),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
            width = 12
        )
        self.UIObject['buttom_reset_delete_console'].bind('<Enter>', lambda x : self.buttom_action('buttom_reset_delete_console', '<Enter>'))
        self.UIObject['buttom_reset_delete_console'].bind('<Leave>', lambda x : self.buttom_action('buttom_reset_delete_console', '<Leave>'))
        self.UIObject['buttom_reset_delete_console'].pack(side = tkinter.RIGHT, padx = (0, 5))

    def init_frame_backup(self):
        self.UIObject['frame_backup_root'] = tkinter.Frame(self.UIObject['Notebook_root'])
        self.UIObject['frame_backup_root'].configure(relief = tkinter.FLAT)
        self.UIObject['frame_backup_root'].grid(
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
        self.UIObject['frame_backup_root'].grid_rowconfigure(0, weight = 0)
        self.UIObject['frame_backup_root'].grid_rowconfigure(1, weight = 15)
        self.UIObject['frame_backup_root'].grid_rowconfigure(2, weight = 0)
        self.UIObject['frame_backup_root'].grid_columnconfigure(0, weight = 15)
        self.UIObject['frame_backup_root'].configure(bg = self.UIConfig['color_001'], borderwidth = 0)

        self.UIObject['tree_backup'] = ttk.Treeview(self.UIObject['frame_backup_root'])
        self.UIObject['tree_backup']['show'] = 'headings'
        self.UIObject['tree_backup']['columns'] = ('KEY', 'NOTE', 'DATA')
        self.UIObject['tree_backup'].column('KEY', width = 140)
        self.UIObject['tree_backup'].column('NOTE', width = 410)
        self.UIObject['tree_backup'].column('DATA', width = 140)
        self.UIObject['tree_backup'].heading('KEY', text = '条目')
        self.UIObject['tree_backup'].heading('NOTE', text = '说明')
        self.UIObject['tree_backup'].heading('DATA', text = '内容')
        self.UIObject['tree_backup'].grid(
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
        self.UIObject['tree_rightkey_menu_backup'] = tkinter.Menu(self.UIObject['root'], tearoff = False)
        self.UIObject['tree_backup'].bind('<Button-3>', lambda x : self.tree_backup_rightKey(x))
        self.UIObject['tree_backup_yscroll'] = ttk.Scrollbar(
            self.UIObject['frame_backup_root'],
            orient = "vertical",
            command = self.UIObject['tree_backup'].yview
        )
        self.UIObject['tree_backup'].configure(
            yscrollcommand = self.UIObject['tree_backup_yscroll'].set
        )
        self.UIObject['tree_backup_yscroll'].grid(
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

        self.UIObject['button_frame_backup'] = tkinter.Frame(self.UIObject['frame_backup_root'])
        self.UIObject['button_frame_backup'].configure(bg = self.UIConfig['color_001'])
        self.UIObject['button_frame_backup'].grid(
            row = 2,
            column = 0,
            sticky = "nsew",
            rowspan = 1,
            columnspan = 2,
            padx = (15, 15),
            pady = (8, 0)
        )

        self.UIObject['buttom_reset_backup'] = tkinter.Button(
            self.UIObject['button_frame_backup'],
            text = '恢复默认配置',
            command = lambda : self.reset_backup_confirm(),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
            width = 12
        )
        self.UIObject['buttom_reset_backup'].bind('<Enter>', lambda x : self.buttom_action('buttom_reset_backup', '<Enter>'))
        self.UIObject['buttom_reset_backup'].bind('<Leave>', lambda x : self.buttom_action('buttom_reset_backup', '<Leave>'))
        self.UIObject['buttom_reset_backup'].pack(side = tkinter.LEFT, padx = (0, 5))

        self.UIObject['buttom_import_backup'] = tkinter.Button(
            self.UIObject['button_frame_backup'],
            text = '导入备份配置',
            command = lambda : self.import_backup_config(),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
            width = 12
        )
        self.UIObject['buttom_import_backup'].bind('<Enter>', lambda x : self.buttom_action('buttom_import_backup', '<Enter>'))
        self.UIObject['buttom_import_backup'].bind('<Leave>', lambda x : self.buttom_action('buttom_import_backup', '<Leave>'))
        self.UIObject['buttom_import_backup'].pack(side = tkinter.LEFT, padx = (0, 5))

        self.UIObject['buttom_export_backup'] = tkinter.Button(
            self.UIObject['button_frame_backup'],
            text = '导出备份配置',
            command = lambda : self.export_backup_config(),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
            width = 12
        )
        self.UIObject['buttom_export_backup'].bind('<Enter>', lambda x : self.buttom_action('buttom_export_backup', '<Enter>'))
        self.UIObject['buttom_export_backup'].bind('<Leave>', lambda x : self.buttom_action('buttom_export_backup', '<Leave>'))
        self.UIObject['buttom_export_backup'].pack(side = tkinter.LEFT, padx = (0, 5))

        self.UIObject['buttom_refresh_backup'] = tkinter.Button(
            self.UIObject['button_frame_backup'],
            text = '刷新备份配置',
            command = lambda : self.refresh_backup_config(),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
            width = 12
        )
        self.UIObject['buttom_refresh_backup'].bind('<Enter>', lambda x : self.buttom_action('buttom_refresh_backup', '<Enter>'))
        self.UIObject['buttom_refresh_backup'].bind('<Leave>', lambda x : self.buttom_action('buttom_refresh_backup', '<Leave>'))
        self.UIObject['buttom_refresh_backup'].pack(side = tkinter.LEFT, padx = (0, 5))

        self.UIObject['buttom_edit_backup'] = tkinter.Button(
            self.UIObject['button_frame_backup'],
            text = '编辑',
            command = lambda : self.tree_backup_edit(),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
            width = 12
        )
        self.UIObject['buttom_edit_backup'].bind('<Enter>', lambda x : self.buttom_action('buttom_edit_backup', '<Enter>'))
        self.UIObject['buttom_edit_backup'].bind('<Leave>', lambda x : self.buttom_action('buttom_edit_backup', '<Leave>'))
        self.UIObject['buttom_edit_backup'].pack(side = tkinter.RIGHT)

        self.UIObject['buttom_reset_delete_backup'] = tkinter.Button(
            self.UIObject['button_frame_backup'],
            text = '恢复/删除',
            command = lambda : self.reset_selected_backup(),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
            width = 12
        )
        self.UIObject['buttom_reset_delete_backup'].bind('<Enter>', lambda x : self.buttom_action('buttom_reset_delete_backup', '<Enter>'))
        self.UIObject['buttom_reset_delete_backup'].bind('<Leave>', lambda x : self.buttom_action('buttom_reset_delete_backup', '<Leave>'))
        self.UIObject['buttom_reset_delete_backup'].pack(side = tkinter.RIGHT, padx = (0, 5))

    def init_frame_account(self):
        """账号管理界面"""
        self.UIObject['frame_account_root'] = tkinter.Frame(self.UIObject['Notebook_root'])
        self.UIObject['frame_account_root'].configure(relief = tkinter.FLAT)
        self.UIObject['frame_account_root'].grid(
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
        self.UIObject['frame_account_root'].grid_rowconfigure(0, weight = 0)
        self.UIObject['frame_account_root'].grid_rowconfigure(1, weight = 0)
        self.UIObject['frame_account_root'].grid_rowconfigure(2, weight = 15)
        self.UIObject['frame_account_root'].grid_rowconfigure(3, weight = 0)
        self.UIObject['frame_account_root'].grid_columnconfigure(0, weight = 15)
        self.UIObject['frame_account_root'].configure(bg = self.UIConfig['color_001'], borderwidth = 0)

        # 说明标签
        self.UIObject['label_account_info'] = tkinter.Label(
            self.UIObject['frame_account_root'],
            text = '多账号连接管理：建立主从关系后，从账号会自动共享主账号的数据\n部分数据（如群开关状态）保持独立，不会被共享',
            font = ('等线', 10),
            bg = self.UIConfig['color_001'],
            fg = self.UIConfig['color_004'],
            justify = 'left',
            anchor = 'w'
        )
        self.UIObject['label_account_info'].grid(
            row = 0,
            column = 0,
            sticky = "nsew",
            padx = (15, 15),
            pady = (15, 5)
        )

        # 主从关系配置区域
        self.UIObject['frame_account_relation'] = tkinter.Frame(self.UIObject['frame_account_root'])
        self.UIObject['frame_account_relation'].configure(bg = self.UIConfig['color_001'])
        self.UIObject['frame_account_relation'].grid(
            row = 1,
            column = 0,
            sticky = "nsew",
            padx = (15, 15),
            pady = (5, 5)
        )

        # 主账号
        self.UIObject['label_master_account'] = tkinter.Label(
            self.UIObject['frame_account_relation'],
            text = '主账号:',
            font = ('等线', 10),
            bg = self.UIConfig['color_001'],
            fg = self.UIConfig['color_004']
        )
        self.UIObject['label_master_account'].pack(side = tkinter.LEFT, padx = (0, 5))

        self.UIData['account_master_StringVar'] = tkinter.StringVar()
        self.UIObject['combo_master_account'] = ttk.Combobox(
            self.UIObject['frame_account_relation'],
            textvariable = self.UIData['account_master_StringVar'],
            width = 20
        )
        self.UIObject['combo_master_account'].configure(state='readonly')
        self.UIObject['combo_master_account'].pack(side = tkinter.LEFT, padx = (0, 15))
        
        # 当前选中的从账号显示
        self.UIObject['label_current_slave'] = tkinter.Label(
            self.UIObject['frame_account_relation'],
            text = '当前从账号: 未选择',
            font = ('等线', 10),
            bg = self.UIConfig['color_001'],
            fg = self.UIConfig['color_006']
        )
        self.UIObject['label_current_slave'].pack(side = tkinter.LEFT, padx = (0, 15))

        # 建立连接按钮
        self.UIObject['button_link_account'] = tkinter.Button(
            self.UIObject['frame_account_relation'],
            text = '建立主从关系',
            command = lambda : self.link_account(),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 1,
            width = 12
        )
        self.UIObject['button_link_account'].bind('<Enter>', lambda x : self.buttom_action('button_link_account', '<Enter>'))
        self.UIObject['button_link_account'].bind('<Leave>', lambda x : self.buttom_action('button_link_account', '<Leave>'))
        self.UIObject['button_link_account'].pack(side = tkinter.LEFT, padx = (0, 5))

        # 断开连接按钮
        self.UIObject['button_unlink_account'] = tkinter.Button(
            self.UIObject['frame_account_relation'],
            text = '断开主从关系',
            command = lambda : self.unlink_account(),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 1,
            width = 12
        )
        self.UIObject['button_unlink_account'].bind('<Enter>', lambda x : self.buttom_action('button_unlink_account', '<Enter>'))
        self.UIObject['button_unlink_account'].bind('<Leave>', lambda x : self.buttom_action('button_unlink_account', '<Leave>'))
        self.UIObject['button_unlink_account'].pack(side = tkinter.LEFT, padx = (0, 5))

        # 账号列表区域
        self.UIObject['tree_account'] = ttk.Treeview(self.UIObject['frame_account_root'])
        self.UIObject['tree_account']['show'] = 'headings'
        self.UIObject['tree_account']['columns'] = ('ROLE', 'NAME', 'ID', 'HASH', 'RELATION')
        self.UIObject['tree_account'].column('ROLE', width = 80)
        self.UIObject['tree_account'].column('NAME', width = 150)
        self.UIObject['tree_account'].column('ID', width = 120)
        self.UIObject['tree_account'].column('HASH', width = 200)
        self.UIObject['tree_account'].column('RELATION', width = 200)
        self.UIObject['tree_account'].heading('ROLE', text = '角色')
        self.UIObject['tree_account'].heading('NAME', text = '名称')
        self.UIObject['tree_account'].heading('ID', text = 'ID')
        self.UIObject['tree_account'].heading('HASH', text = 'Hash')
        self.UIObject['tree_account'].heading('RELATION', text = '主从关系')
        self.UIObject['tree_account'].grid(
            row = 2,
            column = 0,
            sticky = "nsew",
            rowspan = 1,
            columnspan = 1,
            padx = (15, 0),
            pady = (5, 0),
            ipadx = 0,
            ipady = 0
        )
        self.UIObject['tree_account_yscroll'] = ttk.Scrollbar(
            self.UIObject['frame_account_root'],
            orient = "vertical",
            command = self.UIObject['tree_account'].yview
        )
        self.UIObject['tree_account'].configure(
            yscrollcommand = self.UIObject['tree_account_yscroll'].set
        )
        self.UIObject['tree_account_yscroll'].grid(
            row = 2,
            column = 1,
            sticky = "nsw",
            rowspan = 1,
            columnspan = 1,
            padx = (0, 15),
            pady = (5, 0),
            ipadx = 0,
            ipady = 0
        )
        
        # 添加右键菜单
        self.UIObject['menu_account_context'] = tkinter.Menu(self.UIObject['root'], tearoff = 0)
        self.UIObject['menu_account_context'].add_command(label = '复制 Hash', command = self.copy_account_hash)
        self.UIObject['menu_account_context'].add_separator()
        self.UIObject['menu_account_context'].add_command(label = '建立主从关系', command = self.link_account_from_menu)
        self.UIObject['menu_account_context'].add_command(label = '断开主从关系', command = self.unlink_account_from_menu)
        self.UIObject['tree_account'].bind('<Button-3>', self.show_account_context_menu)
        
        # 绑定选择变化事件，更新当前从账号显示
        self.UIObject['tree_account'].bind('<<TreeviewSelect>>', self.update_current_slave_display)

        # 底部按钮区域
        self.UIObject['button_frame_account'] = tkinter.Frame(self.UIObject['frame_account_root'])
        self.UIObject['button_frame_account'].configure(bg = self.UIConfig['color_001'])
        self.UIObject['button_frame_account'].grid(
            row = 3,
            column = 0,
            sticky = "nsew",
            rowspan = 1,
            columnspan = 2,
            padx = (15, 15),
            pady = (8, 15)
        )

        # 刷新按钮
        self.UIObject['button_refresh_account'] = tkinter.Button(
            self.UIObject['button_frame_account'],
            text = '刷新账号列表',
            command = lambda : self.refresh_account_list(),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
            width = 12
        )
        self.UIObject['button_refresh_account'].bind('<Enter>', lambda x : self.buttom_action('button_refresh_account', '<Enter>'))
        self.UIObject['button_refresh_account'].bind('<Leave>', lambda x : self.buttom_action('button_refresh_account', '<Leave>'))
        self.UIObject['button_refresh_account'].pack(side = tkinter.LEFT, padx = (0, 5))

        # 复制到账号按钮
        self.UIObject['button_copy_to_account'] = tkinter.Button(
            self.UIObject['button_frame_account'],
            text = '复制到目标账号',
            command = lambda : self.copy_to_account(),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
            width = 14
        )
        self.UIObject['button_copy_to_account'].bind('<Enter>', lambda x : self.buttom_action('button_copy_to_account', '<Enter>'))
        self.UIObject['button_copy_to_account'].bind('<Leave>', lambda x : self.buttom_action('button_copy_to_account', '<Leave>'))
        self.UIObject['button_copy_to_account'].pack(side = tkinter.LEFT, padx = (0, 5))

        # 导出到压缩包按钮
        self.UIObject['button_export_to_zip'] = tkinter.Button(
            self.UIObject['button_frame_account'],
            text = '导出到压缩包',
            command = lambda : self.export_to_zip(),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
            width = 14
        )
        self.UIObject['button_export_to_zip'].bind('<Enter>', lambda x : self.buttom_action('button_export_to_zip', '<Enter>'))
        self.UIObject['button_export_to_zip'].bind('<Leave>', lambda x : self.buttom_action('button_export_to_zip', '<Leave>'))
        self.UIObject['button_export_to_zip'].pack(side = tkinter.LEFT, padx = (0, 5))

        # 从压缩包导入按钮
        self.UIObject['button_import_from_zip'] = tkinter.Button(
            self.UIObject['button_frame_account'],
            text = '从压缩包导入',
            command = lambda : self.import_from_zip(),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
            width = 14
        )
        self.UIObject['button_import_from_zip'].bind('<Enter>', lambda x : self.buttom_action('button_import_from_zip', '<Enter>'))
        self.UIObject['button_import_from_zip'].bind('<Leave>', lambda x : self.buttom_action('button_import_from_zip', '<Leave>'))
        self.UIObject['button_import_from_zip'].pack(side = tkinter.LEFT, padx = (0, 5))

        # 初始化账号列表
        self.refresh_account_list()

    def update_current_slave_display(self, event=None):
        """更新当前选中的从账号显示"""
        try:
            selection = self.UIObject['tree_account'].selection()
            if not selection:
                self.UIObject['label_current_slave'].config(text='当前从账号: 未选择')
                return
            
            item = self.UIObject['tree_account'].item(selection[0])
            values = item['values']
            bot_name = values[1]  # 名称
            bot_id = values[2]    # ID
            bot_hash = values[3]  # Hash
            
            # 格式化显示
            if bot_id == "-":
                # 未找到的从账号
                display_text = f"当前从账号: {bot_name} ({bot_hash[:8]}...)"
            else:
                display_text = f"当前从账号: {bot_name} ({bot_id})"
            
            self.UIObject['label_current_slave'].config(text=display_text)
        except Exception as e:
            self.UIObject['label_current_slave'].config(text='当前从账号: 未选择')
    
    def link_account(self):
        """建立主从关系"""
        try:
            # 从Treeview中获取选中的账号作为从账号
            selection = self.UIObject['tree_account'].selection()
            if not selection:
                messagebox.showwarning("警告", "请先在账号列表中选择从账号")
                return
            
            item = self.UIObject['tree_account'].item(selection[0])
            values = item['values']
            slave_hash = values[3]  # Hash在第4列
            
            # 获取主账号
            master_key = self.UIData['account_master_StringVar'].get()
            
            if not master_key or master_key == '请选择账号':
                messagebox.showwarning("警告", "请选择主账号")
                return
            
            master_hash = self.UIData['account_hash_map'][master_key]
            
            if slave_hash == master_hash:
                messagebox.showerror("错误", "从账号和主账号不能相同")
                return
            
            # 检查账号不能为unity（大小写模糊）
            if slave_hash.lower() == "unity":
                messagebox.showerror("错误", "从账号不能为unity")
                return
            if master_hash.lower() == "unity":
                messagebox.showerror("错误", "主账号不能为unity")
                return
            
            # 调用账号管理模块
            success, result = OlivaDiceMaster.accountManager.linkAccount(slave_hash, master_hash)
            
            if success:
                # 保存当前主账号选择
                current_master = self.UIData['account_master_StringVar'].get()
                
                messagebox.showinfo("成功", result)
                # 刷新列表（会自动清除选择并更新显示）
                self.refresh_account_list()
                
                # 恢复主账号选择
                if current_master and current_master != '请选择账号':
                    try:
                        values = self.UIObject['combo_master_account']['values']
                        if current_master in values:
                            index = list(values).index(current_master)
                            self.UIObject['combo_master_account'].current(index)
                    except:
                        pass
            else:
                messagebox.showerror("失败", result)
        except Exception as e:
            messagebox.showerror("错误", f"建立主从关系失败：{str(e)}")

    def unlink_account(self):
        """断开主从关系"""
        try:
            # 从Treeview中获取选中的账号作为从账号
            selection = self.UIObject['tree_account'].selection()
            if not selection:
                messagebox.showwarning("警告", "请先在账号列表中选择要断开的从账号")
                return
            
            item = self.UIObject['tree_account'].item(selection[0])
            values = item['values']
            slave_hash = values[3]  # Hash在第4列
            bot_name = values[1]    # 名称
            bot_id = values[2]      # ID
            
            # 格式化显示名称用于确认对话框
            if bot_id == "-":
                display_name = f"{bot_name} ({slave_hash[:8]}...)"
            else:
                display_name = f"{bot_name} ({bot_id})"
            
            # 确认对话框
            if not messagebox.askyesno("确认", f"确定要断开账号 {display_name} 的主从关系吗？"):
                return
            
            # 调用账号管理模块
            success, result = OlivaDiceMaster.accountManager.unlinkAccount(slave_hash)
            
            if success:
                # 保存当前主账号选择
                current_master = self.UIData['account_master_StringVar'].get()
                
                messagebox.showinfo("成功", result)
                # 刷新列表（会自动清除选择并更新显示）
                self.refresh_account_list()
                
                # 恢复主账号选择
                if current_master and current_master != '请选择账号':
                    try:
                        values = self.UIObject['combo_master_account']['values']
                        if current_master in values:
                            index = list(values).index(current_master)
                            self.UIObject['combo_master_account'].current(index)
                    except:
                        pass
            else:
                messagebox.showerror("失败", result)
        except Exception as e:
            messagebox.showerror("错误", f"断开主从关系失败：{str(e)}")

    def get_bot_display_name(self, botHash, bot_info):
        """获取bot的显示名称（类似骰主列表的实现）"""
        bot_name = "未知"
        
        # 先尝试从 bot_info 获取
        if hasattr(bot_info, 'name') and bot_info.name:
            bot_name = bot_info.name
        
        # 尝试从用户配置中获取保存的昵称（如果bot曾经作为用户被记录过）
        try:
            if hasattr(bot_info, 'id') and hasattr(bot_info, 'platform') and bot_info.platform:
                bot_id = str(bot_info.id)
                bot_user_hash = OlivaDiceCore.userConfig.getUserHash(
                    userId = bot_id,
                    userType = 'user',
                    platform = bot_info.platform['platform']
                )
                saved_name = OlivaDiceCore.userConfig.getUserConfigByKeyWithHash(
                    userHash = bot_user_hash,
                    userConfigKey = 'userName',
                    botHash = botHash
                )
                if saved_name and saved_name != '用户':
                    bot_name = saved_name
        except:
            pass
        
        return bot_name
    
    def show_account_context_menu(self, event):
        """显示账号列表的右键菜单"""
        try:
            # 选择右键点击的项目
            item = self.UIObject['tree_account'].identify_row(event.y)
            if item:
                self.UIObject['tree_account'].selection_set(item)
                self.UIObject['tree_account'].focus(item)
                self.UIObject['menu_account_context'].post(event.x_root, event.y_root)
        except Exception as e:
            pass
    
    def copy_account_hash(self):
        """复制选中账号的Hash到剪贴板"""
        try:
            selection = self.UIObject['tree_account'].selection()
            if not selection:
                return
            
            item = self.UIObject['tree_account'].item(selection[0])
            values = item['values']
            bot_hash = values[3]  # Hash在第4列
            
            if bot_hash:
                self.UIObject['root'].clipboard_clear()
                self.UIObject['root'].clipboard_append(bot_hash)
                self.UIObject['root'].update()
                messagebox.showinfo("成功", f"已复制 Hash 到剪贴板：\n{bot_hash}")
        except Exception as e:
            messagebox.showerror("错误", f"复制失败：{str(e)}")
    
    def link_account_from_menu(self):
        """从右键菜单建立主从关系（右键选中的账号作为从账号）"""
        try:
            # 确保有选中的账号
            selection = self.UIObject['tree_account'].selection()
            if not selection:
                messagebox.showwarning("警告", "请先选择一个账号")
                return
            
            # 直接调用现有的建立主从关系函数
            self.link_account()
        except Exception as e:
            messagebox.showerror("错误", f"建立主从关系失败：{str(e)}")
    
    def unlink_account_from_menu(self):
        """从右键菜单断开主从关系（右键选中的账号作为从账号）"""
        try:
            # 确保有选中的账号
            selection = self.UIObject['tree_account'].selection()
            if not selection:
                messagebox.showwarning("警告", "请先选择一个账号")
                return
            
            # 直接调用现有的断开主从关系函数
            self.unlink_account()
        except Exception as e:
            messagebox.showerror("错误", f"断开主从关系失败：{str(e)}")

    def refresh_account_list(self):
        """刷新账号列表"""
        try:
            # 清空树形列表
            for item in self.UIObject['tree_account'].get_children():
                self.UIObject['tree_account'].delete(item)
            
            # 获取所有账号和关系
            relations = OlivaDiceCore.console.getAllAccountRelations()
            
            # 创建主账号到从账号的映射
            master_to_slaves = {}
            for slave, master in relations.items():
                if master not in master_to_slaves:
                    master_to_slaves[master] = []
                master_to_slaves[master].append(slave)
            
            # 准备账号下拉列表
            account_list = ['请选择账号']
            self.UIData['account_hash_map'] = {}
            
            # 第一步：先处理所有在dictBotInfo中的账号（已添加的账号）
            for botHash in OlivaDiceNativeGUI.load.dictBotInfo:
                bot_info = OlivaDiceNativeGUI.load.dictBotInfo[botHash]
                
                # 使用辅助方法获取bot名称
                bot_name = self.get_bot_display_name(botHash, bot_info)
                bot_id = str(bot_info.id) if hasattr(bot_info, 'id') and bot_info.id else "未知"
                
                # 添加到下拉列表
                account_key = f"{bot_name} ({bot_id})"
                account_list.append(account_key)
                self.UIData['account_hash_map'][account_key] = botHash
                
                # 判断账号角色
                role = "独立账号"
                relation_info = "-"
                
                if botHash in relations:
                    # 从账号
                    role = "从账号"
                    masterHash = relations[botHash]
                    if masterHash in OlivaDiceNativeGUI.load.dictBotInfo:
                        master_info = OlivaDiceNativeGUI.load.dictBotInfo[masterHash]
                        master_name = self.get_bot_display_name(masterHash, master_info)
                        relation_info = f"→ {master_name} ({masterHash[:8]}...)"
                    else:
                        relation_info = f"→ {masterHash[:8]}..."
                elif botHash in master_to_slaves:
                    # 主账号
                    role = "主账号"
                    slave_count = len(master_to_slaves[botHash])
                    relation_info = f"← {slave_count} 个从账号"
                
                # 插入到树形列表
                self.UIObject['tree_account'].insert(
                    '',
                    'end',
                    values = (role, bot_name, bot_id, botHash, relation_info)
                )
            
            # 第二步：处理未找到的从账号（在relations中但不在dictBotInfo中）
            for slave_hash in relations.keys():
                # 跳过已经在dictBotInfo中处理过的账号
                if slave_hash in OlivaDiceNativeGUI.load.dictBotInfo:
                    continue
                
                # 从账号不在dictBotInfo中（可能是未登录或不存在）
                bot_name = "未知"
                bot_id = "-"
                
                # 添加到下拉列表，显示Hash以便区分（只显示前8位）
                account_key = f"{bot_name} ({slave_hash[:8]}...)"
                account_list.append(account_key)
                self.UIData['account_hash_map'][account_key] = slave_hash
                
                # 判断账号角色（必然是从账号）
                role = "从账号"
                masterHash = relations[slave_hash]
                if masterHash in OlivaDiceNativeGUI.load.dictBotInfo:
                    master_info = OlivaDiceNativeGUI.load.dictBotInfo[masterHash]
                    master_name = self.get_bot_display_name(masterHash, master_info)
                    relation_info = f"→ {master_name} ({masterHash[:8]}...)"
                else:
                    relation_info = f"→ {masterHash[:8]}..."
                
                # 插入到树形列表
                self.UIObject['tree_account'].insert(
                    '',
                    'end',
                    values = (role, bot_name, bot_id, slave_hash, relation_info)
                )
            
            # 更新下拉框（只更新主账号下拉框）
            self.UIObject['combo_master_account']['values'] = tuple(account_list)
            
            if len(account_list) > 1:
                self.UIObject['combo_master_account'].current(0)
            
            # 更新当前选中的从账号显示
            self.update_current_slave_display()
                
        except Exception as e:
            messagebox.showerror("错误", f"刷新账号列表失败：{str(e)}\n{traceback.format_exc()}")

    def copy_to_account(self):
        """复制源账号数据到目标账号"""
        try:
            # 获取选中的账号作为源账号
            selection = self.UIObject['tree_account'].selection()
            if not selection:
                messagebox.showwarning("警告", "请先在账号列表中选择源账号")
                return
            
            # 获取选中账号的信息
            item = self.UIObject['tree_account'].item(selection[0])
            values = item['values']
            source_bot_hash = values[3]
            source_bot_name = values[1]
            source_bot_id = values[2]
            
            # 创建对话框
            copy_window = tkinter.Toplevel(self.UIObject['root'])
            copy_window.title('复制账号数据')
            copy_window.geometry('480x250')
            copy_window.resizable(False, False)
            copy_window.configure(bg = self.UIConfig['color_001'])
            
            # 显示源账号信息
            frame_source_info = tkinter.Frame(copy_window, bg = self.UIConfig['color_001'])
            frame_source_info.pack(pady = (15, 10), fill = tkinter.X, padx = 15)
            
            label_source_title = tkinter.Label(
                frame_source_info,
                text = '源账号（已选定）：',
                font = ('等线', 11, 'bold'),
                bg = self.UIConfig['color_001'],
                fg = self.UIConfig['color_004']
            )
            label_source_title.pack(anchor = 'w')
            
            source_info_text = f"  名称: {source_bot_name}  |  ID: {source_bot_id}\n  Hash: {source_bot_hash}"
            label_source_info = tkinter.Label(
                frame_source_info,
                text = source_info_text,
                font = ('等线', 10),
                bg = self.UIConfig['color_001'],
                fg = self.UIConfig['color_006'],
                justify = 'left'
            )
            label_source_info.pack(anchor = 'w', padx = 10)
            
            # 分隔线
            separator = tkinter.Frame(copy_window, height=2, bg = self.UIConfig['color_003'])
            separator.pack(fill = tkinter.X, padx = 15, pady = 5)
            
            # 目标账号选择
            frame_target = tkinter.Frame(copy_window, bg = self.UIConfig['color_001'])
            frame_target.pack(pady = 10)
            
            label_target = tkinter.Label(
                frame_target,
                text = '目标账号:',
                font = ('等线', 10),
                bg = self.UIConfig['color_001'],
                fg = self.UIConfig['color_004']
            )
            label_target.pack(side = tkinter.LEFT, padx = (0, 5))
            
            # 获取目标账号列表（排除源账号）
            account_list = []
            for botHash in OlivaDiceNativeGUI.load.dictBotInfo:
                if botHash == source_bot_hash:
                    continue
                bot_info = OlivaDiceNativeGUI.load.dictBotInfo[botHash]
                bot_name = self.get_bot_display_name(botHash, bot_info)
                bot_id = str(bot_info.id) if hasattr(bot_info, 'id') and bot_info.id else "未知"
                account_key = f"{bot_name} ({bot_id}) - {botHash[:8]}..."
                account_list.append((account_key, botHash))
            
            target_var = tkinter.StringVar()
            combo_target = ttk.Combobox(frame_target, textvariable = target_var, width = 42)
            combo_target.configure(state='readonly')
            combo_target['values'] = tuple([item[0] for item in account_list])
            if account_list:
                combo_target.current(0)
            combo_target.pack(side = tkinter.LEFT)
            
            # 按钮
            frame_buttons = tkinter.Frame(copy_window, bg = self.UIConfig['color_001'])
            frame_buttons.pack(pady = 15)
            
            def do_copy():
                target_idx = combo_target.current()
                if target_idx < 0:
                    messagebox.showwarning("警告", "请选择目标账号")
                    return
                
                target_hash = account_list[target_idx][1]
                
                # 检查账号不能为unity（大小写模糊）
                if source_bot_hash.lower() == "unity":
                    messagebox.showerror("错误", "源账号不能为unity")
                    return
                if target_hash.lower() == "unity":
                    messagebox.showerror("错误", "目标账号不能为unity")
                    return
                
                if not messagebox.askyesno("确认", 
                    f"确定要将源账号数据复制到目标账号吗？\n\n源账号: {source_bot_name} ({source_bot_id})\n目标账号: {account_list[target_idx][0]}\n\n目标账号的现有数据会被备份"):
                    return
                
                try:
                    success, result = OlivaDiceMaster.accountManager.importAccountData(
                        source_bot_hash, target_hash, OlivaDiceNativeGUI.load.globalProc, overwrite=False
                    )
                    
                    if success:
                        messagebox.showinfo("成功", result)
                        copy_window.destroy()
                        self.refresh_account_list()
                    else:
                        messagebox.showerror("失败", result)
                except Exception as e:
                    messagebox.showerror("错误", f"复制失败：{str(e)}")
            
            button_ok = tkinter.Button(
                frame_buttons,
                text = '确定',
                command = do_copy,
                bd = 0,
                bg = self.UIConfig['color_003'],
                fg = self.UIConfig['color_004'],
                relief = 'groove',
                height = 2,
                width = 10
            )
            button_ok.pack(side = tkinter.LEFT, padx = 5)
            
            button_cancel = tkinter.Button(
                frame_buttons,
                text = '取消',
                command = copy_window.destroy,
                bd = 0,
                bg = self.UIConfig['color_003'],
                fg = self.UIConfig['color_004'],
                relief = 'groove',
                height = 2,
                width = 10
            )
            button_cancel.pack(side = tkinter.LEFT, padx = 5)
            
        except Exception as e:
            messagebox.showerror("错误", f"打开复制对话框失败：{str(e)}")

    def export_to_zip(self):
        """导出源账号到压缩包"""
        try:
            # 获取选中的账号
            selection = self.UIObject['tree_account'].selection()
            if not selection:
                messagebox.showwarning("警告", "请先在账号列表中选择要导出的账号")
                return
            
            # 获取选中账号的信息
            item = self.UIObject['tree_account'].item(selection[0])
            values = item['values']
            bot_hash = values[3]
            bot_name = values[1]
            
            # 选择保存路径
            default_filename = f"account_export_{bot_hash}.zip"
            file_path = filedialog.asksaveasfilename(
                title="导出账号数据到压缩包",
                defaultextension=".zip",
                initialfile=default_filename,
                initialdir='./plugin/export',
                filetypes=[("压缩文件", "*.zip"), ("所有文件", "*.*")]
            )
            
            if not file_path:
                return
            
            if not messagebox.askyesno("确认", f"确定要导出账号 {bot_name} 的数据到:\n{file_path}\n吗？"):
                return
            
            try:
                success, result = OlivaDiceMaster.accountManager.exportAccountData(
                    bot_hash, OlivaDiceNativeGUI.load.globalProc, file_path
                )
                
                if success:
                    messagebox.showinfo("成功", result)
                else:
                    messagebox.showerror("失败", result)
            except Exception as e:
                messagebox.showerror("错误", f"导出失败：{str(e)}")
                
        except Exception as e:
            messagebox.showerror("错误", f"导出账号数据失败：{str(e)}")

    def import_from_zip(self):
        """从压缩包导入到指定账号（基于选定的账号作为目标）"""
        try:
            # 获取选中的账号作为目标账号
            selection = self.UIObject['tree_account'].selection()
            if not selection:
                messagebox.showwarning("警告", "请先在账号列表中选择目标账号")
                return
            
            # 获取选中账号的信息
            item = self.UIObject['tree_account'].item(selection[0])
            values = item['values']
            target_bot_hash = values[3]  # Hash在第4列
            target_bot_name = values[1]  # 名称在第2列
            target_bot_id = values[2]    # ID在第3列
            
            # 选择压缩包文件
            zip_path = filedialog.askopenfilename(
                title="选择账号数据压缩包",
                initialdir='./plugin/export',
                filetypes=[("压缩文件", "*.zip"), ("所有文件", "*.*")]
            )
            
            if not zip_path:
                return
            
            # 尝试从文件名自动识别源Hash
            auto_detected_hash = None
            filename = os.path.basename(zip_path)
            # 匹配 account_export_xxxxx.zip 或 account_import_xxxxx.zip 格式
            match = re.match(r'account_(?:export_|import_)?([a-f0-9]+)\.zip', filename, re.IGNORECASE)
            if match:
                auto_detected_hash = match.group(1)
            
            # 创建对话框
            import_zip_window = tkinter.Toplevel(self.UIObject['root'])
            import_zip_window.title('从压缩包导入')
            import_zip_window.geometry('520x380')
            import_zip_window.resizable(False, False)
            import_zip_window.configure(bg = self.UIConfig['color_001'])
            
            # 显示压缩包信息
            frame_zip_info = tkinter.Frame(import_zip_window, bg = self.UIConfig['color_001'])
            frame_zip_info.pack(pady = (15, 10), fill = tkinter.X, padx = 15)
            
            label_zip_title = tkinter.Label(
                frame_zip_info,
                text = '源压缩包：',
                font = ('等线', 11, 'bold'),
                bg = self.UIConfig['color_001'],
                fg = self.UIConfig['color_004']
            )
            label_zip_title.pack(anchor = 'w')
            
            zip_info_text = f"  文件: {os.path.basename(zip_path)}\n  路径: {zip_path}"
            
            label_zip_info = tkinter.Label(
                frame_zip_info,
                text = zip_info_text,
                font = ('等线', 9),
                bg = self.UIConfig['color_001'],
                fg = self.UIConfig['color_006'],
                justify = 'left'
            )
            label_zip_info.pack(anchor = 'w', padx = 10)
            
            # 分隔线
            separator1 = tkinter.Frame(import_zip_window, height=2, bg = self.UIConfig['color_003'])
            separator1.pack(fill = tkinter.X, padx = 15, pady = 5)
            
            # 显示目标账号信息（固定，不可更改）
            frame_target_info = tkinter.Frame(import_zip_window, bg = self.UIConfig['color_001'])
            frame_target_info.pack(pady = (10, 10), fill = tkinter.X, padx = 15)
            
            label_target_title = tkinter.Label(
                frame_target_info,
                text = '目标账号（已选定）：',
                font = ('等线', 11, 'bold'),
                bg = self.UIConfig['color_001'],
                fg = self.UIConfig['color_004']
            )
            label_target_title.pack(anchor = 'w')
            
            target_info_text = f"  名称: {target_bot_name}\n  ID: {target_bot_id}\n  Hash: {target_bot_hash}"
            label_target_info = tkinter.Label(
                frame_target_info,
                text = target_info_text,
                font = ('等线', 10),
                bg = self.UIConfig['color_001'],
                fg = self.UIConfig['color_006'],
                justify = 'left'
            )
            label_target_info.pack(anchor = 'w', padx = 10)
            
            # 分隔线
            separator2 = tkinter.Frame(import_zip_window, height=2, bg = self.UIConfig['color_003'])
            separator2.pack(fill = tkinter.X, padx = 15, pady = 5)
            
            # 源账号Hash输入区域
            frame_source_hash = tkinter.Frame(import_zip_window, bg = self.UIConfig['color_001'])
            frame_source_hash.pack(pady = (10, 10), fill = tkinter.X, padx = 15)
            
            label_source_hash = tkinter.Label(
                frame_source_hash,
                text = '源账号Hash:',
                font = ('等线', 10),
                bg = self.UIConfig['color_001'],
                fg = self.UIConfig['color_004']
            )
            label_source_hash.pack(side = tkinter.LEFT, padx = (0, 5))
            
            source_hash_var = tkinter.StringVar()
            if auto_detected_hash:
                source_hash_var.set(auto_detected_hash)
            entry_source_hash = tkinter.Entry(
                frame_source_hash,
                textvariable = source_hash_var,
                width = 45,
                font = ('等线', 9)
            )
            entry_source_hash.pack(side = tkinter.LEFT)
            
            if not auto_detected_hash:
                # 如果自动识别失败，显示提示
                label_hint = tkinter.Label(
                    frame_source_hash,
                    text = '（自动识别失败，请手动输入）',
                    font = ('等线', 8),
                    bg = self.UIConfig['color_001'],
                    fg = self.UIConfig['color_006']
                )
                label_hint.pack(side = tkinter.LEFT, padx = (5, 0))
            
            # 按钮
            frame_buttons = tkinter.Frame(import_zip_window, bg = self.UIConfig['color_001'])
            frame_buttons.pack(pady = 15)
            
            def do_import():
                source_hash = source_hash_var.get().strip()
                
                if not source_hash:
                    messagebox.showwarning("警告", "请输入源账号Hash")
                    return
                
                # 验证Hash格式（应该是十六进制字符串）
                if not re.match(r'^[a-f0-9]+$', source_hash, re.IGNORECASE):
                    messagebox.showerror("错误", "源账号Hash格式不正确，应为十六进制字符串")
                    return
                
                # 检查账号不能为unity（大小写模糊）
                if source_hash.lower() == "unity":
                    messagebox.showerror("错误", "源账号不能为unity")
                    return
                if target_bot_hash.lower() == "unity":
                    messagebox.showerror("错误", "目标账号不能为unity")
                    return
                
                if not messagebox.askyesno("确认", 
                    f"确定要从压缩包导入数据到目标账号吗？\n\n压缩包: {os.path.basename(zip_path)}\n源账号Hash: {source_hash}\n目标账号: {target_bot_name} ({target_bot_id})\nHash: {target_bot_hash}\n\n目标账号的现有数据会被备份"):
                    return
                
                try:
                    success, result, auto_hash = OlivaDiceMaster.accountManager.importAccountDataFromZip(
                        zip_path, target_bot_hash, OlivaDiceNativeGUI.load.globalProc, overwrite=False, sourceBotHash=source_hash
                    )
                    
                    if success:
                        messagebox.showinfo("成功", result)
                        import_zip_window.destroy()
                        self.refresh_account_list()
                    else:
                        messagebox.showerror("失败", result)
                except Exception as e:
                    messagebox.showerror("错误", f"导入失败：{str(e)}")
            
            button_ok = tkinter.Button(
                frame_buttons,
                text = '确定',
                command = do_import,
                bd = 0,
                bg = self.UIConfig['color_003'],
                fg = self.UIConfig['color_004'],
                relief = 'groove',
                height = 2,
                width = 10
            )
            button_ok.pack(side = tkinter.LEFT, padx = 5)
            
            button_cancel = tkinter.Button(
                frame_buttons,
                text = '取消',
                command = import_zip_window.destroy,
                bd = 0,
                bg = self.UIConfig['color_003'],
                fg = self.UIConfig['color_004'],
                relief = 'groove',
                height = 2,
                width = 10
            )
            button_cancel.pack(side = tkinter.LEFT, padx = 5)
            
        except Exception as e:
            messagebox.showerror("错误", f"打开导入对话框失败：{str(e)}")

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

    def init_frame_deck(self):
        self.UIObject['frame_deck_root'] = tkinter.Frame(self.UIObject['Notebook_root'])
        self.UIObject['frame_deck_root'].configure(relief = tkinter.FLAT)
        self.UIObject['frame_deck_root'].grid(
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
        self.UIObject['frame_deck_root'].grid_rowconfigure(0, weight = 0)
        self.UIObject['frame_deck_root'].grid_rowconfigure(1, weight = 0)
        self.UIObject['frame_deck_root'].grid_rowconfigure(2, weight = 0)
        self.UIObject['frame_deck_root'].grid_rowconfigure(3, weight = 0)
        self.UIObject['frame_deck_root'].grid_rowconfigure(4, weight = 0)
        self.UIObject['frame_deck_root'].grid_rowconfigure(5, weight = 0)
        self.UIObject['frame_deck_root'].grid_rowconfigure(6, weight = 0)
        self.UIObject['frame_deck_root'].grid_rowconfigure(7, weight = 15)
        self.UIObject['frame_deck_root'].grid_columnconfigure(0, weight = 30)
        self.UIObject['frame_deck_root'].grid_columnconfigure(1, weight = 0)
        self.UIObject['frame_deck_root'].grid_columnconfigure(2, weight = 0)
        self.UIObject['frame_deck_root'].grid_columnconfigure(3, weight = 0)
        self.UIObject['frame_deck_root'].grid_columnconfigure(4, weight = 0)
        self.UIObject['frame_deck_root'].grid_columnconfigure(5, weight = 30)
        self.UIObject['frame_deck_root'].grid_columnconfigure(6, weight = 0)
        tmp_tree_rowspan = 7
        self.UIObject['frame_deck_root'].configure(bg = self.UIConfig['color_001'], borderwidth = 0)
        self.UIData['deck_local_now'] = None
        self.UIData['deck_remote_now'] = None
        self.UIData['label_deck_remote_note_StringVar_origin'] = '牌堆市场 ☁'
        self.UIData['label_deck_remote_note_StringVar_load'] = '正在刷新 ☁'
        self.UIData['label_deck_remote_note_StringVar_failed'] = '刷新失败 ☁'
        self.UIData['label_deck_remote_note_StringVar'] = tkinter.StringVar()

        self.UIObject['label_deck_local_note'] = tkinter.Label(
            self.UIObject['frame_deck_root'],
            text = '本地牌堆'
        )
        self.UIObject['label_deck_local_note'].configure(
            bg = self.UIConfig['color_001'],
            fg = self.UIConfig['color_004'],
            font = ('等线', 12)
        )
        self.UIObject['label_deck_local_note'].grid(
            row = 0,
            column = 0,
            sticky = "nw",
            rowspan = 1,
            columnspan = 9,
            padx = (0, 0),
            pady = (10, 5),
            ipadx = 0,
            ipady = 0
        )

        self.UIObject['tree_deck_local'] = ttk.Treeview(self.UIObject['frame_deck_root'])
        self.UIObject['tree_deck_local']['show'] = 'headings'
        self.UIObject['tree_deck_local']['columns'] = ('KEY')
        self.UIObject['tree_deck_local'].column('KEY', width = 50)
        self.UIObject['tree_deck_local'].heading('KEY', text = '牌堆名')
        self.UIObject['tree_deck_local'].grid(
            row = 1,
            column = 0,
            sticky = "nsew",
            rowspan = tmp_tree_rowspan,
            columnspan = 1,
            padx = (0, 0),
            pady = (0, 0),
            ipadx = 0,
            ipady = 0
        )
        #self.UIObject['tree_rightkey_menu'] = tkinter.Menu(self.UIObject['root'], tearoff = False)
        #self.UIObject['tree_master'].bind('<Button-3>', lambda x : self.tree_master_rightKey(x))
        self.UIObject['tree_deck_local'].bind('<<TreeviewSelect>>', lambda x : self.treeSelect('tree_deck_local', x))
        self.UIObject['tree_deck_local_yscroll'] = ttk.Scrollbar(
            self.UIObject['frame_deck_root'],
            orient = "vertical",
            command = self.UIObject['tree_deck_local'].yview
        )
        self.UIObject['tree_deck_local'].configure(
            yscrollcommand = self.UIObject['tree_deck_local_yscroll'].set
        )
        self.UIObject['tree_deck_local_yscroll'].grid(
            row = 1,
            column = 1,
            sticky = "nsw",
            rowspan = tmp_tree_rowspan,
            columnspan = 1,
            padx = (0, 0),
            pady = (0, 0),
            ipadx = 0,
            ipady = 0
        )

        self.UIObject['buttom_deck_reload'] = tkinter.Button(
            self.UIObject['frame_deck_root'],
            text = '重载牌堆',
            command = self.reloadDeck_local_gen(),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
        )
        self.UIObject['buttom_deck_reload'].configure(
            font = ('等线', 12)
        )
        self.UIObject['buttom_deck_reload'].bind('<Enter>', lambda x : self.buttom_action('buttom_deck_reload', '<Enter>'))
        self.UIObject['buttom_deck_reload'].bind('<Leave>', lambda x : self.buttom_action('buttom_deck_reload', '<Leave>'))
        self.UIObject['buttom_deck_reload'].grid(
            row = 1,
            column = 2,
            sticky = "new",
            rowspan = 1,
            columnspan = 3,
            padx = (15, 15),
            pady = (0, 2),
            ipadx = 0,
            ipady = 0
        )

        self.UIObject['buttom_deck_remove'] = tkinter.Button(
            self.UIObject['frame_deck_root'],
            text = '删除牌堆 ×',
            command = self.removeDeck_gen(),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
        )
        self.UIObject['buttom_deck_remove'].configure(
            font = ('等线', 12)
        )
        self.UIObject['buttom_deck_remove'].bind('<Enter>', lambda x : self.buttom_action('buttom_deck_remove', '<Enter>'))
        self.UIObject['buttom_deck_remove'].bind('<Leave>', lambda x : self.buttom_action('buttom_deck_remove', '<Leave>'))
        self.UIObject['buttom_deck_remove'].grid(
            row = 2,
            column = 2,
            sticky = "new",
            rowspan = 1,
            columnspan = 1,
            padx = (15, 2),
            pady = (2, 2),
            ipadx = 0,
            ipady = 0
        )

        self.UIObject['buttom_deck_dir_unity'] = tkinter.Button(
            self.UIObject['frame_deck_root'],
            text = '打开全局目录',
            command = self.openDeckPath_gen(flagUnity = True),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
        )
        self.UIObject['buttom_deck_dir_unity'].configure(
            font = ('等线', 12)
        )
        self.UIObject['buttom_deck_dir_unity'].bind('<Enter>', lambda x : self.buttom_action('buttom_deck_dir_unity', '<Enter>'))
        self.UIObject['buttom_deck_dir_unity'].bind('<Leave>', lambda x : self.buttom_action('buttom_deck_dir_unity', '<Leave>'))
        self.UIObject['buttom_deck_dir_unity'].grid(
            row = 5,
            column = 2,
            sticky = "new",
            rowspan = 1,
            columnspan = 1,
            padx = (15, 2),
            pady = (60, 2),
            ipadx = 0,
            ipady = 0
        )

        self.UIObject['buttom_deck_dir_this'] = tkinter.Button(
            self.UIObject['frame_deck_root'],
            text = '打开本机目录',
            command = self.openDeckPath_gen(flagUnity = False),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
        )
        self.UIObject['buttom_deck_dir_this'].configure(
            font = ('等线', 12)
        )
        self.UIObject['buttom_deck_dir_this'].bind('<Enter>', lambda x : self.buttom_action('buttom_deck_dir_this', '<Enter>'))
        self.UIObject['buttom_deck_dir_this'].bind('<Leave>', lambda x : self.buttom_action('buttom_deck_dir_this', '<Leave>'))
        self.UIObject['buttom_deck_dir_this'].grid(
            row = 6,
            column = 2,
            sticky = "new",
            rowspan = 1,
            columnspan = 1,
            padx = (15, 2),
            pady = (2, 2),
            ipadx = 0,
            ipady = 0
        )

        self.UIObject['buttom_deck_install_unity'] = tkinter.Button(
            self.UIObject['frame_deck_root'],
            text = '安装至全局 <<',
            command = self.installDeck_gen(flagUnity = True),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
        )
        self.UIObject['buttom_deck_install_unity'].configure(
            font = ('等线', 12)
        )
        self.UIObject['buttom_deck_install_unity'].bind('<Enter>', lambda x : self.buttom_action('buttom_deck_install_unity', '<Enter>'))
        self.UIObject['buttom_deck_install_unity'].bind('<Leave>', lambda x : self.buttom_action('buttom_deck_install_unity', '<Leave>'))
        self.UIObject['buttom_deck_install_unity'].grid(
            row = 2,
            column = 4,
            sticky = "new",
            rowspan = 1,
            columnspan = 1,
            padx = (2, 15),
            pady = (2, 2),
            ipadx = 0,
            ipady = 0
        )

        self.UIObject['buttom_deck_install_this'] = tkinter.Button(
            self.UIObject['frame_deck_root'],
            text = '安装至本机 <<',
            command = self.installDeck_gen(flagUnity = False),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
        )
        self.UIObject['buttom_deck_install_this'].configure(
            font = ('等线', 12)
        )
        self.UIObject['buttom_deck_install_this'].bind('<Enter>', lambda x : self.buttom_action('buttom_deck_install_this', '<Enter>'))
        self.UIObject['buttom_deck_install_this'].bind('<Leave>', lambda x : self.buttom_action('buttom_deck_install_this', '<Leave>'))
        self.UIObject['buttom_deck_install_this'].grid(
            row = 3,
            column = 4,
            sticky = "new",
            rowspan = 1,
            columnspan = 1,
            padx = (2, 15),
            pady = (2, 2),
            ipadx = 0,
            ipady = 0
        )

        self.UIObject['buttom_deck_upload'] = tkinter.Button(
            self.UIObject['frame_deck_root'],
            text = '上传牌堆',
            command = self.uploadDeckUrl_gen(),
            bd = 0,
            activebackground = self.UIConfig['color_002'],
            activeforeground = self.UIConfig['color_001'],
            bg = self.UIConfig['color_003'],
            fg = self.UIConfig['color_004'],
            relief = 'groove',
            height = 2,
        )
        self.UIObject['buttom_deck_upload'].configure(
            font = ('等线', 12)
        )
        self.UIObject['buttom_deck_upload'].bind('<Enter>', lambda x : self.buttom_action('buttom_deck_upload', '<Enter>'))
        self.UIObject['buttom_deck_upload'].bind('<Leave>', lambda x : self.buttom_action('buttom_deck_upload', '<Leave>'))
        self.UIObject['buttom_deck_upload'].grid(
            row = 6,
            column = 4,
            sticky = "new",
            rowspan = 1,
            columnspan = 1,
            padx = (2, 15),
            pady = (2, 2),
            ipadx = 0,
            ipady = 0
        )

        self.UIObject['label_deck_remote_note'] = tkinter.Label(
            self.UIObject['frame_deck_root'],
            textvariable = self.UIData['label_deck_remote_note_StringVar']
        )
        self.UIData['label_deck_remote_note_StringVar'].set(
            value = self.UIData['label_deck_remote_note_StringVar_origin']
        )
        self.UIObject['label_deck_remote_note'].configure(
            bg = self.UIConfig['color_001'],
            fg = self.UIConfig['color_004'],
            font = ('等线', 12)
        )
        self.UIObject['label_deck_remote_note'].grid(
            row = 0,
            column = 5,
            sticky = "nw",
            rowspan = 1,
            columnspan = 9,
            padx = (0, 0),
            pady = (10, 5),
            ipadx = 0,
            ipady = 0
        )

        self.UIObject['tree_deck_remote'] = ttk.Treeview(self.UIObject['frame_deck_root'])
        self.UIObject['tree_deck_remote']['show'] = 'headings'
        self.UIObject['tree_deck_remote']['columns'] = ('KEY', 'AUTHOR')
        self.UIObject['tree_deck_remote'].column('KEY', width = 35)
        self.UIObject['tree_deck_remote'].column('AUTHOR', width = 15)
        self.UIObject['tree_deck_remote'].heading('KEY', text = '牌堆名')
        self.UIObject['tree_deck_remote'].heading('AUTHOR', text = '作者')
        self.UIObject['tree_deck_remote'].grid(
            row = 1,
            column = 5,
            sticky = "nsew",
            rowspan = tmp_tree_rowspan,
            columnspan = 1,
            padx = (0, 0),
            pady = (0, 0),
            ipadx = 0,
            ipady = 0
        )
        #self.UIObject['tree_rightkey_menu'] = tkinter.Menu(self.UIObject['root'], tearoff = False)
        #self.UIObject['tree_master'].bind('<Button-3>', lambda x : self.tree_master_rightKey(x))
        self.UIObject['tree_deck_remote'].bind('<<TreeviewSelect>>', lambda x : self.treeSelect('tree_deck_remote', x))
        self.UIObject['tree_deck_remote_yscroll'] = ttk.Scrollbar(
            self.UIObject['frame_deck_root'],
            orient = "vertical",
            command = self.UIObject['tree_deck_remote'].yview
        )
        self.UIObject['tree_deck_remote'].configure(
            yscrollcommand = self.UIObject['tree_deck_remote_yscroll'].set
        )
        self.UIObject['tree_deck_remote_yscroll'].grid(
            row = 1,
            column = 6,
            sticky = "nsw",
            rowspan = tmp_tree_rowspan,
            columnspan = 1,
            padx = (0, 0),
            pady = (0, 0),
            ipadx = 0,
            ipady = 0
        )

        self.UIData['label_deck_note_StringVar'] = tkinter.StringVar()
        self.UIObject['label_deck_note'] = tkinter.Text(
            self.UIObject['frame_deck_root'],
            wrap=tkinter.CHAR,
            width=30
        )
        self.UIObject['label_deck_note'].configure(
            bg = self.UIConfig['color_001'],
            fg = self.UIConfig['color_004'],
            bd = 0,
            font = ('等线', 11),
            padx = 4,
            pady = 8,
            state = tkinter.DISABLED,
            relief = tkinter.FLAT
        )
        self.UIObject['label_deck_note'].grid(
            row = 7,
            column = 2,
            sticky = "nswe",
            rowspan = 1,
            columnspan = 3,
            padx = (15, 15),
            pady = (20, 0),
            ipadx = 0,
            ipady = 0
        )

    def reload_deck_info(self):
        self.UIObject['label_deck_note'].configure(state=tkinter.NORMAL)
        tmp_dataList = OlivaDiceOdyssey.webTool.gExtiverseDeck
        tmp_deckName = self.UIData['deck_remote_now']
        self.UIObject['label_deck_note'].delete('1.0', tkinter.END)
        for deck_type_this in ['classic', 'yaml', 'excel']:
            if type(tmp_dataList) is dict \
            and deck_type_this in tmp_dataList \
            and type(tmp_dataList[deck_type_this]) is list:
                for deck_this in tmp_dataList[deck_type_this]:
                    if 'name' in deck_this \
                    and 'desc' in deck_this \
                    and 'version' in deck_this \
                    and 'version_code' in deck_this \
                    and 'author' in deck_this \
                    and 'type' in deck_this \
                    and 'sub_type' in deck_this \
                    and deck_this['name'] == tmp_deckName:
                        tmp_text = '%s\n\n%s\n作者: %s\n版本: %s(%s)\n\n%s' % (
                            str(deck_this['name']),
                            str({
                                'classic': '青果系JSON',
                                'yaml': '塔系YAML',
                                'excel': '梨系Excel'
                            }.get(deck_this['sub_type'], '新型')
                            ) + str({
                                'deck': '牌堆',
                            }.get(deck_this['type'], '未知扩展')),
                            str(deck_this['author']),
                            str(deck_this['version']),
                            str(deck_this['version_code']),
                            str(deck_this['desc'])
                        )
                        self.UIObject['label_deck_note'].insert('1.0', tmp_text)
                        break
        self.UIObject['label_deck_note'].configure(state=tkinter.DISABLED)

    def reloadDeck_local_gen(self):
        def reloadDeck_local_fun():
            try:
                OlivaDiceCore.drawCard.reloadDeck()
            except:
                pass
            self.init_data_deck_local()
        return reloadDeck_local_fun

    def installDeck_gen(self, flagUnity = False):
        def installDeck_fun():
            botHash = 'unity'
            deckName = self.UIData['deck_remote_now']
            if flagUnity:
                botHash = 'unity'
            else:
                botHash = self.UIData['hash_now']
            try:
                OlivaDiceOdyssey.webTool.downloadExtiverseDeckRemote(
                    name = deckName,
                    botHash = botHash
                )
                OlivaDiceCore.drawCard.reloadDeck()
            except:
                pass
            self.init_data_deck_local()
        return installDeck_fun

    def removeDeck_gen(self):
        def removeDeck_fun():
            deckName = self.UIData['deck_local_now']
            botHash = self.UIData['hash_now']
            try:
                OlivaDiceCore.drawCard.removeDeck(
                    botHash = botHash,
                    deckName = deckName
                )
                OlivaDiceCore.drawCard.removeDeck(
                    botHash = 'unity',
                    deckName = deckName
                )
                OlivaDiceCore.drawCard.reloadDeck()
            except Exception as e:
                traceback.print_exc()
            self.init_data_deck_local()
        return removeDeck_fun

    def openDeckPath_gen(self, flagUnity = False):
        def openDeckPath_fun():
            botHash = 'unity'
            deckName = self.UIData['deck_remote_now']
            if flagUnity:
                botHash = 'unity'
            else:
                botHash = self.UIData['hash_now']
            deck_path = os.path.join('plugin', 'data', 'OlivaDice', botHash, 'extend')
            try:
                os.startfile(deck_path)
            except:
                pass
        return openDeckPath_fun

    def uploadDeckUrl_gen(self):
        def uploadDeckUrl_fun():
            self.show_project_site('https://github.com/OlivOS-Team/Extiverse')
        return uploadDeckUrl_fun

    def onNotebookTabChanged(self, event):
        curTab = self.UIObject['Notebook_root'].tab(self.UIObject['Notebook_root'].select(), "text")
        if curTab == '牌堆管理':
            self.init_data_deck_local()
            # 异步执行
            threading.Thread(target = self.onNotebookTabChanged_init_data_deck_remote).start()


    def onNotebookTabChanged_init_data_deck_remote(self):
        if not self.UIData['deck_remote_loaded_flag']:
            # 仅在第一次切过来时刷新
            self.UIData['deck_remote_loaded_flag'] = True
            self.UIData['label_deck_remote_note_StringVar'].set(
                value = self.UIData['label_deck_remote_note_StringVar_load']
            )
            # 可以考虑在网络操作前就进行一次清空
            #self.init_data_deck_remote_pre()
            try:
                OlivaDiceOdyssey.webTool.getExtiverseDeckRemote()
            except:
                self.UIData['label_deck_remote_note_StringVar'].set(
                    value = self.UIData['label_deck_remote_note_StringVar_failed']
                )
            self.init_data_deck_remote()
            self.UIData['label_deck_remote_note_StringVar'].set(
                value = self.UIData['label_deck_remote_note_StringVar_origin']
            )

    def treeSelect(self, name, x):
        if name == 'tree_master':
            force = get_tree_force(self.UIObject['tree_master'])
            self.UIData['entry_master_StringVar'].set(str(force['text']))
        if name == 'tree_deck_local':
            force = get_tree_force(self.UIObject['tree_deck_local'])
            self.UIData['deck_local_now'] = str(force['text'])
        if name == 'tree_deck_remote':
            force = get_tree_force(self.UIObject['tree_deck_remote'])
            self.UIData['deck_remote_now'] = str(force['text'])
            self.reload_deck_info()

    def tree_str_rightKey(self, event):
        self.UIObject['tree_rightkey_menu'].delete(0, tkinter.END)
        self.UIObject['tree_rightkey_menu'].add_command(label = '编辑', command = lambda : self.tree_str_edit())
        self.UIObject['tree_rightkey_menu'].add_command(label='恢复/删除', command=lambda: self.reset_selected_str())
        self.UIObject['tree_rightkey_menu'].post(event.x_root, event.y_root)

    def tree_console_rightKey(self, event):
        self.UIObject['tree_rightkey_menu'].delete(0, tkinter.END)
        self.UIObject['tree_rightkey_menu'].add_command(label = '编辑', command = lambda : self.tree_console_edit())
        self.UIObject['tree_rightkey_menu'].add_command(label='恢复/删除', command=lambda: self.reset_selected_console())
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

    def edit_restore_modules(self):
        """打开恢复模块配置的UI"""
        self.edit_modules_UI(
            root_obj=self.UIObject['root'],
            root_class=self,
            hash_selection=self.UIData['hash_now']
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

    class edit_modules_UI(object):
        def __init__(self, root_obj, root_class, hash_selection):
            self.root = root_obj
            self.root_class = root_class
            self.hash = hash_selection
            self.UIObject = {}
            self.UIConfig = {}
            self.UIConfig.update(dictColorContext)

        def start(self):
            self.UIObject['root'] = tkinter.Toplevel(self.root)
            self.UIObject['root'].title('配置恢复模块')
            self.UIObject['root'].geometry('400x450')
            self.UIObject['root'].minsize(400, 450)
            self.UIObject['root'].resizable(True, True)
            self.UIObject['root'].grid_rowconfigure(0, weight=0)
            self.UIObject['root'].grid_rowconfigure(1, weight=1)
            self.UIObject['root'].grid_columnconfigure(0, weight=1)
            self.UIObject['root'].configure(bg=self.UIConfig['color_001'])

            # 说明标签
            label_info = tkinter.Label(
                self.UIObject['root'],
                text='''在此处编辑恢复模块列表，每行一个模块名。
恢复操作将从这些模块加载默认回复词。
注意：
1. 模块名必须与模块命名空间一致，且区分大小写。
2. 若选择的模块不存在
或没有在该模块的msgCustom.py里定义默认回复词，
则会跳过该模块。
3. 不同 Bot 的恢复模块配置是独立的。
4. 设置完毕后实时更新，无需重载插件。
5. 若需要恢复默认模块列表，请清空文本框。
6. 若不知道这里是做什么的，请不要随意修改。''',
                font=('等线', 11),
                bg=self.UIConfig['color_001'],
                fg=self.UIConfig['color_004'],
                justify='left'
            )
            label_info.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="ew")

            # 文本框
            self.UIObject['text_modules'] = tkinter.Text(
                self.UIObject['root'],
                wrap=tkinter.WORD,
                bg=self.UIConfig['color_004'],
                fg=self.UIConfig['color_005'],
                bd=0,
                font=(None, 10),
                padx=4,
                pady=8
            )
            self.UIObject['text_modules'].grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")

            # 加载当前模块
            current_modules = self.root_class.load_recover_modules(self.hash)
            self.UIObject['text_modules'].insert('1.0', '\n'.join(current_modules))
            
            # 绑定关闭事件
            self.UIObject['root'].protocol("WM_DELETE_WINDOW", self.quit)
            self.UIObject['root'].iconbitmap('./resource/tmp_favoricon.ico')
            self.UIObject['root'].mainloop()

        def quit(self):
            self.save()
            self.UIObject['root'].destroy()

        def save(self):
            """获取文本框内容并保存"""
            content = self.UIObject['text_modules'].get('1.0', tkinter.END)
            # 按行分割，并移除空行和首尾空格
            modules_list = [line.strip() for line in content.splitlines() if line.strip()]
            self.root_class.save_recover_modules(self.hash, modules_list)

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

    class edit_backup_UI(object):
        def __init__(self, root_class, key, value):
            self.root_class = root_class
            self.key = key
            self.value = value
            self.UIObject = {}
            self.UIData = {}
            self.UIConfig = {}
            self.UIConfig.update(dictColorContext)
            self.start()
            
        def start(self):
            self.UIObject['root'] = tkinter.Toplevel(self.root_class.UIObject['root'])
            self.UIObject['root'].title('修改备份配置 - %s' % self.key)
            self.UIObject['root'].minsize(400, 10)
            self.UIObject['root'].resizable(
                width = True,
                height = False
            )
            self.UIObject['root'].grid_rowconfigure(0, weight = 0)
            self.UIObject['root'].grid_rowconfigure(1, weight = 15)
            self.UIObject['root'].grid_columnconfigure(0, weight = 15)
            self.UIObject['root'].configure(bg = self.UIConfig['color_001'])

            # 获取说明信息
            tmp_info = '无说明'
            if self.key in OlivaDiceNativeGUI.msgCustom.dictBackupConfigNote:
                tmp_info = OlivaDiceNativeGUI.msgCustom.dictBackupConfigNote[self.key]

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
            self.UIData['entry_edit_StringVar'].set(str(self.value))

            self.UIObject['root'].iconbitmap('./resource/tmp_favoricon.ico')
            self.UIObject['root'].protocol("WM_DELETE_WINDOW", self.quit)
            self.UIObject['root'].mainloop()

        def quit(self):
            self.save()
            if self.root_class != None:
                self.root_class.init_data_total()
            self.UIObject['root'].destroy()

        def save(self):
            tmp_new_str = self.UIData['entry_edit_StringVar'].get().strip()
            
            # 验证和转换数据
            try:
                if self.key == 'startDate':
                    # 验证日期格式 yyyy-MM-dd
                    import datetime
                    import re
                    # 先检查格式是否严格为 yyyy-MM-dd
                    if not re.match(r'^\d{4}-\d{2}-\d{2}$', tmp_new_str):
                        raise ValueError("日期格式必须为 yyyy-MM-dd")
                    # 再验证日期是否有效
                    datetime.datetime.strptime(tmp_new_str, '%Y-%m-%d')
                    final_value = tmp_new_str
                elif self.key == 'passDay':
                    # 验证整数
                    final_value = int(tmp_new_str)
                    if final_value <= 0:
                        raise ValueError("天数不能为负数或0")
                elif self.key == 'backupTime':
                    # 验证时间格式 HH:mm:ss
                    import datetime
                    import re
                    # 先检查格式是否严格为 HH:mm:ss（两位数:两位数:两位数）
                    if not re.match(r'^\d{2}:\d{2}:\d{2}$', tmp_new_str):
                        raise ValueError("时间格式必须为 HH:mm:ss")
                    # 再验证时间是否有效
                    datetime.datetime.strptime(tmp_new_str, '%H:%M:%S')
                    final_value = tmp_new_str
                elif self.key == 'maxBackupCount':
                    # 验证整数
                    final_value = int(tmp_new_str)
                    if final_value <= 0:
                        raise ValueError("备份数量不能为负数或0")
                elif self.key == 'isBackup':
                    # 验证整数
                    final_value = int(tmp_new_str)
                    if final_value not in [0, 1]:
                        raise ValueError("备份开关只能为0或1")
                else:
                    # 其他配置项按字符串处理
                    final_value = tmp_new_str
                
                # 保存到配置中
                if 'unity' not in OlivaDiceCore.console.dictBackupConfig:
                    OlivaDiceCore.console.dictBackupConfig['unity'] = {}
                
                OlivaDiceCore.console.dictBackupConfig['unity'][self.key] = final_value
                self.root_class.save_backup_config()
                
            except ValueError as e:
                if self.key == 'startDate':
                    messagebox.showerror("格式错误", "日期格式应为 yyyy-MM-dd\n例如：2025-09-01", parent=self.UIObject['root'])
                elif self.key == 'passDay':
                    messagebox.showerror("格式错误", "天数应为非负整数\n例如：1", parent=self.UIObject['root'])
                elif self.key == 'backupTime':
                    messagebox.showerror("格式错误", "时间格式应为 HH:mm:ss\n例如：04:00:00", parent=self.UIObject['root'])
                elif self.key == 'maxBackupCount':
                    messagebox.showerror("格式错误", "备份数量必须为大于0的整数\n例如：1", parent=self.UIObject['root'])
                elif self.key == 'isBackup':
                    messagebox.showerror("格式错误", "备份开关只能为0或1\n0: 启用 1: 禁用\n例如：0", parent=self.UIObject['root'])
                else:
                    messagebox.showerror("格式错误", f"输入格式错误: {str(e)}", parent=self.UIObject['root'])
                return False
            except Exception as e:
                messagebox.showerror("保存失败", f"保存配置时出错: {str(e)}", parent=self.UIObject['root'])
                return False
            
            return True

    def init_data_total(self):
        tmp_hashSelection = self.UIData['hash_now']
        # 全局模式禁用回复词里的所有按钮
        is_global_mode = (tmp_hashSelection == 'unity')
        buttons_to_disable_in_global = ['buttom_config_restore', 'buttom_reset_str', 'buttom_import_str', 'buttom_export_str', 
                                        'buttom_refresh_str', 'buttom_reset_delete_str']
        for button_name in buttons_to_disable_in_global:
            if button_name in self.UIObject:
                state = tkinter.DISABLED if is_global_mode else tkinter.NORMAL
                self.UIObject[button_name].config(state=state)

        self.UIData['onlineStatus_Label_root_StringVar'].set('当前在线: %s' % OlivaDiceNativeGUI.load.onlineAPICount)

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

        # 备份配置树视图更新（只有在有 OlivaDiceMaster 模块时才更新）
        if OlivaDiceNativeGUI.load.masterModelFlag and 'tree_backup' in self.UIObject:
            tmp_tree_item_children = self.UIObject['tree_backup'].get_children()
            for tmp_tree_item_this in tmp_tree_item_children:
                self.UIObject['tree_backup'].delete(tmp_tree_item_this)
            if 'unity' in OlivaDiceCore.console.dictBackupConfig:
                tmp_dictBackupConfig = OlivaDiceCore.console.dictBackupConfig['unity']
                for tmp_dictBackupConfig_this in tmp_dictBackupConfig:
                    try:
                        tmp_value = str(tmp_dictBackupConfig[tmp_dictBackupConfig_this])
                        tmp_value = tmp_value.replace('\r\n', r'\r\n')
                        tmp_value = tmp_value.replace('\n', r'\n')
                        tmp_value = tmp_value.replace('\r', r'\r')
                        tmp_note = ''
                        if tmp_dictBackupConfig_this in OlivaDiceNativeGUI.msgCustom.dictBackupConfigNote:
                            tmp_note = OlivaDiceNativeGUI.msgCustom.dictBackupConfigNote[tmp_dictBackupConfig_this]
                        tmp_note = tmp_note.replace('\n', ' ')
                        tmp_note = tmp_note.replace('\r', ' ')
                        self.UIObject['tree_backup'].insert(
                            '',
                            tkinter.END,
                            text = tmp_dictBackupConfig_this,
                            values=(
                                tmp_dictBackupConfig_this,
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
        self.init_data_deck_local()


    def init_data_deck(self):
        self.init_data_deck_local()

    def init_data_deck_local(self):
        tmp_hashSelection = self.UIData['hash_now']

        self.UIData['deck_local_now'] = None
        tmp_tree_item_children = self.UIObject['tree_deck_local'].get_children()
        for tmp_tree_item_this in tmp_tree_item_children:
            self.UIObject['tree_deck_local'].delete(tmp_tree_item_this)
        tmp_dataList = OlivaDiceCore.drawCardData.dictDeckIndex
        if tmp_hashSelection in tmp_dataList and type(tmp_dataList[tmp_hashSelection]) is dict:
            for deckName_this in tmp_dataList[tmp_hashSelection]:
                try:
                    self.UIObject['tree_deck_local'].insert(
                        '',
                        tkinter.END,
                        text = deckName_this,
                        values=(
                            deckName_this
                        )
                    )
                except:
                    pass


    def init_data_deck_remote_pre(self):
        tmp_hashSelection = self.UIData['hash_now']

        self.UIData['deck_remote_now'] = None
        tmp_tree_item_children = self.UIObject['tree_deck_remote'].get_children()
        for tmp_tree_item_this in tmp_tree_item_children:
            self.UIObject['tree_deck_remote'].delete(tmp_tree_item_this)

    def init_data_deck_remote(self):
        tmp_hashSelection = self.UIData['hash_now']

        self.UIData['deck_remote_now'] = None
        tmp_tree_item_children = self.UIObject['tree_deck_remote'].get_children()
        for tmp_tree_item_this in tmp_tree_item_children:
            self.UIObject['tree_deck_remote'].delete(tmp_tree_item_this)
        tmp_dataList = OlivaDiceOdyssey.webTool.gExtiverseDeck
        for deck_type_this in ['classic', 'yaml', 'excel']:
            if type(tmp_dataList) is dict \
            and deck_type_this in tmp_dataList \
            and type(tmp_dataList[deck_type_this]) is list:
                for deck_this in tmp_dataList[deck_type_this]:
                    if 'name' in deck_this \
                    and 'author' in deck_this:
                        deckName_this = deck_this['name']
                        deckAuthor_this = deck_this['author']
                        try:
                            self.UIObject['tree_deck_remote'].insert(
                                '',
                                tkinter.END,
                                text = deckName_this,
                                values=(
                                    deckName_this,
                                    deckAuthor_this
                                )
                            )
                        except:
                            pass
                        
    def reset_str_confirm(self):
        """显示恢复默认回复词的确认对话框"""
        if messagebox.askyesno(
            "确认恢复",
            "确定要将配置恢复模块中模块的回复词重置为默认值吗？\n此操作将删除配置恢复模块中所有自定义回复词。",
            parent=self.UIObject['root']
        ):
            self.reset_str_default()

    def reset_str_default(self):
        """实际执行恢复默认回复词的操作"""
        tmp_hashSelection = self.UIData['hash_now']
        if tmp_hashSelection in OlivaDiceCore.msgCustom.dictStrCustomDict:
            OlivaDiceCore.msgCustom.dictStrCustomDict[tmp_hashSelection] = self.default_reply_config().copy()
            OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[tmp_hashSelection] = {}
            OlivaDiceCore.msgCustomManager.saveMsgCustomByBotHash(tmp_hashSelection)
            self.init_data_total()
            messagebox.showinfo("完成", "已恢复配置恢复模块中的包含的回复词为默认值", parent=self.UIObject['root'])

    def reset_console_confirm(self):
        """显示恢复默认配置的确认对话框"""
        if messagebox.askyesno(
            "确认恢复",
            "确定要恢复所有配置项为默认值吗？这将重置所有自定义配置。",
            parent=self.UIObject['root']
        ):
            self.reset_console_default()

    def reset_console_default(self):
        """实际执行恢复默认配置的操作"""
        tmp_hashSelection = self.UIData['hash_now']
        if tmp_hashSelection in OlivaDiceCore.console.dictConsoleSwitch:
            # masterList不换
            current_master_list = OlivaDiceCore.console.dictConsoleSwitch[tmp_hashSelection].get('masterList', [])
            default_config = OlivaDiceCore.console.dictConsoleSwitchTemplate['default'].copy()
            OlivaDiceCore.console.dictConsoleSwitch[tmp_hashSelection] = default_config
            OlivaDiceCore.console.dictConsoleSwitch[tmp_hashSelection]['masterList'] = current_master_list
            OlivaDiceCore.console.saveConsoleSwitch()
            self.init_data_total()
            messagebox.showinfo("完成", "已恢复所有配置项为默认值", parent=self.UIObject['root'])

    def reset_selected_str(self):
        """恢复或删除选中的回复词"""
        tmp_key = get_tree_force(self.UIObject['tree_str'])['text']
        if not tmp_key:
            messagebox.showwarning("警告", "请先选择要操作的回复词", parent=self.UIObject['root'])
            return

        tmp_hashSelection = self.UIData['hash_now']
        current_str_dict = OlivaDiceCore.msgCustom.dictStrCustomDict.get(tmp_hashSelection, {})
        default_str_dict = self.default_reply_config_for_delete().copy()

        if tmp_key in default_str_dict:
            if messagebox.askyesno(
                "确认恢复",
                f"确定要恢复'{tmp_key}'的回复词为默认值吗？",
                parent=self.UIObject['root']
            ):
                default_value = default_str_dict[tmp_key]
                current_str_dict[tmp_key] = default_value
                OlivaDiceCore.msgCustom.dictStrCustomDict[tmp_hashSelection] = current_str_dict
                if tmp_hashSelection in OlivaDiceCore.msgCustom.dictStrCustomUpdateDict:
                    if tmp_key in OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[tmp_hashSelection]:
                        del OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[tmp_hashSelection][tmp_key]
                OlivaDiceCore.msgCustomManager.saveMsgCustomByBotHash(tmp_hashSelection)
                self.init_data_total()
        else:
            if messagebox.askyesno(
                "确认删除",
                f"确定要删除'{tmp_key}'的自定义回复词吗？",
                parent=self.UIObject['root']
            ):
                if tmp_key in current_str_dict:
                    del current_str_dict[tmp_key]
                    OlivaDiceCore.msgCustom.dictStrCustomDict[tmp_hashSelection] = current_str_dict
                    
                if tmp_hashSelection in OlivaDiceCore.msgCustom.dictStrCustomUpdateDict:
                    if tmp_key in OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[tmp_hashSelection]:
                        del OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[tmp_hashSelection][tmp_key]
                        
                OlivaDiceCore.msgCustomManager.saveMsgCustomByBotHash(tmp_hashSelection)
                self.init_data_total()

    def reset_selected_console(self):
        """恢复选中的配置项为默认值"""
        tmp_key = get_tree_force(self.UIObject['tree_console'])['text']
        if not tmp_key:
            messagebox.showwarning("警告", "请先选择要操作的配置项", parent=self.UIObject['root'])
            return

        tmp_hashSelection = self.UIData['hash_now']
        default_config = OlivaDiceCore.console.dictConsoleSwitchTemplate['default']
        current_console_dict = OlivaDiceCore.console.dictConsoleSwitch.get(tmp_hashSelection, {})

        if tmp_key in default_config:
            if messagebox.askyesno(
                "确认恢复",
                f"确定要恢复'{tmp_key}'的配置为默认值吗？",
                parent=self.UIObject['root']
            ):
                if isinstance(default_config[tmp_key], list):
                    current_console_dict[tmp_key] = default_config[tmp_key].copy()
                else:
                    current_console_dict[tmp_key] = default_config[tmp_key]
                    
                OlivaDiceCore.console.dictConsoleSwitch[tmp_hashSelection] = current_console_dict
                OlivaDiceCore.console.saveConsoleSwitch()
                self.init_data_total()
        else:
            if messagebox.askyesno(
                "确认删除",
                f"确定要删除'{tmp_key}'的自定义配置吗？",
                parent=self.UIObject['root']
            ):
                if tmp_key in current_console_dict:
                    del current_console_dict[tmp_key]
                    OlivaDiceCore.console.dictConsoleSwitch[tmp_hashSelection] = current_console_dict
                    OlivaDiceCore.console.saveConsoleSwitch()
                    self.init_data_total()

    def import_str_config(self):
        """导入回复词配置"""
        file_path = filedialog.askopenfilename(
            title="选择回复词配置文件",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")],
            parent=self.UIObject['root']
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    import_data = json.load(f)
                if not isinstance(import_data, dict):
                    raise ValueError("配置文件格式不正确，必须是一个JSON文件")
                if messagebox.askyesno(
                    "确认导入",
                    f"确定要导入回复词配置吗？这将覆盖当前配置。",
                    parent=self.UIObject['root']
                ):
                    tmp_hashSelection = self.UIData['hash_now']
                    backup_data = OlivaDiceCore.msgCustom.dictStrCustomDict.get(tmp_hashSelection, {}).copy()
                    backup_update = OlivaDiceCore.msgCustom.dictStrCustomUpdateDict.get(tmp_hashSelection, {}).copy()
                    try:
                        default_reply = self.default_reply_config()
                        final_reply = default_reply.copy()
                        custom_items = {}
                        for key in import_data:
                            if key not in final_reply:
                                custom_items[key] = import_data[key]
                        final_reply.update(import_data)
                        sorted_custom_reply = {}
                        for key in default_reply:
                            if key in import_data:
                                sorted_custom_reply[key] = import_data[key]
                        sorted_custom_reply.update(custom_items)
                        OlivaDiceCore.msgCustom.dictStrCustomDict[tmp_hashSelection] = final_reply
                        OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[tmp_hashSelection] = sorted_custom_reply
                        customReplyDir = os.path.join(OlivaDiceCore.data.dataDirRoot, tmp_hashSelection, 'console')
                        os.makedirs(customReplyDir, exist_ok=True)
                        customReplyPath = os.path.join(customReplyDir, 'customReply.json')
                        with open(customReplyPath, 'w', encoding='utf-8') as f:
                            json.dump(sorted_custom_reply, f, ensure_ascii=False, indent=4)
                        OlivaDiceCore.msgCustomManager.saveMsgCustomByBotHash(tmp_hashSelection)
                        self.init_data_total()
                        messagebox.showinfo("完成", "回复词配置导入成功", parent=self.UIObject['root'])
                    except Exception as e:
                        OlivaDiceCore.msgCustom.dictStrCustomDict[tmp_hashSelection] = backup_data
                        OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[tmp_hashSelection] = backup_update
                        self.init_data_total()
                        raise
            except Exception as e:
                messagebox.showerror("错误", f"导入失败: {str(e)}\n配置未更改", parent=self.UIObject['root'])

    def export_str_config(self):
        """导出回复词配置"""
        file_path = filedialog.asksaveasfilename(
            title="保存回复词配置文件",
            defaultextension=".json",
            initialfile="customReply.json",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")],
            parent=self.UIObject['root']
        )
        if file_path:
            try:
                tmp_hashSelection = self.UIData['hash_now']
                export_data = OlivaDiceCore.msgCustom.dictStrCustomDict.get(tmp_hashSelection, {})
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=4)
                messagebox.showinfo("完成", "回复词配置导出成功", parent=self.UIObject['root'])
            except Exception as e:
                messagebox.showerror("错误", f"导出失败: {str(e)}", parent=self.UIObject['root'])

    def refresh_str_config(self):
        """刷新回复词配置"""
        if messagebox.askyesno(
            "确认刷新",
            "确定要从文件重新加载回复词配置吗？这将覆盖当前所有修改。",
            parent=self.UIObject['root']
        ):
            tmp_hashSelection = self.UIData['hash_now']
            backup_data = OlivaDiceCore.msgCustom.dictStrCustomDict.get(tmp_hashSelection, {}).copy()
            backup_update = OlivaDiceCore.msgCustom.dictStrCustomUpdateDict.get(tmp_hashSelection, {}).copy()
            try:
                default_reply = self.default_reply_config()
                customReplyDir = os.path.join(OlivaDiceCore.data.dataDirRoot, tmp_hashSelection, 'console')
                customReplyFile = 'customReply.json'
                customReplyPath = os.path.join(customReplyDir, customReplyFile)
                update_data = {}
                try:
                    with open(customReplyPath, 'r', encoding='utf-8') as customReplyPath_f:
                        update_data = json.load(customReplyPath_f)
                        if not isinstance(update_data, dict):
                            raise ValueError("自定义回复文件格式不正确")
                except FileNotFoundError:
                    pass
                except Exception as e:
                    raise ValueError(f"读取自定义回复文件失败: {str(e)}")
                final_reply = default_reply.copy()
                custom_items = {}
                for key in update_data:
                    if key not in final_reply:
                        custom_items[key] = update_data[key]
                final_reply.update(update_data)
                sorted_custom_reply = {}
                for key in default_reply:
                    if key in update_data:
                        sorted_custom_reply[key] = update_data[key]
                sorted_custom_reply.update(custom_items)
                OlivaDiceCore.msgCustom.dictStrCustomDict[tmp_hashSelection] = final_reply
                OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[tmp_hashSelection] = sorted_custom_reply
                os.makedirs(customReplyDir, exist_ok=True)
                with open(customReplyPath, 'w', encoding='utf-8') as f:
                    json.dump(sorted_custom_reply, f, ensure_ascii=False, indent=4)
                OlivaDiceCore.msgCustomManager.saveMsgCustomByBotHash(tmp_hashSelection)
                self.init_data_total()
                messagebox.showinfo("完成", "回复词配置刷新成功", parent=self.UIObject['root'])
            except Exception as e:
                OlivaDiceCore.msgCustom.dictStrCustomDict[tmp_hashSelection] = backup_data
                OlivaDiceCore.msgCustom.dictStrCustomUpdateDict[tmp_hashSelection] = backup_update
                messagebox.showerror("错误", f"刷新失败: {str(e)}\n配置未更改", parent=self.UIObject['root'])

    def import_console_config(self):
        """导入控制台配置"""
        file_path = filedialog.askopenfilename(
            title="选择控制台配置文件",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")],
            parent=self.UIObject['root']
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    import_data = json.load(f)

                if not isinstance(import_data, dict):
                    raise ValueError("配置文件格式不正确，必须是一个JSON文件")

                if messagebox.askyesno(
                    "确认导入",
                    f"确定要导入控制台配置吗？这将覆盖当前配置。",
                    parent=self.UIObject['root']
                ):
                    tmp_hashSelection = self.UIData['hash_now']
                    current_config = OlivaDiceCore.console.dictConsoleSwitch.get(tmp_hashSelection, {})
                    backup_data = current_config.copy()
                    try:
                        for key in import_data:
                            current_config[key] = import_data[key]
                        OlivaDiceCore.console.dictConsoleSwitch[tmp_hashSelection] = current_config
                        OlivaDiceCore.console.saveConsoleSwitch()
                        self.init_data_total()
                        messagebox.showinfo("完成", "控制台配置导入成功", parent=self.UIObject['root'])
                    except Exception as e:
                        OlivaDiceCore.console.dictConsoleSwitch[tmp_hashSelection] = backup_data
                        OlivaDiceCore.console.saveConsoleSwitch()
                        self.init_data_total()
                        raise
            except Exception as e:
                messagebox.showerror("错误", f"导入失败: {str(e)}\n配置未更改", parent=self.UIObject['root'])

    def export_console_config(self):
        """导出控制台配置"""
        file_path = filedialog.asksaveasfilename(
            title="保存控制台配置文件",
            defaultextension=".json",
            initialfile="switch.json",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")],
            parent=self.UIObject['root']
        )
        if file_path:
            try:
                tmp_hashSelection = self.UIData['hash_now']
                export_data = OlivaDiceCore.console.dictConsoleSwitch.get(tmp_hashSelection, {})
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=4)
                messagebox.showinfo("完成", "控制台配置导出成功", parent=self.UIObject['root'])
            except Exception as e:
                messagebox.showerror("错误", f"导出失败: {str(e)}", parent=self.UIObject['root'])

    def refresh_console_config(self):
        """刷新控制台配置"""
        if messagebox.askyesno(
            "确认刷新",
            "确定要从文件重新加载控制台配置吗？这将覆盖当前所有修改。",
            parent=self.UIObject['root']
        ):
            tmp_hashSelection = self.UIData['hash_now']
            backup_data = OlivaDiceCore.console.dictConsoleSwitch.get(tmp_hashSelection, {}).copy()
            try:
                default_config = OlivaDiceCore.console.dictConsoleSwitchTemplate['default'].copy()
                custom_config = {}
                config_dir = OlivaDiceCore.data.dataDirRoot + '/' + tmp_hashSelection + '/console'
                config_file = 'switch.json'
                config_path = config_dir + '/' + config_file
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        custom_config = json.load(f)
                        if not isinstance(custom_config, dict):
                            raise ValueError("配置文件格式不正确")
                except FileNotFoundError:
                    pass
                except Exception as e:
                    raise ValueError(f"读取配置文件失败: {str(e)}")
                merged_config = default_config.copy()
                merged_config.update(custom_config)
                if 'masterList' in backup_data:
                    merged_config['masterList'] = backup_data['masterList']
                OlivaDiceCore.console.dictConsoleSwitch[tmp_hashSelection] = merged_config
                OlivaDiceCore.console.saveConsoleSwitch()
                self.init_data_total()
                messagebox.showinfo("完成", "控制台配置刷新成功", parent=self.UIObject['root'])
            except Exception as e:
                OlivaDiceCore.console.dictConsoleSwitch[tmp_hashSelection] = backup_data
                messagebox.showerror("错误", f"刷新失败: {str(e)}\n配置未更改", parent=self.UIObject['root'])

    # 备份配置相关方法
    def get_backup_config_defaults(self):
        """获取备份配置的默认值"""
        import datetime
        
        defaults = {}
        
        # startDate 默认为当前日期
        defaults['startDate'] = datetime.date.today().strftime('%Y-%m-%d')
        backup_template = OlivaDiceCore.console.dictBackupConfigTemplate.get('default', {})
        defaults['passDay'] = int(backup_template['passDay'])
        defaults['backupTime'] = str(backup_template['backupTime'])
        defaults['maxBackupCount'] = int(backup_template['maxBackupCount'])
        defaults['isBackup'] = int(backup_template.get('isBackup', 0))  # 默认为 0（启用）
        
        return defaults

    def validate_backup_config_item(self, key, value):
        """验证单个备份配置项的格式"""
        import datetime
        import re
        
        try:
            if key == 'startDate':
                # 验证日期格式 yyyy-MM-dd
                if not isinstance(value, str):
                    raise ValueError("日期必须为字符串格式")
                if not re.match(r'^\d{4}-\d{2}-\d{2}$', value):
                    raise ValueError("日期格式必须为 yyyy-MM-dd")
                datetime.datetime.strptime(value, '%Y-%m-%d')
            elif key == 'passDay':
                # 验证整数
                if not isinstance(value, int):
                    if isinstance(value, str) and value.isdigit():
                        value = int(value)
                    else:
                        raise ValueError("天数必须为整数")
                if value <= 0:
                    raise ValueError("天数不能为负数或0")
            elif key == 'backupTime':
                # 验证时间格式 HH:mm:ss
                if not isinstance(value, str):
                    raise ValueError("时间必须为字符串格式")
                if not re.match(r'^\d{2}:\d{2}:\d{2}$', value):
                    raise ValueError("时间格式必须为 HH:mm:ss")
                datetime.datetime.strptime(value, '%H:%M:%S')
            elif key == 'maxBackupCount':
                # 验证备份最大数量
                if not isinstance(value, int):
                    if isinstance(value, str) and value.isdigit():
                        value = int(value)
                    else:
                        raise ValueError("备份数量必须为整数")
                if value <= 0:
                    raise ValueError("备份数量不能小于等于0")
            elif key == 'isBackup':
                # 验证备份开关
                if not isinstance(value, int):
                    if isinstance(value, str) and value.isdigit():
                        value = int(value)
                    else:
                        raise ValueError("备份开关必须为整数")
                if value not in [0, 1]:
                    raise ValueError("备份开关只能为0或1，0表示启用，1表示禁用")
            # 其他配置项按字符串处理，不需要特殊验证
            return value if key in ['passDay', 'maxBackupCount', 'isBackup'] else str(value)
        except Exception as e:
            raise ValueError(f"配置项 '{key}' 格式验证失败: {str(e)}")

    def validate_and_clean_backup_config(self, config_dict):
        """验证并清理备份配置，将不符合格式的项恢复为默认值"""
        if not isinstance(config_dict, dict):
            config_dict = {}
        
        defaults = self.get_backup_config_defaults()
        cleaned_config = {}
        restored_items = []
        
        # 确保必需的配置项存在并有效
        for required_key in ['startDate', 'passDay', 'backupTime', 'maxBackupCount', 'isBackup']:
            if required_key in config_dict:
                try:
                    cleaned_value = self.validate_backup_config_item(required_key, config_dict[required_key])
                    cleaned_config[required_key] = cleaned_value
                except ValueError:
                    # 验证失败，恢复默认值
                    cleaned_config[required_key] = defaults[required_key]
                    restored_items.append(f"{required_key}: 已恢复为默认值 ({defaults[required_key]})")
            else:
                # 缺失，设置默认值
                cleaned_config[required_key] = defaults[required_key]
                restored_items.append(f"{required_key}: 已设置为默认值 ({defaults[required_key]})")
        
        # 处理其他配置项
        for key, value in config_dict.items():
            if key not in ['startDate', 'passDay', 'backupTime', 'maxBackupCount', 'isBackup']:
                try:
                    cleaned_value = self.validate_backup_config_item(key, value)
                    cleaned_config[key] = cleaned_value
                except ValueError:
                    # 其他配置项验证失败，保持原值但转换为字符串
                    cleaned_config[key] = str(value)
        
        if restored_items:
            error_msg = "以下配置项已恢复/设置为默认值:\n" + "\n".join(restored_items)
            messagebox.showinfo("配置恢复提示", error_msg, parent=self.UIObject['root'])
        
        return cleaned_config

    def load_backup_config(self):
        """加载备份配置"""
        backup_dir = OlivaDiceCore.data.dataDirRoot + '/unity/console'
        backup_file = 'backup.json'
        backup_path = backup_dir + '/' + backup_file
        
        try:
            with open(backup_path, 'r', encoding='utf-8') as f:
                backup_config = json.load(f)
                if not isinstance(backup_config, dict):
                    backup_config = {}
        except (FileNotFoundError, json.JSONDecodeError):
            backup_config = {}
        
        # 验证并清理配置
        cleaned_config = self.validate_and_clean_backup_config(backup_config)
        
        if 'unity' not in OlivaDiceCore.console.dictBackupConfig:
            OlivaDiceCore.console.dictBackupConfig['unity'] = {}
        
        # 如果清理后的配置与原配置不同，需要保存清理后的配置到文件
        if cleaned_config != backup_config:
            OlivaDiceCore.console.dictBackupConfig['unity'] = cleaned_config
            try:
                self.save_backup_config()
            except Exception as e:
                print(f"警告: 保存清理后的备份配置失败: {str(e)}")
        else:
            # 更新到内存中的配置
            OlivaDiceCore.console.dictBackupConfig['unity'].update(cleaned_config)

    def save_backup_config(self):
        """保存备份配置"""
        backup_dir = OlivaDiceCore.data.dataDirRoot + '/unity/console'
        backup_file = 'backup.json'
        backup_path = backup_dir + '/' + backup_file
        
        # 确保目录存在
        import os
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # 保存配置
        backup_config = OlivaDiceCore.console.dictBackupConfig.get('unity', {})
        try:
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(backup_config, f, ensure_ascii=False, indent=4)
        except Exception as e:
            raise Exception(f"保存备份配置失败: {str(e)}")

    def import_backup_config(self):
        """导入备份配置"""
        file_path = filedialog.askopenfilename(
            title="选择备份配置文件",
            defaultextension=".json",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")],
            parent=self.UIObject['root']
        )
        if file_path:
            backup_data = OlivaDiceCore.console.dictBackupConfig.get('unity', {}).copy()
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    import_data = json.load(f)
                    if not isinstance(import_data, dict):
                        raise ValueError("文件格式不正确，应为JSON对象")
                    
                    # 验证并清理导入的配置
                    cleaned_import_data = self.validate_and_clean_backup_config(import_data)
                    
                    if 'unity' not in OlivaDiceCore.console.dictBackupConfig:
                        OlivaDiceCore.console.dictBackupConfig['unity'] = {}
                    
                    OlivaDiceCore.console.dictBackupConfig['unity'].update(cleaned_import_data)
                    
                    try:
                        self.save_backup_config()
                        self.init_data_total()
                        messagebox.showinfo("完成", "备份配置导入成功", parent=self.UIObject['root'])
                    except Exception as e:
                        OlivaDiceCore.console.dictBackupConfig['unity'] = backup_data
                        self.save_backup_config()
                        self.init_data_total()
                        raise
            except Exception as e:
                messagebox.showerror("错误", f"导入失败: {str(e)}\n配置未更改", parent=self.UIObject['root'])

    def export_backup_config(self):
        """导出备份配置"""
        file_path = filedialog.asksaveasfilename(
            title="保存备份配置文件",
            defaultextension=".json",
            initialfile="backup.json",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")],
            parent=self.UIObject['root']
        )
        if file_path:
            try:
                export_data = OlivaDiceCore.console.dictBackupConfig.get('unity', {})
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=4)
                messagebox.showinfo("完成", "备份配置导出成功", parent=self.UIObject['root'])
            except Exception as e:
                messagebox.showerror("错误", f"导出失败: {str(e)}", parent=self.UIObject['root'])

    def refresh_backup_config(self):
        """刷新备份配置"""
        if messagebox.askyesno(
            "确认刷新",
            "确定要从文件重新加载备份配置吗？这将覆盖当前所有修改。",
            parent=self.UIObject['root']
        ):
            backup_data = OlivaDiceCore.console.dictBackupConfig.get('unity', {}).copy()
            try:
                self.load_backup_config()  # load_backup_config 方法内部已经包含了验证逻辑
                self.init_data_total()
                messagebox.showinfo("完成", "备份配置刷新成功", parent=self.UIObject['root'])
            except Exception as e:
                OlivaDiceCore.console.dictBackupConfig['unity'] = backup_data
                messagebox.showerror("错误", f"刷新失败: {str(e)}\n配置未更改", parent=self.UIObject['root'])

    def reset_backup_confirm(self):
        """确认重置备份配置"""
        if messagebox.askyesno(
            "确认重置",
            "确定要恢复所有备份配置为默认值吗？这将重置所有自定义配置。",
            parent=self.UIObject['root']
        ):
            try:
                # 获取默认值并重置配置
                defaults = self.get_backup_config_defaults()
                if 'unity' not in OlivaDiceCore.console.dictBackupConfig:
                    OlivaDiceCore.console.dictBackupConfig['unity'] = {}
                
                # 设置为默认值而不是清空
                OlivaDiceCore.console.dictBackupConfig['unity'] = defaults.copy()
                
                self.save_backup_config()
                self.init_data_total()
                messagebox.showinfo("完成", "已恢复所有备份配置为默认值", parent=self.UIObject['root'])
            except Exception as e:
                messagebox.showerror("错误", f"重置失败: {str(e)}", parent=self.UIObject['root'])

    def tree_backup_rightKey(self, event):
        """备份配置树右键菜单"""
        try:
            self.UIObject['tree_rightkey_menu_backup'].delete(0, tkinter.END)
            self.UIObject['tree_rightkey_menu_backup'].add_command(label = '编辑', command = lambda : self.tree_backup_edit())
            self.UIObject['tree_rightkey_menu_backup'].add_command(label='恢复/删除', command=lambda: self.reset_selected_backup())
            self.UIObject['tree_rightkey_menu_backup'].post(event.x_root, event.y_root)
        except:
            pass

    def tree_backup_edit(self):
        """编辑备份配置"""
        tmp_selection = None
        for item in self.UIObject['tree_backup'].selection():
            tmp_selection = self.UIObject['tree_backup'].item(item, "values")
        if tmp_selection != None and len(tmp_selection) >= 1:
            tmp_key = tmp_selection[0]
            if 'unity' in OlivaDiceCore.console.dictBackupConfig:
                if tmp_key in OlivaDiceCore.console.dictBackupConfig['unity']:
                    tmp_value = OlivaDiceCore.console.dictBackupConfig['unity'][tmp_key]
                    tmp_edit_backup_UI_obj = self.edit_backup_UI(
                        root_class = self,
                        key = tmp_key,
                        value = tmp_value
                    )
                else:
                    messagebox.showwarning("警告", "未找到对应的备份配置项", parent=self.UIObject['root'])
            else:
                messagebox.showwarning("警告", "未找到备份配置", parent=self.UIObject['root'])
        else:
            messagebox.showwarning("警告", "请先选择要编辑的备份配置项", parent=self.UIObject['root'])

    def reset_selected_backup(self):
        """恢复选中的备份配置项为默认值"""
        tmp_selection = None
        for item in self.UIObject['tree_backup'].selection():
            tmp_selection = self.UIObject['tree_backup'].item(item, "values")
        if tmp_selection != None and len(tmp_selection) >= 1:
            tmp_key = tmp_selection[0]
            
            # 获取默认值 
            defaults = self.get_backup_config_defaults()
            
            if tmp_key in defaults:
                default_value = defaults[tmp_key]
                if messagebox.askyesno(
                    "确认恢复",
                    f"确定要恢复备份配置项 '{tmp_key}' 为默认值 '{default_value}' 吗？",
                    parent=self.UIObject['root']
                ):
                    try:
                        if 'unity' not in OlivaDiceCore.console.dictBackupConfig:
                            OlivaDiceCore.console.dictBackupConfig['unity'] = {}
                        
                        OlivaDiceCore.console.dictBackupConfig['unity'][tmp_key] = default_value
                        self.save_backup_config()
                        self.init_data_total()
                        messagebox.showinfo("完成", f"已恢复备份配置项 '{tmp_key}' 为默认值", parent=self.UIObject['root'])
                    except Exception as e:
                        messagebox.showerror("错误", f"恢复失败: {str(e)}", parent=self.UIObject['root'])
            else:
                # 非必需配置项，提供删除选项
                if messagebox.askyesno(
                    "确认删除",
                    f"配置项 '{tmp_key}' 不是必需项，确定要删除吗？",
                    parent=self.UIObject['root']
                ):
                    try:
                        if 'unity' in OlivaDiceCore.console.dictBackupConfig:
                            if tmp_key in OlivaDiceCore.console.dictBackupConfig['unity']:
                                del OlivaDiceCore.console.dictBackupConfig['unity'][tmp_key]
                                self.save_backup_config()
                                self.init_data_total()
                                messagebox.showinfo("完成", f"已删除备份配置项 '{tmp_key}'", parent=self.UIObject['root'])
                            else:
                                messagebox.showwarning("警告", "未找到对应的备份配置项", parent=self.UIObject['root'])
                        else:
                            messagebox.showwarning("警告", "未找到备份配置", parent=self.UIObject['root'])
                    except Exception as e:
                        messagebox.showerror("错误", f"删除失败: {str(e)}", parent=self.UIObject['root'])
        else:
            messagebox.showwarning("警告", "请先选择要操作的备份配置项", parent=self.UIObject['root'])
    
    def default_reply_config(self):
        '''导入所有的dictStrCustom'''
        # 获取当前内存中的回复词配置
        tmp_hashSelection = self.UIData['hash_now']
        current_config = OlivaDiceCore.msgCustom.dictStrCustomDict.get(tmp_hashSelection, {}).copy()
        import_list = self.load_recover_modules(tmp_hashSelection)
        ordered_reply = {}
        module_replies = {}
        for module_name in import_list:
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, 'msgCustom') and hasattr(module.msgCustom, 'dictStrCustom'):
                    module_replies[module_name] = module.msgCustom.dictStrCustom.copy()
                    ordered_reply.update(module.msgCustom.dictStrCustom)
            except (ImportError, AttributeError):
                continue
        ordered_reply.update(OlivaDiceNativeGUI.msgCustom.dictStrCustom)
        # 排序回复词
        sorted_reply = {}
        for module_name in import_list:
            if module_name in module_replies:
                sorted_reply.update(module_replies[module_name])
        sorted_reply.update(OlivaDiceNativeGUI.msgCustom.dictStrCustom)
        for key in current_config:
            if key not in sorted_reply:
                sorted_reply[key] = current_config[key]
        return sorted_reply
    
    def default_reply_config_for_delete(self):
        '''导入所有的dictStrCustom-删除用'''
        default_reply = {}
        # 从配置文件加载模块列表
        tmp_hashSelection = self.UIData['hash_now']
        import_list = self.load_recover_modules(tmp_hashSelection)
        for module_name in import_list:
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, 'msgCustom') and hasattr(module.msgCustom, 'dictStrCustom'):
                    default_reply.update(module.msgCustom.dictStrCustom)
            except (ImportError, AttributeError):
                continue
        default_reply.update(OlivaDiceNativeGUI.msgCustom.dictStrCustom)
        return default_reply