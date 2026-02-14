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
