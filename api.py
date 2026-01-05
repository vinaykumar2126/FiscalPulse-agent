from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import asyncio
from graph_agent import fiscal_pulse_app

app = FastAPI(
    title="FiscalPulse API",
    description="Autonomous AI-powered audit agent API",
    version="1.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class AuditRequest(BaseModel):
    query: str

    class Config:
        json_schema_extra = {
            "example": {
                "query": "Check my hardware expenses for tax deductions"
            }
        }

class AuditResponse(BaseModel):
    query: str
    category: str
    audit_report: str
    form_prepared: bool
    final_output: str

    class Config:
        json_schema_extra = {
            "example": {
                "query": "Check my hardware expenses for tax deductions",
                "category": "HARDWARE",
                "audit_report": "## Audit Summary\n\nFound 2 hardware transactions...",
                "form_prepared": False,
                "final_output": "Audit complete. See details above."
            }
        }

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": "Welcome to FiscalPulse API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "audit": "/audit (POST)",
            "categories": "/categories",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "FiscalPulse API",
        "message": "All systems operational"
    }

@app.post("/audit", response_model=AuditResponse)
async def perform_audit(request: AuditRequest):
    """
    Perform an audit based on the user's query.
    
    This endpoint processes the query through the AI agent graph:
    1. Routes the query to determine category
    2. Fetches relevant data from MCP servers
    3. Performs audit analysis
    4. Prepares forms if needed
    
    Args:
        request: AuditRequest containing the user's query
        
    Returns:
        AuditResponse with audit results
        
    Raises:
        HTTPException: If audit processing fails
    """
    try:
        print(f"\n[API] 📝 Received audit request: {request.query}")
        
        # Initialize state
        initial_state = {
            "query": request.query,
            "category": "",
            "raw_data": {},
            "audit_report": "",
            "form_prepared": False,
            "final_output": ""
        }
        
        # Run the graph agent
        print("[API] 🤖 Invoking FiscalPulse agent...")
        final_state = await fiscal_pulse_app.ainvoke(initial_state)
        
        print(f"[API] ✅ Audit complete. Category: {final_state.get('category', 'UNKNOWN')}")
        
        # Return response
        return AuditResponse(
            query=request.query,
            category=final_state.get("category", "UNKNOWN"),
            audit_report=final_state.get("audit_report", "No audit report generated"),
            form_prepared=final_state.get("form_prepared", False),
            final_output=final_state.get("final_output", "No output generated")
        )
        
    except Exception as e:
        print(f"[API] ❌ Error during audit: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Audit processing failed: {str(e)}"
        )

@app.get("/categories")
async def get_categories():
    """Get available audit categories"""
    return {
        "categories": [
            {
                "name": "HARDWARE",
                "description": "Hardware purchases and equipment",
                "icon": "💻"
            },
            {
                "name": "SOFTWARE",
                "description": "Software licenses and subscriptions",
                "icon": "💿"
            },
            {
                "name": "RENT",
                "description": "Rental and lease expenses",
                "icon": "🏢"
            },
            {
                "name": "SERVICES",
                "description": "Professional services and consulting",
                "icon": "🤝"
            },
            {
                "name": "DATABASE",
                "description": "Database-related queries",
                "icon": "🗄️"
            },
            {
                "name": "FILESYSTEM",
                "description": "File system and document queries",
                "icon": "📁"
            },
            {
                "name": "GENERAL",
                "description": "General audit queries",
                "icon": "📊"
            }
        ]
    }

# Error Handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "error": "Not Found",
        "message": "The requested endpoint does not exist",
        "status_code": 404
    }

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {
        "error": "Internal Server Error",
        "message": "An unexpected error occurred",
        "status_code": 500
    }

# Startup/Shutdown Events
@app.on_event("startup")
async def startup_event():
    print("\n" + "="*60)
    print("🚀 FiscalPulse API Starting...")
    print("="*60)
    print("📊 Autonomous AI Audit Agent")
    print("🔗 API Docs: http://localhost:8000/docs")
    print("🌐 Frontend: http://localhost:3000")
    print("="*60 + "\n")

@app.on_event("shutdown")
async def shutdown_event():
    print("\n👋 FiscalPulse API Shutting down...")
