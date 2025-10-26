import streamlit as st
import random

# 1. 카테고리별 마스터 음식 리스트 정의
FOOD_MASTER_LIST = {
    "한식 (Korean)": [
        "김치찌개", "된장찌개", "불고기", "삼겹살", "비빔밥", "잡채", 
        "떡볶이", "순대국", "갈비찜", "해장국", "라면", "제육볶음", 
        "부대찌개", "냉면", "보쌈", "칼국수"
    ],
    "중식 (Chinese)": [
        "짜장면", "짬뽕", "탕수육", "깐풍기", "마파두부", "양장피", 
        "볶음밥", "유산슬", "고추잡채", "마라탕", "꿔바로우", "멘보샤",
        "우동", "군만두", "물만두", "짜장밥"
    ],
    "일식 (Japanese)": [
        "초밥", "돈가스", "라멘", "우동", "규동", "카레", 
        "타코야키", "오코노미야키", "소바", "야키니쿠", "스키야키", "덴뿌라",
        "가츠동", "회", "튀김", "장어덮밥"
    ],
    "양식 (Western)": [
        "피자", "파스타 (봉골레)", "스테이크", "샐러드", "햄버거", "샌드위치",
        "리조또", "오믈렛", "수프", "그라탕", "라자냐", "타코",
        "핫도그", "감자튀김", "스튜", "바비큐"
    ]
}

# 2. 초기 설정 및 상태 초기화
if 'foods' not in st.session_state:
    st.session_state.foods = []
if 'current_round_foods' not in st.session_state:
    st.session_state.current_round_foods = []
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'next_round_foods' not in st.session_state:
    st.session_state.next_round_foods = []
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'round_num' not in st.session_state:
    st.session_state.round_num = 0
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None

def start_tournament(category, num_candidates):
    # 선택된 카테고리의 리스트를 가져옵니다.
    category_list = FOOD_MASTER_LIST.get(category, [])
    
    if num_candidates < 2 or len(category_list) < num_candidates:
        st.error(f"선택하신 카테고리({category})의 음식 개수가 부족하거나, 최소 2개 이상의 후보가 필요합니다.")
        return

    # 마스터 리스트에서 지정된 개수만큼 무작위로 음식을 선택합니다.
    selected_foods = random.sample(category_list, k=num_candidates)
    
    st.session_state.foods = selected_foods # 전체 후보 리스트 (최초)
    st.session_state.current_round_foods = list(selected_foods) # 현재 라운드에 남은 음식 리스트
    st.session_state.winner = None
    st.session_state.next_round_foods = []
    st.session_state.game_started = True
    st.session_state.round_num = 1 # 라운드 초기화
    st.session_state.selected_category = category
    st.rerun()

def get_round_title(total, current):
    # 토너먼트 라운드 제목을 동적으로 생성
    if total == 2: return "🍚 최종 결승전"
    if total == 4: return "🍜 4강"
    if total == 8: return "🍲 8강"
    if total == 16: return "🥘 16강"
    return f"Round {current}"

# =========================================================================

st.title("오늘 뭐 먹지? 💡 카테고리별 음식 월드컵!")

# 1. 게임 시작 옵션 (카테고리 선택)
if not st.session_state.game_started:
    st.subheader("1. 음식 카테고리를 선택하세요.")
    
    category_choice = st.selectbox(
        "음식 유형",
        options=list(FOOD_MASTER_LIST.keys()),
        key="category_select"
    )
    
    st.subheader("2. 월드컵 규모를 선택하세요.")
    # 2의 거듭제곱 수로 후보군을 선택
    
    # 선택된 카테고리의 최대 후보 개수 확인
    max_candidates = len(FOOD_MASTER_LIST.get(category_choice, []))
    
    available_options = [c for c in [4, 8, 16] if c <= max_candidates]
    if not available_options:
        st.error(f"선택된 카테고리 **{category_choice}**의 음식 개수가 최소 4개 미만이므로 월드컵을 시작할 수 없습니다. (현재 {max_candidates}개)")
    
    num_candidates = st.selectbox(
        "몇 강으로 시작하시겠어요?",
        options=available_options,
        index=len(available_options) - 1 if available_options else 0
    )
    
    if st.button(f"**{category_choice}** {num_candidates}강 월드컵 시작! 🚀", disabled=not available_options):
        start_tournament(category_choice, num_candidates)

# 2. 토너먼트 진행
if st.session_state.game_started and not st.session_state.winner:
    
    current_foods = st.session_state.current_round_foods
    next_round_foods = st.session_state.next_round_foods
    
    st.subheader(f"선택된 카테고리: **{st.session_state.selected_category}**")
    
    # --- 라운드 전환 로직 ---
    # 남은 음식이 1개이고, 다음 라운드 진출자가 없으면 우승
    if len(current_foods) == 1 and not next_round_foods:
        st.session_state.winner = current_foods[0]
        st.rerun() # 승리 화면으로 전환

    # 현재 라운드에 대결할 음식이 없으면 다음 라운드로 넘어감
    if not current_foods and next_round_foods:
        st.session_state.current_round_foods = list(next_round_foods) # 다음 라운드 음식 설정
        st.session_state.next_round_foods = [] # 다음 라운드 리스트 초기화
        st.session_state.round_num += 1
        st.rerun() # 새로운 라운드 시작

    # --- 대결 진행 ---
    if len(current_foods) >= 2:
        
        # 2개씩 짝짓기
        food1 = current_foods[0]
        food2 = current_foods[1]
        
        # 대결 중인 음식들을 current_round_foods에서 제거
        st.session_state.current_round_foods.pop(0)
        st.session_state.current_round_foods.pop(0)
        
        # 라운드 헤더 표시
        current_num_participants = len(current_foods) + len(next_round_foods) + 2 # 현재 라운드 참가자 수 (대충 계산)
        round_title = get_round_title(current_num_participants, st.session_state.round_num)

        st.header(round_title)
        st.title(f"**{food1}** vs **{food2}**")
        
        col1, col2 = st.columns(2)
        
        # 승자 선택 버튼
        with col1:
            if st.button(f"**{food1}** 선택! 👈", key=f"match_{food1}"):
                st.session_state.next_round_foods.append(food1)
                st.rerun() # 바로 재실행하여 다음 매칭으로 넘어감
        
        with col2:
            if st.button(f"👉 **{food2}** 선택!", key=f"match_{food2}"):
                st.session_state.next_round_foods.append(food2)
                st.rerun() # 바로 재실행하여 다음 매칭으로 넘어감
        
        st.markdown("---")
        # 다음 라운드까지 남은 대결 횟수 계산
        next_matches = len(st.session_state.current_round_foods) // 2
        st.caption(f"이번 라운드 남은 대결: {next_matches}개")


# 3. 결과 출력
if st.session_state.winner:
    st.balloons()
    st.success(f"🎉 **{st.session_state.selected_category}** 월드컵 우승! 오늘 먹을 음식은 바로 **{st.session_state.winner}** 입니다! 🥳")
    
    if st.button("다시 하기"):
        # 세션 상태 초기화
        st.session_state.clear()
        st.rerun()
