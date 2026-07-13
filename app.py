import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# 1. 시스템 설정 및 세션 상태 초기화
# ==========================================
st.set_page_config(page_title="AI & Digital Literacy Platform", layout="wide")

if 'level' not in st.session_state:
    st.session_state.level = "미정"
if 'unesco_module' not in st.session_state:
    st.session_state.unesco_module = "이해(초급)"
if 'process_log' not in st.session_state:
    st.session_state.process_log = {
        "fact_check_attempts": 0,
        "prompt_revisions": 0,
        "license_checks": 0,
        "source_generations": 0
    }

def log_action(action_name):
    """과정 중심 평가를 위한 사용자 행동 로깅 함수"""
    try:
        if action_name in st.session_state.process_log:
            st.session_state.process_log[action_name] += 1
    except Exception as e:
        st.error(f"Logging Error: {e}")

# ==========================================
# 2. 단계별 모듈 함수 정의
# ==========================================
def pre_step_diagnosis():
    st.header("🔍 1단계: 디지털 시민 지수 사전 테스트")
    st.markdown("현재 당신의 디지털 리터러시 수준을 진단합니다.")
    
    with st.form("diagnosis_form"):
        q1 = st.radio("1. 소셜 미디어에서 자극적인 제목의 기사를 보았을 때 당신의 행동은?", 
                      ["바로 공유한다", "제목만 보고 댓글을 단다", "출처와 교차 검증을 한다"])
        q2 = st.radio("2. 인터넷 이미지를 과제에 사용할 때 올바른 행동은?", 
                      ["구글 검색 이미지를 그냥 쓴다", "출처만 링크로 남긴다", "CCL(크리에이티브 커먼즈 라이선스)를 확인한다"])
        submitted = st.form_submit_button("진단 결과 확인")
        
        if submitted:
            score = 0
            if q1 == "출처와 교차 검증을 한다": score += 50
            if q2 == "CCL(크리에이티브 커먼즈 라이선스)를 확인한다": score += 50
            
            if score == 100:
                st.session_state.level = "안전 등급 (디지털 시티즌)"
            elif score == 50:
                st.session_state.level = "주의 등급 (순진한 네티즌)"
            else:
                st.session_state.level = "보안 취약 등급"
            
            st.success(f"당신의 진단 결과: **{st.session_state.level}**")
            
            df = pd.DataFrame({"영역": ["정보 검증", "저작권 의식"], "점수": [50 if q1 == "출처와 교차 검증을 한다" else 10, 50 if q2 == "CCL(크리에이티브 커먼즈 라이선스)를 확인한다" else 10]})
            fig = px.bar(df, x="영역", y="점수", title="영역별 취약점 분석", range_y=[0, 50])
            st.plotly_chart(fig, use_container_width=True)

def main_step_1_simulation():
    st.header("🎮 2단계: 몰입형 시뮬레이션 학습")
    
    st.session_state.unesco_module = st.selectbox(
        "유네스코(UNESCO) 학습 모듈 선택", 
        ["이해(초급) - 팩트체크 시뮬레이터", "적용(중급) - 디지털 발자국 추적기", "창조(고급) - AI 모델 편향성 디버깅"]
    )
    
    if "이해" in st.session_state.unesco_module:
        st.subheader("미션: 오늘의 가짜 뉴스 3개를 찾아라!")
        st.info("[속보] 유명 아이돌, 외계인과 비밀 회동 포착!")
        col1, col2 = st.columns(2)
        if col1.button("게시물 공유하기 (Safe Failure 체험)"):
            st.error("🚨 가상 파장 발생: 허위 사실 유포로 인해 가상 사회 혼란 지수가 30% 상승했습니다! (결과를 직접 확인하세요)")
        if col2.button("출처 및 팩트체크 진행"):
            log_action("fact_check_attempts")
            st.success("✅ 훌륭합니다! 교차 검증 결과, 생성형 AI로 조작된 딥페이크 이미지임을 확인했습니다.")
            
    elif "창조" in st.session_state.unesco_module:
        st.subheader("미션: 채용 AI 모델의 편향성 디버깅")
        st.markdown("현재 AI가 '남성' 지원자에게 가산점을 주고 있습니다. 윤리적 판단을 내려 데이터를 수정하세요.")
        if st.button("편향된 데이터셋 배제 및 재학습 (윤리적 판단)"):
            log_action("fact_check_attempts")
            st.success("균형 잡힌 데이터셋으로 재학습되었습니다. 편향성이 0%로 조정되었습니다.")

def main_step_2_creation():
    st.header("✍️ 3단계: 실천적 창작 및 적용 (PBL)")
    st.markdown("사회적 이슈에 대한 카드뉴스 텍스트를 작성하세요. 타인의 저작권을 존중하는 과정이 평가됩니다.")
    
    content = st.text_area("작성 영역 (AI의 초안을 비판적으로 수정하세요):", height=150)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 글 수정/업데이트 기록하기"):
            log_action("prompt_revisions")
            st.info(f"수정 횟수가 기록되었습니다. (현재 {st.session_state.process_log['prompt_revisions']}회)")
    with col2:
        if st.button("©️ 라이선스(CCL) 체커 실행"):
            log_action("license_checks")
            st.info("비상업적 용도(NC), 출처 표시(BY) 라이선스가 확인되었습니다.")
    with col3:
        if st.button("🔗 출처 표기 생성기"):
            log_action("source_generations")
            st.info("APA 형식 출처가 본문 하단에 자동 생성되었습니다.")

def evaluation_dashboard():
    st.header("📊 과정 중심 평가 대시보드 (Rubric Dashboard)")
    st.markdown("결과물의 길이가 아닌, **윤리적 책임과 과정의 투명성**을 측정합니다.")
    
    logs = st.session_state.process_log
    st.subheader("실시간 윤리적 행동 추적 지표")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("데이터 의심 및 팩트체크", f"{logs['fact_check_attempts']} 회")
    m2.metric("프롬프트/초안 비판적 수정", f"{logs['prompt_revisions']} 회")
    m3.metric("저작권 및 출처 검증", f"{logs['license_checks'] + logs['source_generations']} 회")
    
    total_process_score = sum(logs.values())
    st.markdown("### 🏆 최종 과정 평가 리포트")
    if total_process_score >= 5:
        st.success("훌륭합니다! AI가 생성한 1차 답변을 맹신하지 않고, 출처 확인과 비판적 수정을 거쳐 투명하고 윤리적인 콘텐츠를 생산했습니다.")
    elif total_process_score > 0:
        st.warning("윤리적 콘텐츠 생산을 위한 과정이 시작되었습니다. 글을 제출하기 전 출처와 라이선스를 한 번 더 점검하는 습관을 들이세요.")
    else:
        st.error("주의: 결과물 도출에만 집중하고 있습니다. 정보의 출처를 의심하고 윤리적 판단을 내리는 '과정'이 누락되었습니다.")

# ==========================================
# 3. 메인 앱 라우팅 (Sidebar Navigation)
# ==========================================
def main():
    st.sidebar.title("내비게이션")
    menu = st.sidebar.radio("학습 단계를 선택하세요", 
                            ["1단계: 진단 (Pre-Step)", 
                             "2단계: 시뮬레이션 (Main-Step 1)", 
                             "3단계: 실천적 창작 (Main-Step 2)", 
                             "평가 대시보드 (Rubric)"])
    
    if menu == "1단계: 진단 (Pre-Step)":
        pre_step_diagnosis()
    elif menu == "2단계: 시뮬레이션 (Main-Step 1)":
        main_step_1_simulation()
    elif menu == "3단계: 실천적 창작 (Main-Step 2)":
        main_step_2_creation()
    elif menu == "평가 대시보드 (Rubric)":
        evaluation_dashboard()

if __name__ == "__main__":
    main()
