#!/bin/bash

# 配置本地仓库路径（请确保路径正确）
BUNDLE_PATH="/Users/zhyong/Project/github_public_dl/sentences-bundle/sentences"

# 1. 随机选择一个 JSON 文件
FILES=("$BUNDLE_PATH"/*.json)
FILE_COUNT=${#FILES[@]}
SELECTED_FILE="${FILES[$((RANDOM % FILE_COUNT))]}"

# 2. 检查文件是否存在
if [ ! -f "$SELECTED_FILE" ]; then
    exit 1
fi

# 3. 使用更严谨的 jq 过滤逻辑
# -c 选项：紧凑输出
# shuf 重新引入：如果在 macOS，请确保已执行 `brew install coreutils` 并将 shuf 改为 gshuf
# 如果不想安装 coreutils，请看下方的纯 jq 方案
jq -r '.[] | "\(.hitokoto) @@@ \(.from // "未知") @@@ \(.from_who // "")"' "$SELECTED_FILE" | \
    shuf -n 1 | \
    awk -F ' @@@ ' '{print "\n「"$1"」\n—— "$2" "$3"\n"}'
