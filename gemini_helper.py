import google.generativeai as genai

# Configure API Key
genai.configure(
    api_key="AIzaSyBoONMQqilWpj3Ecs3-ipXAZZAIf3RIn6U"
)

# Load Latest Gemini Model
model = genai.GenerativeModel(
    "models/gemini-2.5-flash"
)

def ask_ai(question):

    response = model.generate_content(
        question
    )

    return response.text