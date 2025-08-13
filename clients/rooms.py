"""Rooms 관련 API 함수 모듈"""
from __future__ import annotations

from typing import Any

from .base import client


def list_rooms() -> list[dict[str, Any]]:
    """모든 방 목록 조회"""
    try:
        res = client.get("/api/rooms")
        # 백엔드가 배열을 반환하는 경우만 정상 처리
        return res if isinstance(res, list) else []
    except Exception:
        return []

def create_room(character: str) -> str:
    """캐릭터로 방을 생성하고 room_id 반환"""
    payload: dict[str, Any] = {"character": character}
    res = client.post("/api/rooms", json=payload)
    # 백엔드가 ObjectId 문자열을 직접 반환하거나 {"roomId": "..."}로 반환하는 두 경우 모두 대응
    if isinstance(res, dict):
        room_id = res.get("roomId") or res.get("id") or res.get("_id")
        if room_id:
            return str(room_id)
    # dict가 아니거나 키가 없으면 전체를 문자열로 취급
    return str(res)


def reset_room(room_id: str) -> dict[str, Any]:
    """기존 방의 대화 맥락(히스토리)을 초기화합니다."""
    return client.post(f"/api/rooms/{room_id}/reset")


def get_room(room_id: str) -> dict[str, Any]:
    """방 정보를 조회합니다."""
    return client.get(f"/api/rooms/{room_id}")


def delete_room(room_id: str) -> dict[str, Any]:
    """방을 삭제합니다."""
    return client.delete(f"/api/rooms/{room_id}")