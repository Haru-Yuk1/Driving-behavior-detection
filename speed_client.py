import socket
import time

from PySide2 import QtCore
################################################################################
## 获取速度
################################################################################
class SpeedClientThread(QtCore.QThread):
    speed_signal = QtCore.Signal(float)  # 定义信号
    aggressive_signal = QtCore.Signal(bool)  # 新增激进驾驶信号
    collision_signal = QtCore.Signal(bool)  # 新增碰撞信号

    # server_ip='172.20.10.5'
    server_ip='127.0.0.1'
    def __init__(self, ui, server_ip=server_ip, port=12345):
        super().__init__(parent=ui)
        self.server_ip = server_ip
        self.port = port
        self.ui = ui
        self.stop_flag = False
        self.client = None

    def run(self):
        while not self.stop_flag:
            try:
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client.settimeout(10)
                self.client.connect((self.server_ip, self.port))
                print(f"[连接成功] 已连接到服务器 {self.server_ip}:{self.port}")

                while not self.stop_flag:
                    data = self.client.recv(1024)
                    if not data:
                        print("[断开] 服务器断开连接")
                        break
                    msg = data.decode().strip()
                    print(f"[接收] {msg}")

                    # 解析 speed 和 aggressive
                    try:
                        parts = msg.split(";")
                        speed_val = None
                        aggressive_flag = None

                        for part in parts:
                            if part.startswith("speed:"):
                                speed_val = float(part.split(":")[1])
                            elif part.startswith("aggressive:"):
                                aggressive_flag = part.split(":")[1].strip() in ["1", "true", "True"]
                            elif part.startswith("collision:"):
                                collision_flag = part.split(":")[1].strip() in ["1", "true", "True"]

                        # ✅ 发射信号
                        if speed_val is not None:
                            self.speed_signal.emit(speed_val)
                        if aggressive_flag is not None:
                            self.aggressive_signal.emit(aggressive_flag)
                        if collision_flag is not None:
                            self.collision_signal.emit(collision_flag)

                    except Exception as e:
                        print(f"[解析错误] 报文解析失败: {e}")

            except Exception as e:
                print(f"[错误] 连接失败或通信错误: {e}")

            finally:
                if self.client:
                    self.client.close()
                    print("[关闭] 客户端已关闭")

            if not self.stop_flag:
                print("[重试] 30秒后尝试重新连接...")
                time.sleep(30)

    def stop(self):
        self.stop_flag = True
        if self.client:
            try:
                self.client.shutdown(socket.SHUT_RDWR)
                self.client.close()
            except:
                pass
