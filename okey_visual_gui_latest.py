import streamlit as st
from collections import defaultdict
from typing import List, Dict, Tuple

COLORS = ['r', 'y', 'b']
ALL_CARDS = [f"{n}{c}" for c in COLORS for n in range(1, 9)]

# Hilfsfunktionen
def parse_card(card: str) -> Tuple[int, str]:
    return int(card[:-1]), card[-1]

def evaluate_card(card: str, hand: List[str], seen: List[str]) -> float:
    number, color = parse_card(card)
    partner_offsets = [-2, -1, 1, 2]
    potential_partners = [f"{number + o}{color}" for o in partner_offsets if 1 <= number + o <= 8]

    score = 0.0
    for partner in potential_partners:
        if partner in hand:
            score += 2.0
        elif partner not in seen:
            score += 1.0
    return score

def advise(hand: List[str], discarded: List[str], played: List[str]) -> Dict[str, float]:
    seen = set(hand + discarded + played)
    return {card: evaluate_card(card, hand, list(seen)) for card in hand}

# Streamlit GUI Setup
st.set_page_config(page_title="Okey Visual Deck", layout="centered")
st.title("🃏 Okey Deck Visualisierung & Empfehlung")

if 'active_hand' not in st.session_state:
    st.session_state.active_hand = []
if 'discarded' not in st.session_state:
    st.session_state.discarded = []
if 'removed' not in st.session_state:
    st.session_state.removed = []

st.subheader("🎴 Aktuelles Deck")
card_layout = {'b': 'Blau', 'y': 'Gelb', 'r': 'Rot'}
color_map = {'b': '#ADD8E6', 'y': '#FFFF99', 'r': '#FF9999', 'disabled': '#DDDDDD'}

for color in COLORS:
    st.markdown(f"**{card_layout[color]}**")
    row = st.columns(8)
    for i in range(1, 9):
        card = f"{i}{color}"
        used = card in st.session_state.active_hand or card in st.session_state.discarded or card in st.session_state.removed
        background = color_map['disabled'] if used else color_map[color]
        with row[i - 1]:
            st.markdown(f"""
            <div onclick="window.location.href='?add={card}'">
                <button style='width: 100%; padding: 0.5em; background-color: {background}; border: 1px solid #666; border-radius: 8px;'>
                    <strong style='color: black;'>{i}</strong>
                </button>
            </div>
            """, unsafe_allow_html=True)

query_params = st.query_params()
if 'add' in query_params:
    card_to_add = query_params['add'][0]
    if card_to_add not in st.session_state.active_hand and len(st.session_state.active_hand) < 5 and card_to_add not in st.session_state.removed:
        st.session_state.active_hand.append(card_to_add)
    st.query_params.clear()

st.markdown("---")

st.subheader("🖐️ Aktives Deck")
active_cols = st.columns(5)
for i in range(5):
    if i < len(st.session_state.active_hand):
        card = st.session_state.active_hand[i]
        num, col = parse_card(card)
        btn_color = color_map[col]
        with active_cols[i]:
            st.markdown(f"""
            <div style='background-color:{btn_color}; text-align:center; padding:0.5em; border-radius:10px; font-size:24px; font-weight:bold;'>
                <a href='?remove={card}' style='color:black; text-decoration:none'>{num}</a>
            </div>
            """, unsafe_allow_html=True)

query_params = st.query_params()
if 'remove' in query_params:
    card_to_remove = query_params['remove'][0]
    if card_to_remove in st.session_state.active_hand:
        st.session_state.active_hand.remove(card_to_remove)
        st.session_state.removed.append(card_to_remove)
    st.query_params.clear()

if len(st.session_state.active_hand) == 5:
    scores = advise(st.session_state.active_hand, st.session_state.discarded + st.session_state.removed, [])
    sorted_cards = sorted(scores.items(), key=lambda x: x[1])
    weakest = sorted_cards[0][0]
    num, col = parse_card(weakest)
    st.markdown("---")
    st.subheader("🔎 Empfehlung")
    st.markdown("**Wirf diese Karte ab:**")
    st.markdown(f"<div style='background-color:{color_map[col]}; text-align:center; padding:0.5em; border-radius:10px; font-size:24px; font-weight:bold;'>{num}</div>", unsafe_allow_html=True)

st.markdown("---")
if st.button("🔄 Zurücksetzen"):
    st.session_state.active_hand = []
    st.session_state.discarded = []
    st.session_state.removed = []
    st.rerun()