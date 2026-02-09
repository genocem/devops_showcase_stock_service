"""
Application entry point
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(
        host='localhost',
        port=5000,
        ssl_context='adhoc'  # For development only, use proper certs in production
    )
