import streamlit as st
from clients import create_room
import base64
from pathlib import Path

st.set_page_config(
    page_title="AI 역사 인물 채팅",
    page_icon="💬",
    layout="wide",
)

# 세션 상태 초기화 함수

def _init_state():
    if "room_id" not in st.session_state:
        st.session_state.room_id = None
        st.session_state.character = None
        st.session_state.messages = []


_init_state()

# CSS 로드 함수

def load_css(path: str):
    """외부 CSS 파일을 읽어 주입합니다."""
    with open(path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 외부 스타일 파일 적용
load_css("styles/chat.css")

def _img_src(path: str) -> str:
    try:
        p = Path(path)
        if not p.exists():
            return ""
        mime = "image/jpeg" if p.suffix.lower() in {".jpg", ".jpeg"} else "image/png"
        b64 = base64.b64encode(p.read_bytes()).decode("utf-8")
        return f"data:{mime};base64,{b64}"
    except Exception:
        return ""

# 카드 클릭(쿼리 파라미터) 처리: ?character=einstein|trump → 방 생성 후 채팅 페이지로 이동
_slug_to_character = {
    "einstein": "아인슈타인",
    "trump": "트럼프",
}

query_params = st.query_params
raw_param = query_params.get("character")
if raw_param:
    # st.query_params는 단일값(str) 또는 시퀀스일 수 있음 → 모두 처리
    selected_slug = raw_param if isinstance(raw_param, str) else raw_param[0]
    selected_character = _slug_to_character.get(selected_slug)

    if selected_character:
        try:
            with st.spinner(f"{selected_character}과(와)의 대화방을 생성하고 있습니다…"):
                room_id = create_room(selected_character)
            st.session_state.room_id = room_id
            st.session_state.character = selected_character
            st.session_state.messages = []
            # 쿼리 파라미터 초기화 후 채팅 페이지로 이동
            st.query_params.clear()
            st.switch_page("pages/2_채팅.py")
        except Exception as exc:
            st.error(f"방 생성 실패: {exc}")
            st.stop()

# 홈 화면은 언제든 접근 가능하도록 자동 리다이렉트 제거

# 메인 홈 화면 - 모던한 랜딩 페이지 컨셉
st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 3rem 2rem;
    border-radius: 15px;
    text-align: center;
    color: white;
    margin-bottom: 2rem;
">
    <div style="display:flex;align-items:center;justify-content:center;gap:12px;">
        <img src="{_img_src('image/einstein.jpg')}" alt="einstein" style="width:40px;height:40px;border-radius:50%;object-fit:cover;border:2px solid rgba(255,255,255,0.7);" />
        <img src="{_img_src('image/Trump.jpg')}" alt="trump" style="width:40px;height:40px;border-radius:50%;object-fit:cover;border:2px solid rgba(255,255,255,0.7);" />
        <h1 style="font-size: 3rem; margin: 0; color: white;">AI 역사 인물 채팅</h1>
    </div>
    <p style="font-size: 1.3rem; margin: 1rem 0 0 0; opacity: 0.9;">역사 속 거장들과 실시간으로 대화해보세요</p>
</div>
""", unsafe_allow_html=True)

# 인물 소개 카드 (카드 자체가 링크로 동작)
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        <a class="hero-card" href="?character=einstein" style="
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        ">
            <div style="display:flex;align-items:center;gap:10px;">
                <img src="{_img_src('image/einstein.jpg')}" alt="einstein" style="width:40px;height:40px;border-radius:50%;object-fit:cover;" />
                <h2>알버트 아인슈타인</h2>
            </div>
            <p>상대성이론의 아버지</p>
            <ul>
                <li>물리학과 우주에 대한 깊이 있는 토론</li>
                <li>과학적 사고와 철학적 통찰</li>
                <li>E=mc²와 시공간의 비밀</li>
            </ul>
            <div class="card-cta">👆 클릭해서 대화 시작하기</div>
        </a>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <a class="hero-card" href="?character=trump" style="
            background: linear-gradient(135deg, #FF9800 0%, #f57c00 100%);
        ">
            <div style="display:flex;align-items:center;gap:10px;">
                <img src="{_img_src('image/Trump.jpg')}" alt="trump" style="width:40px;height:40px;border-radius:50%;object-fit:cover;" />
                <h2>도널드 트럼프</h2>
            </div>
            <p>제45대 미국 대통령</p>
            <ul>
                <li>리더십과 비즈니스 전략</li>
                <li>정치와 협상의 기술</li>
                <li>미국 경제와 정책 논의</li>
            </ul>
            <div class="card-cta">👆 클릭해서 대화 시작하기</div>
        </a>
        """,
        unsafe_allow_html=True,
    )

# 특징 소개
st.markdown("### ✨ 특별한 경험")
feature_col1, feature_col2, feature_col3 = st.columns(3)

with feature_col1:
    st.markdown("""
    **🎯 맞춤형 대화**
    
    각 인물의 실제 사고방식과 성격을 반영한 개성 있는 대화를 경험하세요.
    """)

with feature_col2:
    st.markdown("""
    **🚀 실시간 AI**
    
    최신 AI 기술로 자연스럽고 지능적인 대화가 실시간으로 이루어집니다.
    """)

with feature_col3:
    st.markdown("""
    **📚 교육적 가치**
    
    역사적 인물들의 지식과 경험을 통해 새로운 통찰을 얻어보세요.
    """)

st.divider()

# 시작하기 안내
st.markdown("### 🚀 사용법")
st.markdown("""
1. **위의 인물 카드**를 클릭하면 바로 **대화방이 생성**됩니다
2. 자동으로 **채팅 페이지**로 이동합니다
3. 자유롭게 **질문하고 대화**를 즐겨보세요! 🎉

💡 **팁**: 각 인물마다 추천 대화 주제가 사이드바에 제공됩니다.
""")

# 사이드바 안내
st.sidebar.success("좌측 페이지 메뉴에서 기능을 선택하세요.")

# 최근 활동 표시 (있다면)
if st.session_state.get("room_id"):
    st.info(f"🎯 현재 {st.session_state.character}과(와) 대화 중입니다!")
    if st.button("채팅으로 돌아가기"):
        st.switch_page("pages/2_채팅.py") 