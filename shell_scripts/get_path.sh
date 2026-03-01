#!/bin/bash

# 函数：显示使用帮助
show_help() {
    echo "用法: $0 <文件路径>"
    echo "功能: 获取指定文件的绝对路径，并复制到系统剪切板"
    echo "示例:"
    echo "  $0 ./photo.jpg          # 获取当前目录下photo.jpg的绝对路径并复制"
    echo "  $0 ~/Documents/note.txt # 获取用户目录下note.txt的绝对路径并复制"
}

# 1. 检查参数数量
if [ $# -ne 1 ]; then
    echo "错误：参数数量不正确！"
    show_help
    exit 1
fi

# 2. 定义输入的文件路径，并转换为绝对路径
INPUT_PATH="$1"
# 使用readlink获取标准绝对路径（兼容Linux/macOS）
ABSOLUTE_PATH=$(readlink -f "$INPUT_PATH" 2>/dev/null)

# 如果readlink -f失败（macOS默认没有-f参数），改用realpath或手动拼接
if [ -z "$ABSOLUTE_PATH" ]; then
    if command -v realpath &>/dev/null; then
        ABSOLUTE_PATH=$(realpath "$INPUT_PATH")
    else
        # 手动拼接：当前目录 + 相对路径
        ABSOLUTE_PATH="$(cd "$(dirname "$INPUT_PATH")" && pwd)/$(basename "$INPUT_PATH")"
    fi
fi

# 3. 检查文件是否存在
if [ ! -e "$ABSOLUTE_PATH" ]; then
    echo "错误：文件 '$INPUT_PATH' 不存在！"
    exit 1
fi

# 4. 检测系统剪切板工具
CLIPBOARD_CMD=""
if command -v pbcopy &>/dev/null; then
    # macOS 系统
    CLIPBOARD_CMD="pbcopy"
elif command -v xclip &>/dev/null; then
    # Linux 系统（需要先安装xclip：sudo apt install xclip / sudo yum install xclip）
    CLIPBOARD_CMD="xclip -selection clipboard"
elif command -v xsel &>/dev/null; then
    # Linux 备选工具
    CLIPBOARD_CMD="xsel -ib"
else
    echo "错误：未检测到剪切板工具！"
    echo "macOS 无需额外安装；Linux 请执行：sudo apt install xclip 或 sudo yum install xclip"
    exit 1
fi

# 5. 将绝对路径复制到剪切板
echo "$ABSOLUTE_PATH" | $CLIPBOARD_CMD

# 6. 验证并输出结果
if [ $? -eq 0 ]; then
    echo "✅ 成功！文件绝对路径已复制到剪切板："
    echo "   $ABSOLUTE_PATH"
else
    echo "❌ 失败：路径复制到剪切板出错！"
    exit 1
fi

exit 0
