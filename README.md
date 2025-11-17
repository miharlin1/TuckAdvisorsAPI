# M&A GPT Analysis API

Tuck Advisors Intern Coding Assignment

Mia Harlin

November 17, 2025

A Flask-based REST API for managing M&A analysis markdown with persistent SQLite storage.

## Assignment Requirements

This API parses GPT analysis output and provides:
1. **GET endpoint** - Returns the current markdown string
2. **POST endpoint** - Appends text to the existing markdown
3. **Persistent storage** - Uses SQLite3 to persist data between restarts

## Installation

1. **Install dependencies:**
```bash
pip3 install flask
```

2. **Initialize the database:**
```bash
python3 init_db.py
```

This will create the SQLite database and load the initial GPT output from `src/data/input.json`.

## Running the API

Start the Flask server:

```bash
python3 src/api.py
```

The API will be available at `http://127.0.0.1:5000`

## API Endpoints

### GET /api/markdown

Returns the current markdown string from the database.

**Request:**
```bash
curl http://127.0.0.1:5000/api/markdown
```

**Response:**
```json
{
  "markdown": "Attached is the output generated regarding your company..."
}
```

### POST /api/markdown

Appends a string to the existing markdown as a new sentence.

**Request:**
```bash
curl -X POST http://127.0.0.1:5000/api/markdown \
  -H "Content-Type: application/json" \
  -d '{"text": "This is more analysis."}'
```

**Request Body:**
```json
{
  "text": "String to append to the markdown"
}
```

**Response:**
```json
{
  "markdown": "Attached is the output generated... This is additional analysis."
}
```

## Testing

**Step 1:** Start the API
```bash
python3 src/api.py
```

**Step 2:** Get current markdown (in another terminal)
```bash
curl http://127.0.0.1:5000/api/markdown
```

**Step 3:** Append text
```bash
curl -X POST http://127.0.0.1:5000/api/markdown \
  -H "Content-Type: application/json" \
  -d '{"text": "Adding additional text for this demo."}'
```

**Step 4:** Verify the update
```bash
curl http://127.0.0.1:5000/api/markdown
```
