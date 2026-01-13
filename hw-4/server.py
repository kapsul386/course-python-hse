from __future__ import annotations

import os
from typing import Optional

from dotenv import load_dotenv
from flask import Flask, jsonify, request

from controllers import operation


def get_port(default: int = 5000) -> int:
    """
    Reads PORT from environment (.env supported via python-dotenv).
    Falls back to `default` if not set or invalid.
    """
    port_raw: Optional[str] = os.getenv("PORT")
    if not port_raw:
        return default
    try:
        port = int(port_raw)
        if 1 <= port <= 65535:
            return port
    except ValueError:
        pass
    return default


load_dotenv()

app = Flask(__name__)


@app.route("/")
def server_info() -> str:
    return "My server"


@app.route("/author")
def author():
    data = {
        "name": "Stas",
        "course": 3,
        "age": 21,
    }
    return jsonify(data)


@app.route("/sum")
def sum_route():
    a_raw = request.args.get("a")
    b_raw = request.args.get("b")
    if a_raw is None or b_raw is None:
        return jsonify({"error": "Query params 'a' and 'b' are required"}), 400

    try:
        a = float(a_raw)
        b = float(b_raw)
    except ValueError:
        return jsonify({"error": "Query params 'a' and 'b' must be numbers"}), 400

    result = operation(a, b)
    return jsonify({"a": a, "b": b, "result": result})


if __name__ == "__main__":
    app.run(debug=True, port=get_port())
