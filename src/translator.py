import openai
import os

client = openai.OpenAI(
    api_key=os.getenv("NODEBB_API_KEY")  # Your OpenAI API key
)

def get_translation(post: str) -> str:
    context = "Provide the English translation of the given text which may or may not be written in English, using the following format.\n"\
              "Given text: Hier ist dein erstes Beispiel.\n"\
              "Here is your first example.\n"\
              "If it cannot be translated, return the original text\n" # Insert context
    response = client.chat.completions.create(
      model="gpt-4o-mini",  # model name
      messages=[
          {
            "role": "system",
            "content": context
          },
          {
              "role": "user",
              "content": post
          }
        ]
      )
    return response.choices[0].message.content.strip()

def get_language(post: str) -> str:
    context = "Provide in English, only the name of the language the given text is written in, using the following format.\n"\
              "Given text: Hier ist dein erstes Beispiel.\n"\
              "German\n"\
              "If it is gibberish, return 'English'\n"\
            #   "If it cannot be translated, return --ERROR--\n" # Insert context
    response = client.chat.completions.create(
      model="gpt-4o-mini",  # model name
      messages=[
          {
            "role": "system",
            "content": context
          },
          {
              "role": "user",
              "content": post
          }
        ]
      )
    return response.choices[0].message.content.strip()

def translate_content(content: str) -> tuple[bool, str]:
    language = get_language(content).strip()
    translation = get_translation(content).strip()
    if language != "English":
        return (False, translation)
    return ("English" in language, translation)