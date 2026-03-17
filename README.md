# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip3 install -r requirements.txt`
2. Run the broken app: `python3 -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
  - The game is a number guessing game where the app picks a secret number and you try to guess it within a limited number of attempts.
  - After each guess, the app gives a hint to guide you higher or lower.

- [x] Detail which bugs you found.
  - **Bug 1 (Logic Bug — Backwards Hints):** The `check_guess()` function had the hint messages swapped. When the player's guess was higher than the secret number, the app showed "Go HIGHER" (which would push the player further away). When the guess was lower, it showed "Go LOWER" (also wrong). This made it impossible to follow the hints and win.
  - **Bug 2 (Type Bug — String Conversion on Even Attempts):** Inside the submit block, the code checked `if st.session_state.attempts % 2 == 0` and converted the secret number to a string on every even-numbered attempt (2nd, 4th, 6th click). This caused a `TypeError` when Python tried to compare an integer guess to a string secret. The game would fall into the `except TypeError` block in `check_guess()`, where the hints were also still backwards. So on even attempts, both the comparison and the hints were broken.
  - **Bug 3 (State Bug — New Game Button Not Fully Resetting):** When the "New Game" button was clicked, it only reset `attempts` and `secret`. It did NOT reset `status`, `history`, or `score`. Since `status` was still set to `"won"` or `"lost"` from the previous game, the app would immediately hit `st.stop()` and block the submit button, making it impossible to play again without refreshing the entire page.

- [x] Explain what fixes you applied.
  - **Bug 1:** The problem was in the `check_guess()` function — the messages were simply put in the wrong place. When your guess is too high, you need to go lower, and vice versa. The fix was to swap the two messages so each one appears in the correct condition.
  - **Bug 2:** The code was intentionally converting the secret number from an integer to a string on every 2nd, 4th, and 6th attempt. Python cannot compare a number and a string directly, so it crashed silently into broken behavior. The fix was to remove that conversion entirely so the secret always stays as a number — which is what it should have been from the start.
  - **Bug 3:** The "New Game" button was only resetting two things (attempts and secret) but forgetting to reset the game's status, score, and guess history. Because the status was still "won" or "lost", the app would immediately stop and block the player. The fix was to also reset `status` back to `"playing"`, clear the `history` list, and reset the `score` to 0 — so everything starts fresh like a real new game.

## 📸 Demo

- [ ] [Insert a screenshot of your fixed, winning game here]

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
