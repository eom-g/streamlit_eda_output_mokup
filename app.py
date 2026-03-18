import streamlit as st
import pandas as pd
import numpy as np
import time

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="EDA Agent Output Report", layout="wide")

# 시연을 위해 세션 상태에 모드 설정 (나중에 통합 시 자동 연동됨)
if 'mode' not in st.session_state:
    st.session_state.mode = "🏢 사업팀 인사이트 모드"

# --- 2. 사이드바 (시연용 모드 스위처) ---
with st.sidebar:
    st.title("🎨 시연 설정")
    st.session_state.mode = st.radio(
        "보고 대상 선택",
        ["🏢 사업팀 인사이트 모드", "🧪 분석가 데이터 진단 모드"]
    )
    st.divider()
    st.info("실제 구동 시에는 앞 단계의 선택값이 자동으로 반영됩니다.")

# --- 3. 리포트 헤더 ---
st.title("📊 최종 분석 리포트")
st.caption(f"분석 대상: 최근 3개월 Sim Only 가입자 | 모드: {st.session_state.mode}")
st.divider()

# --- 4. 모드별 맞춤 리포트 출력 ---

if "사업팀" in st.session_state.mode:
    # ---------------------------------------------------------
    # [사업팀용] 1~4번 항목 중심: 비즈니스 인사이트 및 전략
    # ---------------------------------------------------------
    col1, col2, col3 = st.columns(3)
    col1.metric("타겟 모수", "1,245 명", "신규 유입")
    col2.metric("매출 기여도(Lift)", "2.4배", "전체 대비")
    col3.metric("AI 예측 전환율", "15.8%", "High Index")

    t1, t2, t3 = st.tabs(["💡 1-2. 가설 검증 및 현상", "📈 3. 핵심 영향 인자", "🎯 4. 고객 페르소나/전략"])
    
    with t1:
        st.subheader("가설: '20대 타겟은 심야 시간대 유튜브 사용이 높을 것이다'")
        st.success("✅ **검증 결과: 가설 채택**")
        st.write("실제 데이터 확인 결과, 20대 타겟군의 유튜브 사용량은 일반 고객 대비 **142% 높게** 나타났습니다.")
        
        # 시각화 (사업팀용 직관적 차트)
        chart_data = pd.DataFrame({
            "집단": ["타겟군(20대)", "일반군"],
            "유튜브 사용 지수": [85, 35]
        }).set_index("집단")
        st.bar_chart(chart_data)

    with t2:
        st.subheader("타겟 전환에 영향을 미치는 주요 피처")
        st.write("AI 모델이 분석한 결과, 아래 3가지 요소가 가장 결정적인 차이를 만듭니다.")
        st.progress(0.85, text="심야 시간대 데이터 소비량 (85%)")
        st.progress(0.62, text="OTT(넷플릭스 등) 시청 시간 (62%)")
        st.progress(0.31, text="주 활동 지역(대학가/오피스) (31%)")

    with t3:
        st.subheader("추천 페르소나 & 액션 아이템")
        c1, c2 = st.columns(2)
        with c1:
            st.info("### 👥 Persona: 야행성 스트리머\n- **특징**: 22시~02시 활동량 집중\n- **Action**: 해당 시간대 전용 데이터 팩 푸시 발송")
        with c2:
            st.warning("### 👥 Persona: 자급제 알뜰족\n- **특징**: 쇼핑 앱 및 멤버십 활용도 높음\n- **Action**: 제휴 포인트 적립 요금제 노출")

else:
    # ---------------------------------------------------------
    # [분석가용] 5~13번 항목 중심: 데이터 품질 및 기술 검증
    # ---------------------------------------------------------
    st.warning("🧪 본 리포트는 데이터 모델링 적합성 및 통계 검증 수치를 포함합니다.")
    
    t1, t2, t3 = st.tabs(["🔍 5-8. 품질 및 통계 분석", "⚙️ 9-11. 유의성/중요도", "📐 12-13. 한계점/가이드"])

    with t1:
        st.subheader("데이터 품질 및 다중공선성 진단")
        q_col, v_col = st.columns([0.6, 0.4])
        with q_col:
            st.dataframe(pd.DataFrame({
                "Feature": ["cust_age", "data_mb", "app_freq", "call_cnt"],
                "Missing": ["0%", "0.2%", "12.4%", "0%"],
                "Outlier": ["None", "24건", "150건", "None"],
                "Skewness": [0.12, 2.45, 1.88, 0.45]
            }))
        with v_col:
            st.write("**VIF (다중공선성)**")
            st.code("data_mb: 8.4 (High)\napp_freq: 2.1 (Low)\ncall_cnt: 1.5 (Low)")
            st.caption("※ data_mb 피처는 변수 처리가 필요함")

    with t2:
        st.subheader("Feature 유의성 및 중요도 (SHAP Value)")
        st.write("P-Value 검정 결과 모든 주요 피처가 **0.05 미만**으로 유의함이 확인되었습니다.")
        # 분석가용 기술적 차트
        st.area_chart(np.random.randn(20, 3))
        st.caption("각 피처별 타겟 기여도 추이 분석")

    with t3:
        st.subheader("분석 한계점 및 모델링 권고")
        st.error("⚠️ **데이터 한계**: 위치(GPS) 데이터의 결측치가 40% 이상으로 신뢰도가 낮음")
        st.markdown("""
        - **추천 모델**: 비선형 관계 대응에 유리한 **LightGBM** 또는 **XGBoost**
        - **전처리 가이드**: `app_freq` 결측치는 중앙값(Median) 대치 권장
        - **Next Step**: 위치 데이터를 제외한 행동 패턴 위주의 피처 엔지니어링 수행
        """)

# --- 5. 공통 하단 버튼 ---
st.divider()
if st.button("📄 리포트 PDF로 내보내기"):
    st.write("PDF 리포트를 생성하고 있습니다...")
