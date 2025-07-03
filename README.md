# AI FAQ BOT API

## 🛠️ Technologies & Frameworks

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, fast web framework for Python APIs

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

### Option 1: Local Development with Virtual Environment

#### 1. Clone the Repository
```bash
git clone https://github.com/albertoivo/ai-faq-bot.git
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

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Start the Application
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add tests for new features
- Update documentation as needed
- Use meaningful commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pytest Documentation](https://docs.pytest.org/)

## 📞 Support

If you have any questions or issues, please:
- Check the [Issues](https://github.com/albertoivo/ai-faq-bot/issues) page
- Create a new issue if your problem isn't already reported
- Provide detailed information about your environment and the issue

---

**Happy coding!** 🎉