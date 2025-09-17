# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   main.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import OlivaDiceCore
import OlivaDiceNativeGUI

import platform
import threading

version = '0.1.1'

class Event(object):
    def init(plugin_event:OlivOS.API.Event, Proc:OlivOS.pluginAPI.shallow):
        pass

    def init_after(plugin_event:OlivOS.API.Event, Proc:OlivOS.pluginAPI.shallow):
        OlivaDiceNativeGUI.load.globalProc = Proc
        OlivaDiceCore.crossHook.dictHookList['model'].append(['OlivaDiceNativeGUI', OlivaDiceNativeGUI.data.OlivaDiceNativeGUI_ver_short])
        OlivaDiceNativeGUI.load.listPlugin = Proc.get_plugin_list()
        OlivaDiceNativeGUI.load.dictBotInfo = Proc.Proc_data['bot_info_dict']
        
        # 检查是否存在 OlivaDiceMaster 模块
        OlivaDiceNativeGUI.load.backupFlag = False
        plugin_list = Proc.get_plugin_list()
        if 'OlivaDiceMaster' in plugin_list:
            OlivaDiceNativeGUI.load.backupFlag = True

        threading.Thread(
            target = OlivaDiceNativeGUI.load.checkOnlineStatusLoop,
            args = ()
        ).start()

    def save(plugin_event:OlivOS.API.Event, Proc:OlivOS.pluginAPI.shallow):
        pass

    def menu(plugin_event:OlivOS.API.Event, Proc:OlivOS.pluginAPI.shallow):
        if(platform.system() == 'Windows'):
            if plugin_event.data.event == 'OlivaDiceNativeGUI_001':
                if not OlivaDiceNativeGUI.load.flag_open or True:
                    OlivaDiceNativeGUI.load.flag_open = True
                    OlivaDiceNativeGUI.GUI.ConfigUI(
                        Model_name = 'OlivaDiceNativeGUI_manage',
                        logger_proc = Proc.Proc_info.logger_proc.log
                    ).start()
