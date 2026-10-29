from flask import Flask, render_template, request
from datetime import datetime

import os
import time
from bakong_khqr import KHQR

app = Flask(__name__)

# Token
TOKEN = os.getenv("TOKEN")

@app.get("/")
@app.get("/home")
def cart():
    return render_template('cart.html')

@app.post("/checkout")
def checkout():
    form = request.form
    khqr = KHQR(TOKEN)

    amount = form.get("amount", type=int)
    if amount is None or amount <= 0:
        return "Invalid amount", 400

    currency = 'KHR'
    qr_string = khqr.create_qr(
                    account_id="devit009@bkrt",
                    merchant_name="បាយស្រូប ព្រះឳង្ការ",
                    merchant_city="Kampot",
                    amount=amount,
                    currency=currency,
                    store_label="Cashier-01",
                    phone_number="0967234500",
                    bill_number="TRX012345",
                    terminal_label="POS-01",
                    static=False,
                    expiration=1
                )
    base64_uri = khqr.qr_image(qr_string, format="base64_uri")
    # assert False, base64_uri
    return render_template(
        "dialog_qr.html",
        qr_image=base64_uri,
        qr_string=qr_string,
        amount=amount,
        currency=currency
    )

@app.post("/check-payment")
def check_payment():
    qr_string = request.form.get("qr_string")

    if not qr_string:
        return "Missing QR string", 400

    khqr = KHQR(TOKEN)
    md5 = khqr.generate_md5(qr_string)

    # Step 1: Verify payment status
    status = khqr.check_payment(md5)

    if status != "PAID":
        return render_template("failed_payment.html")

    # Step 2: Retrieve payment details
    payment = khqr.get_payment(md5)

    if not payment:
        return render_template("failed_payment.html")

    # Step 3: Extract transaction information
    acknowledged_at = payment.get("acknowledgedDateMs")
    formatted_acknowledged_at = None
    if acknowledged_at:
        formatted_acknowledged_at = datetime.fromtimestamp(
            acknowledged_at / 1000
        ).strftime("%d-%m-%Y %H:%M:%S")

    amount = payment.get("amount")
    currency = payment.get("currency")
    payer = payment.get("fromAccountId")
    receiver = payment.get("toAccountId")
    transaction_hash = payment.get("hash")
    description = payment.get("description")
    created_at = payment.get("createdDateMs")
    acknowledged_at = formatted_acknowledged_at

    return render_template(
        "success_payment.html",
        amount=amount,
        currency=currency,
        payer=payer,
        receiver=receiver,
        transaction_hash=transaction_hash,
        description=description,
        created_at=created_at,
        acknowledged_at=acknowledged_at,
    )


if __name__ == "__main__":
    app.run(debug=True)
