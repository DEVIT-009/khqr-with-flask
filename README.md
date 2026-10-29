# KHQR Payment Integration with Flask

A simple Flask web application that integrates KHQR payments using the `bakong-khqr` Python library. It generates a KHQR payment QR code, allows customers to scan and pay, and checks payment status.

## Features

- Generate dynamic KHQR payment QR codes.
- Display QR codes in a popup dialog.
- Check payment status through the KHQR library.
- Retrieve transaction details after successful payment.
- Display payment success and failure pages.
- Store the Bakong API token securely using environment variables.
- Responsive UI built with Tailwind CSS.
- Khmer-language payment interface.

## Tech Stack

- **Backend:** Python, Flask
- **Payment:** Bakong KHQR
- **Frontend:** HTML, Tailwind CSS
- **Environment Variables:** `python-dotenv`

## Project Structure

```text
project/
├── app.py
├── .env
├── .gitignore
├── requirements.txt
└── templates/
    ├── cart.html
    ├── dialog_qr.html
    ├── success_payment.html
    └── failed_payment.html
```

## Requirements

- Python 3.12 or compatible Python version
- A Bakong API token
- Internet connection for API access and Tailwind CSS CDN

## Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <your-project-folder>
```

### 2. Create a Virtual Environment

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install Flask python-dotenv bakong-khqr
```

If your project already has a `requirements.txt` file, install its dependencies instead:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
TOKEN=your_bakong_token_here
```

Replace the placeholder with your actual Bakong API token.

Load the environment variable in `app.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise RuntimeError("TOKEN is missing from the .env file")
```

**Security:** Never commit your `.env` file or expose your token in frontend code.

Add the following to `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
*.py[cod]
```

### 5. Run the Application

```bash
flask --app app run --debug
```

Open the application in your browser:

```text
http://127.0.0.1:5000
```

## Payment Flow

1. The customer opens the shopping cart.
2. The customer clicks **Proceed to Checkout**.
3. Flask generates a dynamic KHQR payment QR code.
4. The QR code appears in a popup dialog.
5. The customer scans the QR code using a supported banking application.
6. The customer clicks **I have paid**.
7. Flask checks the payment status using the generated QR transaction hash.
8. If payment is confirmed, the application retrieves transaction details and displays the success page.
9. If payment is not confirmed, the application displays the failed-payment page.

## Payment Verification

The application uses the KHQR library to check payment status:

```python
khqr = KHQR(TOKEN)

md5 = khqr.generate_md5(qr_string)
status = khqr.check_payment(md5)

if status == "PAID":
    payment = khqr.get_payment(md5)
```

The payment details can include the transaction hash, payer account, recipient account, currency, amount, and timestamps, depending on the API response.

**Important:** A payment confirmation button does not itself prove that payment succeeded. Always verify the payment with the API before treating an order as paid.

## Important Notes

- Use the amount calculated by your backend rather than trusting a hidden form input.
- Validate the payment amount, currency, and recipient account.
- Prevent a transaction from being used to pay for multiple orders.
- Save verified payment and order details in your database for future reference.
- Handle API errors and pending payments appropriately.
- Use a production-ready Tailwind CSS build for deployment rather than relying on the browser CDN.

## Reference

- **KHQR Python Library:** https://github.com/bsthen/bakong-khqr

## License

Add the license appropriate for your project.
