import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- 리포트 렌더링 함수 ---
def render_custom_report(mode):
    st.divider()
    st.header(f"📊 분석 결과 리포트 ({mode})")
    
    if "사업팀" in mode:
        # [사업팀용] 1~4번 항목 중심
        st.info("💡 사업팀 모드는 비즈니스 의사결정을 위한 핵심 인사이트를 요약합니다.")
        
        # 항목 1: 데이터 현상 및 가설 검증 결과
        st.subheader("1️⃣ 가설 검증 및 현상 파악")
        c1, c2 = st.columns(2)
        with c1:
            st.write("**[입력 가설]**")
            st.info("연령대가 낮을수록 유튜브 사용량이 높을 것이다.")
        with c2:
            st.write("**[검증 결과]**")
            st.success("✅ 가설 일치: 20대 고객의 유튜브 사용량이 평균 대비 42% 높음 확인")

        # 항목 2: 타겟 vs 비교군 특징 차이 (Lift)
        st.subheader("2️⃣ 타겟 vs 비교군 주요 특징 (Lift)")
        lift_data = pd.DataFrame({
            "지표": ["유튜브 시청", "야간 데이터", "멤버십 활용", "평균 ARPU"],
            "Lift Index": [2.4, 1.8, 1.1, 0.9]
        })
        fig_lift = px.bar(lift_data, x="지표", y="Lift Index", color="Lift Index", title="일반 고객 대비 배수(Ratio)")
        st.plotly_chart(fig_lift, use_container_width=True)

        # 항목 3: 핵심 영향 인자 (Top Drivers)
        st.subheader("3️⃣ 성과에 영향을 주는 핵심 요인")
        st.markdown("- **최대 요인:** 주말 미디어 소비 시간 (영향도 45%)")
        st.markdown("- **차순위 요인:** 자급제 단말 이용 여부 (영향도 22%)")

        # 항목 4: 고객 페르소나 및 액션 제안
        st.subheader("4️⃣ 추천 페르소나 및 전략")
        p1, p2 = st.columns(2)
        p1.help("### [Persona: 젊은 스트리머]\n- 특징: 20대, 심야 사용량 높음\n- 제안: 넷플릭스 결합 요금제 노출")
        p2.help("### [Persona: 실속형 통신족]\n- 특징: 30대, Wi-Fi 위주 사용\n- 제안: 저가형 데이터 소량 요금제 유지")

    else:
        # [분석가용] 5~13번 항목 중심
        st.warning("🧪 분석가 모드는 모델링 적합성 및 통계적 데이터 품질을 진단합니다.")
        
        # 항목 5-6: 데이터 품질 및 분포 진단
        st.subheader("5️⃣-6️⃣ 데이터 품질 및 기초 통계 진단")
        q_df = pd.DataFrame({
            "Feature": ["cust_age", "data_mb", "call_cnt"],
            "Missing": ["0%", "0.2%", "5.1%"],
            "Outlier": ["None", "24 (IQR 1.5)", "120 (Z>3)"],
            "Skewness": [0.12, 2.45, 1.88]
        })
        st.table(q_df)

        # 항목 7-8: 상관관계 및 다중공선성 (VIF)
        st.subheader("7️⃣-8️⃣ 변수 간 관계 및 다중공선성 (VIF)")
        col_vif, col_corr = st.columns(2)
        with col_vif:
            st.write("**VIF 결과**")
            st.code("data_mb: 8.4 (High)\napp_freq: 2.1 (Low)\n...데이터 처리 필요")
        with col_corr:
            corr_m = np.random.rand(4,4)
            fig_corr = px.imshow(corr_m, x=['A','B','C','D'], y=['A','B','C','D'], title="Correlation Heatmap")
            st.plotly_chart(fig_corr, use_container_width=True)

        # 항목 9-11: 피처 중요도 및 통계적 유의성 (P-Value)
        st.subheader("9️⃣-1️⃣1️⃣ 피처 유의성 검정 (P-Value/SHAP)")
        importance_df = pd.DataFrame({
            "Feature": ["data_mb", "cust_age", "call_cnt", "svc_period"],
            "P-Value": [0.001, 0.045, 0.231, 0.002],
            "Importance": [0.55, 0.21, 0.05, 0.19]
        }).sort_values('Importance')
        fig_imp = px.bar(importance_df, x="Importance", y="Feature", orientation='h', color="P-Value")
        st.plotly_chart(fig_imp, use_container_width=True)

        # 항목 12-13: 분석 한계점 및 모델링 가이드
        st.subheader("1️⃣2️⃣-1️⃣3️⃣ 분석 한계점 및 Next Step")
        st.error("⚠️ 위치 데이터(GPS)의 결측치가 40% 이상으로, 해당 피처는 모델링에서 제외할 것을 권고함.")
        st.success("📝 추천 알고리즘: LightGBM (비선형 관계 및 이상치 대응에 최적)")

# --- 이전 코드의 버튼 클릭 시 호출 부분 ---
# if st.button("🚀 최종 분석 리포트 생성"):
#     render_custom_report(st.session_state.current_mode)
