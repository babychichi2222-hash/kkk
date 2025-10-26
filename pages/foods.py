import streamlit as st
import random

# 1. 초기 설정 및 상태 초기화
if 'foods' not in st.session_state:
    st.session_state.foods = []
if 'current_round_foods' not in st.session_state:
    st.session_state.current_round_foods = []
if 'winner' not in st.session_state:
    st.session_state.winner = None

def start_tournament():
    # 입력받은 음식 리스트를 세션 상태에 저장하고 토너먼트 시작
    # 입력된 텍스트를 줄바꿈 기준으로 분리하여 리스트로 만듭니다.
    input_foods = [food.strip() for food in st.session_state.food_input.split('\n') if food.strip()]
    
    if len(input_foods) < 2:
        st.error("최소 2개 이상의 음식을 입력해주세요.")
        return
        
    st.session_state.foods = input_foods
    st.session_state.current_round_foods = list(input_foods) # 복사
    st.session_state.winner = None
    # 홀수 개수일 경우를 대비해 무작위로 1개를 미리 부전승 시킬 수도 있습니다. (선택 사항)

def process_match(winner_food):
    # 현재 대결의 승자를 다음 라운드로 이동시킵니다.
    
    # 현재 라운드의 매칭 리스트에서 승자를 제외한 나머지 음식들을 기록
    remaining_foods = [food for food in st.session_state.current_round_foods if food != winner_food and food != "---BYE---"]
    
    # 이전 라운드의 모든 참가자 중에서 현재 승자를 제외한 나머지 사람들을 다음 라운드에 대기시킵니다.
    # 이 부분이 복잡할 수 있으므로, 간단하게는 현재 대결 후 남은 음식들을 다음 라운드 리스트로 설정합니다.
    
    # 현재 라운드에서 대결이 끝난 후, 승자만 다음 라운드 리스트로 옮기는 로직이 필요합니다.
    # 더 간단하게 구현하려면, 현재 라운드 음식 리스트를 처리할 때 승자를 모으는 방식으로 진행합니다.

    # (간단한 로직 예시: 현재 대결에서 승리한 음식만 모으는 방식)
    # 실제 구현에서는 현재 '대결 중인 리스트'에서 승자를 다음 라운드 임시 리스트로 옮겨야 합니다.
    
    # 예시: 4강 -> 2강 -> 결승
    
    # 현재 매칭의 나머지 한쪽을 찾아야 하는데, 토너먼트 구조를 유지하기 위해
    # '현재 라운드의 음식 리스트'를 어떻게 구성했는지에 따라 달라집니다.
    
    # 가장 쉬운 방법: 현재 대결이 끝난 후, 승자만 다음 라운드 리스트에 추가하고,
    # 다음 라운드 시작 시 남아있는 음식들을 다시 2개씩 짝지어줍니다.
    
    if 'next_round_foods' not in st.session_state:
        st.session_state.next_round_foods = []
        
    st.session_state.next_round_foods.append(winner_food)
    
    # 현재 라운드에 남은 음식들을 임시 변수로 처리하여 다음 대결을 준비해야 합니다.
    # 이 부분은 토너먼트 구조(8강, 4강, 2강)를 어떻게 시각적으로 구현하느냐에 따라 달라집니다.
    
    # (추가 구현 필요: 현재 대결이 끝났으면, 다음 대결을 준비해야 합니다.)
    
    # 임시로, 현재 라운드에 있는 모든 음식을 처리했다고 가정하고 다음 라운드 진출자를 확정하는 방식
    # st.session_state.current_round_foods = st.session_state.next_round_foods
    # st.session_state.next_round_foods = [] # 초기화
    
    # 이 방식 대신, 현재 리스트에서 대결을 끝내고 다음 대결로 넘어가는 방식으로 해보겠습니다.
    pass # 실제 구현 시 복잡해지므로 일단 넘어가고 메인 로직을 구성합니다.

st.title("오늘 뭐 먹지? 음식 월드컵!")

# 1. 음식 입력
st.session_state.food_input = st.text_area(
    "먹고 싶은 음식들을 한 줄에 하나씩 입력하세요 (예: 김치찌개, 짜장면, 피자...)", 
    value=st.session_state.get('food_input', "떡볶이\n순대국\n파스타\n초밥") # 기본값 설정
)

if st.button("월드컵 시작!"):
    start_tournament()

# 2. 토너먼트 진행
if st.session_state.foods and not st.session_state.winner:
    
    current_foods = st.session_state.current_round_foods
    
    # 남은 음식이 1개라면 우승
    if len(current_foods) == 1:
        st.session_state.winner = current_foods[0]
    
    # 다음 라운드 진출자 리스트 (이번 라운드에서 승리한 음식들)
    if 'next_round_foods' not in st.session_state:
        st.session_state.next_round_foods = []

    # 현재 라운드에 대결할 음식이 없으면 다음 라운드로 넘어감
    if not current_foods and st.session_state.next_round_foods:
        st.session_state.current_round_foods = st.session_state.next_round_foods
        st.session_state.next_round_foods = []
        st.rerun() # 리로드하여 새로운 라운드 시작

    # 현재 라운드에서 짝을 지어 대결 시키기
    if len(current_foods) >= 2:
        
        # 2개씩 짝짓기
        food1 = current_foods[0]
        food2 = current_foods[1]
        
        # 대결 중인 음식들을 current_round_foods에서 잠시 제거
        st.session_state.current_round_foods.pop(0)
        st.session_state.current_round_foods.pop(0)
        
        st.header(f"Round {len(st.session_state.foods) - len(current_foods) + 1} Match") # 라운드 번호 계산은 복잡할 수 있음
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(food1, key=f"match_{food1}"):
                st.session_state.next_round_foods.append(food1)
                st.rerun() # 바로 재실행하여 다음 매칭으로 넘어감
        
        with col2:
            if st.button(food2, key=f"match_{food2}"):
                st.session_state.next_round_foods.append(food2)
                st.rerun() # 바로 재실행하여 다음 매칭으로 넘어감
                
    elif len(current_foods) == 1 and not st.session_state.next_round_foods:
        # 홀수일 경우 남은 하나를 다음 라운드로 넘김 (이 부분은 토너먼트 설계에 따라 수정 필요)
        st.session_state.next_round_foods.append(current_foods[0])
        st.session_state.current_round_foods = [] # 이번 라운드 종료
        st.rerun()
        
# 3. 결과 출력
if st.session_state.winner:
    st.balloons()
    st.success(f"축하합니다! 오늘 먹을 음식은 바로 **{st.session_state.winner}** 입니다! 🥳")
    
    if st.button("다시 하기"):
        # 세션 상태 초기화
        st.session_state.clear()
        st.rerun()
