import socket
import threading
import time
import random

def handle_client(conn, addr):
    print(f"[连接] 客户端已连接: {addr}")
    try:
        while True:
            speed = round(random.uniform(30, 90), 2)  # 模拟速度值
            message = f"{speed}\n"
            conn.sendall(message.encode())
            print(f"[发送] {message.strip()}")
            time.sleep(1)  # 每隔 5 秒发送一次
    except (ConnectionResetError, BrokenPipeError):
        print(f"[断开] 客户端 {addr} 断开连接")
    finally:
        conn.close()

def start_server(host='127.0.0.1', port=12345):
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
