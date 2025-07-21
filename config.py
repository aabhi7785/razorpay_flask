RAZORPAY_KEY_ID = "your_key_id"
RAZORPAY_KEY_SECRET = "your_key_secret"

# PostgreSQL database URI
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:root@localhost:5433/razorpay_db"



# import os

# basedir = os.path.abspath(os.path.dirname(__file__))

# class Config:
#     SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
#     # Example: postgresql://username:password@localhost:5433/bugtracker
#     SQLALCHEMY_DATABASE_URI = os.environ.get(
#         "DATABASE_URL",
#         "postgresql://postgres:root@localhost:5432/razorpay_db"
#     )
#     SQLALCHEMY_TRACK_MODIFICATIONS = False