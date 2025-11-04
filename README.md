# 🎬 Emojis == Movie

A fun, retro-styled web game where players guess movie titles from emoji sequences! Built with FastAPI backend and single-file React frontend, designed for seamless local development and Databricks Apps deployment.

![Game Preview](https://img.shields.io/badge/Game-Emoji%20Movie%20Quiz-purple?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-0.83+-green?style=for-the-badge)
![React](https://img.shields.io/badge/React-18-blue?style=for-the-badge)
![Tailwind](https://img.shields.io/badge/Tailwind-CSS-cyan?style=for-the-badge)

## ✨ Features

### 🎮 Game Features
- **30+ Movie Puzzles** across Easy, Medium, and Hard difficulties
- **Progressive Hints System** - Year, Genre, and First Letter hints
- **Timer-Based Challenge** - 30-second countdown per puzzle
- **Daily Puzzle Mode** - Get a new puzzle every day (deterministic by date)
- **Fuzzy Answer Matching** - Accepts variations and ignores articles
- **Confetti Celebrations** - Animated confetti on correct answers

### 🎨 UI/UX Features
- **Retro 80s Pixel Art Style** - Fun, colorful, nostalgic design
- **Two-Column Layout** - Puzzle card + Answer/Meta card
- **Responsive Design** - Mobile-friendly, stacks to single column
- **Smooth Animations** - Bounce-in effects, shake on wrong answer, confetti
- **Accessibility** - Screen-reader friendly
- **Loading States** - Proper feedback during API calls
- **Error Handling** - Graceful degradation with user-friendly messages

### 🔧 Technical Features
- **Single-File Frontend** - No build process required, CDN-based React + Tailwind
- **FastAPI Backend** - Modern async Python with comprehensive API
- **RESTful API** - Clean endpoints for puzzles, guessing, hints, and reveals
- **Health Checks** - Multiple monitoring endpoints for production
- **Request Logging** - Comprehensive debugging for Databricks Apps
- **Multiple Path Resolution** - Works in different container environments
- **Prometheus Metrics** - Ready for monitoring integration

---

## 📁 Project Structure

```
emoji-movie-app/
├── app.yaml              # Databricks Apps configuration
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── .gitignore           # Git ignore rules
├── src/
│   ├── app.py           # FastAPI backend entry point
│   └── movies.json      # Movie puzzle database (30+ movies)
└── public/
    └── index.html       # Single-file React + Tailwind frontend
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Modern web browser

### Local Development Setup

1. **Clone or navigate to the project directory**
```bash
cd emoji-movie-app
```

2. **Create a virtual environment (recommended)**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create environment file (optional)**
```bash
# Create .env file for custom configuration
echo "PORT=8000" > .env
echo "HOST=0.0.0.0" >> .env
echo "ENVIRONMENT=development" >> .env
```

5. **Run the application**
```bash
# Method 1: Using uvicorn directly
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload

# Method 2: Using Python module
python -m uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
```

6. **Open your browser**
```
http://localhost:8000
```

🎉 **You're ready to play!**

---

## 🎮 How to Play

1. **View the Emoji Sequence** - Each puzzle shows 2-6 emojis representing a movie
2. **Type Your Guess** - Enter the movie title in the input field
3. **Use Hints if Needed** - Reveal Year, Genre, or First Letter
4. **Beat the Timer** - 30 seconds to guess each movie

---

## 🔌 API Documentation

### Base URL
```
Local: http://localhost:8000
```

### Endpoints

#### `GET /`
Serves the React frontend application

#### `GET /api/puzzles`
Get random movie puzzles
- **Query Parameters**:
  - `difficulty` (optional): Filter by "Easy", "Medium", or "Hard"
  - `count` (optional): Number of puzzles (default: 10)
- **Response**: Array of puzzle objects (without answers)

#### `GET /api/puzzle/{puzzle_id}`
Get a specific puzzle by ID

#### `POST /api/guess`
Check if a guess is correct
- **Body**: `{ "puzzle_id": "string", "guess": "string" }`
- **Response**: `{ "correct": boolean, "message": "string", "movie_title": "string" }`

#### `GET /api/reveal/{puzzle_id}`
Reveal the answer and explanation for a puzzle

#### `GET /api/daily`
Get today's daily puzzle (deterministic by date)

#### `GET /health`, `/healthz`, `/ready`, `/ping`
Health check endpoints for monitoring

#### `GET /metrics`
Prometheus-style metrics

#### `GET /debug`
Debug information for troubleshooting deployment

---

## 📊 Movie Puzzle Format

Each puzzle in `src/movies.json` follows this structure:

```json
{
  "id": "lnk-1994-ez",
  "emojis": "🦁👑🌅",
  "answers": ["the lion king", "lion king"],
  "year": 1994,
  "genre": ["Animation", "Adventure"],
  "difficulty": "Easy",
  "explanation": "Lion + crown = king; sunrise opening scene from Disney's classic."
}
```

### Adding Your Own Movies
1. Open `src/movies.json`
2. Add a new object with the required fields
3. Use lowercase for answers (normalization is automatic)
4. Include multiple answer variations for better UX
5. Restart the server to load new puzzles

---

## 🏗️ Databricks Apps Deployment

### Prerequisites
- Databricks workspace with Apps enabled
- Databricks CLI configured
- App secrets configured (if needed)

### Deployment Steps

1. **Ensure your code is ready**
```bash
# Test locally first!
uvicorn src.app:app --host 0.0.0.0 --port 8000
```

2. **Deploy to Databricks Apps**
```bash
databricks apps deploy emoji-movie-app --source-code-path /path/to/emoji-movie-app
```

3. **Verify deployment**
- Check Databricks Apps dashboard
- Access your app URL
- Test health endpoint: `https://your-app-url/health`

### Databricks Apps Configuration

The `app.yaml` file configures the deployment:
```yaml
command: [
  "uvicorn",
  "src.app:app",
  "--host", "0.0.0.0",
  "--port", "8000"
]

env:
  - name: 'PORT'
    value: "8000"
  - name: 'HOST'
    value: "0.0.0.0"
  - name: 'ENVIRONMENT'
    value: "production"
```

### Important Notes
- **Port 8000 is required** - Don't change this for Databricks Apps
- File sizes must be under 10MB each
- All files must be in the source directory
- Health checks should respond within 5 seconds

---

## 🧪 Testing

### Manual Testing Checklist

**Game Flow**
- [ ] Puzzles load correctly
- [ ] Timer counts down properly
- [ ] Correct answers are recognized
- [ ] Incorrect answers show feedback
- [ ] Hints reveal correctly
- [ ] Skip functionality works
- [ ] Next puzzle loads seamlessly

**Game Mechanics**
- [ ] Hints reveal correctly
- [ ] Difficulty levels display properly

**UI/UX**
- [ ] Responsive on mobile
- [ ] Animations play smoothly
- [ ] Confetti appears on correct guess

**API**
- [ ] All endpoints respond correctly
- [ ] Error handling works
- [ ] Health checks return 200
- [ ] CORS allows frontend requests

### API Testing with curl

```bash
# Health check
curl http://localhost:8000/health

# Get puzzles
curl http://localhost:8000/api/puzzles?difficulty=Easy&count=5

# Check a guess
curl -X POST http://localhost:8000/api/guess \
  -H "Content-Type: application/json" \
  -d '{"puzzle_id":"lnk-1994-ez","guess":"the lion king"}'

# Reveal answer
curl http://localhost:8000/api/reveal/lnk-1994-ez

# Get daily puzzle
curl http://localhost:8000/api/daily

# Debug info
curl http://localhost:8000/debug
```

---

## 🛠️ Development

### Environment Variables

Create a `.env` file in the root directory:

```bash
# Application Configuration
PORT=8000
HOST=0.0.0.0
ENVIRONMENT=development
```

### Hot Reload for Development

The `--reload` flag enables automatic reloading when code changes:
```bash
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
```

### Adding New Features

**Backend (src/app.py)**
- Add new endpoints after existing ones
- Use Pydantic models for request/response validation
- Add logging for debugging
- Update health checks if needed

**Frontend (public/index.html)**
- Edit the `<script type="text/babel">` section
- Use React hooks for state management
- Tailwind classes for styling
- Test in browser console for errors

**Movie Data (src/movies.json)**
- Follow existing JSON structure
- Ensure IDs are unique
- Test answer normalization
- Add varied difficulty levels

---

## 🎨 UI Customization

### Color Scheme
The app uses a retro 80s theme defined in Tailwind config:
```javascript
colors: {
  retro: {
    purple: '#8B5CF6',
    pink: '#EC4899',
    cyan: '#06B6D4',
    yellow: '#FBBF24',
  }
}
```

### Fonts
- **Game Title**: Press Start 2P (pixel font)
- **UI Text**: Courier New (monospace)

### Animations
- `bounce-in`: Entry animations for new content
- `shake`: Wrong answer feedback
- `confetti`: Celebration on correct guess
- `pulse-glow`: Button highlights

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: App won't start
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check port availability
lsof -i :8000  # On Linux/Mac
```

**Issue**: Movies not loading
```bash
# Verify movies.json exists
ls -la src/movies.json

# Check JSON syntax
python -m json.tool src/movies.json
```

**Issue**: Frontend not displaying
```bash
# Verify index.html exists
ls -la public/index.html

# Check browser console for errors
# Open browser DevTools (F12) and check Console tab
```

**Issue**: CORS errors
- Ensure CORS middleware is enabled in `src/app.py`
- Check browser console for specific CORS errors
- Verify API calls use correct URL

**Issue**: Databricks Apps deployment fails
- Verify `app.yaml` syntax
- Check file sizes (must be <10MB)
- Ensure port is set to 8000
- Review Databricks Apps logs

### Debug Mode

Enable detailed logging:
```python
# In src/app.py, change logging level
logging.basicConfig(level=logging.DEBUG)
```

Visit `/debug` endpoint for system information:
```bash
curl http://localhost:8000/debug
```

---

## 📈 Performance Optimization

### Backend
- Movies loaded once at startup (cached in memory)
- Async handlers for non-blocking operations
- Minimal dependencies for fast cold starts
- Efficient JSON parsing

### Frontend
- Single HTML file (no bundling needed)
- CDN-hosted libraries (cached by browser)
- LocalStorage for persistence (no backend state)
- Minimal re-renders with React hooks
- CSS animations (GPU accelerated)

---

## 🔐 Security Considerations

- No authentication required (public game)
- No sensitive data stored
- CORS enabled for frontend access
- Input validation on all endpoints
- No user-generated content vulnerabilities
- Rate limiting recommended for production

---

## 🤝 Contributing

Want to add more movies or features?

1. Fork the repository
2. Create a feature branch
3. Add your movies to `src/movies.json`
4. Test locally
5. Submit a pull request

**Movie Contribution Guidelines**:
- Include explanation of emoji choices
- Add multiple answer variations
- Use appropriate difficulty rating
- Verify emoji render on all platforms
- Test answer normalization

---

## 📝 License

This project is open source and available for educational purposes.

---

## 🎯 Roadmap

**Planned Features**:
- [ ] Lightning Mode (60s, multiple puzzles in rapid succession)
- [ ] Social sharing (share daily puzzle results)
- [ ] More movie categories (by decade, genre)
- [ ] Multiplayer mode
- [ ] Achievement system
- [ ] Sound effects toggle
- [ ] Dark/light theme toggle
- [ ] Accessibility improvements
- [ ] Mobile app version

---

## 💡 Tips for Playing

1. **Try without hints first** - Challenge yourself before revealing hints
2. **Think about the emojis** - Each one represents something about the movie
3. **Learn patterns** - Common emoji combinations for genres and themes
4. **Try Daily Mode** - Compare with friends on the same puzzle

---

## 📞 Support

**Having issues?**
- Check the Troubleshooting section above
- Review `/debug` endpoint output
- Check browser console for errors
- Verify all files are in correct locations
- Ensure Python dependencies are installed

**Feature requests?**
- Open an issue with detailed description
- Include use case and mockups if possible

---

## 🌟 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - UI library
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS
- [Uvicorn](https://www.uvicorn.org/) - ASGI server

Special thanks to all movie lovers and emoji enthusiasts! 🎬🎉

---

**Made with ❤️ for Databricks Apps**

Enjoy the game! 🎮🎬🎉

