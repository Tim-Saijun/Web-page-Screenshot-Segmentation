[![PyPI - Version](https://img.shields.io/pypi/v/Web_page_Screenshot_Segmentation)](https://pypi.org/project/Web_page_Screenshot_Segmentation/) [![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/Tim-Saijun/Web-page-Screenshot-Segmentation/python-publish.yml)](https://github.com/Tim-Saijun/Web-page-Screenshot-Segmentation/actions/workflows/python-publish.yml)[![PyPI - License](https://img.shields.io/pypi/l/Web_page_Screenshot_Segmentation)](https://pypi.org/project/Web_page_Screenshot_Segmentation/)   [![Static Badge](https://img.shields.io/badge/%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-8A2BE2)](README-ZH.md) [![Static Badge](https://img.shields.io/badge/English-blue)](README.md)

## 介绍
该项目用于根据文本的高度将网页的长截图分割成几个部分。主要思想是找到图像的低变化区域，然后在低变化区域中找到分割线。
![红线是分割线](images/demo.png)
输出的是网页的小而完整的图像，可以用于使用[Screen-to-code](https://github.com/abi/screenshot-to-code)生成网页或训练模型。
更多结果可以在[images](images)目录中找到。

## 开始使用
### 安装依赖项
```
pip install opencv-python numpy
```
### 拉取代码
```bash
git clone https://github.com/Tim-Saijun/Web-page-Screenshot-Segmentation.git
cd Web-page-Screenshot-Segmentation/Web_page_Screenshot_Segmentation
```

## 在命令行中使用
获取图像的分割线的高度
```bash
python master.py --file_path path/to/image.jpg --split True --height_threshold 102 --variation_threshold 0.5 --color_threshold 100 --color_variation_threshold 15 --merge_threshold 350
```
在图像中画出分割线
```bash
python spliter.py --image_file path/to/image.jpg --hl [100,200] --color (0,255,0)
```
更多用法解释请参照帮助：
```bash
python master.py --help
python spliter.py --help
```

## 使用Pypi包
```bash
 pip install Web-page-Screenshot-Segmentation
```
### split_heights 函数

`split_heights` 函数用于根据各种阈值将图像分割成几个部分。它接受以下参数：

- `file_path`: 图像文件的路径。
- `split`: 一个布尔值，指示是否分割图像。
- `height_threshold`: 低变化区域的高度阈值。
- `variation_threshold`: 低变化区域的变化阈值。
- `color_threshold`: 颜色差异的阈值。
- `color_variation_threshold`: 颜色差异变化的阈值。
- `merge_threshold`: 两条线之间最小距离的阈值。

如果 `split` 是 `False`，函数返回分割线的高程列表；如果 `split` 是 `True`，则返回分割图像的路径。

#### 示例用法

```python
import Web_page_Screenshot_Segmentation
from Web_page_Screenshot_Segmentation.master import split_heights

# 在 'path/to/image.jpg' 分割图像为几个部分
split_image_path = split_heights(
    file_path='path/to/image.jpg',
    split=True,
    height_threshold=102,
    variation_threshold=0.5,
    color_threshold=100,
    color_variation_threshold=15,
    merge_threshold=350
)

print(f"分割后的图像保存在 {split_image_path}")
```

在这个例子中，根据提供的阈值，'path/to/image.jpg' 的图像被分割成几个部分。分割后的图像保存在函数返回的路径。

### draw_line_from_file 函数

`draw_line_from_file` 函数用于在指定高度的图像上绘制线条。它接受以下参数：

- `image_file`: 图像文件的路径。
- `heights`: 在指定高度绘制线条的高程列表。
- `color`: 线条的颜色。默认颜色为红色 `(0, 0, 255)`。

该函数从提供的文件路径读取图像，在指定的高度绘制线条，然后将修改后的图像保存到新文件中。新文件保存在 `result` 目录下，与原始文件同名，但在文件扩展名前添加了 'result'。

如果函数在读取图像文件时遇到错误（例如，如果文件路径包含 '.' 或中文字符），则会抛出异常。

#### 示例用法

```python
import Web_page_Screenshot_Segmentation
from Web_page_Screenshot_Segmentation.spliter import draw_line_from_file

# 在 'path/to/image.jpg' 的图像上，在高度 100 和 200 处绘制线条
result_image_path = draw_line_from_file(
    image_file='path/to/image.jpg',
    heights=[100, 200],
    color=(0, 255, 0)  # 以绿色绘制线条
)

print(f"修改后的图像保存在 {result_image_path}")
```

在这个例子中，'path/to/image.jpg' 的图像被修改，以在高度 100 和 200 处绘制绿色线条。修改后的图像保存在函数返回的路径。
