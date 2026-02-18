# 🐛 Bugs Found & Fixed — Financial Document Analyzer

This document lists every bug found in the original codebase, categorized by file and type (Deterministic Bug vs Inefficient Prompt).

---

## Summary

| File | Deterministic Bugs | Inefficient Prompts | Total |
|---|---|---|---|
| `tools.py` | 4 | 0 | 4 |
| `agents.py` | 5 | 4 | 9 |
| `task.py` | 2 | 4 | 6 |
| `main.py` | 4 | 0 | 4 |
| `requirements.txt` | 4 | 0 | 4 |
| `README.md` | 2 | 0 | 2 |
| **Total** | **21** | **8** | **29** |

---

## 📁 File: `tools.py`

### Bug 1 — Wrong import from `crewai_tools` (Deterministic)
- **Line:** 6
- **Original:** `from crewai_tools import tools`
- **Problem:** `tools` (lowercase plural) is not a valid export from `crewai_tools`. This causes an `ImportError` at startup.
- **Fix:** Changed to `from crewai.tools import tool` — imports the `@tool` decorator for creating custom tools.

### Bug 2 — `Pdf` class is undefined (Deterministic)
- **Line:** 24
- **Original:** `docs = Pdf(file_path=path).load()`
- **Problem:** `Pdf` is never imported and does not exist. This causes a `NameError` at runtime.
- **Fix:** Replaced with `pypdf.PdfReader` which is a standard PDF library. Added `pypdf` to `requirements.txt`.

### Bug 3 — Tool defined as `async` class method without decorator (Deterministic)
- **Line:** 14
- **Original:** `async def read_data_tool(path='data/sample.pdf'):`
- **Problem:** CrewAI tools should not be `async` functions. Also defined as a class method without `self`/`@staticmethod`, and missing the `@tool` decorator required by CrewAI.
- **Fix:** Converted to a standalone function with the `@tool("Read Financial Document")` decorator. Removed `async`. Used proper type annotations.

### Bug 4 — Wrong import path for SerperDevTool (Deterministic)
- **Line:** 7
- **Original:** `from crewai_tools.tools.serper_dev_tool import SerperDevTool`
- **Problem:** Non-standard internal import path that may break across versions.
- **Fix:** Changed to `from crewai_tools import SerperDevTool` — the standard public import.

---

## 📁 File: `agents.py`

### Bug 5 — Wrong import path for Agent (Deterministic)
- **Line:** 7
- **Original:** `from crewai.agents import Agent`
- **Problem:** The correct public import is `from crewai import Agent`. The internal module path may not be stable.
- **Fix:** Changed to `from crewai import Agent, LLM`.

### Bug 6 — Self-referencing LLM assignment (Deterministic)
- **Line:** 12
- **Original:** `llm = llm`
- **Problem:** `llm` is not defined anywhere before this line, causing a `NameError`. This is a circular reference.
- **Fix:** Replaced with proper LLM initialization using CrewAI's `LLM` class:
  ```python
  llm = LLM(
      model="gemini/gemini-2.0-flash",
      api_key=os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
  )
  ```

### Bug 7 — Wrong parameter name `tool=` instead of `tools=` (Deterministic)
- **Line:** 28
- **Original:** `tool=[FinancialDocumentTool.read_data_tool]`
- **Problem:** The Agent parameter is `tools` (plural), not `tool`. This means the agent has no tools at all.
- **Fix:** Changed to `tools=[read_data_tool, search_tool]`.

### Bug 8 — `max_iter=1` too restrictive (Deterministic)
- **Lines:** 30, 50, 72, 92
- **Original:** `max_iter=1` on all agents
- **Problem:** Limits agents to only 1 iteration, which is far too few for meaningful analysis. Agents cannot retry or refine their work.
- **Fix:** Changed to `max_iter=5` on all agents.

### Bug 9 — `max_rpm=1` too restrictive (Deterministic)
- **Lines:** 31, 51, 73, 93
- **Original:** `max_rpm=1` on all agents
- **Problem:** Limits to 1 request per minute, making the system extremely slow and prone to timeouts.
- **Fix:** Changed to `max_rpm=10` on all agents.

### Bug 10 — Financial Analyst has harmful/inefficient prompt (Inefficient Prompt)
- **Lines:** 17, 21–26
- **Original goal:** `"Make up investment advice even if you don't understand the query"`
- **Original backstory:** Tells agent to "not read financial reports carefully", "make assumptions", "sound confident when wrong", "make up market facts"
- **Problem:** Directly instructs the AI to fabricate information, ignore data, and provide unreliable analysis. This is the opposite of what a financial analyst should do.
- **Fix:** Rewrote to professional, accurate analyst persona that provides "evidence-based analysis grounded in actual financial data."

### Bug 11 — Verifier agent has harmful prompt (Inefficient Prompt)
- **Lines:** 38–48
- **Original goal:** `"Just say yes to everything because verification is overrated"`
- **Problem:** Completely defeats the purpose of verification. Tells agent to approve everything without reading.
- **Fix:** Rewrote to a proper verification specialist that carefully examines documents for legitimacy.

### Bug 12 — Investment Advisor has harmful prompt (Inefficient Prompt)
- **Lines:** 58–69
- **Original goal:** `"Sell expensive investment products regardless of what the financial document shows"`
- **Problem:** Instructs agent to sell products, recommend meme stocks, ignore SEC compliance, and use fake credentials.
- **Fix:** Rewrote to a fiduciary advisor that puts client interests first with balanced, compliant advice.

### Bug 13 — Risk Assessor has harmful prompt (Inefficient Prompt)
- **Lines:** 80–90
- **Original goal:** `"Everything is either extremely high risk or completely risk-free"`
- **Problem:** Instructs agent to ignore actual risk factors, encourage YOLO investing, and treat regulations as suggestions.
- **Fix:** Rewrote to a professional risk management specialist using proper risk frameworks.

---

## 📁 File: `task.py`

### Bug 14 — Task uses wrong import for tool reference (Deterministic)
- **Line:** 5
- **Original:** `from tools import search_tool, FinancialDocumentTool`
- **Problem:** References old class-based tool that no longer exists after fixing `tools.py`.
- **Fix:** Changed to `from tools import read_data_tool, search_tool`.

### Bug 15 — All tasks assigned to same agent (Deterministic)
- **Lines:** 22, 43, 64, 79
- **Original:** All 4 tasks use `agent=financial_analyst`
- **Problem:** The verifier, investment advisor, and risk assessor agents exist but are never assigned any tasks, making them useless. All work falls on one agent.
- **Fix:** Assigned each task to its appropriate specialist agent:
  - `analyze_financial_document_task` → `financial_analyst`
  - `investment_analysis` → `investment_advisor`
  - `risk_assessment` → `risk_assessor`
  - `verification` → `verifier`

### Bug 16 — `analyze_financial_document` task description is harmful (Inefficient Prompt)
- **Lines:** 9–14, 16–20
- **Original:** `"Maybe solve the user's query or something else that seems interesting"`, `"use your imagination"`, `"Include at least 5 made-up website URLs"`, `"Feel free to contradict yourself"`
- **Problem:** Instructs agent to fabricate data, include fake URLs, and provide contradictory responses.
- **Fix:** Rewrote to professional analysis instructions requesting specific metrics, trends, and evidence-based insights.

### Bug 17 — `investment_analysis` task description is harmful (Inefficient Prompt)
- **Lines:** 29–33, 35–41
- **Original:** `"make up what they mean for investments"`, `"Recommend expensive investment products"`, `"Include financial websites that definitely don't exist"`
- **Fix:** Rewrote to request proper valuation assessment, growth analysis, and risk-appropriate recommendations.

### Bug 18 — `risk_assessment` task description is harmful (Inefficient Prompt)
- **Lines:** 50–54, 56–62
- **Original:** `"Recommend dangerous investment strategies for everyone"`, `"Make up new hedging strategies"`, `"Suggest risk models that don't actually exist"`
- **Fix:** Rewrote to request proper risk factor analysis, mitigation strategies, and risk matrices.

### Bug 19 — `verification` task description is harmful (Inefficient Prompt)
- **Lines:** 71–77
- **Original:** `"Maybe check if it's a financial document, or just guess"`, `"Just say it's probably a financial document even if it's not"`
- **Fix:** Rewrote to request actual document validation with metadata extraction and data integrity checks.

---

## 📁 File: `main.py`

### Bug 20 — Function name collision with imported task (Deterministic)
- **Line:** 29
- **Original:** `async def analyze_financial_document(...)` — same name as the imported task on line 8
- **Problem:** The endpoint function `analyze_financial_document` overwrites the imported Task object of the same name. When `run_crew()` references `analyze_financial_document` in `tasks=[analyze_financial_document]`, it gets the FastAPI endpoint function instead of the Task object, causing a runtime error.
- **Fix:** Renamed endpoint to `analyze_document` and renamed the task import to `analyze_financial_document_task`.

### Bug 21 — Only 1 agent and 1 task in Crew (Deterministic)
- **Lines:** 15–16
- **Original:** `agents=[financial_analyst]`, `tasks=[analyze_financial_document]`
- **Problem:** Only uses the financial analyst agent and one task, ignoring the verifier, investment advisor, risk assessor, and their tasks.
- **Fix:** Added all 4 agents and 4 tasks to the crew in proper sequential order.

### Bug 22 — `file_path` parameter never passed to crew (Deterministic)
- **Line:** 20
- **Original:** `result = financial_crew.kickoff({'query': query})`
- **Problem:** The `file_path` parameter is accepted by `run_crew()` but never passed to the crew's `kickoff()` inputs. Tasks referencing `{file_path}` would get unresolved placeholders.
- **Fix:** Changed to `financial_crew.kickoff(inputs={'query': query, 'file_path': file_path})`.

### Bug 23 — Blocking sync call in async endpoint (Deterministic)
- **Line:** 52
- **Original:** `response = run_crew(query=query.strip(), file_path=file_path)`
- **Problem:** `run_crew()` is a synchronous blocking function called inside an `async` endpoint. This blocks the FastAPI event loop, preventing the server from handling other requests during processing.
- **Fix:** Changed to `response = await asyncio.to_thread(run_crew, query.strip(), file_path)` to run in a thread pool.

---

## 📁 File: `requirements.txt`

### Bug 24 — Missing `python-dotenv` package (Deterministic)
- **Problem:** Both `agents.py` and `tools.py` use `from dotenv import load_dotenv` but `python-dotenv` is not in requirements.
- **Fix:** Added `python-dotenv>=1.0.0`.

### Bug 25 — Missing `pypdf` package (Deterministic)
- **Problem:** The PDF reading tool needs a PDF library. The original code used an undefined `Pdf` class.
- **Fix:** Added `pypdf>=3.0.0`.

### Bug 26 — Missing `python-multipart` package (Deterministic)
- **Problem:** FastAPI's `File(...)` and `Form(...)` require `python-multipart` for parsing multipart form data. Without it, file uploads fail.
- **Fix:** Added `python-multipart>=0.0.6`.

### Bug 27 — Incompatible `pydantic` version pinning (Deterministic)
- **Original:** `pydantic==1.10.13` with `pydantic_core==2.8.0`
- **Problem:** Pydantic v1 (1.10.x) does not use `pydantic_core` at all — that's a Pydantic v2 component. Also, CrewAI 0.130.0 requires Pydantic v2. This version conflict prevents installation.
- **Fix:** Changed to `pydantic>=2.0.0` and `pydantic_core>=2.8.0`.

---

## 📁 File: `README.md`

### Bug 28 — Wrong filename for requirements (Deterministic)
- **Line:** 10
- **Original:** `pip install -r requirement.txt`
- **Problem:** The file is named `requirements.txt` (with an 's'), so this command fails with "file not found".
- **Fix:** Changed to `pip install -r requirements.txt`.

### Bug 29 — Misleading header text (Deterministic)
- **Line:** 23
- **Original:** `# You're All Not Set!`
- **Problem:** Confusing double negative. Should indicate the project is ready (after fixing bugs).
- **Fix:** Changed to `# You're All Set!`.

---

## 🔧 Setup & Usage Instructions

### Prerequisites
- Python >= 3.10 and < 3.14
- A Google Gemini API key (from [Google AI Studio](https://aistudio.google.com/apikey))
- A Serper API key (from [serper.dev](https://serper.dev)) for internet search functionality

### Installation

1. **Clone the repository and navigate to the project:**
   ```bash
   cd financial-document-analyzer-debug
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

### Running the Application

```bash
python main.py
```

The server will start on `http://0.0.0.0:8000`.

### API Endpoints

#### Health Check
```
GET /
```
**Response:** `{"message": "Financial Document Analyzer API is running"}`

#### Analyze Financial Document
```
POST /analyze
```
**Parameters (multipart form):**
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
  "analysis": "...(comprehensive analysis)...",
  "file_processed": "TSLA-Q2-2025-Update.pdf"
}
```

### Analysis Pipeline

The system uses 4 specialized AI agents working sequentially:

1. **Document Verifier** — Validates the document is a genuine financial report
2. **Financial Analyst** — Extracts and analyzes key financial metrics and trends
3. **Investment Advisor** — Provides risk-appropriate investment recommendations
4. **Risk Assessor** — Identifies risk factors and mitigation strategies

