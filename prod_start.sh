#!/bin/bash

# =======================
# Django 배포 환경 설정
# =======================
export $(cat /root/mnsystem/.env.prod | xargs)

# 로그 파일 경로
LOG_DIR="/root/mnsystem/logs"
GUNICORN_LOG="${LOG_DIR}/prod_gunicorn.log"
NGINX_LOG="${LOG_DIR}/prod_nginx.log"
VUE_BUILD_LOG="${LOG_DIR}/vue_build.log"

# 로그 디렉토리 확인 및 생성
if [ ! -d "$LOG_DIR" ]; then
  mkdir -p "$LOG_DIR"
  echo "Created log directory at $LOG_DIR"
fi

# =======================
# Vue.js 빌드 및 복사
# =======================
echo "Building Vue.js for production..."
cd /root/mnsystem/frontend
npm run build > "$VUE_BUILD_LOG" 2>&1
echo "Vue.js build logs: $VUE_BUILD_LOG"

# 빌드 결과 복사
echo "Copying Vue.js build files to /var/www/static/..."
sudo cp -r /root/mnsystem/frontend/dist/* /var/www/static/
echo "Vue.js build files successfully copied to /var/www/static/"

# =======================
# Gunicorn 서비스 재시작
# =======================
echo "Restarting Gunicorn service..."
sudo systemctl restart gunicorn > "$GUNICORN_LOG" 2>&1
echo "Gunicorn logs: $GUNICORN_LOG"

# =======================
# Nginx 서비스 재시작
# =======================
echo "Restarting Nginx service..."
sudo systemctl restart nginx > "$NGINX_LOG" 2>&1
echo "Nginx logs: $NGINX_LOG"

