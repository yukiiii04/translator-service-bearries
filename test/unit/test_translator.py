from src.translator import translate_content

# Chinese
def test_chinese():
    is_english, translated_content = translate_content("这是一条中文消息")
    assert is_english == False
    assert "Chinese" in translated_content

# French
def test_french():
    is_english, translated_content = translate_content("Ceci est un message en français")
    assert is_english == False
    assert "French" in translated_content

# English
def test_english():
    is_english, translated_content = translate_content("This is an English message")
    assert is_english == True
    assert "English" in translated_content

# LLM normal response
def test_llm_normal_response():
    is_english, translated_content = translate_content("This is an english message.")
    assert is_english == True
    print(translated_content)
    assert translated_content == "This is an english message."

# LLM gibberish response
def test_llm_gibberish_response():
    is_english, translated_content = translate_content("asdkjhasd lkjhasd!!!")
    assert is_english == True
    assert translated_content == "asdkjhasd lkjhasd!!!"
