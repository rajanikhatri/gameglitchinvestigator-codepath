import random
import sys
import os
import base64

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

import streamlit as st

st.set_page_config(page_title="Number Guesser", page_icon="🎯", layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 50%, #e0f2f1 100%);
}
[data-testid="column"]:first-child {
    background: linear-gradient(160deg, #ede9fe 0%, #ddd6fe 100%);
    border-radius: 14px;
    padding: 12px 10px;
}
[data-testid="column"]:last-child {
    background: linear-gradient(160deg, #ede9fe 0%, #ddd6fe 100%);
    border-radius: 14px;
    padding: 12px 10px;
}
.main-title {
    font-size: 2.4rem;
    font-weight: 900;
    color: #2d6a4f;
    text-align: center;
    margin-bottom: 4px;
}
.range-text {
    text-align: center;
    color: #555;
    font-size: 1rem;
    margin-bottom: 16px;
}
.range-highlight {
    color: #e76f51;
    font-weight: 700;
}
.circle-img {
    display: flex;
    justify-content: center;
    margin-bottom: 12px;
}
.circle-img img {
    width: 160px;
    height: 160px;
    border-radius: 50%;
    object-fit: cover;
    border: 4px solid #2d6a4f;
    box-shadow: 0 4px 16px rgba(45,106,79,0.2);
}
.badge-card {
    padding: 10px 14px;
    border-radius: 10px;
    margin: 6px 0;
    font-size: 0.9rem;
}
.badge-earned {
    background: #fff8e1;
    border-left: 4px solid #f4a261;
    color: #333;
    font-weight: 600;
}
.badge-locked {
    background: #f5f5f5;
    color: #bbb;
}
.section-title {
    font-size: 1.3rem;
    font-weight: 800;
    color: #2d6a4f;
    margin-bottom: 16px;
}
.leaderboard-row {
    display: flex;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid #e0e0e0;
    font-size: 0.95rem;
}
.pro-tip {
    background: #f0fdf4;
    border-left: 4px solid #52b788;
    border-radius: 10px;
    padding: 12px 16px;
    margin-top: 12px;
    font-size: 0.88rem;
    color: #555;
}
</style>
""", unsafe_allow_html=True)

# --- Config ---
attempt_limit_map = {"Easy": 8, "Normal": 6, "Hard": 4}
difficulty_options = ["Easy", "Normal", "Hard"]
diff_emojis = {"Easy": "🌸", "Normal": "🌺", "Hard": "🔥"}

# --- Session state ---
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Normal"

difficulty = st.session_state.difficulty
low, high = get_range_for_difficulty(difficulty)
attempt_limit = attempt_limit_map[difficulty]

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "status" not in st.session_state:
    st.session_state.status = "playing"
if "history" not in st.session_state:
    st.session_state.history = []
if "difficulty_prev" not in st.session_state:
    st.session_state.difficulty_prev = difficulty
if "player_name" not in st.session_state:
    st.session_state.player_name = "Guest Player"
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []
if "badges" not in st.session_state:
    st.session_state.badges = set()
if "show_left" not in st.session_state:
    st.session_state.show_left = True
if "show_right" not in st.session_state:
    st.session_state.show_right = True

# --- Reset game if difficulty changed ---
if st.session_state.difficulty_prev != difficulty:
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.difficulty_prev = difficulty

# --- Three column layout ---
left_w = 1.2 if st.session_state.show_left else 0.01
right_w = 1.2 if st.session_state.show_right else 0.01
left_col, main_col, right_col = st.columns([left_w, 2, right_w])

# =====================
# LEFT COLUMN
# =====================
with left_col:
    if st.button("«" if st.session_state.show_left else "»", key="toggle_left"):
        st.session_state.show_left = not st.session_state.show_left
        st.rerun()
    if st.session_state.show_left:
        st.markdown("### 🎯 Number Guesser")
        st.markdown("**Your Name**")
        player_name = st.text_input("", value=st.session_state.player_name,
                                    label_visibility="collapsed", key="name_input")
        st.session_state.player_name = player_name

        st.markdown("**Difficulty Level**")
        for d in difficulty_options:
            label = f"✅ {d}" if d == difficulty else d
            if st.button(label, key=f"diff_{d}", use_container_width=True):
                st.session_state.difficulty = d
                st.rerun()

        st.divider()
        st.markdown("**Difficulty Settings:**")
        st.markdown("🟠 **Easy:** 1-20 (8 tries)")
        st.markdown("🟠 **Normal:** 1-50 (6 tries)")
        st.markdown("🔴 **Hard:** 1-100 (4 tries)")

        st.markdown("""
        <div class="pro-tip">
            💡 <strong>Pro Tip!</strong><br>
            Higher difficulty gives more points when you win!
        </div>
        """, unsafe_allow_html=True)

        st.divider()
        st.markdown("**🔐 Developer Access**")
        debug_pass = st.text_input("Enter password:", type="password", key="debug_pass")
        if debug_pass == "debug123":
            st.success("Access granted!")
            st.write("Secret:", st.session_state.secret)
            st.write("Attempts:", st.session_state.attempts)
            st.write("Score:", st.session_state.score)
            st.write("Difficulty:", difficulty)
            st.write("History:", st.session_state.history)
        elif debug_pass:
            st.error("Wrong password.")

# =====================
# MAIN COLUMN
# =====================
with main_col:
    # Circular anime image
    anime_path = os.path.join(os.path.dirname(__file__), "luffy.png")
    if os.path.exists(anime_path):
        with open(anime_path, "rb") as f:
            img_data = base64.b64encode(f.read()).decode()
        st.markdown(
            f'<div class="circle-img"><img src="data:image/png;base64,{img_data}"/></div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown("<div style='text-align:center; font-size:5rem;'>🎯</div>",
                    unsafe_allow_html=True)

    st.markdown('<div class="main-title">Guess the Number!</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="range-text">Between '
        f'<span class="range-highlight">{low}</span> and '
        f'<span class="range-highlight">{high}</span></div>',
        unsafe_allow_html=True
    )

    # Reserve placeholders
    info_placeholder = st.empty()
    progress_placeholder = st.empty()
    input_container = st.container()
    button_container = st.container()

    with input_container:
        raw_guess = st.text_input(
            "",
            placeholder="Type your guess...",
            label_visibility="collapsed",
            key=f"guess_{difficulty}"
        )

    with button_container:
        col1, col2 = st.columns(2)
        with col1:
            submit = st.button("✨ Submit Guess ✨", use_container_width=True, type="primary")
        with col2:
            new_game = st.button("🔁 New Game", use_container_width=True)
        show_hint = st.checkbox("Show Hint", value=True)

    # Handle new game
    if new_game:
        st.session_state.attempts = 0
        st.session_state.secret = random.randint(low, high)
        st.session_state.status = "playing"
        st.session_state.history = []
        st.session_state.score = 0

    # Handle game status
    if st.session_state.status != "playing":
        if st.session_state.status == "won":
            st.success(f"🎉 You won! The secret was {st.session_state.secret}. Score: {st.session_state.score}")
        else:
            st.error(f"💀 Out of attempts! The secret was {st.session_state.secret}.")

    elif submit:
        st.session_state.attempts += 1
        ok, guess_int, err = parse_guess(raw_guess)

        if not ok:
            st.session_state.attempts -= 1
            st.error(err)
        elif guess_int < low or guess_int > high:
            st.session_state.attempts -= 1
            st.warning(f"Please enter a number between {low} and {high}.")
        else:
            st.session_state.history.append(guess_int)
            outcome, message = check_guess(guess_int, st.session_state.secret)

            if show_hint:
                if outcome == "Win":
                    st.success(message)
                elif outcome == "Too High":
                    st.error(message)
                else:
                    st.info(message)

            st.session_state.score = update_score(
                current_score=st.session_state.score,
                outcome=outcome,
                attempt_number=st.session_state.attempts,
            )

            if outcome == "Win":
                st.balloons()
                st.session_state.status = "won"
                if st.session_state.attempts == 1:
                    st.session_state.badges.add("First Try Master")
                if st.session_state.attempts <= 3:
                    st.session_state.badges.add("Quick Thinker")
                if difficulty == "Hard":
                    st.session_state.badges.add("Master Player")
                if st.session_state.attempts >= 5:
                    st.session_state.badges.add("Persistent Winner")
                st.session_state.leaderboard.append({
                    "name": st.session_state.player_name,
                    "score": st.session_state.score,
                    "attempts": st.session_state.attempts,
                    "difficulty": difficulty
                })
                st.session_state.leaderboard.sort(key=lambda x: x["score"], reverse=True)

            elif st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(f"💀 Out of attempts! The secret was {st.session_state.secret}.")

    # Fill placeholders after state update
    attempts_left = attempt_limit - st.session_state.attempts
    info_placeholder.markdown(
        f"**Attempts Left** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        f"**{attempts_left} / {attempt_limit}**"
    )
    progress_placeholder.progress(max(attempts_left / attempt_limit, 0.0))

# =====================
# RIGHT COLUMN
# =====================
with right_col:
    if st.button("»" if st.session_state.show_right else "«", key="toggle_right"):
        st.session_state.show_right = not st.session_state.show_right
        st.rerun()
    if st.session_state.show_right:
        st.markdown('<div class="section-title">🏆 Leaderboard</div>', unsafe_allow_html=True)
        if not st.session_state.leaderboard:
            st.markdown("""
            <div style="text-align:center; padding:20px;">
                <div style="font-size:2.5rem;">🏆</div>
                <p style="font-weight:600;">No scores yet!</p>
                <p style="color:#888; font-size:0.85rem;">Be the first to win.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
            for i, entry in enumerate(st.session_state.leaderboard[:5]):
                st.markdown(f"""
                <div class="leaderboard-row">
                    <span>{medals[i]} <strong>{entry['name']}</strong><br>
                    <small style="color:#888;">{entry['difficulty']}</small></span>
                    <span style="color:#2d6a4f; font-weight:700;">{entry['score']} pts</span>
                </div>
                """, unsafe_allow_html=True)

        st.divider()
        st.markdown('<div class="section-title">🏅 Badges</div>', unsafe_allow_html=True)
        all_badges = {
            "🎯 First Try Master": "Win on first attempt",
            "⚡ Quick Thinker": "Win in 3 attempts or less",
            "🏅 Master Player": "Win on Hard mode",
            "🥇 Persistent Winner": "Win after 5 or more guesses"
        }
        for badge, desc in all_badges.items():
            badge_name = " ".join(badge.split(" ")[1:])
            if badge_name in st.session_state.badges:
                st.markdown(
                    f'<div class="badge-card badge-earned">{badge}<br><small>{desc}</small></div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="badge-card badge-locked">{badge}<br><small>{desc}</small></div>',
                    unsafe_allow_html=True
                )
