#!/usr/bin/env bash
# 간편 실행 스크립트
# 사용법: ./start.sh [local|docker] (기본값 local)
#
# API 설정:
# - 환경변수 BACKEND_URL로 백엔드 서버 주소 설정 가능 (기본값: http://localhost:8080)
# - 예: export BACKEND_URL=http://your-backend-server.com && ./start.sh
set -e
MODE=${1:-local}

if [[ "$MODE" == "docker" ]]; then
  echo "[INFO] Docker 모드로 애플리케이션을 실행합니다…"
  docker compose up --build
else
  echo "[INFO] 로컬 가상환경/의존성 설치 후 Streamlit 실행…"
  python -m venv .venv
  source .venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
  streamlit run app.py
fi 