import streamlit as st
import pandas as pd
import numpy as np
import time

# --- 1. 기본 설정 및 세션 초기화 ---
st.set_page_config(page_title="Gen-AI EDA Agent", layout="wide")

if 'step' not in st.session_state:
    st.session_state.step = 1
if 'mode' not in st.session_state:
    st.session_state.mode = "🏢 사업팀 인사이트 모드"

# --- 2. 사이드바 (상태 표시) ---
with st.sidebar:
    st.title("🤖 Agent Status")
    st.success("Feature Store 연결됨 (1,500+)")
    if st.button("🔄 전체 초기화"):
        st.session_state.step = 1
        st.rerun()

# --- 3. 메인 화면 ---
st.title("🔍 Gen-AI EDA Agent")
st.caption("BigQuery 기반 데이터 탐색 및 한글 물리명 매핑 프로토타입")

# Step 1: 모드 선택
st.header("Step 1. 분석 모드 선택")
selected_mode = st.radio(
    "사용자 유형을 선택하세요.",
    ["🏢 사업팀 인사이트 모드", "🧪 분석가 데이터 진단 모드"],
    horizontal=True
)
st.session_state.mode = selected_mode

st.divider()

# Step 2: 입력부 (모드별 동적 구성)
if st.session_state.step == 1:
    st.header("Step 2. 분석 목적 입력")
    
    if "사업팀" in st.session_state.mode:
        c1, c2 = st.columns(2)
        target = c1.text_input("🎯 타겟 정의", "최근 3개월 Sim Only 가입자")
        hypo = c2.text_area("💡 가설", "20대 유저의 유튜브 사용량이 높을 것이다.", height=68)
    else:
        c1, c2 = st.columns(2)
        y_label = c1.text_input("🎯 Target (Y)", "is_churn")
        analyst_goal = c2.text_area("📝 분석 목적", "해지 예측 모델용 피처 품질 진단 요청", height=68)

    if st.button("🪄 AI 변수 매핑 시작", type="primary"):
        with st.spinner("메타 테이블(1,500개)에서 연관 변수 추출 중..."):
            time.sleep(1.5)
            st.session_state.step = 2
            st.rerun()

# Step 3 & Output: 결과 출력부
if st.session_state.step >= 2:
    st.header("Step 3. 최종 분석 셋업 및 리포트")
    
    # 변수 선택 (멀티셀렉트)
    default_vars = ["고객 연령", "고객 성별", "데이터 사용량(MB)", "넷플릭스 시청 시간"]
    st.multiselect("✅ AI 선별 지표 (수정 가능)", options=default_vars + ["평균 통화 시간", "최근 구매 금액"], default=default_vars)

    if st.button("🚀 분석 실행 및 리포트 생성"):
        with st.status("BigQuery 분석 엔진 가동 중...", expanded=True) as status:
            st.write("SQL 쿼리 생성 및 실행...")
            time.sleep(1)
            st.write("통계적 유의성 검정 중...")
            time.sleep(1)
            status.update(label="분석 완료!", state="complete", expanded=False)
        st.session_state.step = 3

if st.session_state.step == 3:
    st.divider()
    st.header(f"📊 분석 결과 리포트 ({st.session_state.mode})")

    if "사업팀" in st.session_state.mode:
        # [사업팀용] 1~4번 항목
        t1, t2, t3 = st.tabs(["💡 가설/현상(1-2)", "📈 영향도(3)", "🎯 전략(4)"])
        with t1:
            st.subheader("1-2. 가설 검증 결과")
            st.success("✅ 가설 일치: 20대 타겟의 유튜브 사용량이 비교군 대비 2.4배 높음")
            # 내장 차트 사용 (Plotly 미사용)
            chart_data = pd.DataFrame([85, 35], index=["타겟", "비교군"], columns=["유튜브 지수"])
            st.bar_chart(chart_data)
        with t2:
            st.subheader("3. 핵심 영향 인자 (Top Drivers)")
            st.write("분석 결과, **'심야 시간대(22-02시) 데이터 사용량'**이 타겟군을 결정짓는 가장 큰 요인입니다.")
            st.progress(85, text="영향도: 85%")
        with t3:
            st.subheader("4. 추천 페르소나 및 액션")
            col_p1, col_p2 = st.columns(2)
            col_p1.info("**Persona: 야행성 스트리머**\n\n- 제안: 넷플릭스 결합 요금제 캠페인 실행")
            col_p2.warning("**Persona: 알뜰 폰족**\n\n- 제안: 데이터 소량/저가형 요금제 유지 관리")

    else:
        # [분석가용] 5~13번 항목
        t1, t2, t3 = st.tabs(["🔍 품질진단(5-6)", "⚙️ 통계분석(7-11)", "📐 가이드(12-13)"])
        with t1:
            st.subheader("5-6. 데이터 품질 현황")
            st.table(pd.DataFrame({
                "지표": ["cust_age", "data_mb", "app_freq"],
                "결측률": ["0%", "0.2%", "12.4%"],
                "이상치": ["0건", "24건", "150건"],
                "조치": ["Keep", "Keep", "Impute"]
            }))
        with t2:
            st.subheader("7-11. 변수 유의성 및 관계")
            st.write("상관관계 및 피처 중요도 분석 결과")
            st.area_chart(np.random.randn(10, 2)) # 시뮬레이션 차트
        with t3:
            st.subheader("12-13. 한계점 및 가이드")
            st.error("⚠️ 위치 데이터 결측치(40%) 과다로 모델링 시 제외 권고")
            st.markdown("- **추천 모델**: XGBoost 또는 LightGBM\n- **Next Step**: 결측치 보정 후 재학습 예정")
