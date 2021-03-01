'''==================================================
@IDE: PyCharm
@Time : 2021/3/1 13:31
@Author : wyp
@File : cmd_pub.py
=================================================='''
import pika
import json

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
        credentials = pika.PlainCredentials('rabbit1', '123456')  # mq用户名和密码
        # 虚拟队列需要指定参数 virtual_host，如果是默认的可以不填。
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='192.168.20.14', port=5672, virtual_host='/', credentials=credentials))
        channel = connection.channel()
        # 声明消息队列，消息将在这个队列传递，如不存在，则创建
        result = channel.queue_declare(queue=queue_name)

        message = json.dumps(data)
        # 向队列插入数值 routing_key是队列名
        channel.basic_publish(exchange='', routing_key=queue_name, body=message)
        connection.close()



if __name__ == '__main__':
    pass