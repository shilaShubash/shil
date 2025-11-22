import streamlit as st
import google.generativeai as genai
import os
from typing import List, TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langgraph.graph import StateGraph, END


#System Prompt

PROMPT_FILE_PATH = "system_prompt.txt"

@st.cache_data 
def load_prompt(file_path):
    if not os.path.exists(file_path):
        st.error(f"Critical error: Prompt file not found at '{file_path}'")
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        st.error(f"Error reading prompt file '{file_path}': {e}")
        return None

HARDCODED_SYSTEM_PROMPT = load_prompt(PROMPT_FILE_PATH)

if not HARDCODED_SYSTEM_PROMPT:
    st.stop() 

DB_DIR = "db_chroma" 

#Application Page Settings
st.set_page_config(page_title="LLM2LLL Customizable Mentor", page_icon="None")

#API Key Configuration
ACTUAL_API_KEY = os.environ.get("GOOGLE_API_KEY_FOR_APP") 
if not ACTUAL_API_KEY:
    st.error("Critical error: Google API key (GOOGLE_API_KEY_FOR_APP) is missing...")
    st.stop() 
try:
    genai.configure(api_key=ACTUAL_API_KEY)
except Exception as e:
    st.error(f"Critical error: Error configuring the Google GenAI API: {e}")
    st.stop() 



@st.cache_resource
def get_tools():
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=ACTUAL_API_KEY)

        vector_store = Chroma(
            persist_directory=DB_DIR, 
            embedding_function=embeddings,
            collection_name="my_collection"
        )

        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        return llm, retriever

    except Exception as e:
        st.error(f"Error initializing tools (Failed to load ChromaDB): {e}")
        st.error(f"Full path being checked: {os.path.abspath(DB_DIR)}")
        st.error(f"Files in current directory: {os.listdir('.')}")
        return None, None

llm, retriever = get_tools()
if not llm or not retriever:
    st.stop()

#LangGraph
class GraphState(TypedDict):
    question: str
    documents: List[Document]
    answer: str

#Nodes
def retrieve_node(state: GraphState):
    question = state["question"]
    documents = retriever.invoke(question)
    return {"documents": documents, "question": question}

def generate_rag_node(state: GraphState):
    question = state["question"]
    documents = state["documents"]
    
    rag_prompt_template = f'''
    {HARDCODED_SYSTEM_PROMPT}
    Based on the following context documents, please answer the user's question.
    If the context does not contain the answer, state that clearly.
    CONTEXT:
    ---
    {{context}}
    ---
    QUESTION: {{question}}
    '''
    prompt = ChatPromptTemplate.from_template(rag_prompt_template)
    context_str = "\n\n".join([doc.page_content for doc in documents])
    rag_chain = prompt | llm | StrOutputParser()
    answer = rag_chain.invoke({"context": context_str, "question": question})
    return {"answer": answer}

def fallback_node(state: GraphState):
    question = state["question"]
    fallback_prompt_template = f'''
    {HARDCODED_SYSTEM_PROMPT}
    The user asked: "{question}"
    I could not find a relevant answer in my document library.
    Please respond, letting them know the information is not available in the documents.
    '''
    prompt = ChatPromptTemplate.from_template(fallback_prompt_template)
    fallback_chain = prompt | llm | StrOutputParser()
    answer = fallback_chain.invoke({})
    return {"answer": answer}


class RelevanceGrader(BaseModel):
    relevant: str = Field(description="Is the document relevant? 'yes' or 'no'.")

def grade_node(state: GraphState):
    question = state["question"]
    documents = state["documents"]
    
    if not documents:
        return "no"
    structured_llm_grader = llm.with_structured_output(RelevanceGrader)
    grader_prompt_template = '''
    Are the following context documents relevant for answering the user's question?
    Respond 'yes' or 'no'.
    CONTEXT: --- {context} ---
    QUESTION: {question}
    '''
    prompt = ChatPromptTemplate.from_template(grader_prompt_template)
    context_str = "\n\n".join([doc.page_content for doc in documents])
    chain = prompt | structured_llm_grader
    try:
        grade = chain.invoke({"context": context_str, "question": question})
        return grade.relevant
    except Exception:
        return "no"

def decide_edge(state: GraphState):
    relevance = grade_node(state)
    if relevance == "yes":
        return "generate_rag"
    else:
        return "fallback"

@st.cache_resource
def build_graph():
    workflow = StateGraph(GraphState)
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("generate_rag", generate_rag_node)
    workflow.add_node("fallback", fallback_node)
    workflow.set_entry_point("retrieve")
    workflow.add_conditional_edges("retrieve", decide_edge, {"generate_rag": "generate_rag", "fallback": "fallback"})
    workflow.add_edge("generate_rag", END)
    workflow.add_edge("fallback", END)
    return workflow.compile()

app_graph = build_graph()

# Streamlit
st.title("LLM2LLL") 
st.markdown("Welcome! This chat provides mentoring and guidance for occupational therapists.") 

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]): 
        st.markdown(message["content"])

if user_input := st.chat_input("Type your question here..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"): 
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Retrieving, grading, and thinking"):
            inputs = {"question": user_input}
            response = app_graph.invoke(inputs, config={"recursion_limit": 5})
            response_text = response.get("answer", "An error occurred.")
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})