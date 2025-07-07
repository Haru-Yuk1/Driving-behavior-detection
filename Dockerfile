# 使用 Python 3.8.5 官方基础镜像
FROM python:3.8.5


# 将当前目录下的所有文件复制到容器的 /app 目录
ADD . /app

# 设置工作目录
WORKDIR . /app

# 安装编译依赖 + 更新 CMake
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    wget \
    curl \
    unzip \
    git \
    libboost-all-dev \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    && apt-get clean

# 手动安装 CMake 3.25.2（可根据需要替换为更高版本）
RUN wget https://github.com/Kitware/CMake/releases/download/v3.25.2/cmake-3.25.2-linux-x86_64.sh && \
    chmod +x cmake-3.25.2-linux-x86_64.sh && \
    ./cmake-3.25.2-linux-x86_64.sh --skip-license --prefix=/usr/local && \
    cmake --version

# 设置国内源加速安装 pip 包
RUN python -m pip install --upgrade pip \
    && pip install dlib==19.24.2 -i https://pypi.tuna.tsinghua.edu.cn/simple
# 启动命令
CMD ["python", "main.py"]
