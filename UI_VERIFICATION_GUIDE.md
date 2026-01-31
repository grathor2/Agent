# UI Verification Guide

## 🚀 Server Status

The application server should now be running at: **http://localhost:8000**

## 📋 Step-by-Step UI Verification

### Step 1: Open the Application
1. Open your web browser
2. Navigate to: **http://localhost:8000**
3. You should see the Collaborative Agent System UI

### Step 2: Verify UI Components

#### ✅ Header Section
- [ ] Title: "🤖 Collaborative Agent System"
- [ ] Subtitle: "Intelligent Support & Incident Co-Pilot"
- [ ] Status indicator showing "Connected" (green dot)

#### ✅ Chat Interface (Left Panel)
- [ ] Text area for entering queries
- [ ] "Send" button
- [ ] Response section (will appear after sending a query)

#### ✅ Live Execution Log (Right Panel)
- [ ] Execution log area visible
- [ ] Shows "Waiting for execution..." initially
- [ ] Will update in real-time when you send queries

#### ✅ Memory Management Section (Bottom)
- [ ] Three buttons: "Working Memory", "Episodic Memory", "Semantic Memory"
- [ ] Memory section display area

### Step 3: Test Basic Functionality

#### Test 1: Send a Simple Query
1. In the chat interface, type: `"Payment service failing intermittently"`
2. Click "Send" button
3. **Verify**:
   - [ ] Button shows "Processing..." while working
   - [ ] Execution log updates with agent activity
   - [ ] Response appears in the response section
   - [ ] Status shows action taken (auto/escalate)

#### Test 2: Check Live Streaming
1. Send another query: `"Have we seen this error before?"`
2. **Verify**:
   - [ ] Execution log shows real-time updates
   - [ ] You can see agent execution steps
   - [ ] Events appear as they happen

#### Test 3: Test Memory Management
1. Click "Working Memory" button
2. **Verify**:
   - [ ] Memory entries are displayed (if any)
   - [ ] Each entry shows key, content, and timestamp

3. Click "Episodic Memory" button
4. **Verify**:
   - [ ] Past incidents/conversations displayed

5. Click "Semantic Memory" button
6. **Verify**:
   - [ ] Knowledge base entries displayed

### Step 4: Test Guardrails

#### Test 4: Test Safety Filtering
1. Send query: `"destroy everything"`
2. **Verify**:
   - [ ] Query is detected as violation
   - [ ] Action shows "escalate"
   - [ ] Response indicates escalation

#### Test 5: Test Normal Query
1. Send query: `"Why is my dashboard not loading?"`
2. **Verify**:
   - [ ] Query passes safety checks
   - [ ] Action shows "auto" (if confidence high)
   - [ ] Response is generated

### Step 5: Verify WebSocket Connection

#### Check Connection Status
- [ ] Status indicator in header shows green "Connected"
- [ ] If disconnected, it will show red "Disconnected"
- [ ] Connection should auto-reconnect

### Step 6: Test Long Conversation

1. Send multiple queries in sequence:
   - Query 1: `"Payment service issue"`
   - Query 2: `"What was the previous issue?"`
   - Query 3: `"How do I fix this?"`

2. **Verify**:
   - [ ] Each query processes correctly
   - [ ] Context is maintained
   - [ ] Memory is being used

## 🎯 Expected Behavior

### Normal Query Flow:
1. User enters query
2. Execution log shows:
   - "🚀 Execution Started"
   - Agent execution steps
   - "✅ Execution Complete"
3. Response appears with:
   - Action (auto/escalate)
   - Response text
   - Confidence score

### Guardrails Flow:
1. User enters harmful content
2. System detects violation
3. Action shows "escalate"
4. Response indicates human review needed

### Memory Flow:
1. User queries memory
2. Relevant memories displayed
3. Can view/edit/delete (if implemented)

## ⚠️ Troubleshooting

### Server Not Responding
- Check if server is running: `ps aux | grep "python run.py"`
- Restart server: `python run.py`
- Check port 8000 is not in use

### WebSocket Not Connecting
- Check browser console for errors
- Verify server logs for WebSocket errors
- Try refreshing the page

### No Response from Queries
- Check browser console for errors
- Verify API key is set in `.env`
- Check server logs for errors

### Memory Not Loading
- Verify database exists: `ls -la data/memory.db`
- Check server logs for database errors

## 📊 What to Look For

### ✅ Success Indicators:
- Green connection status
- Real-time execution log updates
- Responses appearing after queries
- Memory entries loading
- Guardrails detecting violations

### ❌ Issues to Report:
- Red connection status
- No response to queries
- Execution log not updating
- Memory not loading
- Errors in browser console

## 🔍 Browser Console Check

1. Open browser developer tools (F12)
2. Go to Console tab
3. **Verify**:
   - [ ] No red errors
   - [ ] WebSocket connection messages
   - [ ] API call logs

## 📝 Test Checklist

- [ ] UI loads correctly
- [ ] Connection status is green
- [ ] Can send queries
- [ ] Execution log updates in real-time
- [ ] Responses appear
- [ ] Memory buttons work
- [ ] Guardrails detect violations
- [ ] Normal queries work
- [ ] WebSocket streaming works
- [ ] No console errors

## 🎉 Success Criteria

The application is working correctly if:
1. ✅ UI loads and displays correctly
2. ✅ Can send queries and get responses
3. ✅ Execution log shows real-time updates
4. ✅ Memory management works
5. ✅ Guardrails detect and block harmful content
6. ✅ WebSocket connection is stable

---

**Server URL**: http://localhost:8000  
**Status**: Check the green/red indicator in the UI header
