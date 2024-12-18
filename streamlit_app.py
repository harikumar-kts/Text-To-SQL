import streamlit as st
import requests

# Set the URL for the FastAPI backend
API_URL = "http://localhost:8000/predict/"

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []  # List to store chat history

# Title of the app
st.title("Chat with TPMS Chatbot")

# Function to interact with FastAPI
def get_chatbot_response(user_message):
    response = requests.post(API_URL, json={"question": user_message})
    if response.status_code == 200:
        return response.json().get("response")
    else:
        return "Sorry, there was an error."

# Chat input box
with st.form(key="chat_form"):
    user_input = st.text_input("What do you want to know?", key="user_input")
    submit_button = st.form_submit_button(label="Send")

# If the user submits a message
if submit_button and user_input:
    # Append user message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get bot response and append to session state
    bot_response = get_chatbot_response(user_input)
    st.session_state.messages.append({"role": "bot", "content": bot_response})

# Display the conversation history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.write(f"**You:** {message['content']}")
    elif message["role"] == "bot":
        st.write(f"**Bot:** {message['content']}")
