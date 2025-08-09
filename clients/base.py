"""공통 백엔드 HTTP 클라이언트 모듈.

requests.Session 을 활용해 커넥션 풀을 유지하고, 기본 URL·타임아웃을 중앙집중화합니다.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import requests

_DEFAULT_TIMEOUT = 10  # seconds


def _env_backend_url() -> str:
    return os.getenv("BACKEND_URL", "http://localhost:8080")


@dataclass(slots=True)
class BackendClient:
    base_url: str = _env_backend_url()
    session: requests.Session = requests.Session()

    def _url(self, path: str) -> str:  # noqa: D401 - simple URL join
        if not path.startswith("/"):
            path = f"/{path}"
        return f"{self.base_url}{path}"

    def get(self, path: str, **kwargs: Any) -> dict[str, Any]:
        res = self.session.get(self._url(path), timeout=_DEFAULT_TIMEOUT, **kwargs)
        res.raise_for_status()
        return res.json()

    def post(self, path: str, **kwargs: Any) -> dict[str, Any]:
        res = self.session.post(self._url(path), timeout=_DEFAULT_TIMEOUT, **kwargs)
        res.raise_for_status()
        return res.json()


# 싱글톤 클라이언트 인스턴스 (전역 재사용)
client = BackendClient() 