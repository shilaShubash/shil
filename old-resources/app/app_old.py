
import streamlit as st
import google.generativeai as genai
import os

# --- Application Page Settings ---
st.set_page_config(page_title="LLM2LLL Customizable Mentor", page_icon=None)

# --- Default System Prompt ---
DEFAULT_SYSTEM_PROMPT = "You are an experienced mentor for occupational therapists. You must provide professional, supportive and Short answers. Use clear and respectful language."

# --- Model Loading Function (cached based on system_instruction) ---
@st.cache_resource
def get_generative_model(system_instruction_payload):
    # st.sidebar.write(f"DEBUG: Loading/Re-initializing model with system prompt: {system_instruction_payload[:50]}...") # Optional debug
    try:
        model = genai.GenerativeModel(
            model_name = "models/gemini-2.5-flash",
            system_instruction=system_instruction_payload
        )
        return model
    except Exception as e:
        st.error(f"Error creating GenerativeModel with the provided system prompt: {e}")
        return None

# --- API Key Configuration ---
ACTUAL_API_KEY = os.environ.get("GOOGLE_API_KEY_FOR_APP")

if not ACTUAL_API_KEY:
    st.error("Critical error: Google API key (GOOGLE_API_KEY_FOR_APP) is missing from environment secrets.")
    st.caption("Please ensure you have correctly set this secret in your deployment platform. The application cannot proceed.")
    st.stop() 

try:
    genai.configure(api_key=ACTUAL_API_KEY)
except Exception as e:
    st.error(f"Critical error: Error configuring the Google GenAI API with the provided key: {e}")
    st.caption("This might indicate an invalid API key or a problem with the Google Cloud project.")
    st.stop() 

# --- Initialize Session State Variables (if not already present) ---
if "system_prompt_for_chat" not in st.session_state:
    st.session_state.system_prompt_for_chat = DEFAULT_SYSTEM_PROMPT
if "active_reminder_phrase" not in st.session_state:
    st.session_state.active_reminder_phrase = "" # Default to no reminder
if "user_turn_count" not in st.session_state:
    st.session_state.user_turn_count = 0
if "messages" not in st.session_state:
    st.session_state.messages = []


# --- Sidebar ---
st.sidebar.header("Mentor Configuration")
custom_system_prompt_from_sidebar = st.sidebar.text_area(
    "Define the mentor's main behavior (System Prompt):",
    value=st.session_state.system_prompt_for_chat, 
    height=250,
    key="system_prompt_input_widget" 
)

if st.sidebar.button("Apply New System Prompt & Restart Chat"):
    if custom_system_prompt_from_sidebar != st.session_state.system_prompt_for_chat:
        st.session_state.system_prompt_for_chat = custom_system_prompt_from_sidebar
        st.session_state.messages = []  
        if "chat_session" in st.session_state:
            del st.session_state.chat_session  
        st.session_state.user_turn_count = 0 # Reset turn counter
        st.sidebar.success("System prompt updated! Chat has been reset.")
        st.rerun()  
    else:
        st.sidebar.info("System prompt is the same as the current one. No changes applied.")

st.sidebar.markdown("---") 

# New section for custom reminder phrase
st.sidebar.header("In-Chat Reminder Phrase")
reminder_phrase_input = st.sidebar.text_input(
    "Short reminder to inject periodically (leave blank for none):",
    value=st.session_state.active_reminder_phrase,
    key="reminder_phrase_widget"
)

if st.sidebar.button("Update Reminder Phrase"):
    if reminder_phrase_input != st.session_state.active_reminder_phrase:
        st.session_state.active_reminder_phrase = reminder_phrase_input
        st.sidebar.success("Reminder phrase updated!")
        # No need to rerun or reset chat for this, it will be picked up on next applicable turn
    else:
        st.sidebar.info("Reminder phrase is the same. No changes applied.")


# --- Load Model (based on the main system prompt) ---
model = get_generative_model(st.session_state.system_prompt_for_chat)

if not model:
    st.error("Failed to load/initialize the generative model. Application cannot proceed.")
    st.stop() 

# --- Chat Session Initialization ---
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
    if not st.session_state.get("messages"): 
         st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]


# --- Main Application UI ---
st.title("LLM2LLL") 
st.markdown("Welcome! This chat provides mentoring, guidance, and advice for occupational therapists. You can customize the mentor's behavior and reminders using the sidebar.") 
st.caption("Powered by Gemini 2.5 Flash")

# --- Displaying Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]): 
        st.markdown(message["content"])

# --- Getting User Input and Processing It ---
if user_input_from_chat := st.chat_input("Type your question here..."):
    st.session_state.user_turn_count += 1

    st.session_state.messages.append({"role": "user", "content": user_input_from_chat})
    with st.chat_message("user"): 
        st.markdown(user_input_from_chat)

    if "chat_session" in st.session_state: 
        try:
            chat_session_to_use = st.session_state.chat_session
            
            prompt_to_send_to_llm = user_input_from_chat 
            
            # --- Conditionally augment prompt with CUSTOM reminder phrase ---
            active_reminder = st.session_state.get("active_reminder_phrase", "") # Get custom reminder
            REMINDER_FREQUENCY = 3 
            if active_reminder and st.session_state.user_turn_count % REMINDER_FREQUENCY == 0:
                # Using the custom reminder phrase now
                prompt_to_send_to_llm = f"Reminder: '{active_reminder}'. Now, please address the user's message: '{user_input_from_chat}'"
                # st.sidebar.caption(f"Custom reminder injected (Turn {st.session_state.user_turn_count}).")
            
            model_response = chat_session_to_use.send_message(prompt_to_send_to_llm)
            response_text = model_response.text

            st.session_state.messages.append({"role": "assistant", "content": response_text})
            with st.chat_message("assistant"): 
                st.markdown(response_text)

        except Exception as e:
            error_for_display = f"Oops, an error occurred while communicating with the model: {e}"
            st.session_state.messages.append({"role": "assistant", "content": error_for_display})
            with st.chat_message("assistant"): 
                st.error(error_for_display)
            st.toast(f"Error: {e}")
    else:
        st.error("Chat session is not initialized. Please ensure the model and system prompt are correctly configured.")