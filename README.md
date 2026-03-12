ConvoLens 🔍
AI-Powered Conversation Analyzer
ConvoLens analyzes customer service, sales, or support conversations using AI — detecting tone, identifying communication breakdowns, rating agent performance, and suggesting specific improvements.
Built with Python, OpenAI GPT, and Streamlit.

🎯 What It Does
Paste any conversation transcript and ConvoLens will instantly tell you:

Overall Sentiment — Is the conversation positive, negative, or neutral?
Tone Analysis — How does each speaker come across?
Breakdown Detection — Where exactly did communication go wrong?
Agent Performance Score — How well did the agent handle the situation? (1–10)
Improvement Suggestions — Specific, actionable ways the conversation could have gone better


💡 Why I Built This
I study both Computer Science and Mass Communication — and I've always been fascinated by how AI handles human language. Most AI tools can generate text, but fewer can analyze how people actually talk to each other and why those conversations succeed or fail.
ConvoLens sits at that intersection: it uses LLM technology to do what a communication analyst would do — read between the lines, spot friction, and suggest better approaches.
This is directly relevant to companies building AI agents for customer support, sales, and communication — where the quality of conversations drives real business outcomes.

🛠️ Tech Stack
ToolPurposePythonCore languageOpenAI GPT-4oConversation analysis engineStreamlitWeb interfacepython-dotenvEnvironment variable management

🚀 Getting Started
1. Clone the repo
bashgit clone https://github.com/Damola-png/convolens.git
cd convolens
2. Create a virtual environment
bashpython -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
3. Install dependencies
bashpip install -r requirements.txt
4. Add your OpenAI API key
Create a .env file in the root folder:
OPENAI_API_KEY=your-api-key-here
5. Run the app
bashstreamlit run app.py

📸 Demo

App opens in your browser at http://localhost:8501

Paste a conversation like this:
Customer: I've been waiting 3 days for my order and no one has responded to my emails.
Agent: Sorry to hear that. What's your order number?
Customer: It's #45231. This is really frustrating.
Agent: I'll look into it.
Customer: That's what the last agent said too.
ConvoLens will analyze it and return a full breakdown with scores and suggestions.

📁 Project Structure
convolens/
├── app.py              # Streamlit frontend
├── analyzer.py         # OpenAI analysis logic
├── requirements.txt    # Dependencies
├── .env                # API key (not committed)
├── .gitignore          # Ignores .env and venv
└── README.md           # This file

🔮 Future Features

 Upload .txt or .csv conversation files
 Side-by-side comparison of multiple conversations
 Export analysis as PDF report
 Support for multiple languages


👤 Author
Adedamola Olayefun
CS & Mass Communication Student — Principia College
