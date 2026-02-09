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

无损中转：magick 处理完裁剪后，通过 tga:- 将未压缩的原始图像数据直接传给压缩引擎。
跳过磁盘 I/O：处理过程中不产生任何临时文件，直接在内存中完成裁剪到编码的转换，速度极快。
针对性优化：cwebp 和 avifenc 专门针对现代网页和存储进行了算法优化，其压缩比远超传统 magick 自带的输出。
