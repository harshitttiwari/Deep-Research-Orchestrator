# Deep Research Orchestrator 🔍

A powerful AI-driven research assistant built with Streamlit and LangChain that intelligently gathers information from multiple sources to provide comprehensive research responses.

## 🌟 Features

- **Multi-Source Research**: Combines web search, Wikipedia, and file saving capabilities
- **Interactive UI**: Clean Streamlit interface for easy interaction
- **Smart Agent**: Uses Groq's GPT-OSS-120B model with tool-calling capabilities
- **Source Attribution**: Automatically provides sources and tools used for transparency
- **Session Memory**: Remembers previous queries within the session
- **Research Export**: Save research outputs to text files with timestamps

## 🛠️ Tools Integrated

1. **Web Search**: DuckDuckGo search for real-time web information
2. **Wikipedia**: Access to Wikipedia's vast knowledge base
3. **File Saver**: Export research findings to timestamped text files

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Groq API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/harshitttiwari/Deep-Research-Orchestrator.git
   cd Deep-Research-Orchestrator
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .\.venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up configuration**
   Create a `config.py` file with your API keys:
   ```python
   GROQ_API_KEY = "your_groq_api_key_here"
   google_api_key = "your_google_api_key_here"  # Optional
   ```

5. **Run the application**
   ```bash
   streamlit run streamleat.py
   ```

## 💻 Usage

1. **Start the application** and navigate to `http://localhost:8501`
2. **Enter your research question** in the input field
3. **Submit** and watch the agent gather information from multiple sources
4. **View results** with clear source attribution and tools used
5. **Access previous answers** by typing "previous answer" or similar phrases
6. **Export research** - findings are automatically formatted and can be saved

### Example Queries

- "What are the latest developments in quantum computing?"
- "Explain the impact of artificial intelligence on healthcare"
- "Research the history and benefits of renewable energy"
- "What are the current trends in cybersecurity?"

## 🏗️ Architecture

```
Deep Research Orchestrator/
├── streamleat.py          # Main Streamlit application
├── tools.py              # Tool definitions (search, wiki, save)
├── config.py             # API keys configuration
├── requirements.txt      # Python dependencies
├── main.py              # Alternative entry point
└── README.md            # This file
```

### Core Components

- **LangChain Agent**: Orchestrates tool usage and reasoning
- **Groq LLM**: Powers the conversational AI with GPT-OSS-120B
- **Custom Tools**: Specialized functions for research tasks
- **Streamlit UI**: Interactive web interface

## 🔧 Configuration

### Environment Variables

The application supports configuration through `config.py`:

```python
# Required
GROQ_API_KEY = "your_groq_api_key"

# Optional
google_api_key = "your_google_api_key"
```

### Agent Settings

- **Max Iterations**: 10 (prevents infinite loops)
- **Verbose Mode**: Enabled for debugging
- **Model**: OpenAI GPT-OSS-120B via Groq

## 📊 Output Format

The agent provides structured responses with:

- **Main Answer**: Comprehensive research findings
- **Sources**: URLs and references with proper attribution
- **Tools Used**: Transparency on which tools were utilized
- **Timestamp**: When using the save feature

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🛟 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/harshitttiwari/Deep-Research-Orchestrator/issues) page
2. Create a new issue with detailed information
3. Provide error logs and steps to reproduce

## 🔮 Roadmap

- [ ] Add more research sources (arXiv, PubMed, etc.)
- [ ] Implement citation formatting options
- [ ] Add research paper generation templates
- [ ] Include data visualization capabilities
- [ ] Multi-language support

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) for the agent framework
- [Streamlit](https://streamlit.io/) for the UI framework
- [Groq](https://groq.com/) for the LLM API
- [DuckDuckGo](https://duckduckgo.com/) for search capabilities
- [Wikipedia](https://wikipedia.org/) for knowledge base access

---

**Built with ❤️ by [Harshit Tiwari](https://github.com/harshitttiwari)**