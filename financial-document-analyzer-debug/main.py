from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import asyncio

from crewai import Crew, Process
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import analyze_financial_document_task, investment_analysis, risk_assessment, verification

app = FastAPI(title="Financial Document Analyzer")

def run_crew(query: str, file_path: str = "data/sample.pdf"):
    """Run the full financial analysis crew on the given document."""
    financial_crew = Crew(
        agents=[verifier, financial_analyst, investment_advisor, risk_assessor],
        tasks=[verification, analyze_financial_document_task, investment_analysis, risk_assessment],
        process=Process.sequential,
        verbose=True,
    )
    
    result = financial_crew.kickoff(inputs={'query': query, 'file_path': file_path})
    return result

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze-sample")
async def analyze_sample_document(
    query: str = Form(default="Analyze this financial document for investment insights")
):
    """Analyze the sample TSLA document (for testing without file upload)"""
    sample_file_path = "data/TSLA-Q2-2025-Update.pdf"
    
    if not os.path.exists(sample_file_path):
        raise HTTPException(status_code=404, detail=f"Sample file not found at: {sample_file_path}")
    
    try:
        absolute_file_path = os.path.abspath(sample_file_path)
        response = await asyncio.to_thread(run_crew, query.strip(), absolute_file_path)
        
        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": "TSLA-Q2-2025-Update.pdf"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")

@app.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    """Analyze financial document and provide comprehensive investment recommendations"""
    
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"
    
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Validate query
        if query == "" or query is None:
            query = "Analyze this financial document for investment insights"
        
        # Verify file exists before processing
        if not os.path.exists(file_path):
            raise HTTPException(status_code=400, detail=f"File was not saved correctly. Expected at: {file_path}")
        
        # Log the file path for debugging
        print(f"Processing file: {file_path}")
        print(f"File exists: {os.path.exists(file_path)}")
        print(f"File size: {os.path.getsize(file_path) if os.path.exists(file_path) else 'N/A'} bytes")
            
        # Process the financial document with all analysts
        # Pass absolute path to ensure agents can find it
        absolute_file_path = os.path.abspath(file_path)
        response = await asyncio.to_thread(run_crew, query.strip(), absolute_file_path)
        
        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass  # Ignore cleanup errors

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
