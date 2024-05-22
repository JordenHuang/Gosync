from flask import Flask, request, abort
from backend.database import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=8989)