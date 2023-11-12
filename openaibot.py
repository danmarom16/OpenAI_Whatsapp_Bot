import openai
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os

app = Flask(__name__)                                           # Creating Server
load_dotenv()                                                   # Load api_key from .env for enhanced security
openai.api_key = os.getenv("OPENAI_API_KEY")                    # Load Openai's api key from environment variables.


def get_chatgpt_response(prompt):
    """ Get a text prompt from user
    
    Parameters
    __________
    prompt: str
        The prompt user would like to ask chatGPT.

    Returns
    _______
    ChatGPT's response.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = [
            {"role": "user", "content": prompt}
        ]
    )
    print(response)
    return response.choices[0].message['content']


def get_dalle_response(prompt):
    """ Get a text prompt from user asking for image
    
    Parameters
    __________
    prompt: str
        The prompt user would like to ask Dalle.

    Returns
    _______
    Dalle's response.
    """

    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return response['data'][0]['url']   # Load image from Dalle's URL.


@app.route("/webhook", methods=["POST"])
def webhook():
    """ Send a text to user when a webhook is activated.
    
    Returns
    _______
    str(twilo_response)
        The string Text message that will be sent to the user.
    """
    incoming_message = request.values.get("Body", "").lower()
    twilo_response = MessagingResponse()

    if "create ai art" in incoming_message:
        image_url = get_dalle_response(incoming_message)
        twilo_response.message("Here is your image").media(image_url)
    else:
        chatGPT_response = get_chatgpt_response(incoming_message)
        twilo_response.message(chatGPT_response)

    return str(twilo_response)


if __name__ == "__main__":
    app.run(debug=True)
