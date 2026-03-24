import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# --- 1. 기본 페이지 설정 ---
st.set_page_config(page_title="Advanced EDA Dashboard v2", layout="wide")

# --- 2. 사이드바 (글로벌 컨트롤) ---
with st.sidebar:
    st.title("🎯 Report Control")
    user_role = st.sidebar.radio("사용자 모드 선택", ["🏢 Target Profiling Mode", "🧪 Feature Engineering Mode"])
    st.divider()
    st.info("**분석 데이터 정보**\n- 대상: 최근 3개월 Sim Only 가입자\n- 기간: '26.01.01 ~ '26.03.20\n- 모수: 155,200명")

# --- 3. 메인 리포트 영역 ---
st.title(f"📊 {user_role} 리포트")
st.divider()

# ---------------------------------------------------------------------------
# CASE A: 사업팀 인사이트 모드 (Business Mode)
# ---------------------------------------------------------------------------
if user_role == "🏢 Target Profiling Mode":
    tab1, tab2, tab3 = st.tabs(["📋 Summary View", "🔍 Detail View", "🛡️ Guide & Context"])

    with tab1:
        st.subheader("👤 타겟 페르소나 리포트")
        col1, col2 = st.columns([0.4, 0.6])
        with col1:
            st.write("**⚧ 성별 및 단말 비중**")
            gender_data = pd.DataFrame({"성별": ["남성", "여성"], "비중": [62, 38]})
            fig_gender = px.pie(gender_data, values='비중', names='성별', hole=0.6, color_discrete_sequence=['#636EFA', '#EF553B'])
            st.plotly_chart(fig_gender, use_container_width=True)
            st.table(pd.DataFrame({"유형": ["아이폰", "갤럭시프리미엄", "기타"], "비중(%)": [45, 35, 20]}).set_index("유형"))
        with col2:
            st.write("**🚀 핵심 변별 지표 (Top 5 Differentiators)**")
            diff_df = pd.DataFrame({"지표명": ["유튜브 지수", "심야 데이터", "앱 접속", "주말 활동", "멤버십"], "Index": [242, 185, 140, 115, 92]}).sort_values("Index")
            st.plotly_chart(px.bar(diff_df, x="Index", y="지표명", orientation='h', text="Index", color="Index"), use_container_width=True)
            st.info("**💡 Insight**: 본 타겟은 전체 대비 유튜브 시청이 **2.4배** 높은 '2030 나이트아울' 집단입니다.")

    with tab2:
        st.subheader("🔍 고객 행태 딥다이브")
        c1, c2 = st.columns(2)
        with c1:
            st.write("**🔗 결합 유형 비교 (vs 전체)**")
            st.bar_chart(pd.DataFrame({"대상": [78, 22], "전체": [32, 68]}, index=["미결합", "결합중"]))
        with c2:
            st.write("**🎁 멤버십 카테고리 이용 지수**")
            st.bar_chart(pd.DataFrame({"Index": [145, 128, 62, 45]}, index=["생활/외식", "자동차/주유", "나눠쓰기", "통신사"]))

    with tab3:
        st.subheader("🛡️ 데이터 분석 가이드 및 범위")
        # 데이터 신뢰 점수 제거 및 범위/사전 중심으로 재구성
        st.info("**📍 분석 대상 범위 (Scope)**\n- **기간**: 2026.01.01 ~ 2026.03.20\n- **대상**: 최근 3개월 내 가입한 Sim Only 고객 (법인/정지회선 제외)")
        st.divider()
        st.write("**📙 주요 용어 사전**")
        with st.expander("유튜브 시청 지수 (Index)란?"):
            st.write("전체 가입자의 평균 유튜브 시청 시간을 100으로 놓았을 때의 상대적 배수입니다.")
        with st.expander("심야 데이터 헤비 유저 (Night-Owl)"):
            st.write("22시~04시 사이 데이터 사용 비중이 전체의 40%를 초과하는 고객군입니다.")

# ---------------------------------------------------------------------------
# CASE B: 분석가 데이터 진단 모드 (Analyst Mode)
# ---------------------------------------------------------------------------
else:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Summary", "📐 Variable Detail", "📉 Outlier/Correlation", "🛠️ Quality/VIF"])

    with tab1:
        st.subheader("📊 Feature Importance & Correlation")
        col_iv, col_target = st.columns(2)
        with col_iv:
            st.write("**🔍 변수별 예측력 (IV Rank)**")
            iv_df = pd.DataFrame({"Variable": ["total_data", "app_visit", "svc_period", "age"], "IV": [0.45, 0.32, 0.15, 0.08]}).sort_values("IV")
            st.plotly_chart(px.bar(iv_df, x="IV", y="Variable", orientation='h', color="IV"), use_container_width=True)
        with col_target:
            st.write("**🎯 Feature-Target Correlation (Top 5)**")
            ft_df = pd.DataFrame({"Feature": ["total_data", "app_visit", "call_min", "roaming", "points"], "Corr": [0.65, 0.58, 0.42, 0.31, 0.15]})
            st.plotly_chart(px.bar(ft_df, x="Corr", y="Feature", color="Corr", title="타겟 영향력 순위"), use_container_width=True)

    with tab2:
        st.subheader("📐 변수별 상세 진단 (WoE/Lift)")
        target_var = st.selectbox("진단할 변수 선택", ["svc_period_months", "data_usage_mb"])
        bins = ["Bin 1", "Bin 2", "Bin 3", "Bin 4", "Bin 5"]
        fig_combo = go.Figure()
        fig_combo.add_trace(go.Bar(x=bins, y=[2.5, 1.8, 1.2, 0.8, 0.5], name="Lift", yaxis="y1", marker_color='lightblue'))
        fig_combo.add_trace(go.Scatter(x=bins, y=[0.8, 0.4, 0.1, -0.3, -0.7], name="WoE", yaxis="y2", mode='lines+markers', line_color='orange'))
        fig_combo.update_layout(yaxis=dict(title="Lift"), yaxis2=dict(title="WoE", overlaying="y", side="right"), legend=dict(x=0, y=1.1, orientation="h"))
        st.plotly_chart(fig_combo, use_container_width=True)

    with tab3:
        st.subheader("📉 이상치 및 상관관계 분석")
        st.write("**1️⃣ Outlier 영향도 (Box Plot & Stats)**")
        c_box, c_stat = st.columns([0.6, 0.4])
        with c_box:
            # 이상치 제거 전/후 비교 Box Plot
            df_out = pd.DataFrame({
                "Group": ["Original"] * 100 + ["Capped"] * 100,
                "Value": np.concatenate([np.random.normal(50, 20, 95).tolist() + [200, 250, 300, 350, 400], np.random.normal(50, 15, 100)])
            })
            st.plotly_chart(px.box(df_out, x="Group", y="Value", color="Group", title="이상치 처리 전/후 분포 비교"), use_container_width=True)
        with c_stat:
            st.write("**통계량 변화 비교**")
            st.table(pd.DataFrame({"항목": ["평균", "표준편차", "왜도"], "Original": [65.2, 45.1, 2.8], "Capped": [50.1, 14.8, 0.5], "변화율": ["-23%", "-67%", "-82%"]}))

        st.divider()
        st.write("**2️⃣ Interactive Correlation Heatmap**")
        corr_matrix = pd.DataFrame(np.random.uniform(-1, 1, (6, 6)), columns=['Age', 'Data', 'App', 'Call', 'Svc', 'Point'], index=['Age', 'Data', 'App', 'Call', 'Svc', 'Point'])
        fig_corr = px.imshow(corr_matrix, text_auto=".2f", aspect="auto", color_continuous_scale='RdBu_r', title="변수간 상관계수 (마우스 오버 시 수치 확인)")
        st.plotly_chart(fig_corr, use_container_width=True)
        st.info("**💡 추천**: 'Data'와 'App' 변수의 상관계수가 0.85로 높습니다. 다중공선성을 고려하여 'Data' 변수 선별을 권장합니다.")

    with tab4:
        st.subheader("🛠️ Quality & Multicollinearity (VIF)")
        v_col1, v_col2 = st.columns([0.4, 0.6])
        with v_col1:
            st.write("**🚨 VIF 위험 변수 그룹**")
            st.error("삭제 권장 그룹: [total_data, night_data, weekend_data]")
            st.warning("주의 그룹: [avg_call, total_call]")
            st.write("**VIF List**")
            st.table(pd.DataFrame({"변수": ["total_data", "night_data", "avg_call"], "VIF": [15.2, 12.8, 8.5]}))
        with v_col2:
            st.write("**🧹 데이터 품질 진단 (Cardinality)**")
            qual_df = pd.DataFrame({"변수명": ["area_code", "model", "is_active"], "Unique": [1450, 420, 1], "상태": ["High", "High", "Zero-Var"], "조치": ["Target Encoding", "Target Encoding", "삭제"]})
            st.dataframe(qual_df.style.map(lambda x: 'background-color: lightcoral' if x in ['High', 'Zero-Var'] else '', subset=['상태']))
