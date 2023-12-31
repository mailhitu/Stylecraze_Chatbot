import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template

#streamlit run app.py

def get_pdf_text(pdf_path):
    text = ""
    #for pdf in pdf_docs:
    pdf_file = open(pdf_path, 'rb')
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
        text +=page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
        )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()#This Embedding process involves a cost (very minimal but does involve cost)
    #embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl") #locally creates embedding whihc is free but will be very slow
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    load_dotenv()
    st.set_page_config(page_title="StyleCraze Chatbot", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    if "rawtext" not in st.session_state:
        st.session_state.rawtext = None

    
    st.header("Chat with Stylecraze bot ") #Chat with multiple PDFs :books:
    user_question = st.text_input("Ask a question to bot")#Ask a question about your document:
    if user_question:
        handle_userinput(user_question)

    st.write(user_template.replace("{{MSG}}", "Hello robot"), unsafe_allow_html=True)
    st.write(bot_template.replace("{{MSG}}", "Hello human"), unsafe_allow_html=True)
    
    with st.sidebar:
        st.subheader("Your documents")
        #pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        #if st.button("Process"):
        if st.session_state.rawtext == None:
            with st.spinner("Processing"):
            # get the pdf text
        
                pdf_file_path = 'merged_content.pdf'
                raw_text = get_pdf_text(pdf_file_path)
                st.session_state.rawtext = raw_text
                #st.write(raw_text)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)
                #st.write(text_chunks)

                # create vector store 
                vectorstore = get_vectorstore(text_chunks)

                # Create conversation chain and maintain in session sate of UI app (streamlit)
                st.session_state.conversation = get_conversation_chain(vectorstore) #It will take history of conversations and will return the next elemnt in conversation
    
if __name__=='__main__':
    main()