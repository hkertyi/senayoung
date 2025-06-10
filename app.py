    '구세나': {'prob': 0.0008001, 'characters': ['파이', '로지', '쥬리']},
    '전설': {'prob': 0.006545, 'characters': ['테오', '바네사', '스파이크', '제이브', '레이첼', '아일린', '델론즈', '크리스', '루디', '실베스타', '에이스']},
    '준전설': {'prob': 0.0120003, 'characters': ['타카', '파스칼', '아라곤', '엘리스', '발리스타', '챈슬러', '룩', '지크', '세인', '에스파다', '니아', '루리', '벨리카', '리나', '비담', '유신', '녹스']},
    '희귀': {'prob': 0.979856, 'characters': [f'희귀_{i+1}' for i in range(34)]},
}

# 캐릭터별 등급 정보 만들기
char_to_grade = {}
for grade, info in probabilities.items():
    for char in info['characters']:
        char_to_grade[char] = grade

# 등급별 우선순위 (높은 등급일수록 숫자가 작음)
grade_priority = {
    '구세나': 0,
    '전설': 1,
    '준전설': 2,
    '희귀': 3,
}

# 등급별 색깔 지정 (Streamlit markdown 색상 코드)
grade_color = {
    '구세나': 'red',
    '전설': 'orange',
    '준전설': 'purple',  # 보라색으로 변경
    '희귀': 'gray',
}

def simulate_batch(prob_dict, batch_size=100):
    grades = list(prob_dict.keys())
    probs = [prob_dict[grade]['prob'] for grade in grades]
    results = []
    for _ in range(batch_size):
        r = random.random()
        cumulative = 0
        for grade, p in zip(grades, probs):
            cumulative += p
            if r < cumulative:
                char = random.choice(prob_dict[grade]['characters'])
                results.append(char)
                break
    return results

st.title("캐릭터별 합성 시뮬레이션 앱")

batch_size = st.selectbox("한 번에 몇 회 합성할까요?", options=[1, 10, 100], index=2)
num_batches = st.number_input("몇 번 반복할까요?", min_value=1, max_value=10000, value=10)

if st.button("시뮬레이션 시작"):
    batch_counts = []
    for _ in range(num_batches):
        batch_result = simulate_batch(probabilities, batch_size)
        counts = Counter(batch_result)
        batch_counts.append(counts)
    total_counter = Counter()
    for counts in batch_counts:
        total_counter.update(counts)

    st.write(f"전체 {batch_size*num_batches}회 시도 결과")

    # 등급 우선순위 기준으로 정렬
    sorted_chars = sorted(total_counter.items(), key=lambda x: (grade_priority[char_to_grade[x[0]]], -x[1]))

    # 등급별 색깔 입혀서 출력
    for char, count in sorted_chars:
        grade = char_to_grade[char]
        color = grade_color[grade]
        ratio = count / (batch_size*num_batches) * 100
        st.markdown(f"<span style='color:{color}; font-weight:bold;'>{char}</span>: {count}회, 비율: {ratio:.4f}%", unsafe_allow_html=True)

    # 구세나 캐릭터들만 뽑아서 등장 횟수 분포 시각화
    guse_na_chars = probabilities['구세나']['characters']
    guse_na_counts = []
    for counts in batch_counts:
        count = sum(counts.get(char, 0) for char in guse_na_chars)
        guse_na_counts.append(count)

    fig, ax = plt.subplots()
    ax.hist(guse_na_counts, bins=range(max(guse_na_counts)+2), color='coral', edgecolor='black', align='left')
    ax.set_title(f'{batch_size}회 합성 중 구세나(파이, 로지, 쥬리) 등장 횟수 분포 ({num_batches}번 반복)')
    ax.set_xlabel('한 배치 내 구세나 등장 횟수')
    ax.set_ylabel('빈도수')
    st.pyplot(fig)
