## Importing libraries and files
from crewai import Task

from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import read_data_tool, search_tool

## Creating a task to help solve user's query
analyze_financial_document_task = Task(
    description="Thoroughly analyze the financial document to address the user's query: {query}.\n\
\n\
CRITICAL: The financial document file path is: {file_path}\n\
You MUST use the Read Financial Document tool and pass the file_path parameter as: {file_path}\n\
Call the tool like this: read_data_tool(file_path='{file_path}')\n\
\n\
After reading the document, extract key financial metrics including revenue, net income, EPS, margins, cash flow, and debt levels.\n\
Identify significant trends, year-over-year changes, and notable items in the financial data.\n\
Search the internet for relevant market context and industry comparisons if needed.\n\
Provide a comprehensive, data-driven analysis with specific numbers cited from the document.",

    expected_output="""A comprehensive financial analysis report including:
1. Executive Summary - Key findings and highlights from the document
2. Financial Performance Overview - Revenue, profitability, margins, and growth metrics with specific numbers
3. Balance Sheet Analysis - Assets, liabilities, equity position, and liquidity ratios
4. Cash Flow Analysis - Operating, investing, and financing cash flows
5. Key Trends and Observations - Notable year-over-year changes and patterns
6. Market Context - How the company compares to industry benchmarks
7. Sources - References to specific data points from the financial document""",

    agent=financial_analyst,
    tools=[read_data_tool, search_tool],
    async_execution=False,
)

## Creating an investment analysis task
investment_analysis = Task(
    description="Based on the financial analysis, provide well-reasoned investment recommendations.\n\
Review the key financial metrics and trends identified in the previous analysis.\n\
User query: {query}\n\
The financial document is located at: {file_path}\n\
If you need to reference the original document, use the Read Financial Document tool with file path: {file_path}.\n\
Evaluate the company's valuation, growth prospects, and competitive position.\n\
Consider different investor profiles (conservative, moderate, aggressive) in your recommendations.\n\
Ensure all recommendations are grounded in actual financial data from the document.",

    expected_output="""A structured investment analysis report including:
1. Investment Thesis - Clear bull and bear cases supported by financial data
2. Valuation Assessment - Key valuation metrics (P/E, P/B, EV/EBITDA) with context
3. Growth Analysis - Revenue and earnings growth trajectory and sustainability
4. Investment Recommendations - Specific, actionable recommendations for different risk profiles
5. Key Catalysts and Risks - Upcoming events or factors that could impact the investment
6. Disclaimer - Standard investment disclaimer about risks and the importance of personal research""",

    agent=investment_advisor,
    tools=[read_data_tool, search_tool],
    async_execution=False,
)

## Creating a risk assessment task
risk_assessment = Task(
    description="Conduct a comprehensive risk assessment based on the financial document.\n\
Analyze all risk factors present in the financial data and disclosures.\n\
User query: {query}\n\
The financial document is located at: {file_path}\n\
Read the document using the Read Financial Document tool with file path: {file_path} to analyze risk factors.\n\
Evaluate credit risk, market risk, liquidity risk, and operational risk.\n\
Identify potential red flags and vulnerabilities in the financial statements.\n\
Provide actionable risk mitigation strategies based on the actual data.",

    expected_output="""A detailed risk assessment report including:
1. Risk Summary - Overall risk profile rating and key risk factors identified
2. Financial Risk Analysis - Leverage, liquidity, and solvency risks with specific ratios
3. Market Risk Factors - Industry, competitive, and macroeconomic risks
4. Operational Risks - Business model, regulatory, and execution risks
5. Risk Mitigation Strategies - Practical recommendations to manage identified risks
6. Risk Matrix - Summary of risks categorized by likelihood and potential impact""",

    agent=risk_assessor,
    tools=[read_data_tool],
    async_execution=False,
)

    
verification = Task(
    description="Verify that the provided document is a valid financial document.\n\
\n\
CRITICAL: The document file path is: {file_path}\n\
You MUST use the Read Financial Document tool and pass the file_path parameter: read_data_tool(file_path='{file_path}')\n\
\n\
After reading, check for key financial document characteristics such as financial statements, disclosures, and reporting elements.\n\
Extract metadata: company name, reporting period, document type, and filing information.\n\
Confirm the document's data integrity and suitability for financial analysis.",

    expected_output="""A verification report including:
1. Document Validity - Confirmed as valid financial document (Yes/No) with reasoning
2. Document Type - Type of financial report (10-K, 10-Q, Annual Report, Earnings Update, etc.)
3. Company Information - Company name, ticker symbol, and reporting period
4. Document Structure - Key sections identified (income statement, balance sheet, cash flow, etc.)
5. Data Quality - Assessment of data completeness and consistency
6. Recommendation - Whether the document is suitable for detailed financial analysis""",

    agent=verifier,
    tools=[read_data_tool],
    async_execution=False
)
