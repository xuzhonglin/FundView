import sys

from src.fundEnum import DBSource, ColorSwitch, _FundColor


class FundConfig:
    # 平台 darwin/win32
    PLATFORM = sys.platform

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
    # ydi 易读优
    # other 熊博士
    DB_SWITCH = DBSource.YDI

    # 字体
    FONT_NAME = '.AppleSystemUIFont' if PLATFORM == 'darwin' else '微软雅黑'

    # 字体大小
    FONT_SIZE = 13 if PLATFORM == 'darwin' else 9

    # 自动刷新使能
    AUTO_REFRESH_ENABLE = False

    # 刷新超时
    AUTO_REFRESH_TIMEOUT = 60 * 1000

    FUND_COLOR = ColorSwitch.BLACK_ONLY


class FundColor:
    _IS_BLACK = FundConfig.FUND_COLOR != ColorSwitch.BLACK_ONLY
    RED_STR = _FundColor.RED_STR if _IS_BLACK else _FundColor.BLACK_STR
    GREEN_STR = _FundColor.GREEN_STR if _IS_BLACK else _FundColor.BLACK_STR
    RED_BRUSH = _FundColor.RED_BRUSH if _IS_BLACK else _FundColor.BLACK_BRUSH
    GREEN_BRUSH = _FundColor.GREEN_BRUSH if _IS_BLACK else _FundColor.BLACK_BRUSH
    STYLE_RED = _FundColor.STYLE_RED if _IS_BLACK else _FundColor.STYLE_BLACK
    STYLE_GREEN = _FundColor.STYLE_GREEN if _IS_BLACK else _FundColor.STYLE_BLACK
