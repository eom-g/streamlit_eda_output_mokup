import streamlit as st
import pandas as pd
import numpy as np
import time

# --- 1. 기본 설정 및 세션 초기화 ---
st.set_page_config(page_title="Gen-AI EDA Agent", layout="wide")

if 'step' not in st.session_state:
    st.session_state.step = 1

# --- 2. 사이드바 ---
with st.sidebar:
    st.title("🤖 Agent Status")
    st.success("Feature Store 연결됨 (1,500+)")
    if st.button("🔄 처음부터 다시 시작"):
        st.session_state.step = 1
        st.rerun()

# --- 3. 메인 화면 ---
st.title("🔍 Gen-AI EDA Agent")

# --- Step 1. 분석 모드 선택 (항상 표시) ---
st.header("Step 1. 분석 모드 선택")
mode = st.radio(
    "사용자 유형을 선택하세요.",
    ["🏢 사업팀 인사이트 모드", "🧪 분석가 데이터 진단 모드"],
    horizontal=True,
    disabled=(st.session_state.step > 1) # 시작 후에는 모드 고정 (선택사항)
)

st.divider()

# --- Step 2. 분석 목적 입력 (Step 1 완료 후 계속 유지) ---
if st.session_state.step >= 1:
    st.header("Step 2. 분석 목적 입력")
    
    if "사업팀" in mode:
        c1, c2 = st.columns(2)
        target = c1.text_input("🎯 타겟 정의", "최근 3개월 Sim Only 가입자")
        hypo = c2.text_area("💡 가설", "20대 유저의 유튜브 사용량이 높을 것이다.", height=68)
    else:
        c1, c2 = st.columns(2)
        y_label = c1.text_input("🎯 Target (Y)", "is_churn")
        analyst_goal = c2.text_area("📝 분석 목적", "해지 예측 모델용 피처 품질 진단 요청", height=68)

    # 버튼은 Step 1 상태일 때만 표시하거나, 다시 누를 수 있게 둠
    if st.session_state.step == 1:
        if st.button("🪄 AI 변수 매핑 시작", type="primary"):
            with st.spinner("메타 테이블에서 변수 추출 중..."):
                time.sleep(1)
                st.session_state.step = 2
                st.rerun()

# --- Step 3. 최종 분석 셋업 (Step 2 완료 시 아래에 추가) ---
if st.session_state.step >= 2:
    st.divider()
    st.header("Step 3. 최종 분석 셋업 및 리포트")
    
    default_vars = ["고객 연령", "고객 성별", "데이터 사용량(MB)", "넷플릭스 시청 시간"]
    st.multiselect("✅ AI 선별 지표 (수정 가능)", options=default_vars + ["평균 통화 시간", "최근 구매 금액"], default=default_vars)

    if st.session_state.step == 2:
        if st.button("🚀 분석 실행 및 리포트 생성"):
            with st.status("BigQuery 분석 엔진 가동 중...") as status:
                time.sleep(1)
                status.update(label="분석 완료!", state="complete")
            st.session_state.step = 3
            st.rerun()

# --- Output. 리포트 결과 (최하단에 추가) ---
if st.session_state.step >= 3:
    st.divider()
    st.header(f"📊 분석 결과 리포트 ({mode})")

    if "사업팀" in mode:
        t1, t2, t3 = st.tabs(["💡 가설/현상", "📈 영향도", "🎯 전략"])
        with t1:
            st.success("✅ 가설 일치: 20대 타겟의 유튜브 사용량이 비교군 대비 2.4배 높음")
            st.bar_chart(pd.DataFrame([85, 35], index=["타겟", "비교군"]))
        with t2:
            st.write("핵심 영향 인자: **'심야 시간대 데이터 사용량'**")
            st.progress(85)
        with t3:
            st.info("**Persona: 야행성 스트리머**\n\n- 제안: 넷플릭스 결합 요금제 캠페인")
    else:
        t1, t2, t3 = st.tabs(["🔍 품질진단", "⚙️ 통계분석", "📐 가이드"])
        with t1:
            st.table(pd.DataFrame({"지표": ["cust_age", "data_mb"], "결측률": ["0%", "0.2%"]}))
        with t2:
            st.area_chart(np.random.randn(10, 2))
        with t3:
            st.error("⚠️ 위치 데이터 결측치 과다로 모델링 제외 권고")
