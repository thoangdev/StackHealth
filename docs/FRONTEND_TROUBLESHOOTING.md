# Frontend Authentication Troubleshooting Guide

This guide helps resolve common authentication issues in the StackHealth frontend.

## Quick Fix Summary

The main issues were:

1. **❌ Base URL Detection**: Frontend was incorrectly detecting API URL as `http://localhost:3000` instead of `http://localhost:8000`
2. **❌ Tab Switching**: "Create Account" button wasn't working due to incorrect DOM selector
3. **❌ Error Messages**: Generic "Unknown error" messages weren't helpful for debugging

### ✅ Applied Fixes

1. **Fixed Base URL Detection**
   ```javascript
   // OLD (incorrect)
   const port = window.location.hostname === 'localhost' ? ':8000' : '';
   
   // NEW (correct)
   if (hostname === 'localhost' || hostname === '127.0.0.1') {
       return `${protocol}//${hostname}:8000`;
   }
   ```

2. **Fixed Tab Switching**
   ```javascript
   // OLD (unreliable)
   document.querySelector(`#authSection .tab:nth-child(${tab === 'login' ? 1 : 2})`)
   
   // NEW (reliable)
   const tabButtons = document.querySelectorAll('#authSection .tab');
   if (tab === 'login') {
       tabButtons[0].classList.add('active');
   }
   ```

3. **Enhanced Error Reporting**
   - Added console logging for debugging
   - Better error message categorization
   - Network vs server vs unknown error distinction

## Testing the Fixes

### Method 1: Automated Test
```bash
make test-frontend
```

### Method 2: Manual Test
1. Start backend: `cd backend && python3 -m uvicorn main:app --host 0.0.0.0 --port 8000`
2. Start frontend: `cd frontend && python3 -m http.server 3000`
3. Open: http://localhost:3000
4. Test login with: `admin@company.com` / `admin123`

### Method 3: Debug Mode
1. Open browser developer tools (F12)
2. Check Console tab for debug messages
3. Check Network tab for API requests
4. Look for these log messages:
   - `Attempting login with: {email, baseURL}`
   - `Login successful:` or `Login error:`

## Common Issues and Solutions

### Issue: "Network error - could not connect to server"
**Cause**: Backend server not running or wrong URL
**Solution**: 
- Check if backend is running: `curl http://localhost:8000/health`
- Start backend: `cd backend && python3 -m uvicorn main:app --host 0.0.0.0 --port 8000`

### Issue: "Create Account" button does nothing
**Cause**: Tab switching JavaScript not working
**Solution**: 
- Check browser console for JavaScript errors
- Ensure `switchAuthTab` function is defined globally
- Verify HTML onclick handlers: `onclick="switchAuthTab('register')"`

### Issue: "Login failed: Unknown error"
**Cause**: Multiple possible causes
**Debug Steps**:
1. Open browser console and look for detailed error messages
2. Check Network tab to see if request reaches the server
3. Verify API endpoint responds: `curl -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d '{"email":"admin@company.com","password":"admin123"}'`

### Issue: Login appears to work but dashboard doesn't load
**Cause**: Authentication token not properly stored or used
**Debug Steps**:
1. Check localStorage for `authToken`
2. Verify token is included in subsequent requests
3. Check `/auth/me` endpoint response

## Environment Setup

### Prerequisites
- Python 3.7+
- Backend dependencies installed (`pip install -r backend/requirements.txt`)
- Modern web browser with JavaScript enabled

### Backend Setup
```bash
cd backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd frontend
python3 -m http.server 3000
# OR open index.html directly in browser
```

### Sample Data Setup (Optional)
```bash
python3 scripts/create_enhanced_sample_data.py
```

## Configuration

### Default Credentials
- **Email**: `admin@company.com`
- **Password**: `admin123`
- **Role**: Administrator

### API Endpoints
- **Login**: `POST /auth/login`
- **Register**: `POST /auth/register`
- **User Info**: `GET /auth/me`
- **Health Check**: `GET /health`

### Frontend URLs
- **Development**: http://localhost:3000
- **API Base**: http://localhost:8000

## Browser Developer Tools

### Console Tab
Look for these messages:
```
✅ Good: "Attempting login with: {email: 'admin@company.com', baseURL: 'http://localhost:8000'}"
❌ Bad: "Attempting login with: {email: 'admin@company.com', baseURL: 'http://localhost:3000'}"
```

### Network Tab
Check for:
- Request to `http://localhost:8000/auth/login`
- Status 200 for successful login
- Response contains `access_token`

### Application Tab
Check for:
- localStorage item `authToken` after successful login
- Token value should start with `eyJ` (JWT format)

## Debugging Commands

### Test Backend API
```bash
# Health check
curl http://localhost:8000/health

# Test login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@company.com","password":"admin123"}'

# Test registration
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass"}'
```

### Check Database
```bash
sqlite3 data/scorecard.db
.tables
SELECT * FROM admin_users;
.quit
```

### Frontend Debug Mode
Create a simple test file:
```html
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
</head>
<body>
    <script>
        axios.post('http://localhost:8000/auth/login', {
            email: 'admin@company.com',
            password: 'admin123'
        }).then(response => {
            console.log('Success:', response.data);
        }).catch(error => {
            console.error('Error:', error);
        });
    </script>
</body>
</html>
```

## Support

If issues persist after trying these solutions:

1. **Check the logs**: Backend should show request logs in the terminal
2. **Verify versions**: Ensure you're using compatible versions of dependencies
3. **Clear browser cache**: Sometimes cached JavaScript can cause issues
4. **Try a different browser**: Rule out browser-specific issues
5. **Check firewall/proxy**: Ensure nothing is blocking local connections

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Axios Documentation](https://axios-http.com/)
- [Browser Developer Tools Guide](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/What_are_browser_developer_tools)
