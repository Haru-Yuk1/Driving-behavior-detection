# 使用官方 Python 基础镜像
FROM python:3.8.5

# 设置工作目录
WORKDIR /app

# 安装依赖的系统库（如 dlib 和 PyQt5 需要）
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libgtk2.0-dev \
    libboost-all-dev \
    libgl1-mesa-glx \
    && apt-get clean

# 拷贝项目文件到容器中
COPY . /app

# 安装 Python 依赖
RUN pip install --upgrade pip \
    && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 设置容器启动命令（可按项目实际启动方式修改）
CMD ["python", "main.py"]
