# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   msgCustom.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import OlivaDiceNativeGUI

dictConsoleSwitchTemplate = {}

dictStrCustomDict = {}

dictStrCustom = {}

dictStrConst = {}

dictGValue = {}

dictTValue = {}

dictHelpDocTemp = {}

dictStrCustomNote = {
    'strBotName': '机器人的自称',
    'strForGroupOnly': '当在非群聊场景调用功能时回复的缺省语句',
    'strSetStr': '更新 str 回复词时的回复',
    'strBecomeMaster': '完成认证并成为Master时的回复词',
    'strCantBecomeMaster': '未完成认证，无法成为Master时的回复词',
    'strMasterSystemRestart': '远程调用重载时的回复词',
    'strMasterConsoleShow': '显示配置项时的回复词',
    'strMasterConsoleShowList': '显示配置项列表时的回复词',
    'strMasterConsoleSet': '设置配置项时的回复词',
    'strMasterConsoleAppend': '追加配置项时的回复词',
    'strMasterConsoleSetInvalid': '尝试设置非法的配置值时的回复词',
    'strMasterConsoleNotFound': '尝试访问不存在的配置项时的回复词',
    'strMasterRemoteOn': '远程开启时的回复词',
    'strMasterRemoteOff': '远程关闭时的回复词',
    'strMasterRemoteOnAlready': '尝试远程开启，但已经开启时的回复词',
    'strMasterRemoteOffAlready': '尝试远程关闭，但已经关闭时的回复词',
    'strMasterRemoteDefaultOn': '远程默认开启时的回复词',
    'strMasterRemoteDefaultOff': '远程默认关闭时的回复词',
    'strMasterRemoteDefaultOnAlready': '尝试远程默认开启，但已经默认开启时的回复词',
    'strMasterRemoteDefaultOffAlready': '尝试远程默认关闭，但已经默认关闭时的回复词',
    'strMasterRemoteNone': '尝试远程设置但未找到对应的记录时的回复词'
}

dictConsoleSwitchNote = {
    'globalEnable': '全局开关\n当前版本无用，通常不需要调整',
    'userConfigCount' : '用户记录刷写循环计数器，通常不需要调整',
    'pulseInterval' : '心跳上报频率，通常不需要调整',
    'autoAcceptGroupAdd' : '自动同意好友添加请求',
    'autoAcceptFriendAdd' : '自动同意群邀请',
    'disableReplyPrivate' : '禁用私聊',
    'messageFliterMode' : '事件过滤器\n 1 时屏蔽普通群消息\n 2 时屏蔽频道消息\n 3 时屏蔽所有多人窗口消息',
    'messageSplitGate' : '分页门限，超过此长度的文本将被分页处理',
    'messageSplitPageLimit' : '分页上限，超过此数量的页面将不再被发送',
    'messageSplitDelay' : '分页延迟，每个分页间将会等待如此长时间再次发送，单位为毫秒',
    'largeRollLimit' : '大型掷骰细节长度限制\n用于控制诸如ww和dx指令的细节显示\n超过将不显示细节',
    'joyPokeMode' : '戳一戳回复模式\n 0 返回默认版本号\n 1 进行一次默认骰掷骰\n 2 进行一次今日人品查询'
}
