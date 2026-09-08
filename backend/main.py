from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent.core import Agent
from agent.tools import ToolRegistry

app = FastAPI(title="Local AI Agent API")

# Enable CORS so Next.js frontend (port 3000) can communicate with FastAPI (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ToolRegistry and Agent
registry = ToolRegistry()

@registry.register
def calculate_sum(a: int, b: int) -> int:
    """Adds two integers together."""
    return a + b

@registry.register
def multiply_numbers(a: float, b: float) -> float:
    """Multiplies two numbers together."""
    return a * b

agent = Agent(model_name="qwen2.5:3b", registry=registry)

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    response = agent.run(request.prompt)
    return ChatResponse(response=response)

@app.get("/health")
async def health_check():
    return {"status": "ok"}