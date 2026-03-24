import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# --- 1. 기본 페이지 설정 ---
st.set_page_config(page_title="Sim Only vs 단말약정 비교 분석", layout="wide")

# --- 2. 사이드바 (글로벌 컨트롤) ---
with st.sidebar:
    st.title("🎯 Report Control")
    user_role = st.sidebar.radio("사용자 모드 선택", ["🏢 Target Profiling Mode", "🧪 Feature Engineering Mode"])
    st.divider()
    st.info("**분석 데이터 팩트 요약**\n- **대상**: Sim Only 신규 가입자\n- **비교군**: 단말 약정(공시/선약) 고객\n- **특징**: Sim Only는 외부 서비스(비디오/결제)에 민감")
    st.divider()
    st.caption("Last Update: 2026-03-24")

# --- 3. 메인 리포트 영역 ---
st.title(f"📊 {user_role} 리포트")
st.divider()

# ---------------------------------------------------------------------------
# CASE A: 사업팀 인사이트 모드 (Business Mode)
# ---------------------------------------------------------------------------
if user_role == "🏢 Target Profiling Mode":
    tab1, tab2, tab3 = st.tabs(["📋 Summary: 집단간 비교", "🔍 Detail: Sim Only 딥다이브", "🛡️ Guide & Context"])

    with tab1:
        st.subheader("📍 집단간 주요 활동성 비교 (단말 약정 vs Sim Only)")
        
        # 실측 데이터 기반 비교 차트
        compare_data = pd.DataFrame({
            "지표": ["데이터 고사용", "결합 서비스", "자사앱/멤버십", "마케팅 반응성", "비디오 스트리밍", "간편결제 이용"],
            "단말 약정(비교군)": [165, 160, 200, 200, 100, 100],
            "Sim Only(분석군)": [100, 100, 100, 100, 157, 150]
        })
        
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(x=compare_data["지표"], y=compare_data["단말 약정(비교군)"], name="단말 약정 (비교군)", marker_color='#D3D3D3'))
        fig_comp.add_trace(go.Bar(x=compare_data["지표"], y=compare_data["Sim Only(분석군)"], name="Sim Only (분석 대상)", marker_color='#FF4B4B'))
        
        fig_comp.update_layout(
            barmode='group', 
            height=450, 
            yaxis_title="비교 지수 (Index)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_comp, use_container_width=True)

        col_in1, col_in2 = st.columns(2)
        with col_in1:
            st.warning("**🏢 단말 약정 고객 (High Engagement)**\n- 데이터 사용, 결합, 자사 앱 반응도 전반에서 **1.5~2배** 높은 활동성\n- 자사 에코시스템 내 락인(Lock-in) 효과 뚜렷")
        with col_in2:
            st.success("**🎯 Sim Only 고객 (Smart Consumer)**\n- 비디오 스트리밍(**1.57배**), 간편결제(**1.5배**) 등 외부 서비스 활용 특화\n- 자사 혜택보다 실속 있는 외부 연계 소비 지향")

    with tab2:
        st.subheader("🔍 Sim Only 고객 행태 상세 분석")
        
        c1, c2 = st.columns(2)
        with c1:
            st.write("**🎥 외부 서비스 및 외부 데이터 활용도**")
            ext_svc = pd.DataFrame({
                "서비스": ["비디오 스트리밍", "네이버페이 이용", "외부 간편결제", "배달/생활 앱"],
                "Index": [157, 150, 138, 125]
            }).sort_values("Index", ascending=True)
            st.plotly_chart(px.bar(ext_svc, x="Index", y="서비스", orientation='h', color="Index", color_continuous_scale='Reds'), use_container_width=True)
            
        with c2:
            st.write("**🍕 멤버십 이용 카테고리 비중**")
            mem_cat = pd.DataFrame({
                "카테고리": ["외식/카페", "자동차/주유", "피자/베이커리", "데이터/통신사"],
                "비중": [42, 28, 20, 10]
            })
            st.plotly_chart(px.pie(mem_cat, values='비중', names='카테고리', hole=0.5, color_discrete_sequence=px.colors.sequential.RdBu), use_container_width=True)

        st.divider()
        st.write("**🎂 연령대 분포 (2040 세대 집중)**")
        age_dist = pd.DataFrame({"연령대": ["20대", "30대", "40대", "50대 이상"], "비중": [35, 38, 18, 9]})
        st.plotly_chart(px.bar(age_dist, x="연령대", y="비중", text="비중", color_discrete_sequence=['#FF4B4B']), use_container_width=True)

    with tab3:
        st.subheader("🛡️ 분석 가이드 및 용어 사전")
        st.info("**📍 분석 범위 (Context)**\n- **기간**: 2026.01.01 ~ 2026.03.20\n- **비교군**: 동기간 단말 약정(공시지원금/선택약정) 신규 가입 고객\n- **데이터**: 자사 이용량 + 외부 서비스 호출 로그 + 멤버십 승인 데이터")
        st.divider()
        st.write("**📙 주요 용어 사전**")
        with st.expander("비디오 스트리밍 지수 (Video Index)"):
            st.write("주요 OTT(유튜브, 넷플릭스 등) 트래픽 발생량을 기반으로 산출된 지표입니다.")
        with st.expander("간편결제 이용 지수 (Payment Index)"):
            st.write("네이버페이, 카카오페이 등 외부 간편결제 API 호출 빈도를 수치화했습니다.")

# ---------------------------------------------------------------------------
# CASE B: 분석가 데이터 진단 모드 (Analyst Mode)
# ---------------------------------------------------------------------------
else:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Summary", "📐 Var Detail", "📉 Correlation/Outlier", "🛠️ Quality/VIF"])

    with tab1:
        st.subheader("📊 Feature Importance & Target Correlation")
        col_iv, col_target = st.columns(2)
        with col_iv:
            st.write("**🔍 변수별 예측력 (IV Rank)**")
            iv_df = pd.DataFrame({"Variable": ["video_data", "n_pay_call", "lifestyle_member", "age_group"], "IV": [0.58, 0.42, 0.35, 0.18]}).sort_values("IV")
            st.plotly_chart(px.bar(iv_df, x="IV", y="Variable", orientation='h', color="IV"), use_container_width=True)
        with col_target:
            st.write("**🎯 Feature-Target Correlation (Top 5)**")
            ft_df = pd.DataFrame({"Feature": ["video_data", "n_pay_call", "delivery_app", "night_data", "ott_sub"], "Corr": [0.68, 0.62, 0.45, 0.38, 0.22]})
            st.plotly_chart(px.bar(ft_df, x="Corr", y="Feature", color="Corr"), use_container_width=True)

    with tab2:
        st.subheader("📐 변수별 상세 진단 (WoE/Lift)")
        target_var = st.selectbox("진단할 변수 선택", ["video_data_mb", "pay_call_cnt"])
        bins = ["Bin 1", "Bin 2", "Bin 3", "Bin 4", "Bin 5"]
        fig_combo = go.Figure()
        fig_combo.add_trace(go.Bar(x=bins, y=[2.8, 1.5, 0.9, 0.4, 0.2], name="Lift", yaxis="y1", marker_color='pink'))
        fig_combo.add_trace(go.Scatter(x=bins, y=[0.9, 0.3, -0.1, -0.6, -0.9], name="WoE", yaxis="y2", mode='lines+markers', line_color='red'))
        fig_combo.update_layout(yaxis=dict(title="Lift"), yaxis2=dict(title="WoE", overlaying="y", side="right"), legend=dict(x=0, y=1.1, orientation="h"))
        st.plotly_chart(fig_combo, use_container_width=True)

    with tab3:
        st.subheader("📉 이상치 및 상관관계 분석")
        c_box, c_stat = st.columns([0.6, 0.4])
        with c_box:
            df_out = pd.DataFrame({
                "Group": ["Original"] * 100 + ["Capped"] * 100,
                "Value": np.concatenate([np.random.normal(50, 20, 95).tolist() + [250, 300, 350, 400, 450], np.random.normal(50, 15, 100)])
            })
            st.plotly_chart(px.box(df_out, x="Group", y="Value", color="Group", title="이상치 처리 전/후 분포 (Video Data)"), use_container_width=True)
        with c_stat:
            st.write("**통계량 변화 비교**")
            st.table(pd.DataFrame({"항목": ["평균", "표준편차", "왜도"], "Original": [72.5, 52.3, 3.1], "Capped": [51.2, 14.2, 0.4], "변화율": ["-29%", "-72%", "-87%"]}))

        st.divider()
        st.write("**🔗 Interactive Correlation Heatmap**")
        corr_matrix = pd.DataFrame(np.random.uniform(-1, 1, (5, 5)), columns=['Video', 'Pay', 'Life', 'Age', 'Comb'], index=['Video', 'Pay', 'Life', 'Age', 'Comb'])
        st.plotly_chart(px.imshow(corr_matrix, text_auto=".2f", color_continuous_scale='RdBu_r'), use_container_width=True)

    with tab4:
        st.subheader("🛠️ 품질 및 다중공선성(VIF) 진단")
        v1, v2 = st.columns([0.4, 0.6])
        with v1:
            st.write("**🚨 VIF 위험 그룹**")
            st.error("삭제 권장: [total_data, video_data]")
            st.table(pd.DataFrame({"변수": ["total_data", "video_data"], "VIF": [18.4, 14.2]}))
        with v2:
            st.write("**🧹 Cardinality Audit**")
            qual_df = pd.DataFrame({"변수명": ["area_code", "device_model", "is_active"], "Unique": [1450, 420, 1], "상태": ["High", "High", "Zero-Var"], "조치": ["Target Encoding", "Target Encoding", "삭제"]})
            st.dataframe(qual_df.style.map(lambda x: 'background-color: #FFC0CB' if x in ['High', 'Zero-Var'] else '', subset=['상태']))
