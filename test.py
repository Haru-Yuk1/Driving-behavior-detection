import pygame
import time

# 初始化
pygame.mixer.init()

# 加载音频
sound = pygame.mixer.Sound("resources/audio/alarm_80.mp3")

# 播放3次（含原声，共播放3次）
sound.play(loops=2)

# 主线程继续执行，不阻塞
# 如果需要保持主线程一段时间以听到声音：
while True:
    print("lala")

time.sleep(5)
