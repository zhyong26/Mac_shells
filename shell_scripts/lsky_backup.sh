#!/bin/bash

# --- 基础配置 ---
DB_CONTAINER="1Panel-mariadb-HnT9 根据实际替换"     # 数据库容器名
DB_USER="lsky-pro 根据实际替换"                     # 数据库用户名
DB_PASS="xxxxxxxxxxxxxx   根据实际替换"             # 数据库密码
DB_NAME="lsky-pro 根据实际替换"                     # 数据库名
SOURCE_DIR="/data/lsky-pro 根据docker目录映射"            # Lsky Pro 挂载根目录
BACKUP_TEMP_DIR="/data/backups/temp"   # 临时目录
REMOTE_NAME="onedrive 根据实际替换"                 # rclone配置名
REMOTE_PATH="Backup/LskyPro"           # 远程存储路径
RCLONE_CONF="$HOME/.config/rclone/rclone.conf"

DATE=$(date +%Y%m%d)
FILE_NAME="lsky_full_backup_$DATE.tar.gz"

# --- 环境准备 ---
mkdir -p $BACKUP_TEMP_DIR

# --- 1. 导出数据库 ---
# 注意：-u 和 -p 后不要加中括号或空格
# 备份命令：mariadb-dump，如果为mysql，备份命令为 /usr/bin/mysqldump 或 mysqldump
docker exec $DB_CONTAINER mariadb-dump -hlocalhost -u$DB_USER -p$DB_PASS $DB_NAME > $BACKUP_TEMP_DIR/db_backup_$DATE.sql

# 校验 SQL 文件是否存在
if [ ! -s "$BACKUP_TEMP_DIR/db_backup_$DATE.sql" ]; then
    echo "Database export failed."
    exit 1
fi

# --- 2. 打包核心文件 ---
tar -czvf $BACKUP_TEMP_DIR/$FILE_NAME \
    -C / \
    ${BACKUP_TEMP_DIR#/}/db_backup_$DATE.sql \
    ${SOURCE_DIR#/}/.env \
    ${SOURCE_DIR#/}/storage/app/uploads \
    ${SOURCE_DIR#/}/installed.lock

# --- 3. 同步至 OneDrive ---
rclone --config "$RCLONE_CONF" copy $BACKUP_TEMP_DIR/$FILE_NAME $REMOTE_NAME:$REMOTE_PATH

# --- 4. 清理 ---
rm -rf $BACKUP_TEMP_DIR/*
# 自动保留最近 30 天的远程备份
rclone --config "$RCLONE_CONF" delete $REMOTE_NAME:$REMOTE_PATH --min-age 30d
