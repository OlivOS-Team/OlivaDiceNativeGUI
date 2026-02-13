# -*- encoding: utf-8 -*-
"""
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/

@File      :   load.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
"""

import OlivOS
import OlivaDiceNativeGUI
import OlivaDiceCore

import os
import json
import time
import requests as req
from urllib.parse import urlencode

flag_open = False

dictBotInfo = {}

listPlugin = []

globalProc = None

onlineAPIData = None
onlineAPICount = '正在连接...'

masterModelFlag = False


def releaseDir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def checkOnlineStatusLoop():
    while True:
        try:
            checkOnlineStatus()
        except:
            pass
        time.sleep(2 * 60 * 60)


def checkOnlineStatus():
    global onlineAPIData, onlineAPICount
    tmp_res = None
    send_url = OlivaDiceNativeGUI.data.onlineStatusAPIURL
    headers = {'User-Agent': OlivaDiceCore.data.bot_version_short_header}
    msg_res = req.request('GET', send_url, headers=headers, proxies=OlivaDiceCore.webTool.get_system_proxy())
    res_text = str(msg_res.text)
    try:
        tmp_res = json.loads(res_text)
        onlineAPIData = tmp_res
        if tmp_res['status'] == 200 and tmp_res['code'] == 0:
            onlineAPICount = str(tmp_res['data']['online']['day'])
    except:
        pass
