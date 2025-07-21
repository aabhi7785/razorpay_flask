from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    course = db.Column(db.String(50))
    amount = db.Column(db.Integer)
    status = db.Column(db.String(50))

    def __init__(self, payment_id, name, email, phone, course, amount, status):
        self.payment_id = payment_id
        self.name = name
        self.email = email
        self.phone = phone
        self.course = course
        self.amount = amount
        self.status = status
