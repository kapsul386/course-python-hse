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

def get_debug(default: bool = False) -> bool:
    raw = os.getenv("DEBUG")
    if raw is None:
        return default
    return raw.lower() in ("1", "true", "yes", "on")


load_dotenv()

app = Flask(__name__)


@app.route("/")
def server_info() -> str:
    return "My server"


@app.route("/author")
def author():
    data = {
        "name": "Dmritrii",
        "course": 2,
        "age": 19,
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
    return jsonify({"sum": result})



if __name__ == "__main__":
    app.run(
        debug=get_debug(),
        port=get_port(),
    )
