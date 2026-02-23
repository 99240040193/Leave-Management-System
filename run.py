from app import create_app
from seed import seed_data

app = create_app()

# Auto-seed on startup (Render free tier safe)
with app.app_context():
    seed_data()

# Local development only
if __name__ == '__main__':
    app.run(debug=True, port=5000)
