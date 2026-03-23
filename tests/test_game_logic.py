import pytest
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score


# ── get_range_for_difficulty ──────────────────────────────────────────

class TestGetRange:
    def test_easy(self):
        assert get_range_for_difficulty("Easy") == (1, 20)

    def test_normal(self):
        assert get_range_for_difficulty("Normal") == (1, 100)

    def test_hard(self):
        assert get_range_for_difficulty("Hard") == (1, 500)

    def test_unknown_defaults_to_normal(self):
        assert get_range_for_difficulty("Extreme") == (1, 100)


# ── parse_guess ───────────────────────────────────────────────────────

class TestParseGuess:
    def test_valid_integer(self):
        ok, val, err = parse_guess("42")
        assert ok is True
        assert val == 42
        assert err is None

    def test_float_string_truncated(self):
        ok, val, err = parse_guess("3.7")
        assert ok is True
        assert val == 3

    def test_empty_string(self):
        ok, val, err = parse_guess("")
        assert ok is False
        assert val is None
        assert err == "Enter a guess."

    def test_none_input(self):
        ok, val, err = parse_guess(None)
        assert ok is False
        assert err == "Enter a guess."

    def test_non_numeric(self):
        ok, val, err = parse_guess("abc")
        assert ok is False
        assert err == "That is not a number."


# ── check_guess ───────────────────────────────────────────────────────

class TestCheckGuess:
    def test_winning_guess(self):
        outcome, msg = check_guess(50, 50)
        assert outcome == "Win"

    def test_guess_too_high(self):
        outcome, msg = check_guess(60, 50)
        assert outcome == "Too High"
        assert "LOWER" in msg

    def test_guess_too_low(self):
        outcome, msg = check_guess(40, 50)
        assert outcome == "Too Low"
        assert "HIGHER" in msg

    def test_edge_off_by_one_high(self):
        outcome, _ = check_guess(51, 50)
        assert outcome == "Too High"

    def test_edge_off_by_one_low(self):
        outcome, _ = check_guess(49, 50)
        assert outcome == "Too Low"


# ── update_score ──────────────────────────────────────────────────────

class TestUpdateScore:
    def test_win_first_attempt(self):
        # 100 - 10*1 = 90
        assert update_score(0, "Win", 1) == 90

    def test_win_later_attempt(self):
        # 100 - 10*5 = 50
        assert update_score(0, "Win", 5) == 50

    def test_win_minimum_points(self):
        # 100 - 10*15 = -50 → clamped to 10
        assert update_score(0, "Win", 15) == 10

    def test_wrong_guess_deducts(self):
        assert update_score(50, "Too High", 1) == 45
        assert update_score(50, "Too Low", 2) == 45

    def test_score_accumulates(self):
        score = 0
        score = update_score(score, "Too High", 1)   # -5 → -5
        score = update_score(score, "Too Low", 2)     # -5 → -10
        score = update_score(score, "Win", 3)          # +70 → 60
        assert score == 60
