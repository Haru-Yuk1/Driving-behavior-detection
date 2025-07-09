import socket
import threading
import time
import random


host='127.0.0.1'
host='127.0.0.1'
def handle_client(conn, addr):
    print(f"[连接] 客户端已连接: {addr}")
    try:
        while True:
            # 模拟数据
            speed = round(random.uniform(30, 90), 2)  # 模拟车速
            aggressive_flag = random.choice([0, 1])   # 0:正常，1:激进
            collision_flag = random.choices([0, 1], weights=[95, 5])[0]  # 偶尔碰撞

            # 构造 TCP 报文
            message = f"speed:{speed:.2f};aggressive:{aggressive_flag};collision:{collision_flag}\n"

            # 发送数据
            conn.sendall(message.encode())
            print(f"[发送] {message.strip()}")

            time.sleep(1)  # 每秒发送一次
    except (ConnectionResetError, BrokenPipeError):
        print(f"[断开] 客户端 {addr} 断开连接")
    finally:
        conn.close()

def start_server(host=host, port=12345):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[启动] TCP服务器正在监听 {host}:{port}")
    try:
        while True:
            conn, addr = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            client_thread.start()
    except KeyboardInterrupt:
        print("\n[关闭] 手动停止服务器")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
