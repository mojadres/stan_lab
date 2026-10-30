import random
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Chinese Character Reading Quiz",
    page_icon="漢",
    layout="centered",
)

DATA_FILE = Path(__file__).parent / "characters.csv"


@st.cache_data
def load_vocabulary():
    """Load the character and pinyin pairs bundled with the application."""
    data = pd.read_csv(DATA_FILE, dtype=str).dropna()
    data["character"] = data["character"].str.strip()
    data["pinyin"] = data["pinyin"].str.strip()
    data = data[
        (data["character"] != "")
        & (data["pinyin"] != "")
    ].drop_duplicates()

    # Group readings by character so polyphonic characters are handled correctly.
    vocabulary = (
        data.groupby("character")["pinyin"]
        .apply(list)
        .to_dict()
    )
    all_readings = sorted(set(data["pinyin"].tolist()))

    if len(all_readings) < 4:
        raise ValueError("The bundled vocabulary needs at least four distinct readings.")

    return vocabulary, all_readings


def make_question():
    character = random.choice(list(st.session_state.vocabulary.keys()))
    accepted_readings = st.session_state.vocabulary[character]
    correct_reading = random.choice(accepted_readings)

    # Exclude every reading belonging to this character, so only one choice
    # can be correct for the character shown.
    distractors_pool = [
        reading for reading in st.session_state.all_readings
        if reading not in accepted_readings
    ]
    choices = random.sample(distractors_pool, 3) + [correct_reading]
    random.shuffle(choices)

    st.session_state.character = character
    st.session_state.correct_reading = correct_reading
    st.session_state.choices = choices


def start_game():
    st.session_state.score = 0
    st.session_state.attempts_left = 3
    st.session_state.game_over = False
    st.session_state.quit = False
    st.session_state.game_started = True
    st.session_state.feedback = None
    make_question()


def submit_answer():
    selected = st.session_state.get("answer_choice")
    if not selected:
        st.session_state.feedback = ("warning", "Please select an answer first.")
        return

    if selected == st.session_state.correct_reading:
        st.session_state.score += 1
        feedback = ("success", "Correct! You scored one point.")
    else:
        st.session_state.attempts_left -= 1
        feedback = (
            "error",
            f"Incorrect. The correct reading was **{st.session_state.correct_reading}**. "
            "You lose one attempt."
        )

    if st.session_state.attempts_left <= 0:
        st.session_state.game_over = True
    else:
        make_question()

    st.session_state.feedback = feedback


st.title("漢 Chinese Character Reading Quiz")
st.write("Choose the correct pinyin reading for each Chinese character.")

try:
    vocabulary, all_readings = load_vocabulary()
except Exception as exc:
    st.error(f"Could not load the bundled vocabulary: {exc}")
    st.stop()

st.caption(
    f"Vocabulary: {len(vocabulary):,} characters · "
    f"{len(all_readings):,} distinct pinyin readings"
)

if not st.session_state.get("game_started", False):
    st.write("You have three attempts. Each correct answer earns one point.")
    st.button("Start game", type="primary", on_click=start_game)
    st.stop()

score_col, attempts_col = st.columns(2)
score_col.metric("Score", st.session_state.score)
attempts_col.metric("Attempts left", st.session_state.attempts_left)

if st.session_state.get("feedback"):
    kind, message = st.session_state.feedback
    if kind == "success":
        st.success(message)
    elif kind == "error":
        st.error(message)
    else:
        st.warning(message)

if st.session_state.game_over or st.session_state.quit:
    if st.session_state.quit:
        st.info("You quit the game.")
    else:
        st.error("Game over — you have used all three attempts.")

    st.subheader(f"Final score: {st.session_state.score}")
    st.button("Play again", type="primary", on_click=start_game)
    st.stop()

st.divider()
st.subheader("What is the correct reading?")
st.markdown(
    f"""
    <div style="
        font-size: 112px;
        text-align: center;
        line-height: 1.5;
        padding: 18px;
        font-family: 'Noto Sans CJK SC', 'Microsoft YaHei', sans-serif;
    ">{st.session_state.character}</div>
    """,
    unsafe_allow_html=True,
)

with st.form("answer_form"):
    st.radio(
        "Select one of the four readings:",
        options=st.session_state.choices,
        index=None,
        key="answer_choice",
    )
    st.form_submit_button(
        "Go",
        type="primary",
        use_container_width=True,
        on_click=submit_answer,
    )

st.divider()
if st.button("Quit", use_container_width=True):
    st.session_state.quit = True
    st.rerun()
