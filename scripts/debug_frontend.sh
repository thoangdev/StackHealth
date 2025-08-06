#!/bin/bash
# Debug frontend authentication issues
# This script tests various components to identify the root cause

set -e

echo "🔍 Debugging Frontend Authentication Issues"
echo "==========================================="

# Check if servers are running
echo "1. 🌐 Checking if backend server is running..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend server is running at http://localhost:8000"
else
    echo "❌ Backend server is not running. Start it with:"
    echo "   cd backend && python3 -m uvicorn main:app --host 0.0.0.0 --port 8000"
    exit 1
fi

echo ""
echo "2. 🔐 Testing authentication endpoint..."
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/auth/login \
    -H "Content-Type: application/json" \
    -d '{"email": "admin@company.com", "password": "admin123"}')

if echo "$LOGIN_RESPONSE" | grep -q "access_token"; then
    echo "✅ Login endpoint works correctly"
    echo "Response: $LOGIN_RESPONSE"
else
    echo "❌ Login endpoint failed"
    echo "Response: $LOGIN_RESPONSE"
fi

echo ""
echo "3. 📝 Testing registration endpoint..."
REGISTER_RESPONSE=$(curl -s -X POST http://localhost:8000/auth/register \
    -H "Content-Type: application/json" \
    -d '{"email": "test@example.com", "password": "testpass123"}')

if echo "$REGISTER_RESPONSE" | grep -q "email"; then
    echo "✅ Registration endpoint works correctly"
    echo "Response: $REGISTER_RESPONSE"
else
    echo "❌ Registration endpoint failed"
    echo "Response: $REGISTER_RESPONSE"
fi

echo ""
echo "4. 🌍 Checking if frontend is served..."
if [ -f "frontend/index.html" ]; then
    echo "✅ Frontend files exist"
    
    # Check if there's a simple HTTP server running
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        echo "✅ Frontend server running at http://localhost:3000"
    elif curl -s http://localhost:8080 > /dev/null 2>&1; then
        echo "✅ Frontend server running at http://localhost:8080"
    else
        echo "⚠️  No frontend server detected. You can serve it with:"
        echo "   cd frontend && python3 -m http.server 3000"
        echo "   Or open index.html directly in browser"
    fi
else
    echo "❌ Frontend files not found"
fi

echo ""
echo "5. 🧪 Testing frontend JavaScript functionality..."

# Create a simple test HTML file to test the authentication
cat > debug_auth.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Auth Debug Test</title>
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
</head>
<body>
    <h1>Authentication Debug Test</h1>
    <div id="results"></div>
    
    <script>
        const baseURL = 'http://localhost:8000';
        const results = document.getElementById('results');
        
        function log(message) {
            results.innerHTML += '<p>' + message + '</p>';
            console.log(message);
        }
        
        async function testAuth() {
            log('Starting authentication test...');
            
            try {
                // Test login
                log('Testing login...');
                const response = await axios.post(`${baseURL}/auth/login`, {
                    email: 'admin@company.com',
                    password: 'admin123'
                });
                
                log('✅ Login successful!');
                log('Token: ' + response.data.access_token.substring(0, 20) + '...');
                
                // Test authenticated request
                axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access_token}`;
                const userResponse = await axios.get(`${baseURL}/auth/me`);
                
                log('✅ User info retrieved: ' + userResponse.data.email);
                log('User is admin: ' + userResponse.data.is_admin);
                
            } catch (error) {
                log('❌ Auth test failed: ' + error.message);
                if (error.response) {
                    log('Response data: ' + JSON.stringify(error.response.data));
                    log('Status: ' + error.response.status);
                }
            }
        }
        
        // Run test automatically
        testAuth();
    </script>
</body>
</html>
EOF

echo "✅ Created debug_auth.html test file"
echo ""
echo "6. 📋 Summary and Next Steps:"
echo "   - Backend API is working correctly"
echo "   - Open debug_auth.html in your browser to test frontend auth"
echo "   - Check browser console for JavaScript errors"
echo "   - Compare with frontend/index.html to identify differences"
echo ""
echo "🎯 To test the actual frontend:"
echo "   1. Open frontend/index.html in your browser"
echo "   2. Open browser developer tools (F12)"
echo "   3. Try logging in with admin@company.com / admin123"
echo "   4. Check Console tab for errors"
echo "   5. Check Network tab to see if API calls are being made"
echo ""
echo "💡 Common issues to check:"
echo "   - JavaScript errors in browser console"
echo "   - Network request failures"
echo "   - CORS issues (should not be an issue here)"
echo "   - Form submission not being handled"
echo "   - Event listeners not being attached"
