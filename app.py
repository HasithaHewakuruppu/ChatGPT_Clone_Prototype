import streamlit as st
import openai
import os

# Retrieve the OpenAI API key from environment variables
openai.api_key = os.environ.get('OPENAI_API_KEY')
if not openai.api_key:
    st.error("API key is missing! Set the OPENAI_API_KEY environment variable.")
    st.stop()

def ask_gpt3(prompt):
    """Send a prompt to ChatGPT 3.5 and get the response."""
    # Add the new user message to the session state
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages  # Use the full message history
    )
    # Append the model's reply to the session state
    reply = response['choices'][0]['message']['content']
    st.session_state.messages.append({"role": "system", "content": reply})
    
    return reply

# Check if 'messages' is already in the session state
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

st.title('GPT-3.5 Streamlit Chat Interface')

# Display chat history
for message in st.session_state.messages:
    if message['role'] == 'user':
        st.write(f"You: {message['content']}")
    else:
        st.write(f"GPT-3.5: {message['content']}")

user_prompt = st.text_input("Ask GPT-3.5 something:", "")
if user_prompt:
    response = ask_gpt3(user_prompt)
    st.write(f"GPT-3.5: {response}")
