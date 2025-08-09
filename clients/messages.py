"""Messages 관련 API 함수 모듈"""
from __future__ import annotations

from typing import Any

from .base import client


def send_message(room_id: str, content: str) -> str:
    """메시지를 전송하고 캐릭터 답변을 반환"""
    payload: dict[str, Any] = {"content": content}
    res = client.post(f"/api/rooms/{room_id}/messages", json=payload)
    return str(res.get("content"))


def get_history(room_id: str):
    """대화 히스토리 반환 (옵션)"""
    try:
        return client.get(f"/api/rooms/{room_id}/messages")
    except Exception:
        return [] 


def health() -> dict[str, Any]:
    """백엔드 헬스 체크"""
    return client.get("/api/health")