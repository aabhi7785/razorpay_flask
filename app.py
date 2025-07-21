from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_mail import Mail, Message
import razorpay, uuid
from config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET, SQLALCHEMY_DATABASE_URI
from models import db, Payment

app = Flask(__name__)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Email setup
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'aarya01010@gmail.com'
app.config['MAIL_PASSWORD'] = 'aarya(010101)'  # use app password
mail = Mail(app)

# Razorpay client
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

def send_receipt_email(payment):
    msg = Message('Your Payment Receipt',
                  sender='aarya01010@gmail.com',
                  recipients=[payment.email])
    msg.html = render_template('payment_receipt.html',
                               name=payment.name,
                               payment_id=payment.payment_id,
                               course=payment.course,
                               amount=payment.amount / 100,
                               status=payment.status.capitalize())
    mail.send(msg)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-details', methods=['POST'])
def submit_details():
    """Save user details only, no Razorpay API call here."""
    data = request.form
    amount_paise = int(data['amount']) * 100

    # Create a dummy unique ID until payment is done
    dummy_payment_id = f"pending_{uuid.uuid4().hex[:8]}"

    new_payment = Payment(
        payment_id=dummy_payment_id,
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        course=data['course'],
        amount=amount_paise,
        status='pending'
    )
    db.session.add(new_payment)
    db.session.commit()

    return redirect(url_for('pay', payment_id=new_payment.id))

@app.route('/pay/<int:payment_id>')
def pay(payment_id):
    """Show payment page with details."""
    payment = Payment.query.get(payment_id)
    if not payment:
        return "Payment record not found", 404

    return render_template(
        'pay.html',
        razorpay_key=RAZORPAY_KEY_ID,
        payment_db_id=payment.id,
        name=payment.name,
        email=payment.email,
        phone=payment.phone,
        course=payment.course,
        amount=payment.amount
    )

@app.route('/create-razorpay-order', methods=['POST'])
def create_razorpay_order():
    """Trigger Razorpay order creation only when user clicks Pay Now."""
    data = request.get_json()
    amount = data['amount']
    payment_db_id = data['payment_db_id']

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    return jsonify(order)

@app.route('/save-payment', methods=['POST'])
def save_payment():
    """Update payment after Razorpay success."""
    data = request.get_json()
    payment = Payment.query.get(data['payment_db_id'])

    if payment:
        payment.status = 'completed'
        payment.payment_id = data['payment_id']
        db.session.commit()
        return jsonify({'message': 'Payment successful'}), 200  
        # try:
        #     send_receipt_email(payment)
        # except Exception as mail_error:
        #     print("Email sending failed:", mail_error)

        # return jsonify({'message': 'Payment successful and receipt sent'}), 200
    else:
        return jsonify({'error': 'Payment not found'}), 404

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/failure')
def failure():
    return render_template('failure.html')

@app.route('/payments')
def payments():
    all_payments = Payment.query.all()
    return render_template('payments.html', payments=all_payments)

if __name__ == '__main__': 
    app.run(port=5000, debug=True)




# I have raised this with team to check and this is the ticket id for your reference:988941


# from flask import Flask, render_template, request, jsonify, redirect, url_for
# from flask_mail import Mail, Message
# from models import db, Payment
# from config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET, SQLALCHEMY_DATABASE_URI
# import razorpay

# app = Flask(__name__)

# # Database setup
# app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)

# # Email setup
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'aarya01010@gmail.com'
# app.config['MAIL_PASSWORD'] = 'aarya(010101)'  # Use app password
# mail = Mail(app)

# # Razorpay client
# client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# def send_receipt_email(payment):
#     """Send payment receipt via email"""
#     msg = Message('Your Payment Receipt',
#                   sender='aarya01010@gmail.com',
#                   recipients=[payment.email])
#     msg.html = render_template('payment_receipt.html',
#                                name=payment.name,
#                                payment_id=payment.payment_id,
#                                course=payment.course,
#                                amount=payment.amount / 100,
#                                status=payment.status.capitalize())
#     mail.send(msg)

# with app.app_context():
#     db.create_all()

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/submit-details', methods=['POST'])
# def submit_details():
#     """Save user details with status pending"""
#     data = request.form
#     amount_paise = int(data['amount']) * 100

#     new_payment = Payment(
#         payment_id="pending",
#         name=data['name'],
#         email=data['email'],
#         phone=data['phone'],
#         course=data['course'],
#         amount=amount_paise,
#         status='pending'
#     )
#     db.session.add(new_payment)
#     db.session.commit()

#     return redirect(url_for('pay', payment_id=new_payment.id))

# @app.route('/pay/<int:payment_id>')
# def pay(payment_id):
#     """Generate Razorpay order and load pay.html"""
#     payment = Payment.query.get(payment_id)
#     if not payment:
#         return "Payment record not found", 404

#     # Create Razorpay order here
#     order = client.order.create({
#         "amount": payment.amount,
#         "currency": "INR",
#         "payment_capture": "1"
#     })

#     payment.payment_id = order['id']  # Save Razorpay order ID
#     db.session.commit()

#     return render_template(
#         'pay.html',
#         razorpay_key=RAZORPAY_KEY_ID,
#         razorpay_order_id=order['id'],
#         payment_db_id=payment.id,
#         name=payment.name,
#         email=payment.email,
#         phone=payment.phone,
#         course=payment.course,
#         amount=payment.amount
#     )

# @app.route('/save-payment', methods=['POST'])
# def save_payment():
#     """Update payment after successful Razorpay payment"""
#     data = request.get_json()
#     payment = Payment.query.get(data['payment_db_id'])

#     if payment:
#         payment.status = 'completed'
#         payment.payment_id = data['payment_id']
#         db.session.commit()

#         try:
#             send_receipt_email(payment)
#         except Exception as e:
#             print("Email sending failed:", e)

#         return jsonify({'message': 'Payment successful and receipt sent'}), 200
#     else:
#         return jsonify({'error': 'Payment not found'}), 404

# @app.route('/success')
# def success():
#     return render_template('success.html')

# @app.route('/failure')
# def failure():
#     return render_template('failure.html')

# @app.route('/payments')
# def payments():
#     all_payments = Payment.query.all()
#     return render_template('payments.html', payments=all_payments)

# if __name__ == '__main__':
#     app.run(port=5000, debug=True)

#---------------------------------------------------------------------------------

# @app.route('/webhook', methods=['POST'])
# def webhook():
#     from razorpay import Utility
#     data = request.get_data(as_text=True)
#     signature = request.headers.get('X-Razorpay-Signature')

#     try:
#         Utility.verify_webhook_signature(data, signature, "YOUR_WEBHOOK_SECRET")
#         payload = request.get_json()
#         payment_id = payload['payload']['payment']['entity']['id']
#         status = payload['event']

#         # Update DB payment status
#         payment = Payment.query.filter_by(payment_id=payment_id).first()
#         if payment:
#             if status == 'payment.captured':
#                 payment.status = 'completed'
#             elif status == 'payment.failed':
#                 payment.status = 'failed'
#             db.session.commit()
#     except:
#         return jsonify({'error': 'Invalid signature'}), 400

#     return jsonify({'status': 'ok'}), 200
