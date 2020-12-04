import sys

from src.fundEnum import DBSource


class FundConfig:
    # 平台 darwin/win32
    PLATFORM = sys.platform

    YDI_URL = 'https://api.yiduu.com/v1'

    # https: // api.doctorxiong.club / v1
    OTHER_URL = 'https://fund.colinxu.cn/v1'

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
