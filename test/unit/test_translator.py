from unittest.mock import patch
from src.translator import translate_content
from src.translator import get_language
from sentence_transformers import SentenceTransformer, util

# Chinese
def test_chinese():
    is_english, translated_content = translate_content("这是一条中文消息")
    assert is_english == False
    assert "Chinese" in translated_content
    assert eval_single_response_translation("This is a Chinese message", translated_content) > 0.8

# French
def test_french():
    is_english, translated_content = translate_content("Ceci est un message en français")
    assert is_english == False
    assert "French" in translated_content
    assert eval_single_response_translation("This is a message in French", translated_content) > 0.8

# LLM normal response
def test_llm_normal_response():
    is_english, translated_content = translate_content("This is an english message.")
    assert is_english == True
    assert "This is an english message." in translated_content

# LLM gibberish response
def test_llm_gibberish_response():
    is_english, translated_content = translate_content("asdkjhasd lkjhasd!!!")
    assert is_english == True
    assert "asdkjhasd lkjhasd!!!" in translated_content

# Multiple languages
def test_two_languages():
    is_english, translated_content = translate_content("你好我叫安娜贝尔我是 Nevermore 里的一个角色")
    print(f"is_english: {is_english}")
    assert is_english == False
    assert eval_single_response_translation("Hello my name is Annabelle. I am a character in Nevermore.", translated_content) > 0.8

def test_complicated_1():
    original_content = "In a quiet town where clocks all ticked in reverse, a girl named Elara discovered she could remember the future but forget the past. Each morning, she woke with vivid visions of what would happen that day—conversations not yet had, choices not yet made—but no recollection of who she was. One evening, while following a vision of meeting a boy with a blue kite, she found herself laughing like she used to, though she didn’t know why. As the kite danced in the sky and the boy smiled, something inside her whispered: This is home, and for the first time, she decided not to chase the next future—just to stay."
    is_english, translated_content = translate_content(original_content)
    assert is_english == True
    assert original_content == translated_content

def test_complicated_2():
    original_content = "En una ciutat tranquil·la on els rellotges marcaven al revés, una noia anomenada Elara va descobrir que podia recordar el futur però oblidar el passat. Cada matí, es despertava amb visions vívides del que passaria aquell dia: converses encara no tingudes, eleccions encara no preses, però sense record de qui era. Un vespre, mentre seguia la visió de conèixer un noi amb un estel blau, es va trobar rient com abans, encara que no sabia per què. Mentre l'estel ballava al cel i el nen somreia, alguna cosa dins d'ella va xiuxiuejar: Aquesta és casa i, per primera vegada, va decidir no perseguir el proper futur, només quedar-se."
    intended_translation = "In a quiet town where clocks all ticked in reverse, a girl named Elara discovered she could remember the future but forget the past. Each morning, she woke with vivid visions of what would happen that day—conversations not yet had, choices not yet made—but no recollection of who she was. One evening, while following a vision of meeting a boy with a blue kite, she found herself laughing like she used to, though she didn’t know why. As the kite danced in the sky and the boy smiled, something inside her whispered: This is home, and for the first time, she decided not to chase the next future—just to stay."
    is_english, translated_content = translate_content(original_content)
    assert is_english == False
    assert get_language(original_content) == "Catalan"
    print(eval_single_response_translation(intended_translation, translated_content))
    assert eval_single_response_translation(intended_translation, translated_content) > 0.8

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

######################## testing translation accuracy #########################
def eval_single_response_translation(expected_answer: str, llm_response: str) -> float:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embedding1 = model.encode([expected_answer])
    embedding2 = model.encode([llm_response])
    similarities = model.similarity(embedding1, embedding2)
    return similarities[0][0]

####################### Mock tests ###########################################
@patch("src.translator.translate_content")
def test_mock_llm_normal_response(mock_translate_content):
    # Mock the model's response to return a normal English message
    mock_translate_content.return_value = (True, "This is an English message.")
    is_english, translated_content = translate_content("This is an English message.")
    assert is_english == True
    assert translated_content == "This is an English message."

@patch("src.translator.translate_content")
def test_mock_llm_gibberish_response(mock_translate_content):
    # Mock the model's response to return gibberish
    mock_translate_content.return_value = (True, "asdkjhasd lkjhasd!!!")
    is_english, translated_content = translate_content("asdkjhasd lkjhasd!!!")
    assert is_english == True
    assert translated_content == "asdkjhasd lkjhasd!!!"

@patch("src.translator.translate_content")
def test_mock_llm_empty_input(mock_translate_content):
    # Mock the model's response to handle empty input
    mock_translate_content.return_value = (True, "")
    is_english, translated_content = translate_content("")
    assert is_english == True
    assert translated_content == ""

@patch("src.translator.translate_content")
def test_mock_llm_numeric_input(mock_translate_content):
    # Mock the model's response to handle numeric input
    mock_translate_content.return_value = (True, "12345")
    is_english, translated_content = translate_content("12345")
    assert is_english == True
    assert translated_content == "12345"

@patch("src.translator.translate_content")
def test_mock_llm_special_characters(mock_translate_content):
    # Mock the model's response to handle special characters
    mock_translate_content.return_value = (True, "!@#$%^&*()")
    is_english, translated_content = translate_content("!@#$%^&*()")
    assert is_english == True
    assert translated_content == "!@#$%^&*()"
