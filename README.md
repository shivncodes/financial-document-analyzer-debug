# Financial Document Analyzer

A comprehensive financial document analysis system that processes corporate reports, financial statements, and investment documents using AI-powered multi-agent analysis.

## 🎯 Project Status

✅ **All bugs fixed** - 29 bugs resolved (21 deterministic bugs + 8 inefficient prompts)  
✅ **Fully functional** - System is working and ready for production use  
✅ **Free model support** - Works with Groq (free), Ollama (local), or Gemini (free tier)

See [BUGS_FIXED.md](./BUGS_FIXED.md) for complete documentation of all fixes.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10-3.12 (Python 3.12 recommended)
- API keys (see setup below)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd financial-document-analyzer-debug
   ```

2. **Create and activate virtual environment:**
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   ⚠️ **Note:** This may take 5-10 minutes due to many dependencies.

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your API keys (see [Free Model Setup](#free-model-setup) below).

5. **Run the application:**
   ```bash
   ./run.sh
   # Or: python main.py
   ```
   
   The server will start on `http://localhost:8000`

---

## 🔑 Free Model Setup

### Option 1: Groq (RECOMMENDED - Free & Fast)

1. Get your FREE API key: https://console.groq.com/
2. Add to `.env`:
   ```bash
   GROQ_API_KEY=your_groq_api_key_here
   ```

**Available Groq Models:**
- `groq/openai/gpt-oss-120b` (current - most powerful)
- `groq/openai/gpt-oss-20b` (faster, cheaper)
- `groq/llama-3.3-70b-versatile` (high quality)
- `groq/llama-3.1-8b-instant` (fastest, cheapest)

See [FREE_MODEL_SETUP.md](./FREE_MODEL_SETUP.md) for detailed instructions.

---

## 📡 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check
```http
GET /
```

**Response:**
```json
{
  "message": "Financial Document Analyzer API is running"
}
```

#### 2. Analyze Financial Document
```http
POST /analyze
```

**Request (multipart/form-data):**
- `file` (required): PDF file to analyze
- `query` (optional): Custom analysis question (default: "Analyze this financial document for investment insights")

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@data/TSLA-Q2-2025-Update.pdf" \
  -F "query=What are the key revenue trends and investment risks?"
```

**Response:**
```json
{
  "status": "success",
  "query": "What are the key revenue trends and investment risks?",
  "analysis": "...(comprehensive analysis from 4 AI agents)...",
  "file_processed": "TSLA-Q2-2025-Update.pdf"
}
```

**Interactive API Documentation:**
The OpenAPI/Swagger specification is available in `outputs/assignment.yaml`. You can:

1. **Import into API clients:**
   - **Bruno:** Import the YAML file directly
   - **Postman:** Import → File → Select `outputs/assignment.yaml`
   - **Insomnia:** Import → OpenAPI 3.0 → Select `outputs/assignment.yaml`

2. **View in Swagger UI:**
   - Copy the contents of `outputs/assignment.yaml`
   - Paste into https://editor.swagger.io/ for interactive documentation

3. **Use with any OpenAPI-compatible tool:**
   - The YAML file follows OpenAPI 3.0 specification
   - Compatible with all modern API testing tools

---

## 🤖 AI Agents & Analysis Pipeline

The system uses **4 specialized AI agents** working sequentially:

1. **Document Verifier** - Validates the document is a genuine financial report
2. **Financial Analyst** - Extracts and analyzes key financial metrics and trends
3. **Investment Advisor** - Provides risk-appropriate investment recommendations
4. **Risk Assessor** - Identifies risk factors and mitigation strategies

Each agent has specific expertise and tools to provide comprehensive analysis.

---

## 📁 Project Structure

```
financial-document-analyzer-debug/
├── main.py                 # FastAPI application
├── agents.py              # AI agents configuration
├── task.py                # Task definitions
├── tools.py               # Custom tools (PDF reader, search)
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── .env.example           # API key template
├── .gitignore            # Git ignore rules
├── run.sh                # Startup script
├── data/                 # Sample financial documents
│   └── TSLA-Q2-2025-Update.pdf
└── outputs/              # API documentation and outputs
    └── assignment.yaml    # OpenAPI/Swagger specification
```

---

## 🐛 Bugs Fixed

**Total: 29 bugs fixed**

- **21 Deterministic Bugs** - Code errors that would crash the application
- **8 Inefficient Prompts** - AI instructions that produced unreliable output

### Key Fixes:
- ✅ Fixed all import errors and undefined classes
- ✅ Corrected LLM initialization and configuration
- ✅ Fixed agent tool assignments and parameters
- ✅ Rewrote all agent prompts for professional, accurate analysis
- ✅ Fixed task assignments to use correct agents
- ✅ Resolved function name collisions
- ✅ Added missing dependencies
- ✅ Fixed async/sync issues in FastAPI

See [BUGS_FIXED.md](./BUGS_FIXED.md) for complete details with line numbers and explanations.

---

## 🧪 Testing

### Test the API

1. **Health check:**
   ```bash
   curl http://localhost:8000/
   ```

2. **Analyze a document:**
   ```bash
   curl -X POST "http://localhost:8000/analyze" \
     -F "file=@data/TSLA-Q2-2025-Update.pdf" \
     -F "query=Analyze this financial document"
   ```

### Sample Document

The project includes a sample Tesla Q2 2025 financial update in `data/TSLA-Q2-2025-Update.pdf`.

You can also upload any financial PDF through the API endpoint.

---

## 📊 Features

✅ **Multi-Agent Analysis** - 4 specialized AI agents working together  
✅ **PDF Processing** - Extracts and analyzes text from financial documents  
✅ **Investment Recommendations** - Data-driven investment advice  
✅ **Risk Assessment** - Comprehensive risk analysis  
✅ **Market Insights** - Industry context and comparisons  
✅ **REST API** - Easy integration with other systems  
✅ **Free Model Support** - Works with Groq, Ollama, or Gemini  

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```bash
# Groq (Recommended - FREE)
GROQ_API_KEY=your_groq_api_key_here

# OR Gemini (Free tier with limits)
GEMINI_API_KEY=your_gemini_api_key_here

# Serper (Required for internet search)
SERPER_API_KEY=your_serper_api_key_here
```

### Model Selection

Edit `agents.py` to change the model:

```python
# Current: groq/openai/gpt-oss-120b
# Alternatives: groq/openai/gpt-oss-20b, groq/llama-3.3-70b-versatile
llm = LLM(
    model="groq/openai/gpt-oss-120b",
    api_key=groq_api_key
)
```

---

## 📝 API Documentation

Full OpenAPI/Swagger specification is available in `outputs/assignment.yaml`.

**To view interactive documentation:**
1. Open `outputs/assignment.yaml` in any text editor
2. Copy the contents
3. Paste into https://editor.swagger.io/ for interactive Swagger UI

**To use with API clients:**
- Import `outputs/assignment.yaml` into Bruno, Postman, Insomnia, or any OpenAPI-compatible tool

---

## 🛠️ Troubleshooting

### Common Issues

1. **"ModuleNotFoundError"**
   - Solution: Make sure virtual environment is activated: `source venv/bin/activate`

2. **"API quota exceeded"**
   - Solution: Use Groq (free, high limits) or wait for quota reset

3. **"Model not found"**
   - Solution: Check model name in `agents.py` matches Groq documentation

4. **Port already in use**
   - Solution: Change port in `main.py` or kill process using port 8000

---

## 📚 Additional Documentation

- [BUGS_FIXED.md](./BUGS_FIXED.md) - Complete bug fix documentation
- [FREE_MODEL_SETUP.md](./FREE_MODEL_SETUP.md) - Detailed free model setup
- [SUBMISSION_CHECKLIST.md](./SUBMISSION_CHECKLIST.md) - Submission checklist

---

## 🎓 Assignment Completion

✅ **Fixed, working code** - All 29 bugs resolved  
✅ **Comprehensive README** - Complete setup and usage instructions  
✅ **API documentation** - OpenAPI spec in `outputs/assignment.yaml`  
✅ **Bug documentation** - Detailed in BUGS_FIXED.md  

---

## 📄 License

This project was created for educational purposes as part of a debugging assignment.

---

## 🙏 Acknowledgments

- [CrewAI](https://docs.crewai.com/) - Multi-agent framework
- [Groq](https://console.groq.com/) - Free, fast LLM inference
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework

---

## 📞 Support

For issues or questions:
1. Check [BUGS_FIXED.md](./BUGS_FIXED.md) for known issues
2. Review [FREE_MODEL_SETUP.md](./FREE_MODEL_SETUP.md) for model setup
3. Check API documentation in `outputs/assignment.yaml` (OpenAPI spec)

---

**Project Status: ✅ Ready for Submission**
