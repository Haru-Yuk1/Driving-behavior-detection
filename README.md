# 人物专注性检测

## 项目介绍
该项目为人物专注性检测，分为两个检测部分，疲劳检测和分心行为检测。
疲劳检测部分，使用Dlib进行人脸关键点检测，然后通过计算眼睛和嘴巴的开合程度来判断是存在否闭眼或者打哈欠，并使用Perclos模型计算疲劳程度。

分心行为检测部分，使用Yolov5，检测是否存在玩手机、抽烟、喝水这三种行为。


## 使用方法
python版本：3.8.5

依赖：YoloV5、Dlib、PySide2

通过anaconda创建虚拟环境，并下载相关依赖

```
conda create -n yolov5 python==3.8.5
conda activate yolov5
pip install -r requirements.txt
```

然后直接运行main.py，即可使用本程序，具体效果可以观看演示视频。

[bilibili在线观看](https://www.bilibili.com/video/BV1MK4y1d7a8/)

各函数的信息，均在代码中写好了注释，如有疑问可以看原仓库。

## 修改

我修改了一点ui设计，将数据集上传

### 界面如下
1. 首页：展示视频及相关消息
![1.png](images/1.png)
2. 数据分析：展示Perclos疲劳得分
3. 历史记录：展示历史的一些得分数据
4. 系统设置：可以设置相关参数
5. 报警管理：记录一些报警情况


对项目的一些代码进行了简单修改


## 数据集

[数据集地址](https://aistudio.baidu.com/datasetdetail/80631/2)

## 训练
通过Yolov5训练
官方下载相应代码和模型

https://github.com/ultralytics/yolov5/releases

把代码更新到新的yolov5版本 2025/6/28

## 致谢

本项目由[该项目](https://github.com/JingyibySUTsoftware/Yolov5-deepsort-driverDistracted-driving-behavior-detection/tree/V1.0)修改而来，进行了简单的修改，增加了依赖配置，配置更简单。

