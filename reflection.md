# 💭 Reflection: Game Glitch Investigator

## 1. What was broken when you started?

When I first ran the game, it was impossible to win even when I knew the secret number from the Developer Debug Info panel. The hints were completely backwards. When my guess was too high, it said "Go Higher" which sent me further away from the answer. On top of that, every even-numbered click (2nd, 4th, 6th...) the game secretly broke because the secret number was being turned into text, which Python could not compare to my number guess. When I clicked "New Game", the game did not fully reset either. It blocked me from playing again without refreshing the whole page.

## 2. How did you use AI as a teammate?

I used Claude and ChatGPT on this project. I would play the game, notice something was wrong, and describe what I saw to Claude. Claude would then look at the code, confirm if it was really a bug, and explain why it was happening. One example where this worked well: I noticed the hints were backwards and told Claude. Claude looked at the code, confirmed the messages were swapped, and helped me fix it. I verified it by running the game and checking that "Go Lower" showed when my guess was too high. One example where the first suggestion didn't fully work: Claude tried to fix the attempts counter not syncing by using a math trick to add 1 when the button was clicked. It partially worked but the debug panel was still wrong. I described the problem again and we asked ChatGPT, which gave a better solution using placeholders.

## 3. Debugging and testing your fixes

I checked if a bug was fixed by restarting the app and testing that exact situation manually. For example, after fixing the hints, I used the Developer Debug Info to see the secret number and then guessed higher and lower on purpose to check that the hints pointed the right way. I also ran `pytest` in the terminal after moving the logic to `logic_utils.py`. All 3 tests passed, which confirmed that `check_guess()` correctly returned "Win", "Too High", and "Too Low" for the right inputs. Claude helped me understand what the tests were checking and why they were failing at first (the tests expected just a string like `"Win"` but the function returned a tuple like `("Win", "🎉 Correct!")`).

## 4. What did you learn about Streamlit and state?

In the original app, the secret number kept changing because it was not saved anywhere permanent. Every time you clicked a button, Streamlit reran the whole script from the top, and the secret number got picked randomly again. Think of Streamlit like a whiteboard that gets erased and redrawn every time someone clicks anything. `st.session_state` is like a sticky note on the side of the whiteboard. It survives the erase. The fix that gave the game a stable secret number was wrapping it in `if "secret" not in st.session_state`, so it only picks a new number the very first time and keeps the same one after that.

## 5. Looking ahead: your developer habits

One habit I want to reuse is checking the Developer Debug Info while playing. Having a way to see hidden values while testing made it much easier to spot bugs. Next time I work with AI on a coding task, I would ask it to explain what the code does before asking it to change anything, so I understand what I am changing and why. This project changed the way I think about AI code because I learned that AI can write code that looks correct but has hidden bugs. You always need to actually run it, test it, and read it carefully before trusting it.
