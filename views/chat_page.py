from __future__ import annotations

import streamlit as st
from clients import send_message, reset_room, get_history



def _render_messages() -> None:
    """세션에 저장된 메시지를 채팅창처럼 렌더링"""
    if not st.session_state.messages:
        st.info("💬 메시지를 입력해서 대화를 시작해보세요!")
        return
    
    # 메시지 컨테이너 (스크롤 가능한 영역)
    with st.container():
        for i, msg in enumerate(st.session_state.messages):
            role = msg["role"]
            content = msg["content"]
            
            # 메시지 타입에 따른 정보
            if role == "user":
                avatar = "👤"
                name = "나"
            else:
                if st.session_state.character == "아인슈타인":
                    avatar = "🧠"
                    name = "아인슈타인"
                else:
                    avatar = "🇺🇸"
                    name = "트럼프"
            
            # 채팅 버블 스타일링
            if role == "user":
                # 사용자 메시지 (오른쪽 정렬)
                st.markdown(
                    f"""<div style="display: flex; justify-content: flex-end; margin-bottom: 1rem;">
                        <div style="
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            color: white;
                            padding: 12px 16px;
                            border-radius: 18px 18px 4px 18px;
                            max-width: 70%;
                            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
                        ">
                            <div style="font-size: 14px; margin-bottom: 4px; opacity: 0.8;">나</div>
                            <div>{content}</div>
                        </div>
                    </div>""", 
                    unsafe_allow_html=True
                )
            else:
                # AI 메시지 (왼쪽 정렬)
                bg_color = "#e8f5e8" if st.session_state.character == "아인슈타인" else "#fff3cd"
                border_color = "#d4edda" if st.session_state.character == "아인슈타인" else "#ffeaa7"
                
                st.markdown(
                    f"""<div style="display: flex; justify-content: flex-start; margin-bottom: 1rem;">
                        <div style="
                            background: {bg_color};
                            color: #333;
                            border: 1px solid {border_color};
                            padding: 12px 16px;
                            border-radius: 18px 18px 18px 4px;
                            max-width: 70%;
                            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                        ">
                            <div style="font-size: 14px; margin-bottom: 4px; font-weight: 600;">{avatar} {name}</div>
                            <div>{content}</div>
                        </div>
                    </div>""", 
                    unsafe_allow_html=True
                )

def render() -> None:
    """채팅 메인 화면"""
    if not st.session_state.get("room_id"):
        st.warning("먼저 '방 선택' 페이지에서 캐릭터와 방을 생성하세요.")
        st.stop()

    # 첫 로드 시 서버 히스토리를 불러와 세션에 반영 (세션이 비어 있을 때만)
    if not st.session_state.messages:
        try:
            history = get_history(st.session_state.room_id)
            # history가 리스트 또는 {messages: [...]} 형태 모두 허용
            messages = history.get("messages") if isinstance(history, dict) else history
            if isinstance(messages, list):
                normalized: list[dict[str, str]] = []
                for m in messages:
                    role = m.get("role") or ("assistant" if m.get("speaker") == "assistant" else "user")
                    content = m.get("content", "")
                    if role in ("user", "assistant") and content:
                        normalized.append({"role": role, "content": content})
                if normalized:
                    st.session_state.messages = normalized
        except Exception:
            # 히스토리 API는 선택사항이므로 실패하더라도 무시
            pass

    # 캐릭터별 컨셉 설정
    if st.session_state.character == "아인슈타인":
        theme_color = "#4CAF50"
        header_emoji = "🧠"
        description = "상대성이론의 아버지와의 과학적 대화"
    else:  # 트럼프
        theme_color = "#FF9800"
        header_emoji = "🇺🇸"
        description = "제45대 미국 대통령과의 정치・경영 토론"

    # 헤더 (컨셉에 맞는 디자인)
    st.markdown(
        f"""<div style="
            background: linear-gradient(90deg, {theme_color} 0%, {theme_color}AA 100%);
            padding: 1.5rem 2rem;
            border-radius: 10px;
            margin-bottom: 1rem;
            color: white;
        ">
            <h1 style="margin: 0; color: white;">{header_emoji} {st.session_state.character}</h1>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">{description}</p>
        </div>""", 
        unsafe_allow_html=True
    )

    # 채팅방 상태 바
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💬 메시지", len(st.session_state.messages))
    with col2:
        st.metric("🔗 연결", "온라인")
    with col3:
        st.metric("⏱️ 대화시간", f"{len(st.session_state.messages)}분")
    with col4:
        if st.button("🔄 새 대화", type="secondary", use_container_width=True):
            # 서버 컨텍스트(히스토리)도 초기화 시도
            try:
                with st.spinner("대화 기록을 초기화하는 중..."):
                    reset_room(st.session_state.room_id)
            except Exception:
                # 백엔드 미구현이어도 로컬 세션만 초기화하여 진행
                pass
            st.session_state.messages = []
            st.rerun()

    st.divider()

    # 채팅 메시지 영역
    chat_container = st.container()
    with chat_container:
        _render_messages()

    # 하단 고정 입력 영역
    st.markdown("---")
    
    # 메시지 입력 (메인)
    user_input = st.chat_input(f"{st.session_state.character}에게 메시지를 보내세요...")

    if user_input:
        # 사용자 메시지 상태 저장
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # 실제 API 연동 코드
        with st.spinner(f"{st.session_state.character}이(가) 답변을 생성하고 있습니다..."):
            try:
                assistant_reply: str = send_message(st.session_state.room_id, user_input)
            except Exception as exc:
                assistant_reply = f"🚫 연결 오류가 발생했습니다: {exc}\n\n💡 백엔드 서버가 실행 중인지 확인해주세요."

        # 답변 상태 저장
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
        st.rerun()  # 새로운 메시지로 화면 업데이트

    # 사이드바에 캐릭터 정보 및 추천 질문
    with st.sidebar:
        st.markdown(f"### {header_emoji} {st.session_state.character}")
        
        if st.session_state.character == "아인슈타인":
            st.markdown("""
            **추천 대화 주제:**
            - 상대성이론에 대해 설명해주세요
            - E=mc²의 의미는 무엇인가요?
            - 시간과 공간에 대한 견해는?
            - 과학자의 사회적 책임은?
            - 양자역학에 대한 생각은?
            """)
        else:  # 트럼프
            st.markdown("""
            **추천 대화 주제:**
            - 리더십의 핵심은 무엇인가요?
            - 성공적인 비즈니스 전략은?
            - 미국 경제 정책에 대한 견해는?
            - 협상의 기술에 대해 알려주세요
            - 미디어와의 관계는 어떻게 관리하나요?
            """)
        
        st.divider()
        
        if st.button("🏠 인물 변경", use_container_width=True):
            st.switch_page("pages/1_방_선택.py") 