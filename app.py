import os
import streamlit as st
from dotenv import load_dotenv
from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient, BlobClient
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.azuresearch import AzureSearch
from langchain.chat_models import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores.base import Document

# Load environment variables
load_dotenv()

# Azure OpenAI configurations
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_VERSION"] = os.getenv("OPENAI_API_VERSION")
model = "text-embedding-ada-002"

# Azure Search configurations
vector_store_address = os.getenv("AZURE_COGNITIVE_SEARCH_SERVICE_NAME")
vector_store_password = os.getenv("AZURE_COGNITIVE_SEARCH_API_KEY")

# Azure Storage configurations
azure_storage_connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
azure_storage_container = os.getenv("AZURE_STORAGE_CONTAINER")

def upload_to_azure_storage(file):
    blob_service_client = BlobServiceClient.from_connection_string(azure_storage_connection_string)
    blob_client = blob_service_client.get_blob_client(azure_storage_container, file.name)

    blob_client.upload_blob(file, blob_type="BlockBlob")

def download_from_azure_storage(filename):
    blob_service_client = BlobServiceClient.from_connection_string(azure_storage_connection_string)
    blob_client = blob_service_client.get_blob_client(azure_storage_container, filename)

    download_stream = blob_client.download_blob()
    return download_stream.readall()

def get_pdf_text(form_recognizer_client, pdf_docs):
    text = ""
    for pdf in pdf_docs:
        poller = form_recognizer_client.begin_recognize_content(pdf)
        result = poller.result()

        for page in result:
            for line in page.lines:
                text += " ".join([word.text for word in line.words]) + "\n"
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    docs = [Document(page_content=chunk) for chunk in chunks]
    return docs

def get_vectorstore(documents):
    embeddings = OpenAIEmbeddings(deployment=model, chunk_size=1)
    vectorstore = AzureSearch(
        azure_search_endpoint=vector_store_address,
        azure_search_key=vector_store_password,
        index_name="langchain-vector-demo",
        embedding_function=embeddings.embed_query,
    )
    vectorstore.add_documents(documents=documents)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = AzureChatOpenAI(deployment_name="gpt-35-turbo")
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
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
        if i % 2 == 0:  # user's message
            st.write(f"User: {message.content}")
        else:  # bot's message
            st.write(f"Bot: {message.content}")

def main():
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon=":file_folder:")
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with your documents :file_folder:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process Your Docs' which will prepare your app", accept_multiple_files=True, type=['pdf'])
        if st.button("Process Your Docs"):
            with st.spinner("Processing..."):
                form_recognizer_endpoint = os.getenv("FORM_RECOGNIZER_ENDPOINT")
                form_recognizer_api_key = os.getenv("FORM_RECOGNIZER_KEY")
                form_recognizer_client = FormRecognizerClient(form_recognizer_endpoint, AzureKeyCredential(form_recognizer_api_key))

                # Upload files to Azure storage and download them back
                azure_pdf_docs = []
                for pdf_doc in pdf_docs:
                    upload_to_azure_storage(pdf_doc)
                    azure_pdf_doc = download_from_azure_storage(pdf_doc.name)
                    azure_pdf_docs.append(azure_pdf_doc)

                st.write("PDF files uploaded to Azure Storage and returned for processing...")

                # get pdf text
                raw_text = get_pdf_text(form_recognizer_client, azure_pdf_docs)
                st.write("Azure Form Recogniser extracted text from your PDF...")

                # get the text chunks
                documents = get_text_chunks(raw_text)
                st.write("Text split into chunks...")

                # create vector store
                vectorstore = get_vectorstore(documents)
                st.write("Azure Cog Search Vectorstore created...")

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)
                st.write("Conversation chain created...")

if __name__ == '__main__':
    main()
