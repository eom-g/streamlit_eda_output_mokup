import streamlit as st
import pandas as pd
import numpy as np

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="EDA Agent Final Report", layout="wide")

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
    # [사업팀용] 1~3번 항목
    # ---------------------------------------------------------
    t1, t2, t3 = st.tabs(["📊 1. 집단간 비교", "👤 2. 프로파일링", "📱 3. 채널 선호도"])
    
    with t1:
        st.subheader("📍 지표별 특징 Index (전체 대비)")
        # 사라졌던 집단간 비교 지표 복구
        idx_df = pd.DataFrame({
            "지표명": ["유튜브 시청시간", "야간 데이터사용", "주말 통화량", "멤버십 활용"],
            "Index": [242, 185, 110, 95]
        }).sort_values("Index", ascending=False)
        
        for _, row in idx_df.iterrows():
            col_l, col_r = st.columns([0.2, 0.8])
            col_l.write(f"**{row['지표명']}**")
            # Index 100 기준 시각화
            col_r.progress(min(row['Index']/300, 1.0), text=f"Index: {row['Index']}")
        
        st.subheader("🔍 변수별 예측력 (IV Rank)")
        iv_data = pd.DataFrame({"IV Score": [0.45, 0.32, 0.15, 0.08]}, 
                               index=["데이터사용량", "앱접속빈도", "연령", "가입기간"])
        st.bar_chart(iv_data)

    with t2:
        st.subheader("👤 고객 기본 프로파일링 (연령대 분포)")
        # 요청하신 연령대 x축 (10대 ~ 80대 이상) 반영
        age_groups = ["10대", "20대", "30대", "40대", "50대", "60대", "70대", "80대 이상"]
        age_counts = [5, 42, 25, 15, 8, 3, 1, 1]
        
        hist_df = pd.DataFrame({
            "연령대": age_groups,
            "고객 수(명)": age_counts
        }).set_index("연령대")
        
        st.bar_chart(hist_df)
        st.caption("X축: 연령대 그룹 / Y축: 해당 연령대 고객 수 (명)")

    with t3:
        st.subheader("📣 채널 선호도 반응 분석")
        channel_data = pd.DataFrame({"반응": [45, 12, 28], "미반응": [55, 88, 72]}, index=["App Push", "MMS", "알림톡"])
        st.bar_chart(channel_data)

else:
    # ---------------------------------------------------------
    # [분석가용] 1~7번 항목 (ValueError 수정 완료)
    # ---------------------------------------------------------
    t1, t2, t3, t4 = st.tabs(["🧹 1-2. 클렌징", "📉 3. 이상치 영향도", "🔗 4-6. 상관관계", "📐 7. Binning"])
    
    with t1:
        st.subheader("1-2️⃣ 데이터 클렌징 및 카디널리티")
        # ValueError 해결: 리스트 길이를 2개로 통일
        st.table(pd.DataFrame({
            "변수명": ["is_active", "country"], 
            "값": ["Y", "82"], 
            "비고": ["Zero-Variance", "Zero-Variance"] # 개수 맞춤
        }))
        
        card_df = pd.DataFrame({"변수": ["area", "model"], "Unique": [1450, 420], "Status": ["⚠️ High", "⚠️ High"]})
        st.dataframe(card_df.style.highlight_max(axis=0, color='lightcoral'))

    with t2:
        st.subheader("3️⃣ Outlier 영향도 분석 (제거 전/후 비교)")
        st.info("💡 이상치가 평균값을 얼마나 왜곡시키는지 진단합니다.")
        
        c1, c2 = st.columns(2)
        with c1:
            st.write("**[A] 제거 전 (Raw Data)**")
            st.bar_chart(np.random.exponential(50, 20))
            st.caption("X축: 데이터 사용량 구간(MB) / Y축: 고객 빈도(명)")
        
        with c2:
            st.write("**[B] 제거 후 (Refined)**")
            st.bar_chart(np.random.normal(30, 5, 20))
            st.caption("X축: 데이터 사용량 구간(MB) / Y축: 고객 빈도(명)")
        
        st.write("#### 📋 주요 피처별 평균 통계량 변화율")
        # 통계량 변화율 의미: 이상치 제거 시 중심값(평균)이 얼마나 정상화되었는지 표시
        stat_change = pd.DataFrame({
            "통계 항목": ["평균(Mean)", "표준편차(Std)", "최대값(Max)"],
            "data_usage_mb": ["-29.2%", "-45.1%", "-88.5%"],
            "call_dur_min": ["-2.1%", "-5.4%", "-12.0%"]
        }).set_index("통계 항목")
        st.table(stat_change)
        st.warning("분석가 가이드: 'data_usage_mb'의 평균 변화율(-29%)이 매우 크므로 이상치 처리가 필수적입니다.")

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
