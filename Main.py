import os
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse
from openai import OpenAI

# Load OpenAI key from environment
OPENAI_KEY = os.environ.get("OPENAI_KEY")

if not OPENAI_KEY:
    raise Exception("OPENAI_KEY is not set in environment variables")

client = OpenAI(api_key=OPENAI_KEY)

app = Flask(__name__)

# Kannada AI Doctor system prompt
SYSTEM_PROMPT = """
ನೀವು ಒಂದು ವೈದ್ಯ ಸಹಾಯಕ AI. ನಿಮ್ಮ ಹೆಸರು Junior Doctor.
ನೀವು ರೋಗಿಗಳೊಂದಿಗೆ ವಿನಯವಾಗಿ, ಸರಳವಾಗಿ ಮತ್ತು ಸ್ಪಷ್ಟವಾಗಿ ಮಾತನಾಡಬೇಕು.

ನಿಮ್ಮ ಕೆಲಸ:
- ರೋಗಿಯನ್ನು ಸ್ವಾಗತಿಸಿ
- ಅವರ ಆರೋಗ್ಯದ ಬಗ್ಗೆ ಪ್ರಶ್ನೆ ಕೇಳಿ
- ಫಾಲೋಅಪ್ ದಿನಾಂಕ ನೆನಪಿಸಿ
- ಡಾಕ್ಟರ್ ಲಭ್ಯವಿಲ್ಲದಿದ್ದರೆ ಮರುನಿಯೋಜನೆ ನೀಡಿ

ತುರ್ತು ಪರಿಸ್ಥಿತಿ ಕಂಡುಬಂದರೆ:
"ದಯವಿಟ್ಟು ತಕ್ಷಣ ಹತ್ತಿರದ ಆಸ್ಪತ್ರೆಗೆ ಭೇಟಿ ನೀಡಿ ಅಥವಾ 112 ಗೆ ಕರೆ ಮಾಡಿ"
ಎಂದು ಹೇಳಿ.

ಸರಳ ಕನ್ನಡದಲ್ಲಿ ಮಾತನಾಡಿ.
"""

@app.route("/voice", methods=["POST"])
def voice():
    user_input = request.form.get("SpeechResult", "")

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )

    ai_text = response.choices[0].message.content

    twilio_response = VoiceResponse()
    twilio_response.say(ai_text, voice="alice", language="kn-IN")

    return Response(str(twilio_response), mimetype="text/xml")

@app.route("/")
def home():
    return "Junior Doctor Kannada AI is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
