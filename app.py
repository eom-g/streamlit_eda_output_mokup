import streamlit as st
import pandas as pd
import numpy as np

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="EDA Agent Premium Report", layout="wide")

# --- 2. 사이드바 제어 ---
with st.sidebar:
    st.title("🎯 Report Control")
    mode = st.radio("리포트 모드 선택", ["🏢 사업팀 인사이트 모드", "🧪 분석가 데이터 진단 모드"])
    st.divider()
    st.caption("분석 대상: 최근 3개월 Sim Only 신규 가입자")

# --- 3. 메인 리포트 ---
st.title(f"📊 최종 분석 리포트 ({mode})")
st.divider()

if "사업팀" in mode:
    # ---------------------------------------------------------
    # [사업팀용] 1~4번 항목 (결합 및 멤버십 인사이트 보강)
    # ---------------------------------------------------------
    t1, t2, t3, t4 = st.tabs(["📊 1. 집단간 비교", "👤 2. 서비스 수용도 & 멤버십", "📱 3. 채널 선호도", "💡 4. 결론 및 제언"])
    
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
        st.bar_chart(pd.DataFrame({"IV Score": [0.45, 0.32, 0.15]}, index=["데이터사용량", "앱접속빈도", "연령"]))

    with t2:
        st.subheader("👤 Sim Only 타겟 서비스 수용도 및 소비 패턴")
        c1, c2 = st.columns(2)
        
        with c1:
            st.write("**🔗 결합 및 약정 현황**")
            # 유무선/무무선 결합 비율 백데이터 (Sim Only 특성 반영)
            comb_df = pd.DataFrame({
                "결합 유형": ["미결합(단독)", "유무선 결합", "무무선 결합"],
                "비중(%)": [78.4, 15.2, 6.4]
            }).set_index("결합 유형")
            st.bar_chart(comb_df)
            st.caption("💡 Sim Only 고객은 결합 혜택을 통한 락인(Lock-in) 효과가 매우 낮음 (미결합 78%)")

        with c2:
            st.write("**🎁 멤버십 카테고리별 이용 지수**")
            # 내부 서비스 vs 생활 소비 대조 데이터
            member_df = pd.DataFrame({
                "카테고리": ["생활/외식", "자동차/주유", "데이터나눠쓰기", "통신사 부가서비스"],
                "이용 지수(Index)": [145, 128, 62, 45]
            }).set_index("카테고리")
            st.bar_chart(member_df)
            st.caption("💡 통신사 내부 서비스보다 실생활 소비(외식/자동차) 중심의 멤버십 이용이 두드러짐")

        st.divider()
        st.write("**🎂 타겟 연령대 분포**")
        age_groups = ["10대", "20대", "30대", "40대", "50대", "60대 이상"]
        st.bar_chart(pd.DataFrame({"고객 수(명)": [5, 48, 28, 12, 5, 2]}, index=age_groups))

    with t3:
        st.subheader("📣 채널 선호도 반응 분석")
        st.bar_chart(pd.DataFrame({"반응": [45, 12, 28], "미반응": [55, 88, 72]}, index=["App Push", "MMS", "알림톡"]))

    with t4:
        st.subheader("💡 분석 결과 요약 및 전략 제언")
        st.info("### 📝 핵심 인사이트 (Executive Summary)")
        st.markdown("""
        1. **타겟 정체성**: 이번 분석 대상인 'Sim Only' 가입자는 **2030 야행성 데이터 헤비 유저**이며, 특정 통신사에 락인되지 않은 **자립형 고객**입니다. 
        2. **결합 및 소속도 저하**: 유무선/무무선 결합률이 20% 미만으로 매우 낮으며, '데이터 나눠쓰기'나 '통신사 부가서비스' 등 내부 생태계 이용률(Index 45~62) 또한 저조합니다. 이는 통신사 브랜드에 대한 충성도보다 **개인화된 실속 혜택**에 민감함을 시사합니다.
        3. **생활 밀착형 소비 패턴**: 멤버십 사용 이력을 보면 **외식, 자동차(주유/정비)** 등 실생활 소비 카테고리에서의 이용 지수(Index 145)가 높게 나타납니다. 
        4. **접점 최적화**: 활동 정점인 심야 시간대(22-02시)에 **App Push**를 통한 소통이 가장 효과적(반응률 45%)입니다.
        """)
        st.success("### 🎯 실행 제언 (Action Plan)\n- **[상품]** 통신사 내부 서비스 묶음보다는 '유튜브/OTT' 등 외부 콘텐츠 결합 및 '실속형 데이터 충전' 상품 강화\n- **[마케팅]** 멤버십 이용이 많은 '외식/주유' 관련 타겟팅 쿠폰을 App Push로 발송하여 체감 혜택 극대화")

else:
    # ---------------------------------------------------------
    # [분석가용] 데이터 진단 모드 (동일)
    # ---------------------------------------------------------
    t1, t2, t3, t4 = st.tabs(["🧹 1. Cleansing/Cardinality", "📉 2. 이상치 영향도", "🔗 4. 상관관계", "📐 5. Binning"])
    
    with t1:
        st.subheader("1. Zero-Variance 변수 식별")
        st.table(pd.DataFrame({"변수명": ["is_active", "country"], "값": ["Y", "82"], "조치": ["제거", "제거"]}))
        
        st.subheader("2. Cardinality 체크")
        card_df = pd.DataFrame({"변수명": ["area", "model", "grade"], "Unique": [1450, 420, 5], "Status": ["High", "High", "Normal"]})
        st.dataframe(card_df.style.map(lambda x: 'background-color: lightcoral' if x == 'High' else '', subset=['Status']))

    with t2:
        st.subheader("3. Outlier 영향도 분석 (이상치 제거 전/후)")
        c1, c2 = st.columns(2)
        c1.bar_chart(np.random.exponential(50, 15))
        c2.bar_chart(np.random.normal(30, 5, 15))
        st.table(pd.DataFrame({"항목": ["평균", "Std", "Max"], "data_usage": ["-29.2%", "-45.1%", "-88.5%"]}).set_index("항목"))

    with t3:
        st.subheader("4. 상관관계 및 다중공선성")
        corr = pd.DataFrame(np.random.uniform(-1, 1, (5, 5)), columns=['Age', 'Data', 'App', 'Call', 'Svc'], index=['Age', 'Data', 'App', 'Call', 'Svc'])
        st.dataframe(corr.style.background_gradient(cmap='coolwarm').format("{:.2f}"))

    with t4:
        st.subheader("5. 최적 Binning 구간 제안")
        st.bar_chart(pd.DataFrame({"Target Rate(%)": [45.2, 22.5, 12.0, 5.1]}, index=["0-6m", "6-12m", "12-24m", "24m+"]))
