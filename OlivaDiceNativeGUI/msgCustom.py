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
    'strMasterRemoteNone': '尝试远程设置但未找到对应的记录时的回复词',
    
    'strNeedMaster': '没有Master权限却触发了相关指令时的提示',
    'strHello': '入群后的打招呼消息，目前未实现，预留',
    'strBot': '【.bot】指令\n回复的主要信息',
    'strBotExit': '【.bot exit】指令\n指令退群时的回复词',
    'strBotExitRemote': '远程指令退群时的回复词（骰主侧）',
    'strBotExitRemoteShow' : '远程指令退群时的回复词（用户侧）',
    'strBotAddFriendNotice': '好友添加时通知窗口的消息',
    'strBotAddGroupNotice' : '群邀请时通知窗口的消息',
    'strBotAddGroupNoticeIgnoreResult' : '群邀请时自动忽略的通知窗口消息片段',
    'strBotAddGroupRemoteAcceptShow' : '手动接受群邀请时的通知窗口消息',
    'strAccept' : '群邀请时自动接受的通知窗口消息片段\n默认为：已接受',
    'strIgnore' : '群邀请时自动忽略的通知窗口消息片段\n默认为：已忽略',
    'strReject' : '群邀请时自动驳回的通知窗口消息片段\n默认为：已驳回',
    'strBotOn' : '【.bot on】指令\n机器人开启时的回复词',
    'strBotAlreadyOn' : '【.bot on】指令\n尝试开启机器人，\n但是机器人已经处于开启状态时的回复词',
    'strBotOff' : '【.bot off】指令\n机器人关闭时的回复词',
    'strBotAlreadyOff' : '【.bot off】指令\n尝试关闭机器人，\n但是机器人已经处于关闭状态时的回复词',
    'strBotNotUnderHost' : '所使用的功能需要在频道场景下时的回复词',
    'strBotHostLocalOn' : '（默认关闭模式）\n机器人在本主频道开启时的回复词',
    'strBotAlreadyHostLocalOn' : '（默认关闭模式）\n尝试在本主频道开启机器人，\n但是机器人已经处于开启状态时的回复词',
    'strBotHostLocalOff' : '（默认关闭模式）\n机器人在本主频道关闭时的回复词',
    'strBotAlreadyHostLocalOff' : '（默认关闭模式）\n尝试在本主频道关闭机器人，\n但是机器人已经处于关闭状态时的回复词',
    'strBotHostOn' : '（默认开启模式）\n机器人在本主频道开启时的回复词',
    'strBotAlreadyHostOn' : '（默认开启模式）\n尝试在本主频道开启机器人，\n但是机器人已经处于开启状态时的回复词',
    'strBotHostOff' : '（默认开启模式）\n机器人在本主频道关闭时的回复词',
    'strBotAlreadyHostOff' : '（默认开启模式）\n尝试在本主频道关闭机器人，\n但是机器人已经处于关闭状态时的回复词',
    'strHelpDoc' : '【.help】指令\n的回复格式',
    'strHelpDocRecommend' : '【.help】指令\n未找到条目并触发模糊搜索时的回复格式',
    'strHelpDocNotFound' : '【.help】指令\n未找到条目时的回复内容',
    'strDrawTi' : '【.ti】指令\n临时症状抽取的回复词',
    'strDrawLi' : '【.li】指令\n总结症状抽取的回复词',
    'strDrawName' : '【.name】指令\n随机名称抽取的回复词',
    'strDrawDeck' : '【.draw】指令\n牌堆抽取的回复词',
    'strDrawDeckHideShow' : '【.drawh】指令\n牌堆暗抽取的回复词（群内）',
    'strDrawDeckRecommend' : '【.draw/.drawh】指令\n牌堆抽取的回复词（结果）',
    'strDrawDeckNotFound' : '【.draw/.drawh】指令\n牌堆抽取的回复词（结果）',
    'strRoll' : '【.r】等指令\n掷骰时的回复词',
    'strRollWithReason' : '【.r】等指令\n带理由掷骰时的回复词',
    'strRollHide' : '【.rh】等指令\n掷暗骰时的回复词（结果）',
    'strRollHideWithReason' : '【.rh】等指令\n带理由掷暗骰时的回复词（结果）',
    'strRollHideShow' : '【.rh】等指令\n掷暗骰时的回复词（群内）',
    'strRollHideShowWithReason' : '【.rh】等指令\n带理由掷暗骰时的回复词（群内）',
    'strRollRange' : 'OneDice标准的全量测试指令回复格式',
    'strRollError01' : '掷骰错误:\n无法解析的表达式',
    'strRollError02' : '掷骰错误:\n无法计算的表达式',
    'strRollError03' : '掷骰错误:\n输入了非法的表达式',
    'strRollError04' : '掷骰错误:\n输入了非法的子参数',
    'strRollError05' : '掷骰错误:\n输入了非法的运算符',
    'strRollError06' : '掷骰错误:\n发现未定义运算符',
    'strRollError07' : '掷骰错误:\n解析到空语法树',
    'strRollError08' : '掷骰错误:\n错误的左值',
    'strRollError09' : '掷骰错误:\n错误的右值',
    'strRollError10' : '掷骰错误:\n错误的子参数',
    'strRollError11' : '掷骰错误:\n计算极值时出错',
    'strRollError12' : '掷骰错误:\n解析技能变量时出错',
    'strRollErrorUnknown' : '掷骰错误:\n未知的错误',
    'strRollErrorHelp' : '掷骰错误的提示片段',
    'strSetGroupTempRule' : '【.setcoc】等指令\n设置群规则模板',
    'strDelGroupTempRule' : '【.setcoc】等指令\n清除群规则模板',
    'strPcInit' : '【.coc/.dnd】指令\n人物卡作成',
    'strPcUpdateSkillValue' : '【.st】指令\n人物卡技能快速更新',
    'strPcSetSkillValue' : '【.st】指令\n人物卡保存',
    'strPcGetSingleSkillValue' : '【.st】指令\n查看单个技能',
    'strPcShow' : '【.st show】指令\n查看人物卡',
    'strPcList' : '【.st list】指令\n查看人物卡列表',
    'strPcLock' : '【.st lock】指令\n锁定人物卡',
    'strPcLockError' : '【.st lock】指令\n锁定人物卡失败',
    'strPcLockNone' : '【.st lock】指令\n没有人物卡时尝试锁定人物卡',
    'strPcUnLock' : '【.st unlock】指令\n解锁人物卡',
    'strPcUnLockNone' : '【.st unlock】指令\n没有需要解锁的人物卡',
    'strPcInitSt' : '【.st init】指令\n人物卡作成',
    'strPcSet' : '【.st set】指令\n切换人物卡',
    'strPcSetError' : '【.st set】指令\n切换人物卡错误\n人物卡不存在',
    'strPcDel' : '【.st del】指令\n删除人物卡',
    'strPcDelError' : '【.st del】指令\n删除人物卡错误',
    'strPcDelNone' : '【.st del】指令\n删除人物卡错误\n人物卡列表为空',
    'strPcClear' : '【.st clear】指令\n清空人物卡',
    'strPcClearNone' : '【.st clear】指令\n清空人物卡错误\n当前没有人物卡',
    'strPcRm' : '【.st rm】指令\n删除人物卡技能',
    'strPcRmNone' : '【.st rm】指令\n删除人物卡技能失败\n技能不存在',
    'strPcRmCardNone' : '【.st rm】指令\n删除人物卡技能失败\n人物卡不存在',
    'strPcTemp' : '【.st temp】指令\n设置人物卡模板',
    'strPcTempShow' : '【.st temp】指令\n查看人物卡模板',
    'strPcTempError' : '【.st temp】指令\n设置人物卡模板失败',
    'strPcTempRule' : '【.st rule】指令\n设置人物卡模板规则',
    'strPcTempRuleShow' : '【.st rule】指令\n查看人物卡模板规则',
    'strPcTempRuleError' : '【.st rule】指令\n设置人物卡模板规则失败',
    'strPcGroupTempRuleShow' : '【.st temp/rule】指令\n当前群存在人物卡模板时的片段',
    'strPcRename' : '【.nn】指令\n对当前人物卡进行重命名',
    'strPcSkillCheck' : '【.ra】指令\n技能检定格式',
    'strPcSkillCheckHide' : '【.rah】指令\n技能暗检定格式（结果）',
    'strPcSkillCheckHideShow' : '【.rah】指令\n技能暗检定格式（群内）',
    'strPcSkillCheckWithSkillName' : '【.ra】指令\n技能检定格式\n带技能名称',
    'strPcSkillCheckHideWithSkillName' : '【.rah】指令\n技能暗检定格式（结果）\n带技能名称',
    'strPcSkillCheckHideShowWithSkillName' : '【.rah】指令\n技能暗检定格式（群内）\n带技能名称',
    'strPcSkillEnhanceCheck' : '【.en】指令\n指定技能成长',
    'strPcSkillEnhanceContent' : '【.en】指令\n指定技能成长片段',
    'strPcSkillEnhanceAll' : '【.en】指令\n自动技能成长',
    'strPcSkillEnhanceError' : '【.en】指令\n技能成长错误',
    'strSanCheck' : '【.sc】指令\n理智检定',
    'strSanCheckGreatFailed' : '【.sc】指令\n理智检定大失败',
    'strSanCheckError' : '【.sc】指令\n理智检定错误',
    'strIntPositiveInfinite' : '正无穷大',
    'strIntNegativeInfinite' : '负无穷大',
    'strPcSkillCheckSucceed' : '检定结果\n成功',
    'strPcSkillCheckHardSucceed' : '检定结果\n困难成功',
    'strPcSkillCheckExtremeHardSucceed' : '检定结果\n极难成功',
    'strPcSkillCheckGreatSucceed' : '检定结果\n大成功',
    'strPcSkillCheckFailed' : '检定结果\n失败',
    'strPcSkillCheckGreatFailed' : '检定结果\n大失败',
    'strPcSkillCheckFate01' : 'FATE规则书检定结果\n[-2 拙劣]',
    'strPcSkillCheckFate02' : 'FATE规则书检定结果\n[-1 差劲]',
    'strPcSkillCheckFate03' : 'FATE规则书检定结果\n[+0 二流]',
    'strPcSkillCheckFate04' : 'FATE规则书检定结果\n[+1 一般]',
    'strPcSkillCheckFate05' : 'FATE规则书检定结果\n[+2 尚可]',
    'strPcSkillCheckFate06' : 'FATE规则书检定结果\n[+3 良好]',
    'strPcSkillCheckFate07' : 'FATE规则书检定结果\n[+4 极佳]',
    'strPcSkillCheckFate08' : 'FATE规则书检定结果\n[+5 卓越]',
    'strPcSkillCheckFate09' : 'FATE规则书检定结果\n[+6 惊异]',
    'strPcSkillCheckFate10' : 'FATE规则书检定结果\n[+7 史诗]',
    'strPcSkillCheckFate11' : 'FATE规则书检定结果\n[+8 传奇]',
    'strPcSkillCheckNope' : '检定结果\n需要解释',
    'strPcSkillCheckError' : '检定结果\n发生错误',
    'strHelpdocSet' : '【.helpdoc】指令\n自定义帮助文档已设置',
    'strHelpdocDel' : '【.helpdoc】指令\n自定义帮助文档已删除',
    'strObList' : '【.ob list】指令\n当前旁观列表',
    'strObListNone' : '【.ob list】指令\n当前旁观列表为空',
    'strObUserObList' : '当前无用',
    'strObUserObListNone' : '当前无用',
    'strObJoin' : '【.ob/.ob join】指令\n加入旁观',
    'strObJoinAlready' : '【.ob/.ob join】指令\n已在旁观中',
    'strObExit' : '【.ob/.ob exit】指令\n退出旁观',
    'strObExitAlready' : '【.ob/.ob exit】指令\n不在旁观中',
    'strObExitAll' : '【.ob exit all】指令\n退出所有旁观',
    'strObClear' : '【.ob clear】指令\n清空旁观列表'
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
