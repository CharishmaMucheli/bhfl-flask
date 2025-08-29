# BFHL Flask API

- Method: POST
- Route: /bfhl
- Status Code: 200 for successful and gracefully-handled invalid requests

## Example Request
POST /bfhl
Content-Type: application/json

{
  "data": ["a","1","334","4","R","$"]
}

## Example Response
{
  "is_success": true,
  "user_id": "john_doe_17091999",
  "email": "john@xyz.com",
  "roll_number": "ABCD123",
  "odd_numbers": ["1"],
  "even_numbers": ["334","4"],
  "alphabets": ["A","R"],
  "special_characters": ["$"],
  "sum": "339",
  "concat_string": "Ra"
}

## Quick Deploy (Render in ~5-8 min)
1) Push these files to a public GitHub repo.
2) Go to render.com → New → Web Service → Connect your repo.
3) Environment:
   - Runtime: Python 3
   - Build Command: (leave empty)
   - Start Command: gunicorn app:app
4) After deploy, your URL is like https://your-service.onrender.com
5) Test: POST https://your-service.onrender.com/bfhl

## Quick Deploy (Railway)
1) Push to public GitHub.
2) railway.app → New Project → Deploy from GitHub.
3) Set Start Command: gunicorn app:app
4) Test: POST https://your-app.up.railway.app/bfhl

Notes:
- CORS enabled (flask-cors).
- Numbers (including sum) are returned as strings.
- Alphabets list contains only purely alphabetic tokens transformed to uppercase.
- concat_string is built from all alphabetic characters (from those alphabet-only tokens) in reverse order with alternating caps.
"# bhfl-flask" 
