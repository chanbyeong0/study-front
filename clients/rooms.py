"""Rooms 관련 API 함수 모듈"""
from __future__ import annotations

from typing import Any

from .base import client


def create_room(character: str) -> str:
    """캐릭터로 방을 생성하고 room_id 반환"""
    payload: dict[str, Any] = {"character": character}
    res = client.post("/api/rooms", json=payload)
    return str(res.get("roomId")) 


def reset_room(room_id: str) -> dict[str, Any]:
    """기존 방의 대화 맥락(히스토리)을 초기화합니다."""
    return client.post(f"/api/rooms/{room_id}/reset")


def get_room(room_id: str) -> dict[str, Any]:
    """방 정보를 조회합니다."""
    return client.get(f"/api/rooms/{room_id}")


def delete_room(room_id: str) -> dict[str, Any]:
    """방을 삭제합니다."""
    return client.post(f"/api/rooms/{room_id}/delete")