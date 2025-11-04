"""
Emoji == Movie FastAPI Backend
Production-ready backend for Databricks Apps deployment
"""

import json
import logging
import os
import random
import time
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Emoji == Movie",
    description="Guess the movie from emoji sequences",
    version="1.0.0"
)

# CORS Configuration - Allow all origins for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests for debugging Databricks Apps routing"""
    start_time = time.time()
    logger.info(f"Request: {request.method} {request.url.path}")
    logger.info(f"Headers: {dict(request.headers)}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} - {process_time:.3f}s")
    
    return response


# Pydantic Models
class MoviePuzzle(BaseModel):
    id: str
    emojis: str
    answers: List[str]
    year: int
    genre: List[str]
    difficulty: str
    explanation: str


class GuessRequest(BaseModel):
    puzzle_id: str
    guess: str


class GuessResponse(BaseModel):
    correct: bool
    message: str
    movie_title: Optional[str] = None


# Load movie puzzles data
def load_movies() -> List[Dict]:
    """Load movie puzzles from JSON file with multiple path resolution"""
    possible_paths = [
        Path(__file__).parent / "movies.json",
        Path("src/movies.json"),
        Path("movies.json"),
        Path("/app/src/movies.json"),  # Container path
    ]
    
    for path in possible_paths:
        if path.exists():
            logger.info(f"Loading movies from: {path}")
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
    
    logger.error(f"Movies file not found. Tried: {possible_paths}")
    # Return sample data as fallback
    return [{
        "id": "lnk-1994-ez",
        "emojis": "🦁👑🌅",
        "answers": ["the lion king", "lion king"],
        "year": 1994,
        "genre": ["Animation", "Adventure"],
        "difficulty": "Easy",
        "explanation": "Lion + crown = king; sunrise opening scene from Disney's classic."
    }]


# Load movies at startup
MOVIES = load_movies()
logger.info(f"Loaded {len(MOVIES)} movie puzzles")


# Helper Functions
def normalize_answer(text: str) -> str:
    """
    Normalize movie title for fuzzy matching
    - Lowercase, strip whitespace
    - Remove punctuation
    - Remove leading articles (the, a, an)
    """
    import re
    
    # Lowercase and strip
    text = text.lower().strip()
    
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    
    # Collapse multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading articles
    for article in ['the ', 'a ', 'an ']:
        if text.startswith(article):
            text = text[len(article):]
            break
    
    return text


def check_answer(puzzle: Dict, guess: str) -> bool:
    """Check if guess matches any accepted answer for the puzzle"""
    normalized_guess = normalize_answer(guess)
    
    for answer in puzzle['answers']:
        normalized_answer = normalize_answer(answer)
        if normalized_guess == normalized_answer:
            return True
    
    # Simple Levenshtein distance for typos (optional enhancement)
    # For now, exact match only after normalization
    return False


# API Endpoints

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serve the React frontend"""
    possible_paths = [
        Path(__file__).parent.parent / "public" / "index.html",
        Path("public/index.html"),
        Path("/app/public/index.html"),  # Container path
    ]
    
    for path in possible_paths:
        if path.exists():
            logger.info(f"Serving frontend from: {path}")
            return FileResponse(path)
    
    logger.error(f"Frontend not found. Tried: {possible_paths}")
    return HTMLResponse(
        content="<h1>Emoji == Movie</h1><p>Frontend not found. Please check deployment.</p>",
        status_code=500
    )


@app.get("/api/puzzles")
async def get_puzzles(difficulty: Optional[str] = None, count: int = 10):
    """
    Get random movie puzzles
    
    Query Parameters:
    - difficulty: Filter by difficulty (Easy/Medium/Hard)
    - count: Number of puzzles to return (default 10)
    """
    filtered_movies = MOVIES
    
    if difficulty:
        filtered_movies = [m for m in MOVIES if m['difficulty'].lower() == difficulty.lower()]
        if not filtered_movies:
            raise HTTPException(status_code=404, detail=f"No movies found for difficulty: {difficulty}")
    
    # Return random selection
    count = min(count, len(filtered_movies))
    selected = random.sample(filtered_movies, count)
    
    # Don't include answers in response
    return [
        {
            "id": m["id"],
            "emojis": m["emojis"],
            "year": m["year"],
            "genre": m["genre"],
            "difficulty": m["difficulty"]
        }
        for m in selected
    ]


@app.get("/api/puzzle/{puzzle_id}")
async def get_puzzle(puzzle_id: str):
    """Get a specific puzzle by ID (without answers)"""
    puzzle = next((m for m in MOVIES if m['id'] == puzzle_id), None)
    
    if not puzzle:
        raise HTTPException(status_code=404, detail="Puzzle not found")
    
    return {
        "id": puzzle["id"],
        "emojis": puzzle["emojis"],
        "year": puzzle["year"],
        "genre": puzzle["genre"],
        "difficulty": puzzle["difficulty"]
    }


@app.post("/api/guess")
async def check_guess(request: GuessRequest) -> GuessResponse:
    """Check if a guess is correct"""
    puzzle = next((m for m in MOVIES if m['id'] == request.puzzle_id), None)
    
    if not puzzle:
        raise HTTPException(status_code=404, detail="Puzzle not found")
    
    is_correct = check_answer(puzzle, request.guess)
    
    if is_correct:
        # Return the official title (first answer)
        official_title = puzzle['answers'][0].title()
        return GuessResponse(
            correct=True,
            message=f"Correct! It's {official_title} ({puzzle['year']})",
            movie_title=official_title
        )
    else:
        return GuessResponse(
            correct=False,
            message="Not quite! Try again or use a hint."
        )


@app.get("/api/reveal/{puzzle_id}")
async def reveal_answer(puzzle_id: str):
    """Reveal the answer and explanation for a puzzle"""
    puzzle = next((m for m in MOVIES if m['id'] == puzzle_id), None)
    
    if not puzzle:
        raise HTTPException(status_code=404, detail="Puzzle not found")
    
    official_title = puzzle['answers'][0].title()
    return {
        "id": puzzle["id"],
        "title": official_title,
        "year": puzzle["year"],
        "genre": puzzle["genre"],
        "difficulty": puzzle["difficulty"],
        "explanation": puzzle["explanation"],
        "emojis": puzzle["emojis"]
    }


@app.get("/api/daily")
async def get_daily_puzzle():
    """Get today's daily puzzle (deterministic based on date)"""
    from datetime import datetime
    
    # Use current date as seed for reproducible random selection
    today = datetime.now().date()
    seed = int(today.strftime("%Y%m%d"))
    random.seed(seed)
    
    puzzle = random.choice(MOVIES)
    
    # Reset random seed
    random.seed()
    
    return {
        "id": puzzle["id"],
        "emojis": puzzle["emojis"],
        "year": puzzle["year"],
        "genre": puzzle["genre"],
        "difficulty": puzzle["difficulty"],
        "date": today.isoformat()
    }


# Health Check Endpoints

@app.get("/health")
@app.get("/healthz")
@app.get("/ready")
@app.get("/ping")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "emoji-movie-app",
        "movies_loaded": len(MOVIES),
        "timestamp": time.time()
    }


@app.get("/metrics")
async def metrics():
    """Prometheus-style metrics"""
    return f"""# HELP movies_loaded Number of movie puzzles loaded
# TYPE movies_loaded gauge
movies_loaded {len(MOVIES)}

# HELP app_info Application information
# TYPE app_info gauge
app_info{{version="1.0.0",service="emoji-movie-app"}} 1
"""


@app.get("/debug")
async def debug_info():
    """Debug endpoint for troubleshooting deployment"""
    return {
        "environment": os.getenv("ENVIRONMENT", "unknown"),
        "port": os.getenv("PORT", "unknown"),
        "host": os.getenv("HOST", "unknown"),
        "cwd": os.getcwd(),
        "files": {
            "movies_json_exists": any(Path(p).exists() for p in [
                "src/movies.json",
                "movies.json",
                Path(__file__).parent / "movies.json"
            ]),
            "index_html_exists": any(Path(p).exists() for p in [
                "public/index.html",
                Path(__file__).parent.parent / "public" / "index.html"
            ])
        },
        "movies_count": len(MOVIES),
        "python_path": os.getenv("PYTHONPATH", "not set")
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    """Log startup information"""
    logger.info("=" * 60)
    logger.info("🎬 Emoji == Movie Application Starting")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    logger.info(f"Port: {os.getenv('PORT', '8000')}")
    logger.info(f"Movies loaded: {len(MOVIES)}")
    logger.info(f"Working directory: {os.getcwd()}")
    logger.info("=" * 60)


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )

