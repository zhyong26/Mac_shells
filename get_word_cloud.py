#!/usr/bin/env python
# coding=utf-8
import jieba
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import argparse
import os
import sys

def get_macos_font():
    """自动化获取 macOS 可用的中文字体路径"""
    paths = [
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        "/System/Library/Fonts/Hiragino Sans GB.ttc"
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return None

def generate_combined_analysis(file_paths, font_path=None, stop_words_path="~/Project/Python_wordcloud/stopwords/scu_stopwords.txt", exclude_words=None, skip_top=0):
    all_word_counts = Counter()
    processed_files = 0

    # 1. 停用词与排除词处理
    filter_set = set()
    if stop_words_path and os.path.exists(stop_words_path):
        with open(stop_words_path, 'r', encoding='utf-8') as f:
            filter_set.update([line.strip() for line in f.readlines() if line.strip()])
    if exclude_words:
        filter_set.update(exclude_words)

    # 2. 文本处理
    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f"跳过不存在的文件: {file_path}")
            continue
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if not content.strip(): continue
                words = jieba.cut(content)
                filtered = [w for w in words if len(w) > 1 and w not in filter_set]
                all_word_counts.update(filtered)
                processed_files += 1
        except Exception as e:
            print(f"读取文件 {file_path} 出错: {e}")

    # 3. 数据校验与 Skip 逻辑
    if not all_word_counts:
        print("错误：未提取到任何有效关键词，请检查输入文件内容或编码。")
        return

    if skip_top > 0:
        top_n = [item[0] for item in all_word_counts.most_common(skip_top)]
        print(f"已跳过最高频词: {top_n}")
        for w in top_n:
            del all_word_counts[w]

    if not all_word_counts:
        print("错误：跳过高频词后，数据为空。")
        return

    # 4. 字体适配 (核心修复点)
    final_font = font_path
    if not final_font or not os.path.exists(final_font):
        if sys.platform == "darwin":  # macOS
            final_font = get_macos_font()
        elif sys.platform == "win32": # Windows
            final_font = "C:/Windows/Fonts/simhei.ttf"

    if not final_font or not os.path.exists(final_font):
        print("错误：未找到有效的字体文件，请通过 --font 参数手动指定。")
        return

    # 5. 生成词云
    try:
        print(f"正在使用字体: {final_font}")
        wc = WordCloud(
            font_path=final_font,
            background_color='white',
            width=1000,
            height=800,
            max_words=150
        )
        wc.generate_from_frequencies(all_word_counts)

        output_name = "analysis_result.png"
        wc.to_file(output_name)
        print(f"成功！处理文件: {processed_files} | 结果保存至: {os.path.abspath(output_name)}")

        # 打印排名前10的词供校验
        print("最终分析高频词 (Top 20):", all_word_counts.most_common(20))

    except Exception as e:
        print(f"词云生成失败，具体原因: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="多文件词频分析工具")
    parser.add_argument("filenames", nargs='+', help="文件路径")
    parser.add_argument("--font", help="手动指定字体路径")
    parser.add_argument("--stop", help="停用词路径")
    parser.add_argument("--exclude", "-e", nargs='*', help="排除特定词")
    parser.add_argument("--skip_top", type=int, default=0, help="跳过前N个词")

    args = parser.parse_args()
    generate_combined_analysis(args.filenames, args.font, args.stop, args.exclude, args.skip_top)
