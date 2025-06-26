# -*- coding: utf-8 -*-

################################################################################
## 主窗口界面
## 基于原始UI文件改进，添加了现代化样式和更好的布局
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        # 设置窗口属性
        MainWindow.resize(1600, 1300)  # 增加宽度以适应左侧TabBar
        MainWindow.setMinimumSize(QSize(1300, 1200))

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
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

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
        self.status_text = QLabel("系统就绪")
        self.status_text.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                background: none;
            }
        """)
        self.status_indicator = QLabel("●")
        self.status_indicator.setStyleSheet("""
            QLabel {
                color: #2ecc71;
                font-size: 30px;
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
        self.info_card1.setMinimumWidth(430)

        self.label_2 = QLabel("疲劳检测:")
        self.label_2.setStyleSheet("font-weight: bold; color: #6c757d; font-size: 18px;")
        self.label_10 = QLabel("清醒")
        self.label_10.setStyleSheet("color: #008000; font-size: 18px;")

        self.info_layout1.addWidget(self.label_2)
        self.info_layout1.addWidget(self.label_10)
        self.info_layout1.addStretch()
        self.control_layout.addWidget(self.info_card1)

        # 检测信息卡片
        self.info_card2 = QFrame()
        self.info_card2.setStyleSheet(card_style)
        self.info_card2.setMinimumWidth(430)
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
        self.info_card3.setMinimumWidth(430)

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

        self.label_6 = QLabel("手机")
        self.label_6.setStyleSheet("font-weight: bold; color: #6c757d; font-size: 18px;")
        self.label_7 = QLabel("抽烟")
        self.label_7.setStyleSheet("font-weight: bold; color: #6c757d; font-size: 18px;")
        self.label_8 = QLabel("喝水")
        self.label_8.setStyleSheet("font-weight: bold; color: #6c757d; font-size: 18px;")

        self.stats_layout.addWidget(self.label_6)
        self.stats_layout.addWidget(self.label_7)
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

    def create_analytics_page(self):
        """创建数据分析页面"""
        page = QWidget()
        layout = QVBoxLayout(page)

        # 标题
        title = QLabel("📊 数据分析")
        title.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 28px;
                font-weight: bold;
                padding: 20px;
            }
        """)
        layout.addWidget(title)

        # 📈 Perclos 曲线图初始化
        self.perclos_x = []  # 横轴：检测轮数
        self.perclos_y = []  # 纵轴：Perclos 值

        self.perclos_plot_widget = pg.PlotWidget()
        self.perclos_plot_widget.setBackground('w')
        self.perclos_plot_widget.setTitle("Perclos 疲劳得分趋势", color='#34495e', size='18pt')
        self.perclos_plot_widget.setLabel('left', 'Perclos 得分', color='#2c3e50', size='12pt')
        self.perclos_plot_widget.setLabel('bottom', '检测轮数', color='#2c3e50', size='12pt')
        self.perclos_plot_widget.showGrid(x=True, y=True)

        # 设置坐标轴从 (0, 0) 开始
        self.perclos_plot_widget.setXRange(0, 10, padding=0)
        self.perclos_plot_widget.setYRange(0, 1.0, padding=0)

        # 设置横轴刻度为整数
        self.perclos_plot_widget.getAxis('bottom').setTickSpacing(levels=[(1, 0)])

        # 添加红色阈值线（疲劳判断参考线）
        threshold_line = pg.InfiniteLine(pos=0.38, angle=0, pen=pg.mkPen(color='r', style=Qt.DashLine))
        self.perclos_plot_widget.addItem(threshold_line)

        # 添加曲线对象
        self.perclos_curve = self.perclos_plot_widget.plot(pen=pg.mkPen(color='b', width=2))

        layout.addWidget(self.perclos_plot_widget)
        layout.addStretch()

        return page

    def create_history_page(self):
        """创建历史记录页面"""
        page = QWidget()
        layout = QVBoxLayout(page)

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

        # 按钮区域
        btn_layout = QHBoxLayout()
        self.btn_reload_log = QPushButton("🔄 刷新记录")
        self.btn_reload_log.setFixedWidth(160)
        self.btn_reload_log.setStyleSheet("font-size: 15px; padding: 8px;")
        btn_layout.addWidget(self.btn_reload_log)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        # # 按钮和表格区域
        # control_layout = QHBoxLayout()
        # load_btn = QPushButton("📂 加载历史文件")
        # load_btn.setFixedWidth(180)
        # load_btn.setStyleSheet("padding: 10px; font-size: 16px;")
        # control_layout.addWidget(load_btn)
        # control_layout.addStretch()
        # layout.addLayout(control_layout)

        # 表格区域
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["时间", "检测轮", "Perclos值", "状态"])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.history_table.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.history_table)

        # 加载日志函数
        def load_history():
            import os, csv
            log_path = os.path.join(os.getcwd(), "logs", "history_log.csv")
            self.history_table.setRowCount(0)

            if not os.path.exists(log_path):
                self.printf("未找到日志记录文件。")
                return

            with open(log_path, encoding="utf-8") as file:
                reader = csv.reader(file)
                headers = next(reader, None)  # 跳过表头
                for row_idx, row in enumerate(reader):
                    self.history_table.insertRow(row_idx)
                    for col_idx, cell in enumerate(row):
                        item = QTableWidgetItem(cell)
                        if cell == "疲劳":
                            item.setForeground(QBrush(QColor("red")))
                        self.history_table.setItem(row_idx, col_idx, item)

        # 初始加载一次
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
                       }
                   """)
        layout.addWidget(title)

        # 警报音设置
        self.alarm_checkbox = QCheckBox("启用报警音")
        self.alarm_checkbox.setChecked(True)
        self.alarm_checkbox.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.alarm_checkbox)

        # 眼睛阈值调整
        self.eye_thresh_slider = QSlider(Qt.Horizontal)
        self.eye_thresh_slider.setMinimum(5)
        self.eye_thresh_slider.setMaximum(30)
        self.eye_thresh_slider.setValue(15)
        self.eye_thresh_label = QLabel("眼睛闭合阈值: 0.15")
        self.eye_thresh_slider.valueChanged.connect(
            lambda val: self.eye_thresh_label.setText(f"眼睛闭合阈值: {val / 100:.2f}"))
        layout.addWidget(self.eye_thresh_label)
        layout.addWidget(self.eye_thresh_slider)

        # 嘴巴阈值调整
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
        self.btn_clear_alerts.setStyleSheet("font-size: 14px; padding: 6px;")

        self.btn_export_alerts = QPushButton("📁 导出报警记录")
        self.btn_export_alerts.setFixedWidth(160)
        self.btn_export_alerts.setStyleSheet("font-size: 14px; padding: 6px;")

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