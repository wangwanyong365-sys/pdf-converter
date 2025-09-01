# PDF 转换器

一个基于 Python 的图形界面应用程序，用于将 PDF 文件转换为 TXT 文本文件。

## 功能特性

- 📄 支持批量选择多个 PDF 文件
- 📁 自定义输出目录
- 🔄 可选择单独转换或合并转换
- 🎨 简洁美观的图形界面
- 🌐 支持中文界面

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 方法一：双击运行
直接双击 `run.bat` 文件启动程序

### 方法二：命令行运行
```bash
python pdf_converter.py
```

## 操作步骤

1. 点击"选择PDF文件"按钮选择一个或多个PDF文件
2. 点击"选择输出目录"按钮选择保存位置
3. 选择转换选项：
   - 不勾选：每个PDF单独转换为TXT文件
   - 勾选"将所有PDF合并为一个TXT文件"：合并所有PDF内容
4. 点击"转换为 TXT"按钮开始转换

## 项目结构

```
pdf_converter/
├── pdf_converter.py  # 主程序文件
├── requirements.txt  # 依赖包列表
└── run.bat          # Windows启动脚本
```

## 技术栈

- Python 3.x
- Tkinter (GUI界面)
- PyPDF2 (PDF处理)

## 许可证

MIT License