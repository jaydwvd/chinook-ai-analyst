# 🕵️‍♂️ Chinook AI Analyst

A Text-to-SQL chatbot that allows you to talk to your database in plain English. Built with **Streamlit**, **LangChain**, and **OpenAI**.

## 🚀 Features
* **Natural Language Queries**: Ask questions like "Who are the top 5 artists?" without writing SQL.
* **AI-Powered**: Uses GPT-4o-mini to intelligently generate complex SQL queries (Joins, Aggregations, Filtering).
* **Auto-Recovery**: If the AI writes a bad query, it reads the error and fixes itself automatically.
* **Chat History**: Remembers your conversation context.
* **Secure**: Your API Key is handled securely via the sidebar or environment variables.

## 🛠️ Installation & Setup

### 1. Clone the repository
```bash
git clone [https://github.com/your-username/chinook-ai-analyst.git](https://github.com/your-username/chinook-ai-analyst.git)
cd chinook-ai-analyst

2. Install Dependencies
Make sure you have Python installed, then run:

Bash
pip install -r requirements.txt
3. Run the App
Bash
streamlit run app.py
The app will automatically open in your browser at http://localhost:8501.

🔑 Configuration
You need an OpenAI API Key to run this app.

Run the app.

Enter your key in the Sidebar when prompted.

(Optional) For local development, you can set it in your environment:

Bash
export OPENAI_API_KEY="sk-..."
📂 Project Structure
app.py: The main application code containing the Streamlit interface and LangChain logic.

requirements.txt: List of Python libraries required to run the app.

Chinook.db: The SQLite sample database (automatically downloaded on first run if missing).

🤖 Technologies Used
Frontend: Streamlit

LLM Orchestration: LangChain

Model: OpenAI GPT-4o-mini

Database: SQLite (Chinook Sample DB)

📝 Example Questions to Ask
"Show me the top 5 countries by total invoice sales."

"Who is the support agent for customer 'Bjørn Hansen'?"

"List all tracks by AC/DC."

"Which genre has the longest average track length?"
