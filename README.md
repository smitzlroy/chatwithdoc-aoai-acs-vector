#Azure OpenAI Document Chat
This application uses Azure Form Recognizer, Azure Storage, Azure Cognitive Search, and Azure OpenAI's GPT-3 and embedding models to enable users to chat with their documents. The application is built using Streamlit and orchestrated with LanhChain.

##Features
Upload multiple PDF documents
Process and chunk the text within the documents
Vectorize the chunks using OpenAI's GPT-3 model
Store the vectors in Azure Cognitive Search
Retrieve relevant document chunks in response to user queries, using a chat interface
Prerequisites
You need Python 3.6 or later to run this application. You can have multiple Python versions (2.x and 3.x) installed on the same system without problems.

In Ubuntu, you can install Python 3 like this:

arduino
Copy code
sudo apt-get install python3 python3-pip
Quick Start
Clone the repository:

bash
Copy code
git clone https://github.com/<your-repo>/ai-document-chat.git
cd ai-document-chat
Install dependencies:

Copy code
pip install -r requirements.txt
Run the application:

arduino
Copy code
streamlit run app.py
Application Structure
app.py: The main application file that you run.
.env: The file for storing your environment variables, such as Azure credentials.
Environment Variables
Before you run the application, you need to set the following environment variables:

OPENAI_API_BASE: Your OpenAI API base URL.
OPENAI_API_KEY: Your OpenAI API key.
OPENAI_API_VERSION: Your OpenAI API version.
AZURE_COGNITIVE_SEARCH_SERVICE_NAME: Your Azure Cognitive Search service name.
AZURE_COGNITIVE_SEARCH_API_KEY: Your Azure Cognitive Search API key.
FORM_RECOGNIZER_ENDPOINT: Your Azure Form Recognizer endpoint.
FORM_RECOGNIZER_KEY: Your Azure Form Recognizer key.
AZURE_STORAGE_CONNECTION_STRING: Your Azure Storage connection string.
AZURE_STORAGE_CONTAINER: Your Azure Storage container name.
You can set these variables in your .env file.

Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

License
This project is licensed under the terms of the MIT license.
