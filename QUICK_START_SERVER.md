# Quick Start - Run the Server

## 🚀 Start the Server

```bash
cd /Users/gauravr/Downloads/artifacts
source venv/bin/activate
python run.py
```

The server will start on: **http://localhost:8000**

## ✅ Verify Server is Running

### Option 1: Check in Browser
Open: **http://localhost:8000**

You should see the Collaborative Agent System UI.

### Option 2: Check via Terminal
```bash
curl http://localhost:8000/
```

Should return HTML content.

### Option 3: Check Process
```bash
ps aux | grep "python.*run.py"
```

Should show the Python process.

## 🌐 Access the UI

1. **Open Browser**: Chrome, Firefox, Safari, or Edge
2. **Navigate to**: http://localhost:8000
3. **You should see**:
   - Header with title and status indicator
   - Chat interface on the left
   - Execution log on the right
   - Memory management section at bottom

## 🧪 Quick UI Tests

### Test 1: Connection Status
- Look at the header
- Status should show green "Connected" dot
- If red, refresh the page

### Test 2: Send a Query
1. Type in chat: `"Test query"`
2. Click "Send"
3. Watch execution log update
4. Response should appear

### Test 3: Check Memory
1. Click "Working Memory" button
2. Should show memory entries (if any)

## 📋 Full Verification

See `UI_VERIFICATION_GUIDE.md` for complete verification steps.

## 🛑 Stop the Server

Press `Ctrl+C` in the terminal where server is running.

Or if running in background:
```bash
kill $(cat server.pid)
```

## ⚠️ Troubleshooting

### Port Already in Use
```bash
lsof -ti:8000 | xargs kill -9
```

### Server Won't Start
- Check virtual environment is activated
- Check `.env` file exists with API key
- Check logs: `tail -f server.log`

### No Response
- Check API key in `.env`
- Check server logs for errors
- Verify all dependencies installed

---

**Ready to test?** Open http://localhost:8000 in your browser!
