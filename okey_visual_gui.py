
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

st.subheader("🎴 Aktuelles Deck")
card_layout = {'b': 'Blau', 'y': 'Gelb', 'r': 'Rot'}
color_map = {'b': '#ADD8E6', 'y': '#FFFF99', 'r': '#FF9999', 'disabled': '#DDDDDD'}

cols = st.columns(8)
for color in COLORS:
    st.markdown(f"**{card_layout[color]}**")
    row = st.columns(8)
    for i in range(1, 9):
        card = f"{i}{color}"
        used = card in st.session_state.active_hand or card in st.session_state.discarded
        btn_color = color_map['disabled'] if used else color_map[color]
        with row[i-1]:
            if st.button(f"{i}", key=f"{card}_deck", disabled=used):
                if len(st.session_state.active_hand) < 5:
                    st.session_state.active_hand.append(card)

st.markdown("---")

st.subheader("🖐️ Aktives Deck")
active_cols = st.columns(5)
for i in range(5):
    if i < len(st.session_state.active_hand):
        card = st.session_state.active_hand[i]
        num, col = parse_card(card)
        btn_color = color_map[col]
        with active_cols[i]:
            if st.button(f"{num}", key=f"{card}_hand", help="Zum Entfernen klicken"):
                st.session_state.active_hand.remove(card)
    else:
        with active_cols[i]:
            st.empty()

# Empfehlung anzeigen, sobald 5 Karten aktiv
if len(st.session_state.active_hand) == 5:
    scores = advise(st.session_state.active_hand, st.session_state.discarded, [])
    sorted_cards = sorted(scores.items(), key=lambda x: x[1])
    weakest = sorted_cards[0][0]
    num, col = parse_card(weakest)
    st.markdown("---")
    st.subheader("🔎 Empfehlung")
    st.markdown(f"**Wirf diese Karte ab:**")
    st.markdown(f"<div style='background-color:{color_map[col]}; text-align:center; padding:0.5em; border-radius:10px; font-size:24px; font-weight:bold;'>{num}</div>", unsafe_allow_html=True)

# Reset-Knopf
st.markdown("---")
if st.button("🔄 Zurücksetzen"):
    st.session_state.active_hand = []
    st.session_state.discarded = []
    st.experimental_rerun()
