# 图片工具
图片压缩:`img-compress`
图片剪裁及压缩:`img-tool`

环境准备：
```
brew install webp libavif
brew install imagemagick
```

img-tool脚本说明：
这是一个整合了底部裁切（去水印）、尺寸缩放以及Google WebP/AVIF 高效压缩的终极脚本。

技术逻辑说明
该脚本之所以比普通压缩更高效，是因为它采用了流式处理 (Streaming Pipeline)：

- 无损中转：magick 处理完裁剪后，通过 tga:- 将未压缩的原始图像数据直接传给压缩引擎。
- 跳过磁盘 I/O：处理过程中不产生任何临时文件，直接在内存中完成裁剪到编码的转换，速度极快。
- 针对性优化：cwebp 和 avifenc 专门针对现代网页和存储进行了算法优化，其压缩比远超传统 magick 自带的输出。

# markdown导出为pdf或doc
脚本名称：`pkm-export`
安装环境：
```shell
brew install pandoc tectonic
```

# AI总结
安装 Ollama： 若未安装，请执行：brew install ollama。

下载模型： 推荐使用 qwen2.5 或 llama3，它们对中文支持较好且推理速度快。

ollama run qwen2.5:7b

# 使用qwen plus进行markdown总结
针对需要使用 通义千问 (Qwen) 在线 API 进行 Markdown 内容总结的需求，相比于本地的 Ollama，使用 API 的优势在于算力更强（可使用 Qwen-Max）且不占用本地 CPU/显卡资源。
## 环境准备
获取 API Key： 前往 阿里云 DashScope 控制台 创建并获取您的 `DASHSCOPE_API_KEY`。

安装 jq（用于解析 API 返回的 JSON 数据）：
```
brew install jq
```

# 词云图
功能：汇总多文件高频词分析，支持停用词、手动排除及跳过前N个高频词
文件：`get_word_cloud.py`
分词文件：https://github.com/goto456/stopwords
安装环境：
```python
pip install jieba wordcloud matplotlib
```
帮助文档：
```
usage: get_word_cloud.py [-h] [--font FONT] [--stop STOP] [--exclude [EXCLUDE ...]] [--skip_top SKIP_TOP] filenames [filenames ...]

多文件词频分析工具

positional arguments:
  filenames             文件路径

options:
  -h, --help            show this help message and exit
  --font FONT           手动指定字体路径
  --stop STOP           停用词路径
  --exclude, -e [EXCLUDE ...]
                        排除特定词
  --skip_top SKIP_TOP   跳过前N个词
```

# 自动整理文件夹
脚本名称：`organize.py`
使用说明：
```
用法: python3 脚本名.py <目标文件夹路径>
```

功能说明：
- 全深度递归扫描：不仅整理目标根目录，还会穿透所有子文件夹，将散落在深层路径的文件全部提取出来。

- 中文语义分类：根据文件扩展名，将文件自动归类至“图片”、“文档”、“安装包”、“压缩包”、“视频”、“音频”、“脚本与代码”、“设计工程”及“其他”等 9 个中文文件夹。

- 冲突防止机制：若目标分类文件夹中已存在同名文件，脚本会自动重命名新移动的文件（例如：测试文件.pdf 变为 测试文件_1.pdf），确保数据不会被覆盖。

- 自动清理冗余目录：在文件移动完成后，脚本会采用“自底向上”的逻辑检测并删除所有因文件移出而产生的空文件夹。

- 系统环境适配：针对 macOS 优化，自动忽略 .DS_Store 等系统隐藏文件，且在判定文件夹是否为空时会先行排除此类干扰文件。

- 动态路径支持：支持在执行命令时实时输入目标路径，兼容 ~（家目录）及 .（当前目录）等快捷路径符。

# 使用 Python 脚本一键上传图片到兰空图床并自动复制链接
脚本名称：`python_shells/upload_lsky.py`

这个脚本旨在实现一个目标：以最快速度将本地图片转换为可用的网络链接。

它具备以下核心特性：
- 完全脱离浏览器：直接在终端（命令行）通过一条命令完成上传。
- 基于文件名传参：无需复杂的配置，只需告诉脚本你要传哪个文件。
- 自动复制到剪切板：这是灵魂功能！上传成功后，图片 URL 会自动进入你的系统剪切板，你只需在 Markdown 编辑器里按下 Ctrl+V (或 Cmd+V) 即可。
- 安全鉴权：使用 Lsky Pro V2 标准的 API Token 进行验证，无需暴露账号密码。

具体使用方法见：[使用 Python 脚本一键上传图片到兰空图床并自动复制链接 | 材料与逻辑](https://zhyong.site/posts/445e.html)

# Python 自动化实践：Typora 自定义上传接口与兰空图床集成
脚本名称：`python_shells/typora_upload.py`
具体使用方法：[Python 自动化实践：Typora 自定义上传接口与兰空图床集成 | 材料与逻辑](https://zhyong.site/posts/36e9.html)

# 通过 rclone 自动备份 Lsky Pro（兰空图床）数据至 OneDrive

脚本名称：`shell_scripts/lsky_backup.sh`

使用教程：[通过 rclone 自动备份 Lsky Pro（兰空图床）数据至 OneDrive | 材料与逻辑](https://zhyong.site/posts/70dc.html)

# 打开终端或执行清屏命令时显示一言
脚本名称：`shell_scripts/hitokoto.sh`
一言源文件：[hitokoto-osc/sentences-bundle: 一言开源社区官方提供的语句库，系 hitokoto.cn 数据库打包集合。语句接口默认使用此库。](https://github.com/hitokoto-osc/sentences-bundle)
将脚本中的第4行更改为实际路径
克隆或下载脚本文件，然后在`.zshrc`或`.bashrc`文件中加入
```
#打开终端时显示一言或按下c时执行
bash ~/Project/local_shells/hitokoto.sh

c(){
    clear
    bash ~/Project/local_shells/hitokoto.sh
}
```

# 下载图片
脚本名称：`python_shells/dl_imgs.py`

---

## 🛠️ 脚本介绍：通用网页大图抓取工具

该脚本是一个基于 **Python** 的轻量级自动化工具，专门用于从指定网页抓取并下载图片。它具备以下核心特性：

* **参数化运行**：通过命令行直接传递目标 URL，灵活便捷。
* **智能分类**：自动以“**日期_时间**”命名文件夹，确保每次抓取结果独立存储。
* **质量筛选**：内置大小过滤机制，自动剔除小于 **100KB** 的图标、头像或占位图，仅保留高质量大图。
* **高效并发**：采用多线程（ThreadPoolExecutor）技术，支持多张图片同步下载，显著缩短等待时间。
* **懒加载兼容**：支持识别 `src`、`data-src` 及 `data-original` 等多种 HTML 属性，应对现代博客的图片加载技术。

---

## 🚀 使用说明

### 1. 环境准备

确保您的电脑已安装 Python 3.x 环境，并运行以下命令安装必要的依赖库：

```bash
pip install requests beautifulsoup4

```

### 2. 运行脚本

打开终端（Terminal）或命令提示符（CMD），定位到脚本所在目录，执行以下命令：

**基本用法（推荐）：**

```bash
python your_script_name.py https://xxxxx

```

*执行后，脚本会自动在当前目录下创建一个形如 `20260224_103500` 的文件夹。*

**自定义保存目录：**
若想手动指定文件夹名称（如 `my_gallery`），请使用 `-o` 参数：

```bash
python your_script_name.py https://xxx -o my_gallery

```

### 3. 查看结果

* **控制台反馈**：脚本会实时显示下载进度及文件大小（如 `[5/20] 下载成功 (450.5KB): photo.jpg`）。
**过滤提示**：若图片小于 200KB，控制台将提示 `跳过/已删除`。

---

## ⚠️ 注意事项

1. **网络环境**：下载速度取决于您的网络带宽及目标服务器的响应速度。
2. **合规使用**：请确保抓取行为符合目标网站的 `robots.txt` 协议及版权规定，仅限个人学习或研究使用。
3. **防盗链说明**：脚本已内置 `Referer` 伪装，可应对多数博客平台的反爬策略。

# 自动化工具：将 Markdown 文档转换为静态 PNG 思维导图脚本

脚本名称：`python_shells/md2img.py`

具体使用说明查看：[自动化工具：将 Markdown 文档转换为静态 PNG 思维导图脚本 | 材料与逻辑](https://zhyong.site/posts/f040.html)

# Mac复制绝对路径到系统剪切板
文件：`shell_scripts/get_path.sh`

核心功能解释
- 路径转换：自动将相对路径 / 简写路径（如 ~）转换为标准绝对路径，保证路径准确性；
- 跨系统兼容：自动识别 macOS（pbcopy）和 Linux（xclip/xsel）的剪切板工具；
- 错误处理：包含文件存在性检查、工具检测、执行结果验证，避免新手踩坑；
- 友好提示：成功 / 失败都有清晰的可视化提示，直接显示复制的路径。
