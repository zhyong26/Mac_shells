#!/bin/bash

# 检查是否有提交信息作为参数
if [ -z "$1" ]; then
  echo "Usage: ./git-push.sh <commit_message>"
  exit 1
fi

# 添加所有修改
git add .

# 提交
git commit -m "$1"

# 推送到远程仓库 (假设是 origin 和当前分支)
git push origin $(git branch --show-current)

echo "提交和推送完成！"

# 使用方法：
# 1. 保存为 git-push.sh
# 2. 赋予执行权限：chmod +x git-push.sh
# 3. 执行：./git-push.sh "你的提交信息"

