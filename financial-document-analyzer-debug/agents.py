## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, LLM

from tools import search_tool, read_data_tool

### Loading LLM
# FREE MODEL OPTIONS (choose one):
# 1. Groq (FREE, no installation) - Get API key from https://console.groq.com/
#    Production models: groq/openai/gpt-oss-120b, groq/openai/gpt-oss-20b, 
#                       groq/llama-3.3-70b-versatile, groq/llama-3.1-8b-instant
#    See all models: https://console.groq.com/docs/models
# 2. Ollama (FREE, local) - Install: brew install ollama, then: ollama pull llama3.2
#    model="ollama/llama3.2" (requires OLLAMA_API_KEY="" or leave empty for local)
# 3. Gemini (FREE tier, but has quota limits)
#    model="gemini/gemini-pro" (requires GEMINI_API_KEY)

# Using Groq - FREE and fast! Get your API key from https://console.groq.com/
groq_api_key = os.environ.get("GROQ_API_KEY")
gemini_api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

if groq_api_key:
    # Groq - FREE tier with high rate limits
    # Production models from https://console.groq.com/docs/models:
    # - groq/openai/gpt-oss-120b (500 tps, 8K TPM limit) - Smart PDF extraction handles large files
    # - groq/openai/gpt-oss-20b (1000 tps, higher TPM) - Alternative option
    # - groq/llama-3.3-70b-versatile (280 tps, higher context window)
    # - groq/llama-3.1-8b-instant (560 tps, $0.05/$0.08 per 1M tokens) - Fastest, cheapest
    
    # Using gpt-oss-120b with smart PDF extraction to handle large documents
    # The PDF reader tool automatically extracts key financial sections to stay within token limits
    llm = LLM(
        model="groq/openai/gpt-oss-120b",  # As requested
        api_key=groq_api_key
    )
elif gemini_api_key:
    # Fallback to Gemini if Groq not available
    llm = LLM(
        model="gemini/gemini-pro",
        api_key=gemini_api_key
    )
else:
    # Default to Groq (you'll need to add GROQ_API_KEY to .env)
    raise ValueError(
        "No API key found! Please add one of these to your .env file:\n"
        "  GROQ_API_KEY=your_key_here (FREE - get from https://console.groq.com/)\n"
        "  OR GEMINI_API_KEY=your_key_here (FREE tier but has quota limits)"
    )

# Creating an Experienced Financial Analyst agent
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Analyze the financial document thoroughly and provide accurate, data-driven investment "
         "insights based on the user's query: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are a highly experienced senior financial analyst with over 15 years of expertise in "
        "corporate finance, equity research, and financial statement analysis. You hold a CFA charter "
        "and have worked at top-tier investment banks and asset management firms. You are meticulous "
        "in reading financial reports, identifying key metrics, trends, and risks. You provide "
        "well-reasoned, evidence-based analysis grounded in actual financial data from the documents "
        "you review. You always cite specific numbers and figures from the reports you analyze."
    ),
    tools=[read_data_tool, search_tool],
    llm=llm,
    max_iter=5,
    max_rpm=5,  # Reduced to avoid hitting free tier rate limits
    allow_delegation=False
)

# Creating a document verifier agent
verifier = Agent(
    role="Financial Document Verification Specialist",
    goal="Verify that the uploaded document is a valid financial document and extract key metadata "
         "such as company name, reporting period, and document type before analysis proceeds.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a detail-oriented financial document verification specialist with extensive experience "
        "in financial compliance and document authentication. You carefully examine documents to confirm "
        "they are legitimate financial reports, checking for proper formatting, required disclosures, "
        "and data consistency. You ensure that only valid financial documents proceed to analysis, "
        "maintaining high standards of accuracy and regulatory compliance."
    ),
    tools=[read_data_tool],
    llm=llm,
    max_iter=5,
    max_rpm=5,  # Reduced to avoid hitting free tier rate limits
    allow_delegation=False
)


investment_advisor = Agent(
    role="Certified Investment Advisor",
    goal="Based on the financial analysis, provide sound, well-reasoned investment recommendations "
         "that are appropriate for different risk profiles and aligned with the actual financial data.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a certified financial planner (CFP) and registered investment advisor with 15+ years "
        "of experience in portfolio management and investment strategy. You follow fiduciary standards "
        "and always put client interests first. You provide balanced investment advice based on "
        "fundamental analysis, considering risk tolerance, time horizon, and diversification principles. "
        "You comply with all SEC regulations and always include appropriate disclaimers in your advice."
    ),
    tools=[read_data_tool, search_tool],
    llm=llm,
    max_iter=5,
    max_rpm=5,  # Reduced to avoid hitting free tier rate limits
    allow_delegation=False
)


risk_assessor = Agent(
    role="Financial Risk Assessment Specialist",
    goal="Conduct a thorough risk assessment of the financial data, identifying key risk factors, "
         "potential vulnerabilities, and providing actionable risk mitigation strategies.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a seasoned risk management professional with deep expertise in financial risk analysis, "
        "stress testing, and regulatory compliance. You have experience with Basel frameworks, VaR models, "
        "and enterprise risk management. You carefully analyze financial statements to identify credit risk, "
        "market risk, liquidity risk, and operational risk factors. You provide practical, well-calibrated "
        "risk mitigation strategies based on actual financial data and industry best practices."
    ),
    tools=[read_data_tool],
    llm=llm,
    max_iter=5,
    max_rpm=5,  # Reduced to avoid hitting free tier rate limits
    allow_delegation=False
)
