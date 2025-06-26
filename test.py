import sys
import os
from PySide2.QtWidgets import QApplication
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent
from PySide2.QtCore import QUrl

# 启动应用
app = QApplication(sys.argv)

# 获取文件的绝对路径（确保路径正确）
current_dir = os.path.dirname(os.path.abspath(__file__))
audio_path = os.path.join(current_dir, "resources/audio/alarm_80.mp3")

# 检查文件是否存在
if not os.path.exists(audio_path):
    print(f"错误：文件不存在 {audio_path}")
else:
    player = QMediaPlayer()
    player.setMedia(QMediaContent(QUrl.fromLocalFile(audio_path)))
    player.play()

app.exec_()  # 进入事件循环