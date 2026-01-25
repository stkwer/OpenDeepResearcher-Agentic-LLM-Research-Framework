# 🧠 OpenDeepResearcher

An agentic LLM research assistant that automatically conducts comprehensive research on any topic using a three-agent pipeline.

## 🏗️ Architecture

The system uses three specialized AI agents working in sequence:

1. **Planner Agent** - Breaks down research topics into focused sub-questions
2. **Search Agent** - Retrieves relevant information using Tavily search API
3. **Writer Agent** - Synthesizes findings into structured reports

## 🚀 Features

- **Automated Research Pipeline**: End-to-end research automation
- **Multi-Agent System**: Specialized agents for planning, searching, and writing
- **Web Interface**: Clean Streamlit UI with search history
- **Local LLM Support**: Works with LM Studio for privacy
- **Structured Output**: Professional research reports with clear sections

## 📋 Prerequisites

1. **LM Studio** running locally on port 1234
2. **Tavily API Key** for web search capabilities
3. **Python 3.8+**

## 🛠️ Installation

1. Clone or download the project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your `.env` file:
   ```
   TAVILY_API_KEY=your_tavily_api_key_here
   ```git remote remove origin
git remote add origin git@github.com:SRIKRISHNAPRIYAS/OpenDeepResearcher-Agentic-LLM-Research-Framework.git
git remote -v


4. Start LM Studio with a model (recommended: qwen2.5-7b-instruct)

## 🎯 Usage

### Web Interface (Recommended)
```bash
streamlit run app.py
```

### Command Line Interface
```bash
python main.py
```

## 🔧 Configuration

### LLM Settings
- **Base URL**: `http://127.0.0.1:1234/v1`
- **Model**: `qwen2.5-7b-instruct`
- **API Key**: `lm-studio` (placeholder)

### Search Settings
- **Max Results**: 2 per sub-question
- **Content Length**: 350 characters per snippet
- **Timeout**: 5 seconds per search

### Research Parameters
- **Sub-questions**: 8 per topic
- **Search Depth**: Basic
- **Output Format**: Structured markdown

## 📁 Project Structure

```
PROJECT/
├── app.py              # Streamlit web interface
├── main.py             # Command line interface
├── graph/
│   └── research_graph.py  # Main research pipeline
├── planner.py          # Planner agent
├── search.py           # Search agent  
├── writer.py           # Writer agent
├── test_llm.py         # LLM connection test
├── .env                # Environment variables
└── requirements.txt    # Dependencies
```

## 🔍 How It Works

1. **Input**: User provides a research topic
2. **Planning**: Planner agent generates 8 focused sub-questions
3. **Search**: Search agent finds relevant information for each sub-question
4. **Writing**: Writer agent creates a structured research report
5. **Output**: Professional report with introduction, sections, and conclusion

## 🎨 Example Topics

- "Impact of Artificial Intelligence in Healthcare"
- "Blockchain Technology in Supply Chain Management"
- "Climate Change Effects on Global Agriculture"
- "Quantum Computing Applications in Cryptography"

## 🔒 Privacy & Security

- Uses local LLM (LM Studio) for processing
- Only search queries sent to external APIs
- No sensitive data stored remotely
- Full control over data processing

## 🛡️ Error Handling

- Graceful search timeout handling
- Fallback content for failed searches
- Input validation and sanitization
- Session state management

## 📊 Performance

- **Average Research Time**: 30-60 seconds
- **Sub-questions Generated**: 8 per topic
- **Sources Retrieved**: 16 total (2 per sub-question)
- **Report Length**: 500-1000 words

## 🔧 Troubleshooting

### LM Studio Connection Issues
1. Ensure LM Studio is running on port 1234
2. Check if model is loaded
3. Verify base URL in code

### Tavily API Issues
1. Check API key in `.env` file
2. Verify internet connection
3. Check API rate limits

### Streamlit Issues
1. Update Streamlit: `pip install --upgrade streamlit`
2. Clear browser cache
3. Restart the application

## 🚀 Future Enhancements

- [ ] Multiple LLM provider support
- [ ] Advanced search filters
- [ ] Export formats (PDF, DOCX)
- [ ] Research templates
- [ ] Collaborative features
- [ ] API endpoints
- [ ] Database integration

## 📄 License

Open source - feel free to modify and distribute.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

---

**Built with ❤️ using LangChain, Streamlit, and Tavily**
