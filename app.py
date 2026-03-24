import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# --- 1. 기본 페이지 설정 ---
st.set_page_config(page_title="Advanced EDA Dashboard", layout="wide")

# --- 2. 사이드바 (글로벌 컨트롤) ---
with st.sidebar:
    st.title("🎯 Report Control")
    user_role = st.sidebar.radio("사용자 모드 선택", ["🏢 Target Profiling Mode", "🧪 Feature Engineering Mode"])
    st.divider()
    st.info("**분석 데이터 정보**\n- 대상: 최근 3개월 Sim Only 가입자\n- 기간: '26.01.01 ~ '26.03.20\n- 모수: 15,200명")
    st.divider()
    st.caption("Produced by Gemini 3 Flash")

# --- 3. 메인 리포트 영역 ---
st.title(f"📊 {user_role} 리포트")
st.divider()

# ---------------------------------------------------------------------------
# CASE A: 사업팀 인사이트 모드 (Business Mode)
# ---------------------------------------------------------------------------
if user_role == "🏢 Target Profiling Mode":
    tab1, tab2, tab3 = st.tabs(["📋 Summary View", "🔍 Detail View", "🛡️ Guide & Trust"])

    with tab1:
        st.subheader("👤 타겟 페르소나 리포트")
        col1, col2 = st.columns([0.4, 0.6])
        
        with col1:
            st.write("**⚧ 성별 및 단말 비중**")
            gender_data = pd.DataFrame({"성별": ["남성", "여성"], "비중": [62, 38]})
            fig_gender = px.pie(gender_data, values='비중', names='성별', hole=0.6, 
                                color_discrete_sequence=['#636EFA', '#EF553B'])
            fig_gender.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_gender, use_container_width=True)
            
            device_df = pd.DataFrame({
                "유형": ["아이폰", "갤럭시프리미엄", "갤럭시중저가", "기타"],
                "비중(%)": [45, 35, 12, 8]
            }).set_index("유형")
            st.table(device_df)

        with col2:
            st.write("**🚀 핵심 변별 지표 (Top 5 Differentiators)**")
            diff_df = pd.DataFrame({
                "지표명": ["유튜브 시청 지수", "심야 데이터 사용량", "앱 접속 빈도", "주말 활동 지수", "멤버십 활용도"],
                "Index": [242, 185, 140, 115, 92]
            }).sort_values("Index", ascending=True)
            
            fig_diff = px.bar(diff_df, x="Index", y="지표명", orientation='h', text="Index",
                              color="Index", color_continuous_scale='Blues')
            st.plotly_chart(fig_diff, use_container_width=True)
            st.info("**💡 Insight**: 본 타겟은 전체 대비 유튜브 시청이 **2.4배** 높으며, 심야 활동이 두드러지는 '2030 나이트아울' 집단입니다.")

    with tab2:
        st.subheader("🔍 고객 행태 딥다이브")
        c1, c2 = st.columns(2)
        with c1:
            st.write("**🔗 결합 유형 비교 (vs 전체)**")
            comb_df = pd.DataFrame({
                "구분": ["Sim Only(대상)", "전체 가입자", "Sim Only(대상)", "전체 가입자"],
                "결합상태": ["미결합", "미결합", "결합중", "결합중"],
                "비중(%)": [78.4, 32.1, 21.6, 67.9]
            })
            fig_comb = px.bar(comb_df, x="구분", y="비중(%)", color="결합상태", barmode="group")
            st.plotly_chart(fig_comb, use_container_width=True)

        with c2:
            st.write("**🎁 멤버십 카테고리 이용 지수**")
            member_df = pd.DataFrame({
                "카테고리": ["생활/외식", "자동차/주유", "데이터나눠쓰기", "통신사 서비스"],
                "Index": [145, 128, 62, 45]
            })
            fig_member = px.bar(member_df, x="카테고리", y="Index", color="Index")
            st.plotly_chart(fig_member, use_container_width=True)

        st.divider()
        st.write("**📣 채널 선호도 및 최적 시간대**")
        ch_col, time_col = st.columns(2)
        with ch_col:
            st.bar_chart(pd.DataFrame({"반응률(%)": [45, 12, 28]}, index=["App Push", "MMS", "알림톡"]))
        with time_col:
            time_data = pd.DataFrame({"시간": list(range(24)), "활동량": np.random.normal(50, 15, 24)})
            st.line_chart(time_data.set_index("시간"))

    with tab3:
        st.subheader("🛡️ 데이터 분석 가이드 및 신뢰도")
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.success("**✅ 데이터 신뢰 점수: 98.2%**\n\n품질 검증이 완료된 정교한 데이터셋입니다.")
            st.write("**📍 분석 대상 범위**")
            st.write("- **기간**: 2026.01.01 ~ 2026.03.20\n- **대상**: 최근 3개월 내 가입한 Sim Only 고객\n- **제외**: 법인, 일시정지, 테스트 단말")
        with col_t2:
            st.write("**📙 주요 용어 사전**")
            with st.expander("유튜브 시청 지수 (Index)란?"):
                st.write("전체 가입자의 평균 유튜브 시청 시간을 100으로 놓았을 때, 해당 타겟 그룹의 상대적인 시청 시간 배수를 의미합니다.")
            with st.expander("심야 데이터 헤비 유저 (Night-Owl)"):
                st.write("22시부터 익일 04시 사이의 데이터 사용 비중이 전체 사용량의 40%를 초과하는 고객군입니다.")

# ---------------------------------------------------------------------------
# CASE B: 분석가 데이터 진단 모드 (Analyst Mode)
# ---------------------------------------------------------------------------
else:
    tab1, tab2, tab3 = st.tabs(["📊 Summary View", "📐 Detail View", "🛠️ Data Quality"])

    with tab1:
        st.subheader("📊 피처 중요도 리포트 (IV Rank)")
        iv_df = pd.DataFrame({
            "Variable": ["total_data_mb", "app_visit_cnt", "svc_period", "age", "avg_call_min"],
            "IV_Score": [0.45, 0.32, 0.15, 0.08, 0.03]
        }).sort_values("IV_Score", ascending=True)
        fig_iv = px.bar(iv_df, x="IV_Score", y="Variable", orientation='h', color="IV_Score")
        st.plotly_chart(fig_iv, use_container_width=True)
        
        st.write("**📉 데이터셋 기초 통계 요약**")
        st.table(pd.DataFrame({
            "항목": ["Total Rows", "Total Columns", "Missing Rate", "Outlier Count"],
            "Value": ["15,200", "45", "0.2%", "228건"]
        }))

    with tab2:
        st.subheader("📐 변수별 상세 진단 (Interactive)")
        target_var = st.selectbox("진단할 변수 선택", ["svc_period_months", "data_usage_mb", "membership_points"])
        
        # WoE/Lift Combo Chart
        bins = ["Bin 1", "Bin 2", "Bin 3", "Bin 4", "Bin 5"]
        lift_data = [2.5, 1.8, 1.2, 0.8, 0.5]
        woe_data = [0.8, 0.4, 0.1, -0.3, -0.7]

        fig_combo = go.Figure()
        fig_combo.add_trace(go.Bar(x=bins, y=lift_data, name="Lift (배수)", yaxis="y1", marker_color='lightblue'))
        fig_combo.add_trace(go.Scatter(x=bins, y=woe_data, name="WoE (지표)", yaxis="y2", mode='lines+markers', line_color='orange'))
        fig_combo.update_layout(yaxis=dict(title="Lift"), yaxis2=dict(title="WoE", overlaying="y", side="right"),
                                legend=dict(x=0, y=1.1, orientation="h"))
        st.plotly_chart(fig_combo, use_container_width=True)
        st.warning(f"**[Advice]** `{target_var}` 변수는 Bin 1~2 구간에서 강력한 비선형 패턴이 관측되므로 범주화(Binning)를 권장합니다.")

    with tab3:
        st.subheader("🛠️ 기술적 결함 리포트")
        st.write("**1️⃣ Zero-Variance & Cardinality Audit**")
        
        qual_df = pd.DataFrame({
            "변수명": ["is_active", "country_code", "area_code", "device_model", "cust_grade"],
            "Unique": [1, 1, 1450, 420, 5],
            "상태": ["Zero-Var", "Zero-Var", "High", "High", "Normal"],
            "조치": ["삭제", "삭제", "Target Encoding", "Target Encoding", "유지"]
        })
        
        def color_status(val):
            color = 'lightcoral' if val in ['Zero-Var', 'High'] else 'white'
            return f'background-color: {color}'
        
        st.dataframe(qual_df.style.map(color_status, subset=['상태']))
        
        st.divider()
        st.write("**2️⃣ VIF(다중공선성) 위험군**")
        st.error("**Alert**: `total_data_mb`와 `night_data_mb`의 VIF 지수가 15.2로 산출되었습니다. 변수 통합(PCA)이 필요합니다.")
