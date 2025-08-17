from __future__ import annotations

import streamlit as st
from clients import create_room, list_rooms
from clients.rooms import delete_room
import base64
from pathlib import Path

EINSTEIN_IMG_PATH = "image/einstein.jpg"
TRUMP_IMG_PATH = "image/Trump.jpg"

def _img_src(path: str) -> str:
    try:
        file_path = Path(path)
        if not file_path.exists():
            return ""
        mime = "image/jpeg" if file_path.suffix.lower() in {".jpg", ".jpeg"} else "image/png"
        b64 = base64.b64encode(file_path.read_bytes()).decode("utf-8")
        return f"data:{mime};base64,{b64}"
    except Exception:
        return ""

def render() -> None:
    """방/캐릭터 선택 화면을 그립니다."""
    st.header("💬 대화할 역사적 인물을 선택하세요")
    if "confirm_delete_room_id" not in st.session_state:
        st.session_state.confirm_delete_room_id = None

    # 카드 공통 스타일 주입
    st.markdown(
        """
        <style>
        .char-card {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.75rem;
            padding: 1rem 1.25rem;
            border-radius: 16px;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: 0 6px 18px rgba(0,0,0,0.12);
        }
        .char-card img {
            width: 160px; height: 160px;
            border-radius: 50%;
            object-fit: cover; object-position: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        .char-card .name { font-size: 1.1rem; font-weight: 700; }
        .char-card .desc { font-size: 0.9rem; opacity: 0.8; text-align: center; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 상단 목록은 제거하고, 하단에 기본 펼침 리스트로 제공

    # 캐릭터 선택을 카드 형태로
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            f"""
            <div class=\"char-card\">
                <img src=\"{_img_src(EINSTEIN_IMG_PATH)}\" alt=\"einstein\" />
                <div class=\"name\">알버트 아인슈타인</div>
                <div class=\"desc\">상대성이론의 아버지</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("아인슈타인", use_container_width=True, type="primary"):
            # 바로 방 생성하고 채팅으로 이동
            try:
                with st.spinner("아인슈타인과의 대화방을 생성하고 있습니다..."):
                    room_id: str = create_room("아인슈타인")
                st.session_state.room_id = room_id
                st.session_state.character = "아인슈타인"
                st.session_state.messages = []
                st.success("방이 생성되었습니다! 채팅 페이지로 이동합니다...")
                st.switch_page("pages/2_채팅.py")
            except Exception as exc:
                st.error(f"방 생성 실패: {exc}")
                st.error("백엔드 서버가 실행 중인지 확인해주세요.")
        
        st.markdown("""
        **알버트 아인슈타인**
        - 상대성이론의 아버지
        - 물리학 혁명가
        - 과학과 철학에 대한 깊이 있는 대화
        """)
    
    with col2:
        st.markdown(
            f"""
            <div class=\"char-card\">
                <img src=\"{_img_src(TRUMP_IMG_PATH)}\" alt=\"trump\" />
                <div class=\"name\">도널드 트럼프</div>
                <div class=\"desc\">제45대 미국 대통령</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("트럼프", use_container_width=True, type="primary"):
            # 바로 방 생성하고 채팅으로 이동
            try:
                with st.spinner("트럼프와의 대화방을 생성하고 있습니다..."):
                    room_id: str = create_room("트럼프")
                st.session_state.room_id = room_id
                st.session_state.character = "트럼프"
                st.session_state.messages = []
                st.success("방이 생성되었습니다! 채팅 페이지로 이동합니다...")
                st.switch_page("pages/2_채팅.py")
            except Exception as exc:
                st.error(f"방 생성 실패: {exc}")
                st.error("백엔드 서버가 실행 중인지 확인해주세요.")
        
        st.markdown("""
        **도널드 트럼프**
        - 제45대 미국 대통령
        - 비즈니스 리더
        - 정치와 경영에 대한 직설적인 대화
        """)
    
    st.divider()
    st.info("💡 인물을 선택하면 바로 대화방이 생성되고 채팅 페이지로 이동합니다!")

    # 하단: 내 방 목록 (펼친 상태의 리스트)
    with st.expander("내 방 목록 보기", expanded=True):
        rooms = list_rooms()
        if not rooms:
            st.caption("현재 생성된 방이 없습니다.")
        else:
            for r in rooms:
                raw_id = r.get("roomId") or r.get("id") or r.get("_id")
                room_id = str(raw_id)
                character = r.get("character", "?")
                img_path = EINSTEIN_IMG_PATH if character == "아인슈타인" else TRUMP_IMG_PATH

                left, mid, right = st.columns([7, 1, 1])
                with left:
                    st.markdown(
                        f"""
                        <div style="display:flex;align-items:center;gap:12px;padding:12px 14px;margin-bottom:10px;border:1px solid #e9ecef;border-radius:10px;background:#ffffff;box-shadow:0 2px 6px rgba(0,0,0,0.04);">
                            <img src="{_img_src(img_path)}" alt="{character}" style="width:36px;height:36px;border-radius:50%;object-fit:cover;object-position:center;" />
                            <div>
                                <div style="font-weight:700;color:#212529;">{character}</div>
                                <div style="color:#6c757d;font-size:0.85rem;">ID: {room_id}</div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with mid:
                    if st.button("삭제", key=f"delete-room-{room_id}", type="secondary"):
                        st.session_state.confirm_delete_room_id = room_id
                with right:
                    if st.button("입장", key=f"enter-bottom-{room_id}"):
                        st.session_state.room_id = room_id
                        st.session_state.character = character
                        st.session_state.messages = []
                        st.switch_page("pages/2_채팅.py")

                if st.session_state.confirm_delete_room_id == room_id:
                    st.warning("정말 이 방을 삭제하시겠습니까? 되돌릴 수 없습니다.")
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("삭제 확정", key=f"confirm-delete-{room_id}"):
                            try:
                                delete_room(room_id)
                                st.session_state.confirm_delete_room_id = None
                                st.success("삭제되었습니다")
                                st.rerun()
                            except Exception as exc:
                                st.error(f"삭제 실패: {exc}")
                    with c2:
                        if st.button("취소", key=f"cancel-delete-{room_id}"):
                            st.session_state.confirm_delete_room_id = None