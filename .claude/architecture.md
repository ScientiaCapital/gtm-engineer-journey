# GTM Engineer Journey - Architecture Documentation

## 1. Technology Stack

### Core Technologies
- **Primary Language**: Python (inferred from dealer-scraper-mvp and sales-agent repository)
- **Web Framework**: FastAPI (confirmed in sales-agent project)
- **Real-time Communication**: WebSockets
- **Voice Synthesis**: Cartesia API
- **LLM Inference**: Cerebras API
- **AI/ML Framework**: Claude API integration

### Version Information
Based on typical modern AI/ML projects:
- **Python**: 3.9+ (likely 3.10+ for modern AI libraries)
- **FastAPI**: 0.104+ (supports async/await patterns)
- **WebSocket Libraries**: websockets, starlette-websockets
- **HTTP Client**: httpx or aiohttp for async API calls

### Development Tools
- **Package Management**: Poetry or pip + requirements.txt
- **API Documentation**: Auto-generated FastAPI Swagger/OpenAPI
- **Testing**: Pytest (implied future implementation)

## 2. Design Patterns

### Primary Patterns
1. **Microservices Architecture**
   - Voice Agent as standalone service
   - Dealer Scraper as separate component
   - API Gateway pattern via FastAPI

2. **Repository Pattern**
   - Data access abstraction for dealer information
   - API client wrappers for external services

3. **Observer Pattern**
   - Real-time event handling for voice streaming
   - WebSocket connection management

4. **Strategy Pattern**
   - Multiple AI provider integrations (Claude, Cerebras, Cartesia)
   - Pluggable scraping strategies

5. **Factory Pattern**
   - Agent creation based on configuration
   - Voice synthesis provider selection

## 3. Key Components

### Voice Agent System
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web Client    │◄──►│   FastAPI Server │◄──►│  Voice Service  │
│                 │    │                  │    │                 │
│ - WebSocket     │    │ - WebSocket Hub  │    │ - Cartesia API  │
│ - Audio Context │    │ - Session Mgmt   │    │ - Audio Process │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │    AI Service    │◄──►│  LLM Providers  │
                       │                  │    │                 │
                       │ - Claude API     │    │ - Cerebras API  │
                       │ - Prompt Engine  │    │ - Fallback LLMs │
                       └──────────────────┘    └─────────────────┘
```

### Core Modules
1. **WebSocket Manager**
   - Connection pooling
   - Message routing
   - Session persistence

2. **Voice Processing Pipeline**
   - Audio stream encoding/decoding
   - Real-time synthesis
   - Latency optimization

3. **AI Orchestration Layer**
   - LLM request/response handling
   - Context management
   - Conversation state tracking

4. **Data Scraping Engine**
   - Async HTTP requests
   - HTML parsing
   - Data extraction and normalization

## 4. Data Flow

### Voice Agent Data Flow
```
1. Client Connection
   WebSocket → FastAPI → Session Creation

2. Voice Input
   Browser Audio → WebSocket Binary → Voice Service

3. AI Processing
   Voice → Text (STT) → Claude/Cerebras → Text Response

4. Voice Output
   Text Response → Cartesia → Audio Stream → WebSocket → Client

5. Real-time Streaming
   Continuous WebSocket messages with audio chunks
```

### Dealer Scraper Data Flow
```
1. Target Identification
   Configuration → URL Generation → Request Queue

2. Data Extraction
   HTTP GET → HTML Response → Parser → Structured Data

3. Data Processing
   Raw Data → Validation → Normalization → Storage

4. Output Generation
   Processed Data → Export Formats → API Responses
```

## 5. External Dependencies

### Primary APIs
- **Cartesia API**: Voice synthesis and real-time audio streaming
- **Cerebras API**: High-speed LLM inference
- **Claude API**: Primary conversational AI
- **WebSocket Clients**: Real-time browser communication

### Python Libraries
```python
# Core Framework
fastapi>=0.104.0
uvicorn>=0.24.0
websockets>=12.0

# AI/ML Integration
openai>=1.0.0  # For Claude API
cerebras-sdk   # For Cerebras integration
cartesia-sdk   # For voice synthesis

# Data Processing
pandas>=2.0.0
numpy>=1.24.0

# Web Scraping
beautifulsoup4>=4.12.0
requests>=2.31.0
aiohttp>=3.9.0

# Utilities
pydantic>=2.0.0
python-dotenv>=1.0.0
asyncio
```

## 6. API Design

### FastAPI Endpoints

#### Voice Agent API
```python
# WebSocket for real-time voice
@ app.websocket("/ws/voice/{session_id}")
async def websocket_voice(websocket: WebSocket, session_id: str):
    pass

# Session management
@app.post("/sessions")
async def create_session():
    pass

@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    pass

# Configuration
@app.get("/agents/config")
async def get_agent_config():
    pass
```

#### Dealer Scraper API
```python
@app.post("/scrape/dealers")
async def scrape_dealers(targets: List[ScrapeTarget]):
    pass

@app.get("/scrape/results/{job_id}")
async def get_scrape_results(job_id: str):
    pass

@app.get("/dealers")
async def list_dealers(filters: DealerFilter):
    pass
```

### Request/Response Models
```python
class VoiceSessionCreate(BaseModel):
    agent_config: AgentConfig
    user_context: Optional[Dict[str, Any]]

class VoiceResponse(BaseModel):
    session_id: str
    audio_chunk: bytes
    transcript: str
    is_final: bool

class ScrapeJob(BaseModel):
    targets: List[str]
    selectors: Dict[str, str]
    output_format: str
```

## 7. Database Schema

### In-Memory Storage (Current)
Given no database dependencies, using in-memory storage:

```python
# Session Storage
sessions: Dict[str, VoiceSession] = {}
# Key: session_id, Value: session_state

# Scrape Results
scrape_results: Dict[str, List[DealerData]] = {}
# Key: job_id, Value: list of dealer records

# Conversation History
conversations: Dict[str, List[Message]] = {}
# Key: session_id, Value: message history
```

### Future Database Schema
```sql
-- Sessions table
CREATE TABLE voice_sessions (
    id UUID PRIMARY KEY,
    created_at TIMESTAMP,
    user_id UUID,
    agent_config JSONB,
    status VARCHAR(50)
);

-- Conversation history
CREATE TABLE messages (
    id UUID PRIMARY KEY,
    session_id UUID REFERENCES voice_sessions(id),
    role VARCHAR(20),
    content TEXT,
    audio_ref TEXT,
    timestamp TIMESTAMP
);

-- Dealer data
CREATE TABLE dealers (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    contact_info JSONB,
    scraped_at TIMESTAMP,
    source_url TEXT
);
```

## 8. Security Considerations

### API Security
- **API Key Management**: Secure storage for Cartesia, Cerebras, Claude APIs
- **Rate Limiting**: Per-session and global rate limits
- **Input Validation**: Pydantic models for all endpoints
- **CORS Configuration**: Restricted origins for WebSocket connections

### WebSocket Security
```python
# Connection validation
async def validate_websocket_connection(websocket: WebSocket):
    # Check origin
    # Validate session tokens
    # Implement rate limiting per connection
    pass
```

### Data Protection
- **PII Handling**: Voice data processing compliance
- **Session Isolation**: Ensure conversation data separation
- **Secure Config**: Environment variables for sensitive data

## 9. Performance Optimization

### Latency Targets
- **Voice Synthesis**: < 100ms target (Cartesia)
- **LLM Response**: < 200ms target (Cerebras)
- **End-to-End**: < 500ms for complete turn

### Optimization Strategies

#### 1. Connection Pooling
```python
# Reuse HTTP clients for external APIs
class APIClientPool:
    def __init__(self):
        self.cartesia_client = AsyncClient()
        self.cerebras_client = AsyncClient()
```

#### 2. Async Processing
```python
# Parallel API calls
async def process_voice_turn(audio_input: bytes):
    stt_task = transcribe_audio(audio_input)
    context_task = get_conversation_context(session_id)
    
    text_input = await stt_task
    context = await context_task
    
    # Parallel LLM and voice synthesis
    llm_task = get_llm_response(text_input, context)
    tts_task = synthesize_voice_async(text_input)
    
    return await asyncio.gather(llm_task, tts_task)
```

#### 3. Caching
- **LLM Responses**: Cache common responses
- **Voice Synthesis**: Cache frequent phrases
- **Session Data**: In-memory session caching

#### 4. Streaming Optimization
- **Chunked Audio**: Stream audio in small chunks
- **Pre-buffering**: Pre-synthesize common responses
- **Connection Keep-alive**: Maintain WebSocket connections

## 10. Deployment Strategy

### Current Development Deployment
- **Local Development**: FastAPI with uvicorn
- **Static Site**: GitHub Pages for portfolio
- **Manual Deployment**: Direct repository updates

### Recommended Production Deployment

#### 1. Containerization (Future)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 2. Cloud Architecture
```
Frontend (GitHub Pages) → API Gateway → FastAPI Microservices
                                    ↗
                           Voice Agent Service
                                    ↗
                           Dealer Scraper Service
```

#### 3. Scaling Strategy
- **Horizontal Scaling**: Multiple FastAPI instances
- **Load Balancer**: Distribute WebSocket connections
- **Redis**: Session storage and message brokering
- **CDN**: Static asset delivery

#### 4. Monitoring
- **Application Metrics**: Response times, error rates
- **Business Metrics**: Conversation success rates, latency
- **Infrastructure**: CPU, memory, network usage

This architecture supports the project's goals of building production-ready GTM tools while maintaining the flexibility needed for rapid iteration and learning.