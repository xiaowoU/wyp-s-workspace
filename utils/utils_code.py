'''==================================================
@IDE: PyCharm
@Time : 2021/3/1 15:27
@Author : wyp
@File : utils_code.py
=================================================='''

# 设备种类
T_OUTLINE = 0x0001      # 轮廓测量系统
T_UNIFY1 = 0x1001       # 一体化设备-裂缝计
T_UNIFY2 = 0x1002       # 一体化设备-激光计
T_UNIFY3 = 0x1003       # 一体化设备-应变计


# CMD指令
CMD_GET_ALLINFO = 0x00    # 设备所有信息上传

CMD_SET_MEASURE_AREA = 0x03 	 # 测量区段设置
CMD_GET_MEASURE_AREA = 0x04 	 # 测量区段查询
CMD_SET_START_STOP = 0x11       # 测量启停
CMD_SET_ZERO_OFFSET = 0x23 	 # 零偏参数设置
CMD_GET_ZERO_OFFSET = 0x24 	 # 零偏参数查询
CMD_SET_PID = 0x21    # PID参数设置
# CMD_GET_DEVICE_INFO =     0x22 	 # PID参数查询
CMD_ERR_REPORT = 0x92   # 故障上报

CMD_GET_VERSION = 0x30 	 # 设备版本查询
CMD_ENABLE_UPDATE = 0x31 	 # 询问指定版本是否支持升级
CMD_UPDATE_FILE = 0x32 	 # 启动版本数据大小（发过去）
    # 0x41 	 # 设备状态
CMD_COLLECT_DATA = 0x80 	 # 测量数据上传
CMD_ONLINE = 0x90 	         # 设备上线请求
# ------------------------------------------------分割线-一体化设备
CMD_SET_UNIFY_PARAM = 0x61        # 一体化设备参数设置
CMD_GET_UNIFY_PARAM = 0x62        # 一体化设备参数查询
CMD_SET_UNIFY_PARAM1 = 0x63       # 一体化设备参数设置(终端主动查询，开机或短连接）
CMD_UNIFY_DATA = 0x81             # 一体化设备测量数据上传



