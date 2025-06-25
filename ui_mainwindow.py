# -*- coding: utf-8 -*-

################################################################################
## 美化版本的主窗口界面
## 基于原始UI文件改进，添加了现代化样式和更好的布局
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        # 设置窗口属性
        MainWindow.resize(1500, 1300)
        MainWindow.setMinimumSize(QSize(1200, 1200))

        # 设置窗口图标和标题
        MainWindow.setWindowTitle("车载驾驶员行为监控系统")

        # 创建动作
        self.actionOpen_camera = QAction(MainWindow)
        self.actionOpen_camera.setObjectName(u"actionOpen_camera")
        self.actionOpen_camera.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))

        self.actionClose_camera = QAction(MainWindow)
        self.actionClose_camera.setObjectName(u"actionClose_camera")
        self.actionClose_camera.setIcon(self.style().standardIcon(QStyle.SP_DialogCancelButton))

        # 主界面容器
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        # 设置主容器样式
        self.centralwidget.setStyleSheet("""
            QWidget {
                background-color: #f5f6fa;
                font-family: 'Microsoft YaHei', 'Segoe UI', Arial, sans-serif;
            }
        """)

        # 主布局
        self.main_layout = QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        # 标题区域
        self.title_frame = QFrame()
        self.title_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 10px;
                padding: 15px;
            }
        """)
        self.title_layout = QHBoxLayout(self.title_frame)

        self.title_label = QLabel("车载驾驶员行为监控系统")
        self.title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background: none;
            }
        """)
        self.title_layout.addWidget(self.title_label)
        self.title_layout.addStretch()

        # 状态指示器
        self.status_indicator = QLabel("●")
        self.status_indicator.setStyleSheet("""
            QLabel {
                color: #2ecc71;
                font-size: 20px;
                background: none;
            }
        """)
        self.status_text = QLabel("系统就绪")
        self.status_text.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                background: none;
            }
        """)
        self.title_layout.addWidget(self.status_indicator)
        self.title_layout.addWidget(self.status_text)

        self.main_layout.addWidget(self.title_frame)

        # 内容区域
        self.content_layout = QHBoxLayout()
        self.content_layout.setSpacing(20)

        # 左侧视频显示区域
        self.video_frame = QFrame()
        self.video_frame.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border-radius: 15px;
                border: 3px solid #34495e;
            }
        """)
        self.video_layout = QVBoxLayout(self.video_frame)
        self.video_layout.setContentsMargins(15, 15, 15, 15)
        self.video_layout.setSpacing(10)

        # 视频标题 - 移到左上角
        self.video_title = QLabel("🎥 实时视频")
        self.video_title.setStyleSheet("""
            QLabel {
                color: #ecf0f1;
                font-size: 20px;
                font-weight: bold;
                background: none;
                border: 0px;
                padding-bottom: 10px;
            }
        """)
        self.video_title.setAlignment(Qt.AlignLeft)  # 左对齐
        self.video_layout.addWidget(self.video_title)

        # 主视频显示区域 - 移除固定尺寸，使其可以随窗口变化
        self.label = QLabel()
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(400, 300))  # 设置最小尺寸
        self.label.setStyleSheet("""
            QLabel {
                background-color: #34495e;
                border: 5px dashed #5d6d7e;
                border-radius: 10px;
                color: #bdc3c7;
                font-size: 14px;
            }
        """)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("点击菜单打开车载摄像头")
        self.label.setScaledContents(True)  # 允许内容缩放
        # 设置尺寸策略，使其能够扩展
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.video_layout.addWidget(self.label)

        # 设置视频框架的尺寸策略
        self.video_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.content_layout.addWidget(self.video_frame, 2)  # 给视频区域更多空间权重

        # 右侧控制面板 - 增加宽度
        self.control_panel = QFrame()
        self.control_panel.setMinimumWidth(500)  # 从400增加到500
        self.control_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
                border: 1px solid #ddd;
            }
        """)
        self.control_layout = QVBoxLayout(self.control_panel)
        self.control_layout.setContentsMargins(25, 25, 25, 25)  # 增加内边距
        self.control_layout.setSpacing(20)  # 增加间距

        # 控制面板标题
        self.control_title = QLabel("📊 系统信息")
        self.control_title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 20px;
                font-weight: bold;
                border:0px;
            }
        """)
        self.control_layout.addWidget(self.control_title)

        # 信息卡片样式
        card_style = """
            QFrame {
                background-color: #f8f9fa;
                border-radius: 12px;
                border: 1px solid #e9ecef;
                padding: 18px;
            }
            QLabel {
                background: none;
                color: #495057;
                font-size: 18px;
            }
        """

        # 基本信息卡片
        self.info_card1 = QFrame()
        self.info_card1.setStyleSheet(card_style)
        self.info_layout1 = QHBoxLayout(self.info_card1)

        self.info_card1.setMinimumWidth(430)  # 设置最小宽度
        self.label_2 = QLabel("疲劳检测:")
        self.label_2.setStyleSheet("font-weight: bold; color: #6c757d; font-size: 18px;")
        self.label_10 = QLabel("正常驾驶")
        self.label_10.setStyleSheet("color: #008000; font-size: 18px;")

        self.info_layout1.addWidget(self.label_2)
        self.info_layout1.addWidget(self.label_10)
        self.info_layout1.addStretch()
        self.control_layout.addWidget(self.info_card1)

        # 检测信息卡片
        self.info_card2 = QFrame()
        self.info_card2.setStyleSheet(card_style)
        self.info_card2.setMinimumWidth(430)  # 设置最小宽度
        self.info_layout2 = QHBoxLayout(self.info_card2)

        self.label_3 = QLabel("眨眼次数：0")
        self.label_3.setStyleSheet("font-weight: bold; color: #6c757d; font-size: 18px;")
        self.label_4 = QLabel("哈欠次数：0")
        self.label_4.setStyleSheet("font-weight: bold; color: #6c757d; font-size: 18px;")

        self.info_layout2.addWidget(self.label_3)
        self.info_layout2.addWidget(self.label_4)
        self.info_layout2.addStretch()
        self.control_layout.addWidget(self.info_card2)

        # 性能信息卡片
        self.info_card3 = QFrame()
        self.info_card3.setStyleSheet(card_style)
        self.info_layout3 = QHBoxLayout(self.info_card3)
        self.info_card3.setMinimumWidth(430)  # 设置最小宽度
        self.label_5 = QLabel("行为检测：")
        self.label_5.setStyleSheet("font-weight: bold; font-size: 18px;")
        self.label_9 = QLabel("正常驾驶")
        self.label_9.setStyleSheet("color: #008000; font-size: 18px;")

        self.info_layout3.addWidget(self.label_5)
        self.info_layout3.addWidget(self.label_9)
        self.info_layout3.addStretch()
        self.control_layout.addWidget(self.info_card3)

        # 统计信息卡片
        self.stats_card = QFrame()
        self.stats_card.setStyleSheet(card_style)
        self.stats_layout = QHBoxLayout(self.stats_card)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setStyleSheet("font-weight: bold; color: #6c757d; font-size: 18px; align:'center'; content: '手机';")
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setStyleSheet("font-weight: bold; color: #6c757d; font-size: 18px; align: 'center'; content: '抽烟';")
        self.stats_layout.addWidget(self.label_6)
        self.stats_layout.addWidget(self.label_7)
        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setStyleSheet("font-weight: bold; color: #6c757d; font-size: 18px; align: 'center'; content: '喝水';")
        self.stats_layout.addWidget(self.label_8)

        self.control_layout.addWidget(self.stats_card)

        # 日志区域
        self.log_title = QLabel("💻 系统日志")
        self.log_title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 20px;
                font-weight: bold;
                border:0px;
                margin: -10px;
            }
        """)
        self.control_layout.addWidget(self.log_title)

        # 日志文本浏览器 - 调整尺寸适应新的面板
        self.textBrowser = QTextBrowser()
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setMinimumSize(QSize(430, 250))  # 增加最小尺寸
        self.textBrowser.setStyleSheet("""
            QTextBrowser {
                background-color: #2c3e50;
                color: #ecf0f1;
                border: 2px solid #34495e;
                border-radius: 12px;
                padding: 12px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 13px;
                selection-background-color: #3498db;
            }
            QScrollBar:vertical {
                background-color: #34495e;
                width: 14px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical {
                background-color: #5d6d7e;
                border-radius: 7px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #7f8c8d;
            }
        """)
        # 设置日志区域的尺寸策略，使其能够扩展
        self.textBrowser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.control_layout.addWidget(self.textBrowser)

        self.content_layout.addWidget(self.control_panel, 1)  # 给控制面板较小的空间权重

        self.main_layout.addLayout(self.content_layout)

        MainWindow.setCentralWidget(self.centralwidget)

        # 菜单栏
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 30))
        self.menubar.setStyleSheet("""
            QMenuBar {
                background-color: #34495e;
                color: white;
                font-size: 14px;
                padding: 5px;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 8px 15px;
                border-radius: 5px;
            }
            QMenuBar::item:selected {
                background-color: #3498db;
            }
            QMenu {
                background-color: #34495e;
                color: white;
                border: 1px solid #5d6d7e;
                border-radius: 5px;
            }
            QMenu::item {
                padding: 8px 20px;
            }
            QMenu::item:selected {
                background-color: #3498db;
            }
        """)

        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)

        # 状态栏
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setStyleSheet("""
            QStatusBar {
                background-color: #34495e;
                color: white;
                font-size: 12px;
                padding: 5px;
            }
        """)
        MainWindow.setStatusBar(self.statusbar)

        # 添加菜单项
        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.actionOpen_camera)
        self.menu.addAction(self.actionClose_camera)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

        # 初始化日志
        self.printf("=== 车载驾驶员行为监控系统启动 ===")
        self.printf("系统就绪，等待摄像头连接...")
        self.printf("请通过菜单栏打开摄像头设备")

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("车载驾驶员行为监控系统 v1.0")
        self.actionOpen_camera.setText("打开摄像头")
        self.actionOpen_camera.setShortcut("Ctrl+O")
        self.actionOpen_camera.setStatusTip("连接并打开摄像头设备")
        self.actionClose_camera.setText("关闭摄像头")
        self.actionClose_camera.setShortcut("Ctrl+C")
        self.actionClose_camera.setStatusTip("关闭摄像头设备")
        self.menu.setTitle("设备")

    def printf(self, mes):
        """美化的消息显示函数"""
        import datetime
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{current_time}] {mes}"

        self.textBrowser.append(formatted_message)

        # 自动滚动到底部
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(cursor.End)
        self.textBrowser.setTextCursor(cursor)

        # 限制日志行数，避免内存过多占用
        if self.textBrowser.document().blockCount() > 100:
            cursor.movePosition(cursor.Start)
            cursor.select(cursor.BlockUnderCursor)
            cursor.removeSelectedText()

    def update_status(self, status, color="#2ecc71"):
        """更新状态指示器"""
        self.status_indicator.setStyleSheet(f"""
            QLabelu {{
                color: {color};
                font-size: 20px;
                background: none;
            }}
        """)
        self.status_text.setText(status)

    def update_device_status(self, status, is_connected=False):
        """更新设备状态"""
        color = "#28a745" if is_connected else "#dc3545"
        self.label_10.setText(status)
        self.label_10.setStyleSheet(f"color: {color};")

    def update_fps(self, fps):
        """更新帧率显示"""
        self.label_9.setText(f"{fps} FPS")
        color = "#28a745" if fps > 20 else "#ffc107" if fps > 10 else "#dc3545"
        self.label_9.setStyleSheet(f"color: {color};")