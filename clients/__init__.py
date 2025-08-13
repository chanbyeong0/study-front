"""백엔드 API 최상위 인터페이스

외부에서는 이 모듈만 import 해 사용하도록 권장합니다.

예)
    from clients import create_room, send_message
"""
from __future__ import annotations

from .rooms import create_room, reset_room, get_room, delete_room, list_rooms  # noqa: F401
from .messages import get_history, send_message, health  # noqa: F401

__all__: list[str] = [
    "create_room",
    "reset_room",
    "get_room",
    "delete_room",
    "send_message",
    "get_history",
    "health",
    "list_rooms",
] 