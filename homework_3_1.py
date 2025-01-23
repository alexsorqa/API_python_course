def test_phrase_generator():
    phrase = input("Set a phrase: ")
    assert len(phrase) < 15, f"The phrase should be less then 15 characters long, but have {len(phrase)} instead."