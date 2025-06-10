import streamlit as st
import random
import matplotlib.pyplot as plt
from collections import Counter

# 캐릭터 리스트
characters = {
    '구세나': ['파이', '로지', '쥬리'],
    '전설': ['테오', '바네사', '스파이크', '제이브', '레이첼', '아일린', '델론즈', '크리스', '루디', '실베스타', '에이스'],
    '준전설': ['타카', '파스칼', '아라곤', '엘리스', '발리스타', '챈슬러', '룩', '지크', '세인', '에스파다', '니아', '루리', '벨리카', '리나', '비담', '유신', '녹스'],
    '희귀': ['희귀{}'.format(i+1) for i in range(34)]
}

# 확률 설정
rarity_probs = {
    '구세나': 0.0008001,
    '전설': 0.006545,
    '준전설': 0.0120003,
    '희귀': 0.979856
}

rarity_colors = {
    '구세나': 'red',
    '전설': 'orange',
    '준전설': 'purple',
    '희귀': 'gray'
}

def simulate_once():
    roll = random.random()
    cumulative = 0
    for rarity, prob in rarity_probs.items():
        cumulative += prob
        if roll < cumulative:
            return random.choice(characters[rarity]), rarity
    return random.choice(characters['희귀']), '희귀'  # fallback

def simulate(n):
    results = []
    for _ in range(n):
        char, rarity = simulate_once()
        results.append((char, rarity))
    return results

st.title("세븐나이츠 합성 시뮬레이터")

# 버튼 UI
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("1회 합성"):
        results = simulate(1)
with col2:
    if st.button("10회 합성"):
        results = simulate(10)
with col3:
    if st.button("100회 합성"):
        results = simulate(100)

# 결과 출력
if 'results' in locals():
    st.subheader("결과")

    # 결과 정리
    count_by_rarity = Counter(rarity for _, rarity in results)
    sorted_rarities = ['구세나', '전설', '준전설', '희귀']

    # 보기 좋게 출력
    for rarity in sorted_rarities:
        entries = [char for char, r in results if r == rarity]
        if entries:
            st.markdown(f"**:<span style='color:{rarity_colors[rarity]}'>{rarity}</span>:** {len(entries)}개", unsafe_allow_html=True)
            st.write(', '.join(entries))

    # 시각화
    labels = [r for r in sorted_rarities if count_by_rarity[r] > 0]
    values = [count_by_rarity[r] for r in labels]
    colors = [rarity_colors[r] for r in labels]

    fig, ax = plt.subplots()
    ax.bar(labels, values, color=colors)
    ax.set_title("등급별 획득 수")
    st.pyplot(fig)
