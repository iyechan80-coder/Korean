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
    st.header("🔍 1단계: 초·중·고 통합형 디지털 리터러시 진단 테스트")
    st.markdown("주어진 상황을 읽고, 본인이 가장 먼저 할 것 같은 행동을 선택해 주세요.")
    
    with st.form("diagnosis_form"):
        # Q1. 정보 판별
        st.markdown("### Q1. [정보 판별 영역] SNS에 뜬 자극적인 뉴스")
        st.info("📱 **화면 연출:** 유튜브 쇼츠 또는 인스타그램 릴스 형태의 가상 영상 팝업\n\n**상황:** 스마트폰으로 피드를 내리다가 요즘 청소년들 사이에서 엄청 유행하는 앱이나 간식에 대해 **'충격 고발! 내일부터 전면 금지된다? 위험 성분 검출'**이라는 영상을 발견했습니다. 조회수도 수십만 회가 넘고 댓글창도 '헐 나 어제 먹었는데'라며 난리가 났을 때, 나의 행동은?")
        q1 = st.radio("선택지 (Q1):", [
            "A. 친구들이 알면 난리 나겠지? 유행에 뒤처지기 전에 반 단톡방에 영상 링크를 바로 공유한다.",
            "B. 조회수가 이렇게 높고 댓글에도 다들 진짜로 믿는 분위기인 걸 보니 사실이 맞는 것 같다. 일단 믿고 하트를 누른다.",
            "C. 조회수를 노린 자극적인 가짜 뉴스일 수 있으므로, 포털 사이트에 검색해 보거나 공식 뉴스 기사가 있는지 교차 검증한다."
        ], index=None)

        st.divider()

        # Q2. 디지털 윤리
        st.markdown("### Q2. [디지털 윤리 영역] 단톡방에서의 친구 험담")
        st.info("💬 **화면 연출:** 스마트폰 카카오톡 단체 대화방 UI 화면\n\n**상황:** 우리 반 친구들이 다 같이 있는 단톡방에서, 몇몇 친구들이 특정 친구의 굴욕 사진을 올리거나 그 친구의 단점을 지적하며 '진짜 짜증 난다', '킹받는다'라며 비웃고 있습니다. 이때 나의 행동은?")
        q2 = st.radio("선택지 (Q2):", [
            "A. 단톡방 흐름을 깨기 싫고 나도 재밌으니까 'ㅋㅋㅋ'를 연발하거나 웃기는 이모티콘을 보내며 같이 장난을 친다.",
            "B. 당사자 친구가 보면 상처받을 것 같아 마음이 불편하지만, 나도 무리에서 찍히거나 미움받을까 봐 아무 말도 안 하고 가만히 지켜본다.",
            "C. '이런 글 올리면 OO이가 속상할 것 같아'라고 단호하게 말리거나, 험담에 참여하지 않고 조용히 단톡방을 나온다."
        ], index=None)

        st.divider()

        # Q3. 디지털 보안
        st.markdown("### Q3. [디지털 보안 영역] 공짜 쿠폰 이벤트 문자의 유혹")
        st.info("📩 **화면 연출:** 스마트폰 문자 메시지 알림 팝업 화면\n\n**상황:** 모르는 번호로 문자 메시지가 한 통 도착했습니다. **'[이벤트 당첨] 축하합니다! 치킨+콜라 세트 쿠폰 당첨! 아래 링크를 눌러 이름과 전화번호를 입력하고 받아 가세요'**라는 내용과 함께 영어로 된 긴 인터넷 주소(URL) 링크가 적혀 있을 때, 나의 행동은?")
        q3 = st.radio("선택지 (Q3):", [
            "A. 와, 대박! 마침 배고팠는데 잘 됐다 싶어서 의심 없이 즉시 링크를 누르고 내 이름과 스마트폰 번호를 입력한다.",
            "B. 사기 문자 같아서 조금 불안하긴 하지만, 혹시 진짜일지도 모르니까 링크만 살짝 눌러서 어떤 화면이 나오나 확인해 본다.",
            "C. 개인정보를 빼가거나 악성코드를 심는 '스미싱' 문자이므로 링크를 절대 누르지 않고 문자를 바로 삭제하거나 신고한다."
        ], index=None)

        st.divider()

        # Q4. 저작권
        st.markdown("### Q4. [저작권 영역] 학교 숙제(과제)를 위한 인터넷 검색")
        st.info("💻 **화면 연출:** 노트북이나 태블릿의 포털 검색창 화면\n\n**상황:** 학교 수행평가나 숙제로 발표 자료(PPT)를 만들어야 합니다. 인터넷을 열심히 검색하던 중, 내가 찾던 주제와 완벽하게 일치하는 블로그의 글과 아주 멋진 사진을 발견했을 때 나의 행동은?")
        q4 = st.radio("선택지 (Q4):", [
            "A. 아무도 모르겠지? 블로그 주인의 글을 그대로 복사해서 붙여넣고, 사진도 그대로 저장해서 내가 만든 것처럼 제출한다.",
            "B. 통째로 베끼면 걸릴 수 있으니 문장 끝말만 슬쩍 바꾸고, 자료 맨 마지막 페이지에 대충 '출처: 네이버 블로그'라고만 적어 둔다.",
            "C. 사진은 상업적 이용이나 재배포가 가능한 무료 이미지(CCL)인지 확인하고 쓰며, 글은 완전히 이해한 뒤 내 문장으로 바꾸어 쓰고 정확한 웹사이트 주소를 밝힌다."
        ], index=None)

        st.divider()

        # Q5. 디지털 발자국
        st.markdown("### Q5. [디지털 발자국 영역] SNS에 올리는 나의 일상 사진")
        st.info("📸 **화면 연출:** 인스타그램/틱톡의 피드 업로드 대기 화면\n\n**상황:** 친구들과 학교 끝나고 떡볶이를 먹으러 가서 신나게 '인생샷'을 찍었습니다. 사진을 내 SNS에 업로드하려고 보니, 내 뒤로 다른 반 친구의 얼굴이 선명하게 찍혀 있고, 배경에 우리 집 아파트 이름과 동 번호가 슬쩍 노출되어 있는 것을 발견했습니다. 이때 나의 행동은?")
        q5 = st.radio("선택지 (Q5):", [
            "A. 사진이 너무 잘 나왔고 내 SNS인데 뭐 어때? 신경 쓰지 않고 전체 공개로 즉시 업로드한다.",
            "B. 아파트 이름은 좀 찜찜하지만 친구 얼굴은 잘 나온 것 같으니, 친한 친구들만 볼 수 있게 비공개 계정으로 올린다.",
            "C. 같이 찍힌 친구에게 동의를 구하고, 배경에 나온 집 주소나 타인의 얼굴은 모자이크/스티커로 가린 후 안전하게 업로드한다."
        ], index=None)

        submitted = st.form_submit_button("진단 결과 및 점수 확인")
        
        if submitted:
            # 모든 문항을 선택했는지 검증
            answers = [q1, q2, q3, q4, q5]
            if None in answers:
                st.warning("모든 문항을 선택해야 결과를 확인할 수 있습니다.")
                return

            # 점수 계산 로직 (A=0점, B=5점, C=10점)
            def get_score(answer):
                if answer.startswith("A"): return 0
                elif answer.startswith("B"): return 5
                elif answer.startswith("C"): return 10
                return 0
            
            scores = [get_score(ans) for ans in answers]
            total_score = sum(scores)
            
            # 등급 판별 (최대 50점)
            if total_score >= 40:
                st.session_state.level = "안전 등급 (디지털 시티즌)"
                color = "green"
            elif total_score >= 20:
                st.session_state.level = "주의 등급 (순진한 네티즌)"
                color = "orange"
            else:
                st.session_state.level = "보안 취약 등급"
                color = "red"
            
            st.markdown(f"### 🎯 당신의 총점: **{total_score}점 / 50점**")
            st.markdown(f"### 🛡️ 진단 결과: :{color}[**{st.session_state.level}**]")
            
            # 5개 영역별 시각적 피드백 (Plotly Bar Chart)
            categories = ["정보 판별", "디지털 윤리", "디지털 보안", "저작권", "디지털 발자국"]
            df = pd.DataFrame({"진단 영역": categories, "점수": scores})
            
            fig = px.bar(
                df, x="진단 영역", y="점수", 
                title="5대 디지털 리터러시 영역별 강·약점 분석", 
                range_y=[0, 10],
                color="점수",
                color_continuous_scale="Teal"
            )
            fig.update_layout(showlegend=False)
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
