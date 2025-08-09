from __future__ import annotations

import streamlit as st
from clients import create_room

def render() -> None:
    """방/캐릭터 선택 화면을 그립니다."""
    st.header("💬 대화할 역사적 인물을 선택하세요")

    # 캐릭터 선택을 카드 형태로
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🧑‍🔬 아인슈타인", use_container_width=True, type="primary"):
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
        if st.button("🇺🇸 트럼프", use_container_width=True, type="primary"):
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