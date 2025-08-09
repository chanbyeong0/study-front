"""View-layer 패키지

이곳에서 하위 모듈의 대표 render 함수를 재노출하여 짧은 import 경로를 제공합니다.

예)
    from views import room_select, chat_page

    room_select()  # 1_방_선택.py
    chat_page()    # 2_채팅.py
"""
from __future__ import annotations

from .room_select import render as room_select  # noqa: F401
from .chat_page import render as chat_page      # noqa: F401

__all__: list[str] = [
    "room_select",
    "chat_page",
] 