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
      The game is a number guessing game where the app picks a secret number and you try to guess it within a limited number of attempts. After each guess, the app gives a hint to guide you higher or lower.

- [x] Detail which bugs you found.
      Bug 1 (Logic Bug): The hints were backwards — "Go HIGHER" appeared when the guess was too high, and "Go LOWER" when the guess was too low.
      Bug 2 (Type Bug): On every even-numbered attempt, the secret number was converted to a string, causing a TypeError when comparing it to the integer guess. This made the game behave inconsistently.

- [x] Explain what fixes you applied.
      Bug 1: Swapped the hint messages in `check_guess()` in `app.py` so "Go LOWER" shows when the guess is too high and "Go HIGHER" shows when the guess is too low.
      Bug 2: Removed the even/odd attempt check that was converting the secret to a string. The secret is now always compared as an integer.

## 📸 Demo

- [ ] [Insert a screenshot of your fixed, winning game here]

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
