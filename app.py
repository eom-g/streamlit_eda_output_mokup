import streamlit as st
import pandas as pd
import numpy as np
import time

# --- 1. 페이지 설정 및 세션 초기화 ---
st.set_page_config(page_title="Gen-AI EDA Agent Premium", layout="wide")

if 'step' not in st.session_state:
    st.session_state.step = 1

# --- 2. 사이드바 ---
with st.sidebar:
    st.title("🤖 Agent Control")
    st.info("💡 모드를 변경하면 해당 직군에 최적화된 리포트가 생성됩니다.")
    if st.button("🔄 전체 초기화 및 다시 시작"):
        st.session_state.step = 1
        st.rerun()

# --- 3. 메인 화면 ---
st.title("🔍 Gen-AI EDA Agent")

# Step 1. 분석 모드 선택
st.header("Step 1. 분석 모드 선택")
mode = st.radio(
    "사용자 유형을 선택하세요.",
    ["🏢 사업팀 인사이트 모드", "🧪 분석가 데이터 진단 모드"],
    horizontal=True,
    disabled=(st.session_state.step > 1)
)

st.divider()

# Step 2. 분석 목적 입력
if st.session_state.step >= 1:
    st.header("Step 2. 분석 목적 입력")
    c1, c2 = st.columns(2)
    
    if "사업팀" in mode:
        target_input = c1.text_input("🎯 타겟 정의", "최근 3개월 Sim Only 가입자")
        hypo_input = c2.text_area("💡 가설", "20대 유저의 유튜브 사용량이 높을 것이다.", height=68)
    else:
        target_input = c1.text_input("🎯 Target (Y)", "is_churn_3m")
        goal_input = c2.text_area("📝 진단 목적", "해지 예측 모델링 전 피처 품질 및 통계적 유의성 검증", height=68)

    if st.session_state.step == 1:
        if st.button("🪄 AI 변수 매핑 및 분석 시작", type="primary"):
            with st.status("BigQuery 엔진 연동 및 통계 계산 중...") as status:
                time.sleep(1.5)
                status.update(label="분석 완료!", state="complete")
            st.session_state.step = 3
            st.rerun()

# --- Step 3. 리포트 출력 영역 ---
if st.session_state.step >= 3:
    st.divider()
    st.header(f"📊 최종 분석 리포트 ({mode})")

    # -------------------------------------------------------------------------
    # CASE A: 사업팀 인사이트 모드 (1~3번 항목)
    # -------------------------------------------------------------------------
    if "사업팀" in mode:
        t1, t2, t3 = st.tabs(["📊 1. 집단간 비교", "👤 2. 프로파일링", "📱 3. 채널 선호도"])
        
        with t1:
            st.subheader("📍 지표별 특징 Index (전체 대비)")
            idx_df = pd.DataFrame({
                "지표명": ["유튜브 시청시간", "야간 데이터사용", "주말 통화량", "멤버십 활용"],
                "Index": [242, 185, 110, 95]
            }).sort_values("Index", ascending=False)
            
            for _, row in idx_df.iterrows():
                col_left, col_right = st.columns([0.2, 0.8])
                col_left.write(f"**{row['지표명']}**")
                color = "blue" if row['Index'] > 100 else "grey"
                col_right.progress(min(row['Index']/300, 1.0), text=f"Index: {row['Index']}")
            
            st.subheader("🔍 변수별 예측력 (IV Rank)")
            iv_data = pd.DataFrame({"IV": [0.45, 0.32, 0.15, 0.08]}, index=["데이터사용량", "앱접속빈도", "연령", "가입기간"])
            st.bar_chart(iv_data)

        with t2:
            st.subheader("👥 고객 기본 프로파일링")
            c1, c2 = st.columns(2)
            c1.write("**성별 비중**")
            c1.table(pd.DataFrame({"비중(%)": [62, 38]}, index=["남성", "여성"]))
            c2.write("**연령대 분포**")
            c2.bar_chart(np.random.normal(28, 5, 15))

        with t3:
            st.subheader("📣 채널 선호도 반응 분석")
            channel_data = pd.DataFrame({
                "반응": [45, 12, 28],
                "미반응": [55, 88, 72]
            }, index=["App Push", "MMS", "알림톡"])
            st.bar_chart(channel_data)

    # -------------------------------------------------------------------------
    # CASE B: 분석가 데이터 진단 모드 (1~7번 항목)
    # -------------------------------------------------------------------------
    else:
        t1, t2, t3, t4 = st.tabs(["🧹 1-2. 클렌징/카디널리티", "📉 3. 이상치 영향도", "🔗 4-6. 상관관계/VIF", "📐 7. Binning 제안"])
        
        with t1:
            st.subheader("1️⃣ Zero-Variance 변수 식별")
            st.write("값이 하나뿐이라 모델 학습에 의미가 없는 변수 리스트입니다.")
            st.table(pd.DataFrame({"변수명": ["is_active_user", "country_code"], "값": ["Y", "82"], "조치": ["제거 권고", "제거 권고"]}))
            
            st.subheader("2️⃣ Cardinality 체크 (범주형)")
            card_df = pd.DataFrame({
                "변수명": ["main_activity_area", "device_model", "cust_grade"],
                "Unique 값 개수": [1450, 420, 5],
                "상태": ["⚠️ 과다 (High)", "⚠️ 과다 (High)", "✅ 정상"]
            })
            st.dataframe(card_df.style.highlight_max(axis=0, subset=["Unique 값 개수"], color='pink'))

        with t2:
            st.subheader("3️⃣ Outlier 영향도 분석")
            st.write("이상치 제거 전/후의 주요 통계량 변화입니다.")
            col_box1, col_box2 = st.columns(2)
            col_box1.caption("[전] 데이터 사용량 분포")
            col_box1.bar_chart(np.random.exponential(50, 20))
            col_box2.caption("[후] 이상치 제거 후 분포")
            col_box2.bar_chart(np.random.normal(30, 5, 20))
            
            st.write("**평균 변화율 요약**")
            st.table(pd.DataFrame({"피처": ["data_usage_mb", "call_dur"], "기존 평균": [45.2, 120.5], "정제후 평균": [32.1, 118.2], "변화율": ["-29.0%", "-1.9%"]}))

        with t3:
            st.subheader("4-5️⃣ Multicollinearity (VIF) & Heatmap")
            st.write("**다중공선성 위험 변수 그룹**")
            st.error("그룹 A: [total_data_mb, night_data_mb, day_data_mb] -> 하나만 선택 권장")
            
            st.write("**Interactive Heatmap (상관관계)**")
            corr_data = pd.DataFrame(np.random.rand(5, 5), columns=['Age', 'Data', 'App', 'Call', 'Svc'], index=['Age', 'Data', 'App', 'Call', 'Svc'])
            st.dataframe(corr_data.style.background_gradient(cmap='coolwarm'))
            
            st.subheader("6️⃣ Feature-Target Correlation")
            st.write("타겟(is_churn)과 상관관계가 가장 높은 변수 순위입니다.")
            target_corr = pd.DataFrame({"Correlation": [0.65, 0.42, -0.35, 0.12]}, index=["data_usage", "complain_cnt", "svc_period", "age"])
            st.bar_chart(target_corr)

        with t4:
            st.subheader("7️⃣ 최적 Binning 구간 제안")
            st.write("연속형 변수를 범주형으로 변환 시 타겟 적중률이 가장 높은 구간입니다.")
            st.write("**[변수: 서비스 가입 기간]**")
            bin_df = pd.DataFrame({
                "구간 (Months)": ["0-6m", "6-12m", "12-24m", "24m+"],
                "타겟 적중률(%)": [45.2, 22.5, 12.0, 5.1]
            }).set_index("구간 (Months)")
            st.bar_chart(bin_df)
            st.info("💡 가입 6개월 미만 구간에서 해지율이 급격히 높으므로 별도 관리가 필요합니다.")

# 하단 공통 영역
if st.session_state.step >= 3:
    st.divider()
    if st.button("📋 전체 분석 리포트 PDF 다운로드"):
        st.write("리포트를 생성 중입니다...")
