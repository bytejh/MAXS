#!/bin/bash

# =======================
# Django 개발 환경 설정
# =======================
export  $(cat /root/mnsystem/.env.rnd | xargs)
export DJANGO_SETTINGS_MODULE=backend.settings.rnd
export DJANGO_SECRET_KEY='0qbv&y+nz+0%65j4=5$n6*k92l35fp%7jgq5uty3c3!wz!^n1g'

# 로그 파일 경로
LOG_DIR="/root/mnsystem/logs"
DJANGO_LOG_FILE="${LOG_DIR}/rnd_server.log"
VUE_LOG_FILE="${LOG_DIR}/vue_dev_server.log"

# 로그 디렉토리 확인 및 생성
if [ ! -d "$LOG_DIR" ]; then
  mkdir -p "$LOG_DIR"
  echo "Created log directory at $LOG_DIR"
fi

# =======================
# Django 서버 실행
# =======================
echo "Starting Django development server..."
nohup python /root/mnsystem/backend/manage.py runserver 0.0.0.0:8000 > "$DJANGO_LOG_FILE" 2>&1 &

# =======================
# Vue.js 개발 서버 실행
# =======================
echo "Starting Vue.js development server..."
cd /root/mnsystem/frontend
npm run serve -- --host 0.0.0.0 --port 8081 > "$VUE_LOG_FILE" 2>&1 &

echo "Django development server logs: $DJANGO_LOG_FILE"
echo "Vue.js development server logs: $VUE_LOG_FILE"

