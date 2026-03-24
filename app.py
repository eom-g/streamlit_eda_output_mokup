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
    user_role = st.sidebar.radio("사용자 모드 선택", ["🏢 Target Profiling Mode", "🧪 eature Engineering Mode"])
    st.divider()
    st.info("**분석 데이터 팩트**\n- **대상**: Sim Only 신규 가입자\n- **비교군**: 단말 약정 가입자\n- **핵심**: 자사 활동성(약정) vs 외부/생활 활동성(Sim Only) 대조")

# --- 3. 메인 리포트 영역 ---
st.title(f"📊 {user_role} 리포트")
st.caption("주제: 단말 약정 대비 Sim Only 고객의 차별적 행태 분석")
st.divider()

# ---------------------------------------------------------------------------
# CASE A: 사업팀 인사이트 모드 (Business Mode)
# ---------------------------------------------------------------------------
if user_role == "🏢 Target Profiling Mode":
    tab1, tab2, tab3 = st.tabs(["📋 Summary: 집단간 비교", "🔍 Detail: Sim Only 딥다이브", "🛡️ Guide & Context"])

    with tab1:
        st.subheader("📍 핵심 지표별 집단간 차이 (단말 약정 vs Sim Only)")
        
        # 1. 개별 변수별 비교 데이터 (사용자 제공 팩트 기반)
        # 지표별로 약정이 높은 항목과 Sim Only가 높은 항목을 구분하여 배치
        compare_df = pd.DataFrame({
            "지표": ["자사 앱 접속일수", "자사 멤버십 사용일수", "MMS/푸쉬 반응", "유무선/무무선 결합", "데이터 사용량", "네이버페이 사용일수", "간편결제 웹앱 접속"],
            "단말 약정(비교군)": [200, 200, 200, 180, 165, 100, 100],
            "Sim Only(분석군)": [100, 100, 100, 100, 100, 150, 155]
        })
        
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(x=compare_df["지표"], y=compare_df["단말 약정(비교군)"], name="단말 약정 (약 1.5~2배 높음)", marker_color='#D3D3D3'))
        fig_comp.add_trace(go.Bar(x=compare_df["지표"], y=compare_df["Sim Only(분석군)"], name="Sim Only (외부 앱/웹 우세)", marker_color='#FF4B4B'))
        
        fig_comp.update_layout(barmode='group', height=450, yaxis_title="지수 (Index)", legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig_comp, use_container_width=True)

        st.divider()
        
        # 2. 1위 카테고리 비교 (데이터 사용 vs 멤버십 사용)
        col_cat1, col_cat2 = st.columns(2)
        with col_cat1:
            st.write("**📱 데이터 사용 1위 카테고리 비중**")
            # Sim Only는 비디오 스트리밍이 압도적 (1.57배 반영)
            data_cat = pd.DataFrame({
                "카테고리": ["비디오 스트리밍", "유튜브", "SNS", "웹서핑", "게임/음악"],
                "Sim Only 비중": [45, 25, 15, 10, 5]
            })
            st.plotly_chart(px.pie(data_cat, values='Sim Only 비중', names='카테고리', hole=0.4, color_discrete_sequence=px.colors.sequential.Reds_r), use_container_width=True)
            st.caption("💡 Sim Only 고객은 비디오/유튜브 합산 **70%**로 미디어 소비에 집중됨")

        with col_cat2:
            st.write("**🍕 멤버십 사용 1위 카테고리 비중**")
            # Sim Only는 생활 소비(외식, 피자, 자동차) 중심
            mem_cat = pd.DataFrame({
                "카테고리": ["외식/커피", "피자/베이커리", "자동차/여행", "도서/쇼핑", "자사 서비스"],
                "Sim Only 비중": [40, 25, 20, 10, 5]
            })
            st.plotly_chart(px.pie(mem_cat, values='Sim Only 비중', names='카테고리', hole=0.4, color_discrete_sequence=px.colors.sequential.Purp_r), use_container_width=True)
            st.caption("💡 약정 고객(자사 서비스 중심)과 달리 Sim Only는 **생활 밀착형 소비**가 90% 이상")

    with tab2:
        st.subheader("🔍 Sim Only 분석 변수별 상세 (Single Metric)")
        
        # 각 변수들을 별개의 건으로 보여주기 위해 컬럼 분할
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("비디오 스트리밍 데이터", "1.57배", "+57% vs 약정")
            st.write("**네이버페이 앱 사용일수**")
            st.plotly_chart(px.bar(pd.DataFrame({"구분": ["약정", "Sim Only"], "일수": [4.2, 6.3]}), x="구분", y="일수", color="구분", color_discrete_map={"약정":"#D3D3D3", "Sim Only":"#FF4B4B"}), use_container_width=True)
            
        with m2:
            st.metric("간편결제 이용 지수", "1.5배", "+50% vs 약정")
            st.write("**데이터 사용 1위: 비디오**")
            st.progress(0.45, text="45% 가입자가 비디오 1위")
            
        with m3:
            st.metric("생활 카테고리 멤버십", "90%", "외식/피자/자동차 중심")
            st.write("**결합 상품 보유 비율**")
            st.plotly_chart(px.pie(pd.DataFrame({"구분": ["미보유", "보유"], "비중": [78, 22]}), values="비중", names="구분", color_discrete_sequence=['#FF4B4B', '#D3D3D3']), use_container_width=True)

        st.divider()
        st.write("**🎂 타겟 연령대 상세 (20~40대 중심)**")
        st.bar_chart(pd.DataFrame({"비중(%)": [35, 38, 18, 9]}, index=["20대", "30대", "40대", "50대+"]))

    with tab3:
        st.subheader("🛡️ 분석 가이드 및 용어 사전")
        st.success("**📍 분석 범위**\n- 기간: 2026.01.01 ~ 2026.03.20\n- 대상: Sim Only 가입자 (비교군: 단말 약정 가입자)")
        st.divider()
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            with st.expander("데이터 사용 1위 카테고리"):
                st.write("고객별 데이터 사용량이 가장 많은 APP/웹 서비스를 6개군(비디오, 유튜브, 게임 등)으로 분류하여 산출")
            with st.expander("멤버십 사용 1위 카테고리"):
                st.write("U+멤버십 승인 건수가 가장 많은 업종을 13개군(자사, 네이버플러스, 배달 등)으로 분류")
        with col_g2:
            with st.expander("간편결제 웹앱 접속 일수"):
                st.write("네이버페이 외 삼성페이, 카카오페이 등 외부 간편결제 서비스의 웹/앱 접속 로그 일수")

# ---------------------------------------------------------------------------
# CASE B: 분석가 데이터 진단 모드 (Analyst Mode)
# ---------------------------------------------------------------------------
else:
    tab1, tab2, tab3 = st.tabs(["📊 변수 중요도(IV)", "📈 상관관계/이상치", "🛠️ 품질 및 VIF"])

    with tab1:
        st.subheader("📊 Sim Only 판별 핵심 변수 (IV Rank)")
        # 실측 변수명 기반 IV 랭킹
        iv_data = pd.DataFrame({
            "Variable": ["video_data_usage", "npay_use_days", "membership_cat_rank", "age_group", "combined_ratio"],
            "IV": [0.57, 0.48, 0.41, 0.22, 0.15]
        }).sort_values("IV")
        st.plotly_chart(px.bar(iv_data, x="IV", y="Variable", orientation='h', color="IV", color_continuous_scale='Reds'), use_container_width=True)

    with tab2:
        st.subheader("📉 이상치 및 상관관계 진단")
        c1, c2 = st.columns([0.6, 0.4])
        with c1:
            st.write("**🔗 주요 변수간 상관관계 히트맵**")
            corr = pd.DataFrame(np.random.uniform(-1, 1, (5, 5)), columns=['Video', 'N-Pay', 'Member', 'Age', 'Comb'], index=['Video', 'N-Pay', 'Member', 'Age', 'Comb'])
            st.plotly_chart(px.imshow(corr, text_auto=".2f", color_continuous_scale='RdBu_r'), use_container_width=True)
        with c2:
            st.write("**📉 Outlier Check (Box Plot)**")
            out_df = pd.DataFrame({"Data": np.random.normal(50, 15, 100).tolist() + [300, 350, 400]})
            st.plotly_chart(px.box(out_df, y="Data", title="데이터 사용량 이상치"), use_container_width=True)

    with tab3:
        st.subheader("🛠️ 데이터 품질 및 VIF")
        v_col1, v_col2 = st.columns(2)
        with v_col1:
            st.error("**[VIF Warning]** `total_data_usage`와 `video_data_usage` 간 다중공선성 높음 (VIF: 14.5)")
            st.table(pd.DataFrame({"변수": ["video_data", "npay_days"], "VIF": [14.5, 4.2]}))
        with v_col2:
            st.write("**🧹 Cardinality 진단**")
            st.table(pd.DataFrame({"변수명": ["mem_cat_1st", "data_cat_1st"], "Unique": [13, 6], "상태": ["Normal", "Normal"]}))
