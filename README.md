# Azure OpenAI Document Chat
Generated with AI:
This application uses Azure Form Recognizer, Azure Storage, Azure Cognitive Search, and Azure OpenAI's GPT-3 and embedding models to enable users to chat with their documents. The application is built using Streamlit and orchestrated with LanhChain.

## Features
Upload multiple PDF documents
Process and chunk the text within the documents
Vectorize the chunks using OpenAI's GPT-3 model
Store the vectors in Azure Cognitive Search
Retrieve relevant document chunks in response to user queries, using a chat interface

## Prerequisites
* You need Python 3.6 or later to run this application. You can have multiple Python versions (2.x and 3.x) installed on the same system without problems.
* Azure OpenAI service with deployment of models
* Azure Cognitive Search Service (for Form Recogniser API)
* Azure Storage Account


## install Packages

`pip install -r requirements.txt`

## Run the app

`streamlit run app.py`

Once the streamlit page opens you can upload your PDF file and click "process your docs" to kick off the process of:

- Azure Form recogniser extracting text from PDF
- LangChain chunking file (configurable in the app.py)
- LangChain using Azure OpenAI model "text-embedding-ada-002" to add embeddings to chunked docs
- LangChain creating the vectorstore in Azure Cognitive Search and storing vectors
- Now you can ask questions of your docs in the text window

## Update your .env 

OPENAI_API_BASE: Your OpenAI API base URL 

OPENAI_API_KEY: Your OpenAI API key 

OPENAI_API_VERSION: Your OpenAI API version 

AZURE_COGNITIVE_SEARCH_SERVICE_NAME: Your Azure Cognitive Search service name 

AZURE_COGNITIVE_SEARCH_API_KEY: Your Azure Cognitive Search API key 

FORM_RECOGNIZER_ENDPOINT: Your Azure Form Recognizer endpoint 

FORM_RECOGNIZER_KEY: Your Azure Form Recognizer key 

AZURE_STORAGE_CONNECTION_STRING: Your Azure Storage connection string 

AZURE_STORAGE_CONTAINER: Your Azure Storage container name 



