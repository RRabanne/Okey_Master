import streamlit as st
from collections import defaultdict
from typing import List, Dict, Tuple

COLORS = ['r', 'y', 'b']
ALL_CARDS = {f"{n}{c}" for c in COLORS for n in range(1, 9)}

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

st.set_page_config(page_title="Okey Kartenberater", layout="centered")
st.title("🃏 Okey Kartenberater (mit Wahrscheinlichkeit)")

st.markdown("""
Wähle deine aktuelle Handkarten und optional Karten, die du bereits **abgelegt** oder **gespielt** hast.
Der Algorithmus bewertet jede Karte anhand ihrer Kombinationsmöglichkeiten und der verbleibenden Chancen.
""")

hand = st.multiselect("🖐️ Deine Hand (5 Karten)", sorted(ALL_CARDS), max_selections=5)
discarded = st.multiselect("🗑️ Bereits abgelegte Karten", sorted(ALL_CARDS))
played = st.multiselect("✅ Bereits gespielte Kombinationen", sorted(ALL_CARDS))

if len(hand) == 5:
    scores = advise(hand, discarded, played)
    sorted_cards = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    st.subheader("📊 Kartenbewertung")
    for card, score in sorted_cards:
        st.write(f"{card}: Score {score:.2f}")

    weakest = sorted_cards[-1][0]
    st.markdown(f"### 🗑️ **Empfehlung:** Wirf **{weakest}** weg (niedrigster Score)")

    st.subheader("🔍 Visualisierung")
    st.bar_chart({k: v for k, v in scores.items()})
else:
    st.info("Bitte genau 5 Karten auswählen, um eine Empfehlung zu erhalten.")
