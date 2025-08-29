import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Static identifiers per the problem statement/examples
FULL_NAME = "john_doe"        # full name in lowercase with underscore
DOB_DDMMYYYY = "17091999"     # ddmmyyyy
EMAIL = "john@xyz.com"
ROLL_NUMBER = "ABCD123"


def process_data(data):
    even_numbers = []
    odd_numbers = []
    alphabets = []
    special_characters = []
    sum_numbers = 0

    # Collect all alphabetical characters (from purely alphabetic tokens) in sequence
    alpha_chars_sequence = []

    for item in data:
        # Normalize input to either str or number cases
        if isinstance(item, str):
            s = item.strip()

            if s == "":
                special_characters.append(s)
                continue

            # Integer detection including optional leading +/-
            if s.lstrip("+-").isdigit():
                try:
                    n = int(s)
                except Exception:
                    special_characters.append(s)
                    continue

                sum_numbers += n
                if n % 2 == 0:
                    even_numbers.append(str(n))  # return numbers as strings
                else:
                    odd_numbers.append(str(n))

            elif s.isalpha():  # purely alphabetic
                alphabets.append(s.upper())
                alpha_chars_sequence.extend(list(s))
            else:
                # Mixed alphanumerics or symbols
                special_characters.append(s)

        elif isinstance(item, int):
            n = item
            sum_numbers += n
            if n % 2 == 0:
                even_numbers.append(str(n))
            else:
                odd_numbers.append(str(n))
        else:
            # Any other data type -> treat as special (stringified)
            special_characters.append(str(item))

    # Build alternating-caps reverse concatenation from collected alphabetical characters
    reversed_chars = list(reversed(alpha_chars_sequence))
    alt_caps_chars = []
    for idx, ch in enumerate(reversed_chars):
        alt_caps_chars.append(ch.upper() if idx % 2 == 0 else ch.lower())
    concat_string = "".join(alt_caps_chars)

    return {
        "is_success": True,
        "user_id": f"{FULL_NAME}_{DOB_DDMMYYYY}",
        "email": EMAIL,
        "roll_number": ROLL_NUMBER,
        "odd_numbers": odd_numbers,
        "even_numbers": even_numbers,
        "alphabets": alphabets,
        "special_characters": special_characters,
        "sum": str(sum_numbers),  # sum as a string
        "concat_string": concat_string,
    }


@app.route("/bfhl", methods=["POST"])
def bfhl():
    try:
        payload = request.get_json(silent=True)
        if not payload or "data" not in payload or not isinstance(payload["data"], list):
            # Graceful invalid payload response (still 200 as per instructions)
            return jsonify({
                "is_success": False,
                "user_id": f"{FULL_NAME}_{DOB_DDMMYYYY}",
                "email": EMAIL,
                "roll_number": ROLL_NUMBER,
                "odd_numbers": [],
                "even_numbers": [],
                "alphabets": [],
                "special_characters": [],
                "sum": "0",
                "concat_string": "",
                "error": "Invalid payload. Expected JSON with 'data' as an array."
            }), 200

        resp = process_data(payload["data"])
        return jsonify(resp), 200

    except Exception as e:
        # Catch-all to keep contract (status 200 with is_success=false)
        return jsonify({
            "is_success": False,
            "user_id": f"{FULL_NAME}_{DOB_DDMMYYYY}",
            "email": EMAIL,
            "roll_number": ROLL_NUMBER,
            "odd_numbers": [],
            "even_numbers": [],
            "alphabets": [],
            "special_characters": [],
            "sum": "0",
            "concat_string": "",
            "error": str(e)
        }), 200


@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
