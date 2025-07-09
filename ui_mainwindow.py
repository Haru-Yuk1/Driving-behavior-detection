# -*- coding: utf-8 -*-
import datetime

import pygame
from PySide2.QtCharts import QtCharts
################################################################################
## 主窗口界面
## 基于原始UI文件改进
## 主要功能包括：
## - 左侧TabBar导航
## - 右侧内容区域使用堆叠窗口管理不同页面
## - 增强的样式和交互体验
## - 支持摄像头连接和状态更新
## - 日志显示和状态指示器
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import pyqtgraph as pg

from model import SessionLocal, SpeedRecord, FatigueRecord
from datetime import datetime

from models.experimental import attempt_load
from utils.general import check_img_size
from utils.torch_utils import select_device
import torch
from numpy import random

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        self.speed_counter = 0  # 初始化速度计数器
        self.perclos_counter = 0  # 用于记录Perclos模型的计数器

        # 数据分析用
        self.count_fatigue = 0
        self.count_awake = 0
        self.count_aggressive = 0
        self.count_normal = 0
        self.count_speeding = 0
        self.count_collision = 0
        self.count_distracted = 0  # 分心行为

        # 初始化音频
        pygame.mixer.init()

        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        # 设置窗口属性
        MainWindow.resize(1600, 1300)  # 增加宽度以适应左侧TabBar
        MainWindow.setMinimumSize(QSize(1000, 1000))

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

        # 主布局 - 水平布局，包含左侧TabBar和右侧内容
        self.main_horizontal_layout = QHBoxLayout(self.centralwidget)
        self.main_horizontal_layout.setContentsMargins(10, 10, 10, 10)
        self.main_horizontal_layout.setSpacing(15)

        # 左侧TabBar区域
        self.tab_frame = QFrame()
        self.tab_frame.setFixedWidth(160)
        self.tab_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 12px;
                border: none;
            }
        """)

        self.tab_layout = QVBoxLayout(self.tab_frame)
        self.tab_layout.setContentsMargins(10, 20, 10, 20)
        self.tab_layout.setSpacing(15)

        # Logo区域
        self.logo_label = QLabel("🚗")
        self.logo_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 40px;
                background: none;
                padding: 10px;
            }
        """)
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.tab_layout.addWidget(self.logo_label)

        # 系统标题
        # self.system_title = QLabel("")
        # self.system_title.setStyleSheet("""
        #     QLabel {
        #         color: white;
        #         font-size: 16px;
        #         font-weight: bold;
        #         background: none;
        #         padding-bottom: 20px;
        #     }
        # """)
        # self.system_title.setAlignment(Qt.AlignCenter)
        # self.tab_layout.addWidget(self.system_title)

        # 定义Tab按钮样式
        tab_button_style = """
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                padding: 15px 10px;
                font-size: 18px;
                font-weight: bold;
                text-align: left;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
                border: 2px solid rgba(255, 255, 255, 0.4);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.3);
            }
            QPushButton:checked {
                background-color: rgba(255, 255, 255, 0.25);
                border: 2px solid white;
                color: #fff;
            }
        """

        # 创建Tab按钮
        self.tab_buttons = []

        # 主监控页面
        self.btn_monitor = QPushButton("📹 实时监控")
        self.btn_monitor.setStyleSheet(tab_button_style)
        self.btn_monitor.setCheckable(True)
        self.btn_monitor.setChecked(True)  # 默认选中
        self.tab_buttons.append(self.btn_monitor)
        self.tab_layout.addWidget(self.btn_monitor)

        # 数据分析页面
        self.btn_analytics = QPushButton("🛠️ 数据分析")
        self.btn_analytics.setStyleSheet(tab_button_style)
        self.btn_analytics.setCheckable(True)
        self.tab_buttons.append(self.btn_analytics)
        self.tab_layout.addWidget(self.btn_analytics)

        # 历史记录页面
        self.btn_history = QPushButton("📋 历史记录")
        self.btn_history.setStyleSheet(tab_button_style)
        self.btn_history.setCheckable(True)
        self.tab_buttons.append(self.btn_history)
        self.tab_layout.addWidget(self.btn_history)

        # 系统设置页面
        self.btn_settings = QPushButton("⚙️ 系统设置")
        self.btn_settings.setStyleSheet(tab_button_style)
        self.btn_settings.setCheckable(True)
        self.tab_buttons.append(self.btn_settings)
        self.tab_layout.addWidget(self.btn_settings)

        # 报警管理页面
        self.btn_alerts = QPushButton("🚨 报警管理")
        self.btn_alerts.setStyleSheet(tab_button_style)
        self.btn_alerts.setCheckable(True)
        self.tab_buttons.append(self.btn_alerts)
        self.tab_layout.addWidget(self.btn_alerts)

        # 添加弹性空间
        self.tab_layout.addStretch()

        # 版本信息
        self.version_label = QLabel("v1.0.0")
        self.version_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                font-size: 12px;
                background: none;
                padding: 10px;
            }
        """)
        self.version_label.setAlignment(Qt.AlignCenter)
        self.tab_layout.addWidget(self.version_label)

        # 添加左侧TabBar到主布局
        self.main_horizontal_layout.addWidget(self.tab_frame)

        # 右侧内容区域容器
        self.content_container = QWidget()
        self.content_container.setStyleSheet("""
            QWidget {
                background-color: transparent;
            }
        """)

        # 右侧主布局
        self.main_layout = QVBoxLayout(self.content_container)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(20)

        # 创建堆叠窗口部件来管理不同页面
        self.stacked_widget = QStackedWidget()

        # 页面1：主监控页面（原来的内容）
        self.monitor_page = self.create_monitor_page()
        self.stacked_widget.addWidget(self.monitor_page)

        # 页面2：数据分析页面
        self.analytics_page = self.create_analytics_page()
        self.stacked_widget.addWidget(self.analytics_page)

        # 页面3：历史记录页面
        self.history_page = self.create_history_page()
        self.stacked_widget.addWidget(self.history_page)

        # 页面4：系统设置页面
        self.settings_page = self.create_settings_page()
        self.stacked_widget.addWidget(self.settings_page)

        # 页面5：报警管理页面
        self.alerts_page = self.create_alerts_page()
        self.stacked_widget.addWidget(self.alerts_page)

        self.main_layout.addWidget(self.stacked_widget)

        # 添加右侧内容到主布局
        self.main_horizontal_layout.addWidget(self.content_container, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        # 菜单栏
        self.setup_menubar(MainWindow)

        # 状态栏
        self.setup_statusbar(MainWindow)

        # 连接Tab按钮信号
        self.setup_tab_connections()

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def create_monitor_page(self):
        """创建主监控页面"""
        # 页面创建与标题区域
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # 标题区域 - 高度优化
        self.title_frame = QFrame()
        self.title_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 10px;
                padding: 10px;  /* 减小内边距 */
            }
        """)
        self.title_layout = QHBoxLayout(self.title_frame)
        self.title_layout.setContentsMargins(10, 5, 10, 5)  # 减少布局边距
        self.title_layout.setSpacing(8)  # 减小元素间距

        # 主标题 - 高度优化
        self.title_label = QLabel("车载驾驶员行为监控系统")
        self.title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;  /* 减小字体大小 */
                font-weight: bold;
                background: none;
            }
        """)
        self.title_layout.addWidget(self.title_label)
        # === 新增：加载模型按钮 ===
        self.btn_load_model = QPushButton("加载模型")
        self.btn_load_model.setStyleSheet("""
            QPushButton {
                background-color: #1abc9c;
                color: white;
                font-size: 16px;
                border-radius: 10px;
                padding: 6px 16px;
            }
            QPushButton:hover {
                background-color: #16a085;
            }
        """)
        self.btn_load_model.setFixedHeight(32)
        self.btn_load_model.clicked.connect(self.load_yolo_model)
        self.title_layout.addWidget(self.btn_load_model)

        self.title_layout.addStretch()

        # 状态指示器 - 高度优化
        self.status_text = QLabel("系统就绪")
        self.status_text.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;  /* 减小字体大小 */
                background: none;
            }
        """)
        self.status_indicator = QLabel("●")
        self.status_indicator.setStyleSheet("""
            QLabel {
                color: #2ecc71;
                font-size: 24px;  /* 减小指示灯大小 */
                background: none;
            }
        """)

        self.title_layout.addWidget(self.status_text)
        self.title_layout.addWidget(self.status_indicator)
        layout.addWidget(self.title_frame)

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

        # 视频标题
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
        self.video_title.setAlignment(Qt.AlignLeft)
        self.video_layout.addWidget(self.video_title)

        # 主视频显示区域
        self.label = QLabel()
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(400, 300))
        self.label.setStyleSheet("""
            QLabel {
                background-color: #34495e;
                border: 4px dashed #5d6d7e;
                border-radius: 10px;
                color: #bdc3c7;
                font-size: 14px;
            }
        """)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("点击菜单打开车载摄像头")
        self.label.setScaledContents(True)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.video_layout.addWidget(self.label)

        self.video_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.content_layout.addWidget(self.video_frame, 2)

        # 右侧控制面板
        self.control_panel = QFrame()
        self.control_panel.setMinimumWidth(500)
        self.control_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
                border: 1px solid #ddd;
            }
        """)
        self.control_layout = QVBoxLayout(self.control_panel)
        self.control_layout.setContentsMargins(25, 25, 25, 25)
        self.control_layout.setSpacing(20)

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

        # 修改卡片样式 - 移除固定高度
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
                align: center;
            }
        """
        # 基本信息卡片 - 使用垂直布局合并信息
        self.info_card1 = QFrame()
        self.info_card1.setStyleSheet(card_style)
        self.info_layout1 = QVBoxLayout(self.info_card1)
        self.info_layout1.setContentsMargins(10, 5, 10, 5)  # 减少边距
        self.info_layout1.setSpacing(5)  # 设置垂直间距

        # 第一行：疲劳检测状态
        self.first_row_layout = QHBoxLayout()
        self.first_row_layout.setContentsMargins(0, 0, 0, 0)

        self.label_2 = QLabel("疲劳检测:")
        self.label_2.setStyleSheet("font-weight: bold; color: #6c757d; font-size: 18px;")
        self.label_2.setAlignment(Qt.AlignCenter)  # 居中对齐

        self.label_10 = QLabel("清醒")
        self.label_10.setStyleSheet("color: #008000; font-size: 18px;")
        self.label_10.setAlignment(Qt.AlignCenter)  # 居中对齐

        self.first_row_layout.addWidget(self.label_2, 1)  # 添加拉伸因子
        self.first_row_layout.addWidget(self.label_10, 1)  # 添加拉伸因子

        # 第二行：眨眼次数和哈欠次数
        self.second_row_layout = QHBoxLayout()
        self.second_row_layout.setContentsMargins(0, 0, 0, 0)

        self.label_3 = QLabel("眨眼次数：0")
        self.label_3.setStyleSheet("font-weight: bold; color: #6c757d; font-size: 18px;")
        self.label_3.setAlignment(Qt.AlignCenter)  # 居中对齐

        self.label_4 = QLabel("哈欠次数：0")
        self.label_4.setStyleSheet("font-weight: bold; color: #6c757d; font-size: 18px;")
        self.label_4.setAlignment(Qt.AlignCenter)  # 居中对齐

        self.second_row_layout.addWidget(self.label_3, 1)  # 添加拉伸因子
        self.second_row_layout.addWidget(self.label_4, 1)  # 添加拉伸因子

        # 将两行布局添加到主布局
        self.info_layout1.addLayout(self.first_row_layout)
        self.info_layout1.addLayout(self.second_row_layout)

        self.control_layout.addWidget(self.info_card1, 1)  # 卡片可拉伸

        # 行为检测信息卡片
        self.info_card3 = QFrame()
        self.info_card3.setStyleSheet(card_style)
        self.info_layout3 = QVBoxLayout(self.info_card3)  # 改为垂直布局
        self.info_layout3.setSpacing(10)  # 设置行与行之间的间距

        # 第一行：行为检测标签和状态
        self.behavior_row = QHBoxLayout()
        self.label_5 = QLabel("行为检测：")
        self.label_5.setStyleSheet("font-weight: bold; font-size: 18px; padding: 8px 0;")  # 增加内边距
        self.label_5.setAlignment(Qt.AlignCenter)  # 居中对齐

        self.label_9 = QLabel("正常驾驶")
        self.label_9.setStyleSheet("color: #008000; font-size: 18px; padding: 8px 0;")  # 增加内边距
        self.label_9.setAlignment(Qt.AlignCenter)  # 居中对齐

        self.behavior_row.addWidget(self.label_5, 1)  # 添加拉伸因子
        self.behavior_row.addWidget(self.label_9, 1)  # 添加拉伸因子

        # 第二行：具体行为统计（手机、抽烟、喝水）
        self.stats_row = QHBoxLayout()
        self.label_6 = QLabel("手机")
        self.label_6.setStyleSheet("font-weight: bold; color: #6c757d; font-size: 18px; padding: 8px 0;")  # 增加内边距
        self.label_6.setAlignment(Qt.AlignCenter)  # 居中对齐

        self.label_7 = QLabel("抽烟")
        self.label_7.setStyleSheet("font-weight: bold; color: #6c757d; font-size: 18px; padding: 8px 0;")  # 增加内边距
        self.label_7.setAlignment(Qt.AlignCenter)  # 居中对齐

        self.label_8 = QLabel("喝水")
        self.label_8.setStyleSheet("font-weight: bold; color: #6c757d; font-size: 18px; padding: 8px 0;")  # 增加内边距
        self.label_8.setAlignment(Qt.AlignCenter)  # 居中对齐

        self.stats_row.addWidget(self.label_6, 1)  # 添加拉伸因子
        self.stats_row.addWidget(self.label_7, 1)  # 添加拉伸因子
        self.stats_row.addWidget(self.label_8, 1)  # 添加拉伸因子

        # 将两行添加到主布局
        self.info_layout3.addLayout(self.behavior_row)
        self.info_layout3.addLayout(self.stats_row)

        # 将卡片添加到控制布局
        self.control_layout.addWidget(self.info_card3, 1)  # 卡片可拉伸

        # 速度显示卡片 - 使用垂直布局合并碰撞检测信息
        self.speed_card = QFrame()
        self.speed_card.setStyleSheet(card_style)
        self.speed_layout = QVBoxLayout(self.speed_card)
        self.speed_layout.setContentsMargins(10, 5, 10, 5)  # 减少边距
        self.speed_layout.setSpacing(5)  # 设置垂直间距

        # 第一行：碰撞检测状态
        self.collision_row_layout = QHBoxLayout()
        self.collision_row_layout.setContentsMargins(0, 0, 0, 0)

        self.label_collision_text = QLabel("碰撞检测:")
        self.label_collision_text.setStyleSheet("font-weight: bold; color: #6c757d; font-size: 18px;")
        self.label_collision_text.setAlignment(Qt.AlignCenter)  # 居中对齐

        self.label_collision_status = QLabel("正常驾驶")
        self.label_collision_status.setStyleSheet("color: #008000; font-size: 18px;")
        self.label_collision_status.setAlignment(Qt.AlignCenter)  # 居中对齐

        self.collision_row_layout.addWidget(self.label_collision_text, 1)  # 添加拉伸因子
        self.collision_row_layout.addWidget(self.label_collision_status, 1)  # 添加拉伸因子

        # 第二行：车速信息
        self.speed_row_layout = QHBoxLayout()
        self.speed_row_layout.setContentsMargins(0, 0, 0, 0)

        self.label_speed_text = QLabel("车速：")
        self.label_speed_text.setStyleSheet("font-weight: bold; font-size: 18px;")
        self.label_speed_text.setAlignment(Qt.AlignCenter)  # 居中对齐

        self.label_speed_value = QLabel("0 km/h")
        self.label_speed_value.setStyleSheet("color: #6c757d; font-size: 18px;")
        self.label_speed_value.setAlignment(Qt.AlignCenter)  # 居中对齐

        self.speed_row_layout.addWidget(self.label_speed_text, 1)  # 添加拉伸因子
        self.speed_row_layout.addWidget(self.label_speed_value, 1)  # 添加拉伸因子

        # 将两行布局添加到主布局
        self.speed_layout.addLayout(self.collision_row_layout)
        self.speed_layout.addLayout(self.speed_row_layout)

        self.control_layout.addWidget(self.speed_card, 1)  # 卡片可拉伸

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

        # 日志文本浏览器
        self.textBrowser = QTextBrowser()
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setMinimumSize(QSize(430, 250))
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
        self.textBrowser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.control_layout.addWidget(self.textBrowser)

        self.content_layout.addWidget(self.control_panel, 1)
        layout.addLayout(self.content_layout)

        # 初始化日志
        self.printf("=== 车载驾驶员行为监控系统启动 ===")
        self.printf("系统就绪，等待摄像头连接...")
        self.printf("请通过菜单栏打开摄像头设备")

        return page

    # def create_analytics_page(self):
    #     """创建数据分析页面"""
    #     page = QWidget()
    #     layout = QVBoxLayout(page)
    #
    #     # 标题
    #     title = QLabel("📊 数据分析")
    #     title.setStyleSheet("""
    #         QLabel {
    #             color: #2c3e50;
    #             font-size: 28px;
    #             font-weight: bold;
    #             padding: 20px;
    #         }
    #     """)
    #     layout.addWidget(title)
    #
    #     # 📈 Perclos 曲线图初始化
    #     self.perclos_x = []  # 横轴：检测轮数
    #     self.perclos_y = []  # 纵轴：Perclos 值
    #
    #     self.perclos_plot_widget = pg.PlotWidget()
    #     self.perclos_plot_widget.setBackground('w')
    #     self.perclos_plot_widget.setTitle("Perclos 疲劳得分趋势", color='#34495e', size='18pt')
    #     self.perclos_plot_widget.setLabel('left', 'Perclos 得分', color='#2c3e50', size='12pt')
    #     self.perclos_plot_widget.setLabel('bottom', '检测轮数', color='#2c3e50', size='12pt')
    #     self.perclos_plot_widget.showGrid(x=True, y=True)
    #
    #     # 设置坐标轴从 (0, 0) 开始
    #     self.perclos_plot_widget.setXRange(0, 10, padding=0)
    #     self.perclos_plot_widget.setYRange(0, 1.0, padding=0)
    #
    #     # 设置横轴刻度为整数
    #     self.perclos_plot_widget.getAxis('bottom').setTickSpacing(levels=[(1, 0)])
    #
    #     # 添加红色阈值线（疲劳判断参考线）
    #     threshold_line = pg.InfiniteLine(pos=0.38, angle=0, pen=pg.mkPen(color='r', style=Qt.DashLine))
    #     self.perclos_plot_widget.addItem(threshold_line)
    #
    #     # 添加曲线对象
    #     self.perclos_curve = self.perclos_plot_widget.plot(pen=pg.mkPen(color='b', width=2))
    #
    #     layout.addWidget(self.perclos_plot_widget)
    #     layout.addStretch()
    #
    #     # 📈 车速趋势图初始化
    #     self.speed_x = []
    #     self.speed_y = []
    #
    #     self.speed_plot_widget = pg.PlotWidget()
    #     self.speed_plot_widget.setBackground('w')
    #     self.speed_plot_widget.setTitle("车速趋势图", color='#34495e', size='18pt')
    #     self.speed_plot_widget.setLabel('left', '速度 (km/h)', color='#2c3e50', size='12pt')
    #     self.speed_plot_widget.setLabel('bottom', '时间点', color='#2c3e50', size='12pt')
    #     self.speed_plot_widget.showGrid(x=True, y=True)
    #     self.speed_plot_widget.setYRange(0, 120)
    #     # self.speed_plot_widget.setXRange(0, 20)
    #     self.speed_plot_widget.setXRange(0,20)
    #     self.speed_plot_widget.getAxis('bottom').setTickSpacing(levels=[(1, 0)])
    #
    #
    #     self.speed_curve = self.speed_plot_widget.plot(pen=pg.mkPen(color='b', width=2))
    #
    #
    #     # 添加红色阈值线（超速判断参考线）
    #     threshold_line = pg.InfiniteLine(pos=80, angle=0, pen=pg.mkPen(color='r', style=Qt.DashLine))
    #     self.speed_plot_widget.addItem(threshold_line)
    #
    #
    #     layout.addWidget(self.speed_plot_widget)
    #
    #     return page

    def create_analytics_page(self):
        """创建数据分析页面（增强大屏风格 + 饼图 + 卡片 + 原始趋势图）"""

        page = QWidget()
        main_layout = QVBoxLayout(page)

        # 页面标题
        title = QLabel("📊 数据分析总览")
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 32px;
                font-weight: bold;
                padding: 20px;
            }
        """)
        main_layout.addWidget(title)

        # === 顶部：两张饼图 ===
        pie_layout = QHBoxLayout()

        def create_pie_chart_widget(self, title, data_dict, colors):
            chart = QtCharts.QChart()
            series = QtCharts.QPieSeries()
            for i, (label, value) in enumerate(data_dict.items()):
                slice = series.append(label, value)
                slice.setBrush(QColor(colors[i % len(colors)]))
                if value > 0:
                    slice.setLabel(f"{label} ({value})")
                    slice.setLabelVisible(True)
            chart.addSeries(series)
            chart.setTitle(title)
            chart.setBackgroundBrush(QBrush(Qt.white))
            chart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)
            chart_view = QtCharts.QChartView(chart)
            chart_view.setRenderHint(QPainter.Antialiasing)
            chart_view.setMinimumHeight(260)
            return chart, series, chart_view

        # 示例数据
        fatigue_data = {"疲劳": self.count_fatigue, "清醒": self.count_awake}
        behavior_data = {
            "激进": self.count_aggressive,
            "正常": self.count_normal,
            "超速": self.count_speeding,
            "碰撞": self.count_collision,
            "分心": self.count_distracted
        }
        fatigue_colors = ["#e74c3c", "#2ecc71"]
        behavior_colors = ["#f39c12", "#3498db", "#e74c3c", "#9b59b6", "#1abc9c"]

        self.fatigue_chart, self.fatigue_series, self.fatigue_chart_view = create_pie_chart_widget(self,
            "🧠 疲劳检测占比", fatigue_data, fatigue_colors)

        self.behavior_chart, self.behavior_series, self.behavior_chart_view =create_pie_chart_widget(self,
            "🚗 行为状态占比", behavior_data, behavior_colors)

        pie_layout.addWidget(self.fatigue_chart_view)
        pie_layout.addWidget(self.behavior_chart_view)

        main_layout.addLayout(pie_layout)

        # === 中部：统计卡片 ===
        card_layout = QHBoxLayout()

        def create_stat_card(label_text, color, attr_name):
            frame = QFrame()
            frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {color};
                    border-radius: 15px;
                    padding: 15px;
                }}
                QLabel {{
                    color: white;
                }}
            """)
            vbox = QVBoxLayout(frame)
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 18px;")
            value = QLabel("0")
            value.setStyleSheet("font-size: 28px; font-weight: bold;")
            setattr(self, attr_name, value)  # 保存 value label 到 self
            vbox.addWidget(label)
            vbox.addWidget(value)
            return frame

        card1 = create_stat_card("疲劳报警次数", "#e67e22", "card_label_fatigue")
        card2 = create_stat_card("超速次数", "#e74c3c", "card_label_speeding")
        card3 = create_stat_card("碰撞报警次数", "#9b59b6", "card_label_collision")

        # card1 = create_stat_card("疲劳报警次数", "7", "#e67e22")
        # card2 = create_stat_card("超速次数", "5", "#e74c3c")
        # card3 = create_stat_card("碰撞报警次数", "2", "#9b59b6")

        card_layout.addWidget(card1)
        card_layout.addWidget(card2)
        card_layout.addWidget(card3)
        main_layout.addLayout(card_layout)

        # === 下部趋势图区域：Perclos + 车速 ===
        trend_layout = QVBoxLayout()

        # Perclos
        self.perclos_x = []
        self.perclos_y = []
        self.perclos_plot_widget = pg.PlotWidget()
        self.perclos_plot_widget.setBackground('w')
        self.perclos_plot_widget.setTitle("Perclos 疲劳得分趋势", color='#34495e', size='18pt')
        self.perclos_plot_widget.setLabel('left', 'Perclos 得分', color='#2c3e50', size='12pt')
        self.perclos_plot_widget.setLabel('bottom', '检测轮数', color='#2c3e50', size='12pt')
        self.perclos_plot_widget.showGrid(x=True, y=True)
        self.perclos_plot_widget.setXRange(0, 10, padding=0)
        self.perclos_plot_widget.setYRange(0, 1.0, padding=0)
        self.perclos_plot_widget.getAxis('bottom').setTickSpacing(levels=[(1, 0)])
        self.perclos_curve = self.perclos_plot_widget.plot(pen=pg.mkPen(color='b', width=2))
        threshold_line1 = pg.InfiniteLine(pos=0.38, angle=0, pen=pg.mkPen(color='r', style=Qt.DashLine))
        self.perclos_plot_widget.addItem(threshold_line1)
        trend_layout.addWidget(self.perclos_plot_widget)

        # Speed
        self.speed_x = []
        self.speed_y = []
        self.speed_plot_widget = pg.PlotWidget()
        self.speed_plot_widget.setBackground('w')
        self.speed_plot_widget.setTitle("车速趋势图", color='#34495e', size='18pt')
        self.speed_plot_widget.setLabel('left', '速度 (km/h)', color='#2c3e50', size='12pt')
        self.speed_plot_widget.setLabel('bottom', '时间点', color='#2c3e50', size='12pt')
        # 2c3e50', size='12pt')
        self.speed_plot_widget.showGrid(x=True, y=True)
        self.speed_plot_widget.setYRange(0, 120)
        self.speed_plot_widget.setXRange(0, 20)
        self.speed_plot_widget.getAxis('bottom').setTickSpacing(levels=[(1, 0)])
        self.speed_curve = self.speed_plot_widget.plot(pen=pg.mkPen(color='b', width=2))
        threshold_line2 = pg.InfiniteLine(pos=80, angle=0, pen=pg.mkPen(color='r', style=Qt.DashLine))
        self.speed_plot_widget.addItem(threshold_line2)
        trend_layout.addWidget(self.speed_plot_widget)

        main_layout.addLayout(trend_layout)
        return page
    @Slot(float)
    def update_speed(self, speed_val: float):
        """更新速度显示与趋势图"""
        self.label_speed_value.setText(f"{speed_val:.2f} km/h")

        # 设置字体颜色和报警
        if speed_val > 80:
            self.label_speed_value.setStyleSheet("color: red; font-size: 18px;")

            self.label_9.setText("<font color=red>超速驾驶!!!</font>")

            alarm_msg = f"{datetime.now().strftime('%H:%M:%S')} - 车速过快 - 当前：{speed_val:.1f} km/h"

            # 报警，如果已经在报警了，则略过
            if not pygame.mixer.get_busy():
                # 加载音频
                sound = pygame.mixer.Sound("resources/audio/alarm_80.mp3")
                # 播放3次（含原声，共播放3次）
                sound.play(loops=2)


            if hasattr(self, "alert_list"):
                self.alert_list.addItem(alarm_msg)

            self.count_speeding += 1
            self.update_analytics_data()
        else:
            self.label_speed_value.setStyleSheet("color: #007bff; font-size: 18px;")

        # 更新图表,x 随调用次数增加
        self.speed_x.append(self.speed_counter)
        self.speed_y.append(speed_val)
        self.speed_counter += 1

        if len(self.speed_x) > 20:
            self.speed_x = self.speed_x[1:]
            self.speed_y = self.speed_y[1:]

        # 设置动态 X 范围
        if self.speed_x:
            self.speed_plot_widget.setXRange(self.speed_x[0], self.speed_x[-1])

        if hasattr(self, 'speed_curve'):
            self.speed_curve.setData(self.speed_x, self.speed_y)

        # 更新数据库
        session = SessionLocal()
        if session is None:
            self.printf("数据库连接失败，无法保存速度记录。")
            return
        session.add(SpeedRecord(timestamp=datetime.now(), speed=speed_val))
        session.commit()
        session.close()

    def update_perclos(self, perclos_val: float):
        """更新 Perclos 曲线图"""
        self.perclos_y.append(perclos_val)
        self.perclos_x.append(self.perclos_counter)
        self.perclos_counter += 1
        if len(self.perclos_y) > 20:
            self.perclos_y = self.perclos_y[1:]
            self.perclos_x = self.perclos_x[1:]

        # 设置动态 X 范围
        if self.perclos_x:
            self.perclos_plot_widget.setXRange(self.perclos_x[0], self.perclos_x[-1])

        if hasattr(self, 'perclos_curve'):
            self.perclos_curve.setData(self.perclos_x, self.perclos_y)

    @Slot(bool)
    def update_aggressive_flag(self, flag: bool):
        print(f"[UI] 激进驾驶状态：{flag}")
        if flag:
            self.label_9.setText("<font color='orange'>激进驾驶</font>")

            self.count_aggressive += 1
        else:
            self.count_normal += 1
        self.update_analytics_data()

    @Slot(bool)
    def update_collision_status(self, flag: bool):
        if flag:
            print("[碰撞] 🚨 发生碰撞！")
            self.label_collision_status.setText("<font color='red'>🚨 即将碰撞！</font>")
            # 报警提示
            if not pygame.mixer.get_busy():
                sound = pygame.mixer.Sound("resources/audio/alarm_80.mp3")
                sound.play(loops=2)

            # 添加报警列表记录
            if hasattr(self, "alert_list"):
                time_str = datetime.now().strftime('%H:%M:%S')
                self.alert_list.addItem(f"{time_str} - 碰撞报警")

            self.count_collision += 1
            self.update_analytics_data()
        else:
            self.label_collision_status.setText("<font color='green'>正常驾驶</font>")
            print("[碰撞] 状态正常")

    def update_analytics_data(self):
        # 更新饼图数据
        fatigue_data = {
            "疲劳": self.count_fatigue,
            "清醒": self.count_awake
        }
        fatigue_colors = ["#e74c3c", "#2ecc71"]

        self.fatigue_series.clear()
        for i, (label, value) in enumerate(fatigue_data.items()):
            slice = self.fatigue_series.append(label, value)
            slice.setBrush(QColor(fatigue_colors[i]))
            if value > 0:
                slice.setLabel(f"{label} ({value})")
                slice.setLabelVisible(True)

        # 保持固定颜色顺序
        behavior_data = {
            "激进": self.count_aggressive,
            "正常": self.count_normal,
            "超速": self.count_speeding,
            "碰撞": self.count_collision,
            "分心": self.count_distracted
        }
        behavior_colors = ["#f39c12", "#3498db", "#e74c3c", "#9b59b6", "#1abc9c"]

        self.behavior_series.clear()
        for i, (label, value) in enumerate(behavior_data.items()):
            slice = self.behavior_series.append(label, value)
            slice.setBrush(QColor(behavior_colors[i]))
            if value > 0:
                slice.setLabel(f"{label} ({value})")
                slice.setLabelVisible(True)

        # 更新标签文本
        self.card_label_fatigue.setText(str(self.count_fatigue))
        self.card_label_speeding.setText(str(self.count_speeding))
        self.card_label_collision.setText(str(self.count_collision))

    def create_history_page(self):
        """创建历史记录页面（左右分栏 + 表头排序）"""
        from PySide2.QtWidgets import QHeaderView

        page = QWidget()
        layout = QVBoxLayout(page)

        # 页面标题
        title = QLabel("📋 历史记录")
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 28px;
                font-weight: bold;
                padding: 20px;
            }
        """)
        layout.addWidget(title)

        # 刷新按钮区域
        btn_layout = QHBoxLayout()
        self.btn_reload_log = QPushButton("🔄 刷新记录")
        self.btn_reload_log.setFixedWidth(160)
        self.btn_reload_log.setStyleSheet("font-size: 15px; padding: 8px;")
        btn_layout.addWidget(self.btn_reload_log)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # 横向布局：左侧是疲劳记录，右侧是速度记录
        table_layout = QHBoxLayout()

        # 疲劳检测历史记录表
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["时间", "检测轮", "Perclos值", "状态"])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.history_table.setStyleSheet("font-size: 14px;")
        self.history_table.setSortingEnabled(True)  # ✅ 启用排序
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)



        left_layout = QVBoxLayout()
        fatigue_label = QLabel("🧠 疲劳检测记录")
        fatigue_label.setStyleSheet("""
                    QLabel {
                        font-size: 20px;  /* Increase font size */
                        font-weight: bold;  /* Optional: Make the text bold */
                        color: #2c3e50;  /* Optional: Set text color */
                    }
                """)
        left_layout.addWidget(fatigue_label)
        left_layout.addWidget(self.history_table)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        # 车速历史记录表
        self.speed_table = QTableWidget()
        self.speed_table.setColumnCount(2)
        self.speed_table.setHorizontalHeaderLabels(["时间", "车速 (km/h)"])
        self.speed_table.horizontalHeader().setStretchLastSection(True)
        self.speed_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.speed_table.setStyleSheet("font-size: 14px;")
        self.speed_table.setSortingEnabled(True)  # ✅ 启用排序
        self.speed_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)



        right_layout = QVBoxLayout()

        # Create the label with enhanced styling
        speed_label = QLabel("🚗 车速记录")
        speed_label.setStyleSheet("""
                    QLabel {
                        font-size: 20px;  /* Increase font size */
                        font-weight: bold;  /* Make the text bold */
                        color: #2c3e50;  /* Set text color */
                    }
                """)
        right_layout.addWidget(speed_label)
        right_layout.addWidget(self.speed_table)
        right_widget = QWidget()
        right_widget.setLayout(right_layout)

        # 添加左右两个表格
        table_layout.addWidget(left_widget)
        table_layout.addWidget(right_widget)
        layout.addLayout(table_layout)

        # 加载数据函数
        def load_history():
            session = SessionLocal()

            # 疲劳记录
            fatigue_data = session.query(FatigueRecord).order_by(FatigueRecord.timestamp.desc()).limit(100).all()
            self.history_table.setRowCount(len(fatigue_data))
            for row_idx, record in enumerate(fatigue_data):
                row = [
                    record.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    str(record.epoch),
                    f"{record.perclos_score:.3f}",
                    record.status
                ]
                for col_idx, cell in enumerate(row):
                    item = QTableWidgetItem(cell)
                    if cell == "疲劳":
                        item.setForeground(QBrush(QColor("red")))
                    self.history_table.setItem(row_idx, col_idx, item)

            # 车速记录
            speed_data = session.query(SpeedRecord).order_by(SpeedRecord.timestamp.desc()).limit(100).all()
            self.speed_table.setRowCount(len(speed_data))
            for row_idx, record in enumerate(speed_data):
                row = [
                    record.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    f"{record.speed:.2f}"
                ]
                for col_idx, cell in enumerate(row):
                    item = QTableWidgetItem(cell)
                    self.speed_table.setItem(row_idx, col_idx, item)

            session.close()

        # 首次加载 + 绑定刷新按钮
        load_history()
        self.btn_reload_log.clicked.connect(load_history)

        return page

    def create_settings_page(self):
        """创建系统设置页面"""
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("⚙️ 系统设置")
        title.setStyleSheet("""
                       QLabel {
                           color: #2c3e50;
                           font-size: 28px;
                           font-weight: bold;
                           padding: 20px;
                           margin-bottom: 20px;
                       }
                   """)
        layout.addWidget(title)

        # 警报音设置 TODO :实际实现，再加个选择报警音？
        self.alarm_checkbox = QCheckBox("启用报警音")
        self.alarm_checkbox.setChecked(True)
        self.alarm_checkbox.setStyleSheet("font-size: 20px;")
        layout.addWidget(self.alarm_checkbox)

        # 眼睛阈值调整 TODO：实际实现
        self.eye_thresh_slider = QSlider(Qt.Horizontal)
        self.eye_thresh_slider.setMinimum(5)
        self.eye_thresh_slider.setMaximum(30)
        self.eye_thresh_slider.setValue(15)
        self.eye_thresh_label = QLabel("眼睛闭合阈值: 0.15")
        self.eye_thresh_slider.valueChanged.connect(
            lambda val: self.eye_thresh_label.setText(f"眼睛闭合阈值: {val / 100:.2f}"))
        layout.addWidget(self.eye_thresh_label)
        layout.addWidget(self.eye_thresh_slider)

        # 嘴巴阈值调整 TODO：实际实现
        self.mouth_thresh_slider = QSlider(Qt.Horizontal)
        self.mouth_thresh_slider.setMinimum(30)
        self.mouth_thresh_slider.setMaximum(100)
        self.mouth_thresh_slider.setValue(65)
        self.mouth_thresh_label = QLabel("打哈欠阈值: 0.65")
        self.mouth_thresh_slider.valueChanged.connect(
            lambda val: self.mouth_thresh_label.setText(f"打哈欠阈值: {val / 100:.2f}"))
        layout.addWidget(self.mouth_thresh_label)
        layout.addWidget(self.mouth_thresh_slider)

        layout.addStretch()

        return page


    def create_alerts_page(self):
        """创建报警管理页面"""
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("🚨 报警管理")
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 28px;
                font-weight: bold;
                padding: 20px;
            }
        """)
        layout.addWidget(title)

        # 报警列表显示
        self.alert_list = QListWidget()
        self.alert_list.setStyleSheet("""
            QListWidget {
                font-size: 14px;
                padding: 10px;
                background-color: #fffbea;
                border: 1px solid #e6c200;
            }
            QListWidget::item {
                padding: 6px;
            }
        """)
        layout.addWidget(self.alert_list)

        # 按钮区域
        btn_layout = QHBoxLayout()
        self.btn_clear_alerts = QPushButton("🧹 清空记录")
        self.btn_clear_alerts.setFixedWidth(120)
        self.btn_clear_alerts.setStyleSheet("font-size: 18px; padding: 6px;")

        self.btn_export_alerts = QPushButton("📁 导出报警记录")
        self.btn_export_alerts.setFixedWidth(160)
        self.btn_export_alerts.setStyleSheet("font-size: 18px; padding: 6px;")

        btn_layout.addWidget(self.btn_clear_alerts)
        btn_layout.addWidget(self.btn_export_alerts)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # 功能：清空
        self.btn_clear_alerts.clicked.connect(self.alert_list.clear)

        # 功能：导出
        def export_alerts():
            path, _ = QFileDialog.getSaveFileName(None, "导出报警记录", "alerts.csv", "CSV 文件 (*.csv)")
            if path:
                with open(path, 'w', encoding='utf-8', newline='') as f:
                    import csv
                    writer = csv.writer(f)
                    writer.writerow(["时间", "内容"])
                    for index in range(self.alert_list.count()):
                        item_text = self.alert_list.item(index).text()
                        if " - " in item_text:
                            time, msg = item_text.split(" - ", 1)
                            writer.writerow([time, msg])
                        else:
                            writer.writerow(["", item_text])

        self.btn_export_alerts.clicked.connect(export_alerts)

        layout.addStretch()
        return page


    def setup_menubar(self, MainWindow):
        """设置菜单栏"""
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

        # 添加菜单项
        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.actionOpen_camera)
        self.menu.addAction(self.actionClose_camera)

    def setup_statusbar(self, MainWindow):
        """设置状态栏"""
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

    def setup_tab_connections(self):
        """设置Tab按钮连接"""
        self.btn_monitor.clicked.connect(lambda: self.switch_tab(0))
        self.btn_analytics.clicked.connect(lambda: self.switch_tab(1))
        self.btn_history.clicked.connect(lambda: self.switch_tab(2))
        self.btn_settings.clicked.connect(lambda: self.switch_tab(3))
        self.btn_alerts.clicked.connect(lambda: self.switch_tab(4))

    def switch_tab(self, index):
        """切换标签页"""
        # 设置当前页面
        self.stacked_widget.setCurrentIndex(index)

        # 更新按钮状态
        for i, button in enumerate(self.tab_buttons):
            button.setChecked(i == index)

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
            QLabel {{
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

    def load_yolo_model(self):
        """弹出文件选择框并加载 YOLOv5 模型"""
        from PySide2.QtWidgets import QFileDialog
        from models.experimental import attempt_load
        from utils.general import check_img_size
        from utils.torch_utils import select_device
        import torch
        from numpy import random

        # 打开文件选择对话框
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "选择 YOLOv5 模型文件",
            "./weights",  # 默认打开路径
            "YOLO 模型 (*.pt)"
        )

        if not file_path:
            self.printf("取消加载模型。")
            return

        imgsz = 640
        device = select_device('')
        half = device.type != 'cpu'

        try:
            self.model = attempt_load(file_path, map_location=device)
            self.imgsz = check_img_size(imgsz, s=self.model.stride.max())
            self.device = device
            self.half = half
            if self.half:
                self.model.half()
            self.names = self.model.module.names if hasattr(self.model, 'module') else self.model.names
            self.colors = [[random.randint(0, 255) for _ in range(3)] for _ in self.names]

            self.printf(f"✅ 模型加载成功：{file_path}")
            self.status_text.setText("模型已加载")
            self.status_indicator.setStyleSheet("color: #f1c40f; font-size: 24px;")
        except Exception as e:
            self.printf(f"❌ 加载模型失败: {e}")
            self.status_text.setText("模型加载失败")
            self.status_indicator.setStyleSheet("color: red; font-size: 24px;")

