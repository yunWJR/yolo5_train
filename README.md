# YOLOv5 总结

[YOLOv5 git](https://github.com/ultralytics/yolov5)



## 1、环境部署

clone YOLOv5的代码到本地。

使用 conda 部署

```sh
conda create -n yolov5 python=3.8

conda activate yolov5

pip install -U -r requirements.txt
```

## 2、训练



### 2.1 训练数据准备

YOLOv5的数据集格式和之前的YOLOv3一致。

这里采用[精灵标注助手](http://www.jinglingbiaozhu.com/)来标注，然后转换为YOLOv5的训练格式。

1. `file_reform.py`：将分类的文件夹内的图片自动改名
2. 使用精灵标注助手的位置标注功能标注，并导出 XML 标注文件
3. 使用`jlbz_reform.py`：将精灵标注助手标注的 XML 文件转为 yolo 训练文件，并且输出分类数和分类列表（在names.txt中）

### 2.1 数据集的配置文件dataset.yaml

参考**data**下面的配置文件，编写自己训练数据的配置文件

```yaml

# train and val datasets (image directory or *.txt file with image paths)  
train: ./datasets/wheat/images/train/  
val: ./datasets/wheat/images/val/  

# number of classes  
nc: 1  

# class names  
names: ['xxx']  
```



### 2.3 训练自己的数据

其中，基于官方网络yolov5s.pt 继续训练

```sh
python train.py –data dataset.yaml --cfg  yolov5s.yaml --weights yolov5s.pt --batch-size 16
```

训练结果保存再 `run/train/exp*`下。



## 3、检测

```sh
python detect.py --source inference/images/ --weights  best.pt
```





