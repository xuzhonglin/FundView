import sys


class FundConfig:
    # 平台 darwin/win32
    PLATFORM = sys.platform

    # 自定义接口地址 https://fund.colinxu.cn/v1 https://api.doctorxiong.club/v1 https://api.yiduu.com/v1
    URL = 'https://api.yiduu.com/v1'

    # 代理地址
    PROXY_POOL = 'http://proxy-pool.colinxu.cn'

    # 是否开启代理
    ENABLE_PROXY = False

    # 数据源 tt/ant/other
    DB_SWITCH = 'other'

    # 字体
    FONT_NAME = '.AppleSystemUIFont' if PLATFORM == 'darwin' else '微软雅黑'

    # 字体大小
    FONT_SIZE = 13 if PLATFORM == 'darwin' else 9
