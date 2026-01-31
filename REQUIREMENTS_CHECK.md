# Requirements Check for Testing

## ✅ What's Already Done

1. **Environment File**: `.env` created with your API key
2. **All Code**: Complete implementation with all 8 agents
3. **Test Script**: `phased_testing.py` ready to run

## 📋 What You Need to Do

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Or if you prefer to install manually, key packages are:
- `langgraph` - Agent orchestration
- `langchain` - LLM integration
- `langchain-openai` - OpenAI integration
- `fastapi` - Web server
- `uvicorn` - ASGI server
- `chromadb` - Vector store
- `python-dotenv` - Environment variables
- `pypdf` - PDF processing
- `python-docx` - Word document processing
- `pillow` - Image processing
- `pytesseract` - OCR (requires Tesseract binary)
- `sqlalchemy` - Database
- And others (see requirements.txt)

### Step 2: Install Tesseract OCR (Optional, for image processing)

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**Windows:**
Download from: https://github.com/UB-Mannheim/tesseract/wiki

### Step 3: Run Phased Testing

```bash
python phased_testing.py
```

This will test the system in 8 phases:
1. Environment check
2. Component imports
3. Component initialization
4. Individual agents
5. Memory system
6. RAG system
7. Orchestration
8. Full system end-to-end

## 🎯 Quick Test (Minimal Requirements)

If you want to test quickly without all dependencies:

### Minimal Test Script

```python
# quick_test.py
import os
from dotenv import load_dotenv

load_dotenv()

# Check API key
api_key = os.getenv("OPENAI_API_KEY", "")
print(f"API Key: {'✅ Found' if api_key else '❌ Missing'}")
print(f"Length: {len(api_key)}")

# Check basic imports
try:
    from agents import IngestionAgent
    print("✅ Agents import: OK")
except Exception as e:
    print(f"❌ Agents import: {e}")

try:
    from memory import MemoryStore
    print("✅ Memory import: OK")
except Exception as e:
    print(f"❌ Memory import: {e}")

try:
    from rag import DocumentProcessor
    print("✅ RAG import: OK")
except Exception as e:
    print(f"❌ RAG import: {e}")
```

Run: `python quick_test.py`

## 📊 Testing Phases Explained

### Phase 1-3: Foundation (No API calls)
- Environment setup
- Package checks
- Component imports
- Basic initialization

**Cost**: $0 (no API calls)

### Phase 4-6: Components (No API calls)
- Agent functionality
- Memory operations
- RAG initialization

**Cost**: $0 (no API calls)

### Phase 7-8: Integration (Makes API calls)
- Full orchestration
- End-to-end workflows
- Real scenarios

**Cost**: ~$0.01-0.05 per test (uses GPT-4)

## 🚀 After Testing Passes

Once all phases pass:

1. **Generate Test Data** (optional):
   ```bash
   python tests/generate_test_data.py
   ```

2. **Index Knowledge Base** (optional):
   ```bash
   python setup_knowledge_base.py
   ```

3. **Start Server**:
   ```bash
   python run.py
   ```

4. **Access UI**: http://localhost:8000

## ⚠️ Important Notes

1. **API Costs**: Phases 7-8 make OpenAI API calls (small cost)
2. **Network**: Requires internet for API calls
3. **Time**: Full test takes 2-5 minutes
4. **Dependencies**: Some packages may need compilation (chromadb, etc.)

## 🔍 Troubleshooting

### "Module not found" errors
→ Run: `pip install -r requirements.txt`

### "API key not found"
→ Check `.env` file exists and has correct key

### "Tesseract not found" (for image OCR)
→ Install Tesseract or skip image processing tests

### Import errors
→ Check Python path, ensure you're in the artifacts directory

## ✅ Current Status

- [x] Environment file created
- [x] API key configured
- [x] Test script ready
- [ ] Dependencies installed (you need to do this)
- [ ] Phased testing run (you need to do this)

## Next Command to Run

```bash
pip install -r requirements.txt && python phased_testing.py
```
