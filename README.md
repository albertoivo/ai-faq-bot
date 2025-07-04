# AI FAQ BOT API

## 🤖 Description

The **AI FAQ Bot** is an intelligent API that uses **semantic search** and **natural language processing** to find the best answers in FAQ systems. Through OpenAI embeddings and similarity algorithms, the bot understands the context of user questions and returns relevant answers, even when the question is not identical to those in the FAQ.

## 💡 Motivation

The creation of this project arose from the need to make FAQ systems more intelligent and efficient. Traditionally, FAQs depend on exact text matches, which limits the user experience. With this bot:

- **🎯 Semantic Search**: Finds relevant answers even with different words
- **🌍 Multilingual**: Automatically detects language (Portuguese/English)
- **🤝 Friendly Answers**: Uses AI to make answers more conversational
- **⚡ Fast and Efficient**: Smart caching for better performance
- **🔗 Flexible**: Works with any FAQ hosted online

## 🌟 Different Implementations

This project offers two different approaches to serve various use cases:

### 📡 Branch `main` - Versatile API
**Ideal for**: Companies that want to integrate semantic search into their existing systems

The main branch offers an **API as a service** where:
- The user sends a question and the URL of their FAQ file
- The API automatically processes any FAQ in JSON format
- Perfect for multiple clients with different FAQs
- No prior configuration required

**Usage example:**
```bash
curl -X POST "http://localhost:8000/api/v1/faq/search" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "How does the API work?",
       "faq_url": "https://github.com/user/repo/blob/main/faq.json",
       "enhance_with_llm": true
     }'
```

### 🏠 Branch `standalone` - Closed Project
**Ideal for**: Companies that want a complete and independent solution

The standalone branch offers a **complete system** where:
- The FAQ is an integral part of the project
- JSON file already included in the project
- Ideal for deploying a specific solution
- Perfect for a single, dedicated FAQ

**FAQ format:**
```json
{
  "faq": [
    {
      "question": "My question?",
      "answer": "FAQ answer"
    }
  ]
}
```

## 🛠️ Technologies & Frameworks

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, fast web framework for Python APIs
- **[OpenAI](https://openai.com/)** - Embeddings and language models
- **[Scikit-learn](https://scikit-learn.org/)** - Cosine similarity calculations

### AI & Machine Learning
- **[OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)** - Text-to-vector conversion
- **[GPT-3.5-turbo](https://platform.openai.com/docs/models/gpt-3-5)** - Language detection and answer enhancement
- **Semantic Search** - Context-aware question matching

### Development & Testing
- **[Pytest](https://docs.pytest.org/)** - Testing framework
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI server for running the application

### Code Quality
- **[Black](https://black.readthedocs.io/)** - Code formatter
- **[Flake8](https://flake8.pycqa.org/)** - Linting tool
- **Type Hints** - Full type annotation coverage

## 🔧 Installation & Setup

### Prerequisites
- Python 3.10+
- Git
- OpenAI API Key

### Local Development with Virtual Environment

#### 1. Clone the Repository
```bash
# For API version (main)
git clone https://github.com/albertoivo/ai-faq-bot.git
cd ai-faq-bot

# For standalone version
git clone -b standalone https://github.com/albertoivo/ai-faq-bot.git
cd ai-faq-bot
```

#### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

#### 3. Setup Environment Variables
```bash
# Add to your ~/.bashrc, ~/.zshrc, or create a .env file
export OPENAI_API_KEY="your-openai-api-key-here"
```

#### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 5. Start the Application
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🚀 How to Use

### Branch `main` - API
```bash
# Search for answer in external FAQ
curl -X POST "http://localhost:8000/api/v1/faq/search" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "What is this API?",
       "faq_url": "https://raw.githubusercontent.com/user/repo/main/faq.json",
       "enhance_with_llm": true
     }'
```

### Branch `standalone` - Closed Project
```bash
# Search for answer in internal FAQ
curl -X POST "http://localhost:8000/api/v1/faq/search" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "How does this system work?",
       "enhance_with_llm": true
     }'
```

## 📊 Features

### 🔍 Intelligent Semantic Search
- Finds relevant answers even with different words
- Uses OpenAI embeddings for contextual understanding
- Calculates cosine similarity for answer ranking

### 🌐 Multilingual Support
- Automatic language detection (Portuguese/English)
- Works with FAQs in different languages
- Enhanced answers in the detected language

### 🤖 AI Enhancement
- Option to make answers more friendly and conversational
- Contextualizes the answer for the specific question
- Improves user experience

### ⚡ Optimized Performance
- Smart embedding caching
- Avoids unnecessary recalculations
- Supports multiple URLs simultaneously

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### 📝 Development Guidelines
- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Use meaningful commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Pytest Documentation](https://docs.pytest.org/)

## 📞 Support

If you have any questions or issues, please:
- Check the [Issues](https://github.com/albertoivo/ai-faq-bot/issues) page
- Create a new issue if your problem isn't already reported
- Provide detailed information about your environment and the issue

---

**Happy coding!** 🎉
