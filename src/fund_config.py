import os
import sys

from src.fund_enum import DBSource, ColorSwitch


class FundConfig:
    APP_NAME = '韭菜盒子'

    VERSION = '1.3.0'

    CUR_PID = os.getpid()

    UPDATE_URL = 'http://api.colinxu.cn/leekbox/update.json'

    # 平台 darwin/win32
    PLATFORM = sys.platform

    RUN_DIR = os.path.expanduser('~') + '\\.LeekBox'

    YDI_URL = 'https://api.yiduu.com/v1'

    # https: // api.doctorxiong.club / v1
    OTHER_URL = 'https://fund.colinxu.cn/fundApi/v1'

    ANT_URL = 'http://www.fund123.cn/api/fund'

    # 代理地址
    PROXY_POOL = 'http://proxy-pool.colinxu.cn'

    # 是否开启代理
    ENABLE_PROXY = False

    # 数据源
    # tt 天天基金
    # ant 蚂蚁财富
    DB_SWITCH = DBSource.TTT

    # 字体
    FONT_NAME = '.AppleSystemUIFont' if PLATFORM == 'darwin' else '微软雅黑'

    # 字体大小
    FONT_SIZE = 13 if PLATFORM == 'darwin' else 9

    # 自动刷新使能
    AUTO_REFRESH_ENABLE = False

    # 刷新超时
    AUTO_REFRESH_TIMEOUT = 60 * 1000

    # 配色方案
    FUND_COLOR = ColorSwitch.RED_GREEN

    FUND_MID = ''

    ENABLE_SYNC = False

    SWAP_FLAG = False

    CONFIG_KEYS = ["positions", "optional", "source", "fontName", "fontSize", "enableAutoRefresh", "autoRefreshTimeout",
                   "colorScheme", "enableProxy", "proxyAddress", "mid", "enableSync", "optionalCoins", "exchangeApi",
                   'timeZone', 'localCurrency']

    EXCHANGE_API = {'okex': {
        'apiAddress': 'https://www.ouyi.cc',
        'apiKey': '',
        'apiSecret': '',
        'passPhrase': ''
    }}

    EXCHANGE_SETTING = {
        'timeZone': 0,
        'localCurrency': 0
    }
