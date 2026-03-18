from logic_utils import check_guess, parse_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"

# --- Edge Case Tests ---

def test_non_numeric_string():
    # Typing letters like "abc" should fail parsing and return an error
    ok, guess_int, err = parse_guess("abc")
    assert ok == False
    assert guess_int is None
    assert err == "That is not a number."

def test_empty_input():
    # Submitting an empty string should fail and ask the player to enter a guess
    ok, guess_int, err = parse_guess("")
    assert ok == False
    assert guess_int is None
    assert err == "Enter a guess."

def test_negative_number():
    # Negative numbers should parse successfully as integers
    ok, guess_int, _ = parse_guess("-5")
    assert ok == True
    assert guess_int == -5

def test_decimal_input():
    # A decimal like "7.9" should be accepted and truncated to 7
    ok, guess_int, _ = parse_guess("7.9")
    assert ok == True
    assert guess_int == 7

def test_none_input():
    # None input (no value at all) should fail gracefully
    ok, _, err = parse_guess(None)
    assert ok == False
    assert err == "Enter a guess."
