import google.generativeai as genai

# Configure API Key
genai.configure(
    api_key="AIzaSyBQ9edSuR8QvmQL21L-BM0_NFUm8DpZPIQ"
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