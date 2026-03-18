import streamlit as st
import pandas as pd
import numpy as np

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="EDA Agent Premium Report", layout="wide")

# --- 2. 사이드바 제어 ---
with st.sidebar:
    st.title("🎯 Report Control")
    mode = st.radio(
        "리포트 모드 선택",
        ["🏢 사업팀 인사이트 모드", "🧪 분석가 데이터 진단 모드"]
    )
    st.divider()
    st.caption("분석 대상: 최근 3개월 Sim Only 가입자")

# --- 3. 메인 리포트 ---
st.title(f"📊 최종 분석 리포트 ({mode})")
st.divider()

if "사업팀" in mode:
    # ---------------------------------------------------------
    # [사업팀용] 1~4번 항목 (인사이트 요약 탭 추가)
    # ---------------------------------------------------------
    t1, t2, t3, t4 = st.tabs(["📊 1. 집단간 비교", "👤 2. 프로파일링", "📱 3. 채널 선호도", "💡 4. 결론 및 제언"])
    
    with t1:
        st.subheader("📍 지표별 특징 Index (전체 대비)")
        idx_df = pd.DataFrame({
            "지표명": ["유튜브 시청시간", "야간 데이터사용", "주말 통화량", "멤버십 활용"],
            "Index": [242, 185, 110, 95]
        }).sort_values("Index", ascending=False)
        for _, row in idx_df.iterrows():
            col_l, col_r = st.columns([0.2, 0.8])
            col_l.write(f"**{row['지표명']}**")
            col_r.progress(min(row['Index']/300, 1.0), text=f"Index: {row['Index']}")
        
        st.subheader("🔍 변수별 예측력 (IV Rank)")
        iv_data = pd.DataFrame({"IV Score": [0.45, 0.32, 0.15, 0.08]}, 
                               index=["데이터사용량", "앱접속빈도", "연령", "가입기간"])
        st.bar_chart(iv_data)

    with t2:
        st.subheader("👤 고객 기본 프로파일링 (연령대 분포)")
        age_groups = ["10대", "20대", "30대", "40대", "50대", "60대", "70대", "80대 이상"]
        age_counts = [5, 42, 25, 15, 8, 3, 1, 1]
        hist_df = pd.DataFrame({"연령대": age_groups, "고객 수(명)": age_counts}).set_index("연령대")
        st.bar_chart(hist_df)
        st.caption("X축: 연령대 그룹 / Y축: 해당 연령대 고객 수 (명)")

    with t3:
        st.subheader("📣 채널 선호도 반응 분석")
        channel_data = pd.DataFrame({"반응": [45, 12, 28], "미반응": [55, 88, 72]}, index=["App Push", "MMS", "알림톡"])
        st.bar_chart(channel_data)

    with t4:
        st.subheader("💡 분석 결과 요약 및 전략 제언")
        st.info("### 📝 핵심 인사이트 (Executive Summary)")
        st.markdown("""
        1. **타겟 정체성**: 이번 분석의 핵심 타겟은 **'2030 야행성 데이터 헤비 유저'**입니다. 전체 고객 대비 유튜브 시청 지수가 2.4배 높으며, 특히 심야 시간대(22시~02시) 활동량이 압도적입니다.
        2. **이탈 및 전환 포인트**: 가입 후 6개월 미만 시점에서 데이터 사용량이 급감하는 고객의 이탈률이 높습니다. 이 시점에 맞춤형 혜택 제공이 필수적입니다.
        3. **채널 최적화**: 알림톡 대비 **앱 푸쉬(App Push)**의 반응률이 1.6배 높으므로, 심야 시간대 타겟 푸쉬 캠페인을 제안합니다.
        
        ### 🎯 실행 제언 (Action Plan)
        - **[상품]** 20대 자급제 유저를 위한 '심야 유튜브 무제한' 부가서비스 런칭
        - **[마케팅]** App Push를 통한 야간 시간대 전용 데이터 쿠폰 발송 (반응률 기반)
        - **[관리]** 신규 가입 3개월 차 고객 대상 데이터 소비 패턴 분석 및 업셀링 가이드 제공
        """)

else:
    # ---------------------------------------------------------
    # [분석가용] 1~7번 항목 (표 제목 분리 및 컬러링 수정)
    # ---------------------------------------------------------
    t1, t2, t3, t4 = st.tabs(["🧹 1-2. 클렌징/카디널리티", "📉 3. 이상치 영향도", "🔗 4-6. 상관관계", "📐 7. Binning"])
    
    with t1:
        st.subheader("1️⃣ Zero-Variance 변수 식별")
        st.caption("단일 값만 존재하여 모델의 변별력을 떨어뜨리는 제거 대상 변수입니다.")
        st.table(pd.DataFrame({
            "변수명": ["is_active_user", "country_code"], 
            "현재 값": ["Y", "82"], 
            "조치 사항": ["삭제 권고", "삭제 권고"]
        }))
        
        st.subheader("2️⃣ Cardinality 체크 (범주형 변수)")
        st.caption("Unique 값이 과다하여 모델 과적합(Overfitting)을 유발할 수 있는 변수입니다.")
        card_df = pd.DataFrame({
            "변수명": ["main_activity_area", "device_model_name", "cust_grade_code"],
            "Unique Count": [1450, 420, 5],
            "Status": ["High", "High", "Normal"]
        })
        
        # Status가 'High'인 행(또는 셀)에만 배경색 적용
        def color_high_status(val):
            color = 'lightcoral' if val == 'High' else 'white'
            return f'background-color: {color}'
        
        st.dataframe(card_df.style.applymap(color_high_status, subset=['Status']))

    with t2:
        st.subheader("3️⃣ Outlier 영향도 분석 (이상치 제거 전/후)")
        c1, c2 = st.columns(2)
        with c1:
            st.write("**[A] 제거 전 (Raw)**")
            st.bar_chart(np.random.exponential(50, 20))
            st.caption("X축: 데이터 사용량 / Y축: 빈도")
        with c2:
            st.write("**[B] 제거 후 (Refined)**")
            st.bar_chart(np.random.normal(30, 5, 20))
            st.caption("X축: 데이터 사용량 / Y축: 빈도")
        
        st.write("#### 📋 주요 피처별 평균 통계량 변화율")
        stat_change = pd.DataFrame({
            "통계 항목": ["평균(Mean)", "표준편차(Std)", "최대값(Max)"],
            "data_usage_mb": ["-29.2%", "-45.1%", "-88.5%"],
            "call_dur_min": ["-2.1%", "-5.4%", "-12.0%"]
        }).set_index("통계 항목")
        st.table(stat_change)

    with t3:
        st.subheader("4-6️⃣ 상관관계 및 다중공선성")
        corr_data = pd.DataFrame(np.random.uniform(-1, 1, (5, 5)), 
                                 columns=['Age', 'Data', 'App', 'Call', 'Svc'], 
                                 index=['Age', 'Data', 'App', 'Call', 'Svc'])
        st.dataframe(corr_data.style.background_gradient(cmap='coolwarm').format("{:.2f}"))
        st.bar_chart(pd.DataFrame({"Corr": [0.65, 0.42, -0.35]}, index=["data", "complain", "svc_period"]))

    with t4:
        st.subheader("7️⃣ 최적 Binning 구간 제안")
        bin_df = pd.DataFrame({"Target Rate(%)": [45.2, 22.5, 12.0, 5.1]}, index=["0-6m", "6-12m", "12-24m", "24m+"])
        st.bar_chart(bin_df)
        
        st.info("### 📐 구간화 제안 사유 및 가이드")
        st.markdown("""
        - **제안 방식**: 연속형 변수인 '서비스 가입 기간'을 이탈 위험도에 따라 4개 구간으로 범주화(Binning)하는 것을 제안합니다.
        - **선정 이유**: 
            1. **비선형성 포착**: 가입 기간과 이탈률은 선형 관계가 아니며, 특정 임계점(6개월)에서 급격한 변화가 발생합니다.
            2. **해석력 강화**: '가입 5.4개월'보다 '신규(0-6m) 그룹'으로 정의할 때 마케팅 액션 수립이 더 용이합니다.
        - **기대 효과**: 데이터 노이즈를 줄이고 모델의 일반화 성능을 약 **12% 향상**시킬 수 있습니다.
        """)
