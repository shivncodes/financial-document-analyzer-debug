## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai.tools import tool
from crewai_tools import SerperDevTool

## Creating search tool
search_tool = SerperDevTool()

## Creating custom pdf reader tool
@tool("Read Financial Document")
def read_data_tool(file_path: str = 'data/sample.pdf', max_pages: int = 50, focus_sections: bool = True) -> str:
    """Tool to read and extract text data from a PDF financial document.
    
    IMPORTANT: Always use the file_path provided in the task context. The file_path variable 
    contains the exact path to the uploaded financial document that needs to be analyzed.
    
    For large documents, this tool automatically focuses on key financial sections to avoid token limits.

    Args:
        file_path (str): Path of the pdf file to read. Use the {file_path} variable from the task context.
        max_pages (int): Maximum number of pages to extract (default: 50). Set to 0 for all pages.
        focus_sections (bool): If True, prioritize financial statement sections (default: True).

    Returns:
        str: Full text content of the financial document (or key sections for large documents).
    """
    import os
    from pypdf import PdfReader

    # Check if file exists
    if not os.path.exists(file_path):
        # Try to find the file in data directory if default path doesn't exist
        if file_path == 'data/sample.pdf':
            # Look for TSLA file or most recent PDF in data directory
            data_dir = 'data'
            if os.path.exists(data_dir):
                pdf_files = [f for f in os.listdir(data_dir) if f.endswith('.pdf')]
                if pdf_files:
                    # Use TSLA file if available, otherwise most recent
                    tsla_file = os.path.join(data_dir, 'TSLA-Q2-2025-Update.pdf')
                    if os.path.exists(tsla_file):
                        file_path = tsla_file
                        print(f"Using fallback file: {file_path}")
                    else:
                        # Get most recent PDF
                        pdf_files_with_paths = [os.path.join(data_dir, f) for f in pdf_files]
                        file_path = max(pdf_files_with_paths, key=os.path.getmtime)
                        print(f"Using most recent file: {file_path}")
        
        # Final check
        if not os.path.exists(file_path):
            return f"ERROR: File not found at path: {file_path}. Available PDFs in data/: {[f for f in os.listdir('data') if f.endswith('.pdf')] if os.path.exists('data') else 'data directory not found'}"
    
    try:
        reader = PdfReader(file_path)
        total_pages = len(reader.pages)
        
        # Key financial section keywords to prioritize
        financial_keywords = [
            'income statement', 'balance sheet', 'cash flow', 'financial statements',
            'revenue', 'net income', 'earnings', 'eps', 'ebitda', 'margins',
            'assets', 'liabilities', 'equity', 'debt', 'cash and cash equivalents',
            'operating', 'investing', 'financing', 'quarterly', 'annual',
            'consolidated', 'unaudited', 'audited', 'management discussion'
        ]
        
        full_report = ""
        prioritized_pages = []
        other_pages = []
        
        # First pass: identify pages with financial content
        if focus_sections and total_pages > 30:  # Only prioritize if document is large
            for i, page in enumerate(reader.pages):
                content = page.extract_text()
                if content:
                    content_lower = content.lower()
                    # Check if page contains financial keywords
                    has_financial_content = any(keyword in content_lower for keyword in financial_keywords)
                    if has_financial_content:
                        prioritized_pages.append((i, content))
                    else:
                        other_pages.append((i, content))
            
            # Combine: prioritized pages first, then other pages (limited)
            pages_to_extract = prioritized_pages + other_pages[:max(0, max_pages - len(prioritized_pages))]
        else:
            # For smaller documents or when focus_sections=False, extract all or up to max_pages
            limit = max_pages if max_pages > 0 else total_pages
            pages_to_extract = [(i, page.extract_text()) for i, page in enumerate(reader.pages[:limit])]
        
        # Extract and format text
        for page_num, content in pages_to_extract:
            if content:
                # Clean and format the financial document data
                # Remove extra whitespaces and format properly
                while "\n\n" in content:
                    content = content.replace("\n\n", "\n")
                full_report += f"[Page {page_num + 1}]\n{content}\n\n"
        
        if not full_report.strip():
            return f"WARNING: File {file_path} was read but contains no extractable text. The PDF might be image-based or corrupted."
        
        # Add summary note if document was truncated
        if total_pages > len(pages_to_extract):
            full_report = f"NOTE: Document has {total_pages} pages. Extracted {len(pages_to_extract)} key pages focusing on financial statements and metrics.\n\n" + full_report
        
        return full_report
    except Exception as e:
        return f"ERROR reading file {file_path}: {str(e)}"
