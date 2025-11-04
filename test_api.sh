#!/bin/bash
# API Test Script for Emoji == Movie

BASE_URL="http://localhost:8000"

echo "🧪 Testing Emoji == Movie API"
echo "================================"
echo ""

# Test 1: Health Check
echo "1️⃣  Testing Health Check..."
response=$(curl -s -w "\n%{http_code}" $BASE_URL/health)
http_code=$(echo "$response" | tail -n 1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "200" ]; then
    echo "✅ Health check passed"
    echo "   Response: $body"
else
    echo "❌ Health check failed (HTTP $http_code)"
fi
echo ""

# Test 2: Get Puzzles
echo "2️⃣  Testing Get Puzzles..."
response=$(curl -s -w "\n%{http_code}" "$BASE_URL/api/puzzles?count=3")
http_code=$(echo "$response" | tail -n 1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "200" ]; then
    echo "✅ Get puzzles passed"
    echo "   Retrieved puzzles (sample):"
    echo "$body" | python3 -m json.tool 2>/dev/null | head -n 15
else
    echo "❌ Get puzzles failed (HTTP $http_code)"
fi
echo ""

# Test 3: Get Puzzles by Difficulty
echo "3️⃣  Testing Get Puzzles by Difficulty (Easy)..."
response=$(curl -s -w "\n%{http_code}" "$BASE_URL/api/puzzles?difficulty=Easy&count=2")
http_code=$(echo "$response" | tail -n 1)

if [ "$http_code" = "200" ]; then
    echo "✅ Get puzzles by difficulty passed"
else
    echo "❌ Get puzzles by difficulty failed (HTTP $http_code)"
fi
echo ""

# Test 4: Get Specific Puzzle
echo "4️⃣  Testing Get Specific Puzzle..."
response=$(curl -s -w "\n%{http_code}" "$BASE_URL/api/puzzle/lnk-1994-ez")
http_code=$(echo "$response" | tail -n 1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "200" ]; then
    echo "✅ Get specific puzzle passed"
    echo "   Puzzle: $body"
else
    echo "❌ Get specific puzzle failed (HTTP $http_code)"
fi
echo ""

# Test 5: Check Correct Guess
echo "5️⃣  Testing Correct Guess..."
response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/guess" \
    -H "Content-Type: application/json" \
    -d '{"puzzle_id":"lnk-1994-ez","guess":"the lion king"}')
http_code=$(echo "$response" | tail -n 1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "200" ]; then
    if echo "$body" | grep -q '"correct":true'; then
        echo "✅ Correct guess test passed"
        echo "   Response: $body"
    else
        echo "⚠️  Guess submitted but not marked correct"
    fi
else
    echo "❌ Guess check failed (HTTP $http_code)"
fi
echo ""

# Test 6: Check Incorrect Guess
echo "6️⃣  Testing Incorrect Guess..."
response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/guess" \
    -H "Content-Type: application/json" \
    -d '{"puzzle_id":"lnk-1994-ez","guess":"wrong movie"}')
http_code=$(echo "$response" | tail -n 1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "200" ]; then
    if echo "$body" | grep -q '"correct":false'; then
        echo "✅ Incorrect guess test passed"
        echo "   Response: $body"
    else
        echo "⚠️  Guess submitted but incorrectly marked"
    fi
else
    echo "❌ Guess check failed (HTTP $http_code)"
fi
echo ""

# Test 7: Reveal Answer
echo "7️⃣  Testing Reveal Answer..."
response=$(curl -s -w "\n%{http_code}" "$BASE_URL/api/reveal/lnk-1994-ez")
http_code=$(echo "$response" | tail -n 1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "200" ]; then
    echo "✅ Reveal answer passed"
    echo "   Answer details:"
    echo "$body" | python3 -m json.tool 2>/dev/null
else
    echo "❌ Reveal answer failed (HTTP $http_code)"
fi
echo ""

# Test 8: Get Daily Puzzle
echo "8️⃣  Testing Daily Puzzle..."
response=$(curl -s -w "\n%{http_code}" "$BASE_URL/api/daily")
http_code=$(echo "$response" | tail -n 1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "200" ]; then
    echo "✅ Daily puzzle passed"
    echo "   Today's puzzle:"
    echo "$body" | python3 -m json.tool 2>/dev/null
else
    echo "❌ Daily puzzle failed (HTTP $http_code)"
fi
echo ""

# Test 9: Metrics
echo "9️⃣  Testing Metrics Endpoint..."
response=$(curl -s -w "\n%{http_code}" "$BASE_URL/metrics")
http_code=$(echo "$response" | tail -n 1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "200" ]; then
    echo "✅ Metrics endpoint passed"
    echo "   Sample metrics:"
    echo "$body" | head -n 5
else
    echo "❌ Metrics endpoint failed (HTTP $http_code)"
fi
echo ""

# Test 10: Debug Info
echo "🔟 Testing Debug Endpoint..."
response=$(curl -s -w "\n%{http_code}" "$BASE_URL/debug")
http_code=$(echo "$response" | tail -n 1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "200" ]; then
    echo "✅ Debug endpoint passed"
    echo "   Debug info:"
    echo "$body" | python3 -m json.tool 2>/dev/null
else
    echo "❌ Debug endpoint failed (HTTP $http_code)"
fi
echo ""

# Test 11: Frontend
echo "1️⃣1️⃣  Testing Frontend (HTML)..."
response=$(curl -s -w "\n%{http_code}" "$BASE_URL/")
http_code=$(echo "$response" | tail -n 1)

if [ "$http_code" = "200" ]; then
    echo "✅ Frontend served successfully"
else
    echo "❌ Frontend failed to load (HTTP $http_code)"
fi
echo ""

echo "================================"
echo "✨ API Test Suite Complete!"
echo ""
echo "To test in browser, visit:"
echo "👉 $BASE_URL"
echo ""

