#!/bin/bash
# Test the fixed frontend authentication

echo "🔧 Testing Fixed Frontend Authentication"
echo "======================================="

# Check if backend is running
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "❌ Backend server is not running. Please start it first:"
    echo "   cd backend && python3 -m uvicorn main:app --host 0.0.0.0 --port 8000"
    exit 1
fi

echo "✅ Backend server is running"

# Start a simple HTTP server for the frontend if not already running
if ! curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "🌐 Starting frontend server..."
    cd frontend
    python3 -m http.server 3000 &
    SERVER_PID=$!
    echo $SERVER_PID > ../frontend_server.pid
    sleep 2
    cd ..
    echo "✅ Frontend server started at http://localhost:3000"
else
    echo "✅ Frontend server already running at http://localhost:3000"
fi

echo ""
echo "🎯 Testing Instructions:"
echo "========================"
echo "1. Open your browser and go to: http://localhost:3000"
echo "2. Open browser developer tools (F12)"
echo "3. Test the following:"
echo ""
echo "   📝 Create Account Test:"
echo "   - Click 'Create Account' tab"
echo "   - Should switch to registration form"
echo "   - Fill out the form and submit"
echo "   - Check console for debug messages"
echo ""
echo "   🔐 Login Test:"
echo "   - Use credentials: admin@company.com / admin123"
echo "   - Should login successfully and show dashboard"
echo "   - Check console for debug messages"
echo ""
echo "💡 What to check in browser console:"
echo "   - 'Attempting login with:' message shows correct baseURL"
echo "   - Network requests go to http://localhost:8000"
echo "   - No JavaScript errors"
echo ""
echo "🛠️ Fixes Applied:"
echo "   ✅ Fixed baseURL detection to always use port 8000 for API"
echo "   ✅ Improved switchAuthTab method for better tab switching"
echo "   ✅ Added detailed error logging and better error messages"
echo "   ✅ Added console debugging for authentication attempts"
echo ""
echo "Press Ctrl+C to stop the frontend server when done testing..."

# Wait for user to stop the server
trap 'echo "🛑 Stopping frontend server..."; kill $SERVER_PID 2>/dev/null; rm -f frontend_server.pid; exit 0' INT

# Keep script running
if [ ! -z "$SERVER_PID" ]; then
    wait $SERVER_PID
fi
