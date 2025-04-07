from src.translator import translate_content
from src.translator import get_language

# # Chinese
# def test_chinese():
#     is_english, translated_content = translate_content("这是一条中文消息")
#     assert is_english == False
#     print(translated_content)
#     assert "Chinese" in translated_content

# # French
# def test_french():
#     is_english, translated_content = translate_content("Ceci est un message en français")
#     assert is_english == False
#     print(translated_content)
#     assert "French" in translated_content

# # English
# def test_english():
#     is_english, translated_content = translate_content("This is an English message")
#     assert is_english == True
#     assert "English" in translated_content

# # LLM normal response
# def test_llm_normal_response():
#     is_english, translated_content = translate_content("This is an english message.")
#     assert is_english == True
#     print(translated_content)
#     assert "This is an english message." in translated_content

# # LLM gibberish response
# def test_llm_gibberish_response():
#     is_english, translated_content = translate_content("asdkjhasd lkjhasd!!!")
#     assert is_english == True
#     print(translated_content)
#     assert "asdkjhasd lkjhasd!!!" in translated_content

# Multiple languages
def test_two_languages():
    is_english, translated_content = translate_content("你好我叫安娜贝尔我是 Nevermore 里的一个角色")
    print(f"is_english: {is_english}")
    print(translated_content)
    assert is_english == False

######################## Test our get_language function ########################
def test_languages():
    assert get_language("我很喜欢吃意大利面") == "Chinese"
    assert get_language("Me gusta mucho comer pasta.") == "Spanish"
    assert get_language("I really like eating pasta") == "English"
    assert get_language("Labai mėgstu valgyti makaronus") == "Lithuanian"
    assert get_language("Nagyon szeretek tésztát enni") == "Hungarian"
    assert get_language("Më pëlqen shumë të ha makarona") == "Albanian"
    assert get_language("Runtii waxaan jeclahay cunista baasto") == "Somali"
    assert get_language("ຂ້ອຍມັກກິນ") == "Lao"
    assert get_language("Makemake au e ʻai i ka pāpaʻi") == "Hawaiian"
    assert get_language("Ik hou heel veel van pasta eten") == "Dutch"
    assert get_language("ང་དངོས་གནས་པ་སྟ་ཟ་རྒྱུར་དགའ།") == "Tibetan"
    assert get_language("ฉันชอบกินพาสต้ามาก") == "Thai"
    assert get_language("Мен макарон жегенді қатты жақсы көремін") == "Kazakh"
    assert get_language("M'agrada molt menjar pasta") == "Catalan"

