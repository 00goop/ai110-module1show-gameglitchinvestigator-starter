# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game, it looked like a simple number-guessing UI built in Streamlit, but it was completely unwinnable. The most obvious bug was that the hints were **backwards** — when my guess was too high, the game told me to "Go HIGHER," and when too low it said "Go LOWER," sending me in the wrong direction every time. On top of that, the secret number was being converted to a string on even-numbered attempts, so even if I guessed the exact number, the comparison `42 == "42"` would fail in Python and never register as a win. I also noticed that the difficulty ranges were wrong (Hard mode used 1–50, which is actually easier than Normal's 1–100), and the attempt counter started at 1 instead of 0, giving players one fewer guess than advertised.

---

## 2. How did you use AI as a teammate?

I used an AI coding assistant (Antigravity / Gemini-based) to help me analyze the starter code and identify all the planted bugs systematically. One example of a **correct** AI suggestion was identifying the secret-type coercion bug on lines 158–161 of the original `app.py` — the AI pointed out that `str(secret)` would cause `int == str` comparisons to fail, and removing the coercion fixed the issue immediately; I verified by playing the game and winning on the first correct guess. One **misleading** moment was when I initially assumed the `update_score` even-attempt bonus (+5 on "Too High") might have been an intentional game mechanic rather than a bug — the AI flagged it as a bug, and after reading the assignment instructions more carefully I agreed, since the behavior was inconsistent and confusing to the player.

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed by writing a targeted pytest case and confirming it passed, then also manually playing the game in Streamlit to double-check the user-facing behavior. For example, I wrote `test_guess_too_high` which calls `check_guess(60, 50)` and asserts the outcome is `"Too High"` and the message contains `"LOWER"` — before my fix this would have failed because the original code had the hints swapped. The AI helped me design the test structure by suggesting I organize tests into classes by function (`TestCheckGuess`, `TestParseGuess`, etc.) and include edge cases like off-by-one guesses and the minimum score clamp, which made the test suite much more thorough than if I'd only tested the happy path.

---

## 4. What did you learn about Streamlit and state?

Streamlit works differently from most web frameworks because it **reruns your entire Python script from top to bottom** every time the user interacts with any widget (clicking a button, typing in a text box, etc.). This means that any regular Python variable defined at the top of the script gets reset to its initial value on every rerun — so if you write `secret = random.randint(1, 100)` at the top level, you get a brand-new secret number every time you click "Submit." The solution is `st.session_state`, which is a special dictionary that persists across reruns — by writing `st.session_state.secret = random.randint(...)` *only once* (inside an `if "secret" not in st.session_state` guard), the value sticks around until you explicitly change it.

---

## 5. Looking ahead: your developer habits

One habit I want to reuse is **writing tests immediately after fixing a bug** — not waiting until the end — because it forced me to think precisely about what "correct" behavior looks like and saved me from accidentally re-introducing bugs later when I refactored the code into `logic_utils.py`. Next time I work with AI on a coding task, I would **read through the AI's suggestions more critically before accepting them**, especially for logic that looks plausible but might have subtle off-by-one errors or type mismatches. This project changed the way I think about AI-generated code by showing me that AI can write code that *looks* clean and professional but still contains sneaky bugs — the lesson is that AI is a powerful first-draft tool, but human review and testing are absolutely essential.
