# 使用官方 Python 基础镜像
FROM python:3.8.5

# 设置工作目录
WORKDIR /app

# 拷贝项目文件到容器中
COPY . /app

# 安装系统构建依赖（为编译 dlib 等 C++ 扩展）
#RUN apt-get update && \
#    apt-get install -y cmake build-essential python3-dev && \
#    apt-get clean && rm -rf /var/lib/apt/lists/*
# 安装 PySide2 运行依赖
RUN sed -i 's|http://deb.debian.org|http://mirrors.aliyun.com|g' /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y \
        libpulse-dev \
        libglib2.0-0 \
        libgstreamer1.0-0 \
        libgstreamer-plugins-base1.0-0 \
        libqt5multimedia5-plugins \
        libgl1-mesa-glx \
        libxkbcommon-x11-0 \
        libxcb-xinerama0 \
        libxcb1 \
        libx11-xcb1 \
        libxcb-glx0 \
        libxcb-keysyms1 \
        libxcb-image0 \
        libxcb-shm0 \
        libxcb-icccm4 \
        libxcb-sync1 \
        libxcb-xfixes0 \
        libxcb-shape0 \
        libxcb-render-util0 \
        libxrender1 \
        libsm6 \
        libxext6 \
        libxrandr2 \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY ./packages /packages
RUN pip install --upgrade pip && \
    pip install Cmake -i https://pypi.tuna.tsinghua.edu.cn/simple &&\
    pip install boost -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install --find-links=/packages -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 设置容器启动命令（可按项目实际启动方式修改）
CMD ["python", "main.py"]
