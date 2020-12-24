import math
import uuid
from datetime import datetime

from webdav3.client import Client
from webdav3.exceptions import LocalResourceNotFound
from src.fundConfig import FundConfig


class CloudSync:
    def __init__(self, local_path: str, config_id: str):
        options = {
            'webdav_hostname': "https://dav.jianguoyun.com/dav",
            'webdav_login': "xuzhonglin@outlook.com",
            'webdav_password': "a3jubjdwhjhd9sn6",
            'disable_check': True
        }
        self.config_id = config_id
        self.backup_dir = 'LeekBox'
        self.local_file_name = local_path
        self.remote_file_name = self.backup_dir + '/' + self.config_id + '.json'
        self.client = Client(options)

    def backup(self, config_id: str = None):
        if not self.client.mkdir(self.backup_dir):
            raise Exception('please create dir first')
        try:
            if config_id is not None:
                self.remote_file_name = self.backup_dir + '/' + config_id + '.json'
            self.client.upload(self.remote_file_name, self.local_file_name)
            # 打印结果，之后会重定向到log
            print('upload success %s' % self.remote_file_name)
        except LocalResourceNotFound as exception:
            print('An error happen: LocalResourceNotFound ---')
            return False
        return True

    def recovery(self, config_id: str = None):
        try:
            if config_id is not None:
                self.remote_file_name = self.backup_dir + '/' + config_id + '.json'
            self.client.download(self.remote_file_name, self.local_file_name)
        except Exception as ex:
            print(ex)
            return False
        return True
