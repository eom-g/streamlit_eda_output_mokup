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
        idx_df = pd.DataFrame({
            "지표명": ["유튜브 시청시간", "야간 데이터사용", "주말 통화량", "멤버십 활용"],
            "Index": [242, 185, 110, 95]
        }).sort_values("Index", ascending=False)
        for _, row in idx_df.iterrows():
            col_l, col_r = st.columns([0.2, 0.8])
            col_l.write(f"**{row['지표명']}**")
            col_r.progress(min(row['Index']/300, 1.0), text=f"Index: {row['Index']}")

    with t2:
        st.subheader("👤 고객 기본 프로파일링 (연령대 분포)")
        # 요청하신 연령대 그룹화 데이터 생성
        age_groups = ["10대", "20대", "30대", "40대", "50대", "60대", "70대", "80대 이상"]
        age_counts = [5, 42, 25, 15, 8, 3, 1, 1] # 샘플 데이터
        
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
    # [분석가용] 1~7번 항목
    # ---------------------------------------------------------
    t1, t2, t3, t4 = st.tabs(["🧹 1-2. 클렌징", "📉 3. 이상치 영향도", "🔗 4-6. 상관관계", "📐 7. Binning"])
    
    with t1:
        st.subheader("1-2️⃣ 데이터 클렌징 및 카디널리티")
        st.table(pd.DataFrame({"변수명": ["is_active", "country"], "값": ["Y", "82"], "비고": ["Zero-Variance"]}))
        card_df = pd.DataFrame({"변수": ["area", "model"], "Unique": [1450, 420], "Status": ["⚠️ High", "⚠️ High"]})
        st.dataframe(card_df.style.highlight_max(axis=0, color='lightcoral'))

    with t2:
        st.subheader("3️⃣ Outlier 영향도 분석 (이상치 제거 전/후 비교)")
        st.info("💡 이상치가 평균값을 얼마나 왜곡시키는지 진단합니다.")
        
        c1, c2 = st.columns(2)
        # x, y축 명시를 위한 가이드와 차트
        with c1:
            st.write("**[A] 제거 전 (Raw Data)**")
            st.bar_chart(np.random.exponential(50, 20))
            st.caption("X축: 데이터 사용량 구간 / Y축: 고객 빈도 (이상치로 인해 우측으로 길게 늘어짐)")
        
        with c2:
            st.write("**[B] 제거 후 (Refined)**")
            st.bar_chart(np.random.normal(30, 5, 20))
            st.caption("X축: 데이터 사용량 구간 / Y축: 고객 빈도 (정상 범위 내 분포 집중)")
        
        st.write("#### 📋 주요 피처별 평균 통계량 변화율")
        st.markdown("> **변화율(%)** = (제거 후 평균 - 제거 전 평균) / 제거 전 평균 * 100")
        
        stat_change = pd.DataFrame({
            "항목": ["평균(Mean)", "표준편차(Std)", "최대값(Max)"],
            "data_usage_mb": ["-29.2%", "-45.1%", "-88.5%"],
            "call_dur_min": ["-2.1%", "-5.4%", "-12.0%"]
        }).set_index("항목")
        st.table(stat_change)
        st.warning("분석 결과: 'data_usage_mb'는 이상치 제거 시 평균이 약 29% 감소하므로, 반드시 정제 후 모델링이 필요합니다.")

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
