# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create `.env` file:
```
OPENAI_API_KEY=your_key_here
```

### 3. Generate Test Data

```bash
python tests/generate_test_data.py
```

### 4. Index Knowledge Base

```bash
python setup_knowledge_base.py
```

### 5. Run the System

```bash
python run.py
```

### 6. Open Browser

Navigate to: `http://localhost:8000`

## ✅ Verify Installation

1. Check that all agents are loaded (check logs)
2. Test a query in the UI
3. Verify WebSocket connection (green status indicator)
4. Check that execution log shows agent activity

## 🧪 Test the System

Run test suite:
```bash
pytest tests/test_agents.py -v
```

## 📝 Sample Queries

Try these in the UI:

1. **Support Ticket**: "Payment service failing intermittently for EU users"
2. **Question**: "Have we seen this error code before?"
3. **Incident**: "Dashboard not loading for customers"

## 🐛 Troubleshooting

- **Import errors**: Make sure all dependencies are installed
- **API errors**: Check your OpenAI API key in `.env`
- **OCR errors**: Install Tesseract OCR
- **Port already in use**: Change port in `run.py` or `config.py`
