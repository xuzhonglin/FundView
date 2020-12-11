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

    # 配色方案
    FUND_COLOR = ColorSwitch.RED_GREEN

    SWAP_FLAG = False


def get_color(value, colorType):
    is_black = FundConfig.FUND_COLOR != ColorSwitch.BLACK_ONLY
    is_green_red = FundConfig.FUND_COLOR == ColorSwitch.GREEN_RED

    if value >= 0 and colorType == 'str':
        if is_green_red:
            return _FundColor.GREEN_STR
        return _FundColor.RED_STR if is_black else _FundColor.BLACK_STR
    elif colorType == 'str':
        if is_green_red:
            return _FundColor.RED_STR
        return _FundColor.GREEN_STR if is_black else _FundColor.BLACK_STR

    if value >= 0 and colorType == 'brush':
        if is_green_red:
            return _FundColor.GREEN_BRUSH
        return _FundColor.RED_BRUSH if is_black else _FundColor.BLACK_BRUSH
    elif colorType == 'brush':
        if is_green_red:
            return _FundColor.RED_BRUSH
        return _FundColor.GREEN_BRUSH if is_black else _FundColor.BLACK_BRUSH

    if value >= 0 and colorType == 'style':
        if is_green_red:
            return _FundColor.STYLE_GREEN
        return _FundColor.STYLE_RED if is_black else _FundColor.STYLE_BLACK
    elif colorType == 'style':
        if is_green_red:
            return _FundColor.STYLE_RED
        return _FundColor.STYLE_GREEN if is_black else _FundColor.STYLE_BLACK
