'''==================================================
@IDE: PyCharm
@Time : 2021/3/1 13:31
@Author : wyp
@File : cmd_pub.py
=================================================='''
import pika
import json
import os
from configparser import ConfigParser

# 获取相关配置文件
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file = os.path.join(BASE_DIR, 'conf', 'conf.ini')
cfg = ConfigParser()
cfg.read(config_file)

class CmdPub(object):
    def __init__(self):
        pass

    '''
        body = {
            "type": obj.type,
            "cmd": CMD_SET_START_STOP,
            "device_sn": obj.device_sn,
            "data": {
                "status": 0,    # 启动/停止/暂停
            }
        }
   '''
    @staticmethod
    def send_cmd(data):
        print(data)
        queue_name = 'Q_%s' % data.get("device_sn")
        credentials = pika.PlainCredentials(cfg.get('mq', 'name'),
                                            cfg.get('mq', 'pswd'))  # mq用户名和密码
        # 虚拟队列需要指定参数 virtual_host，如果是默认的可以不填。
        param = pika.ConnectionParameters(host=cfg.get('mq', 'host'),
                                          port=cfg.get('mq', 'port'),
                                          virtual_host='/',
                                          credentials=credentials)
        connection = pika.BlockingConnection(param)
        channel = connection.channel()
        # 声明消息队列，消息将在这个队列传递，如不存在，则创建
        result = channel.queue_declare(queue=queue_name)

        message = json.dumps(data)
        # 向队列插入数值 routing_key是队列名
        channel.basic_publish(exchange='', routing_key=queue_name, body=message)
        connection.close()



if __name__ == '__main__':
    pass