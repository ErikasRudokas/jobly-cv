# CV Parser

Processes CV PDFs and extracts structured details with a trained NLP model.

## Language Handling

- The service auto-detects CV text language.
- If Lithuanian (`lt`) is detected, text is translated to English before extraction.
- If translation fails, extraction continues with original text.

## Install Dependencies

```bash
pip install --no-cache-dir -r requirements.txt
```

## Running the application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Response Notes

The parse response now also includes:
- `detectedLanguage`
- `translationApplied`
- `translationError`
