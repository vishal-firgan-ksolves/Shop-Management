from email.message import EmailMessage
from datetime import datetime
import smtplib


class EmailService:
    smtp_server = "smtp.example.com"
    smtp_port = 587
    username = "your-username"
    password = "your-password"

    @staticmethod
    def create_email(subject, body, to_email, from_email='no-reply@example.com'):

        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
        return msg

    @staticmethod
    def format_email_body(to_name, low_stock_products):

        if not low_stock_products:
            return f"""
            Dear {to_name},

              We would like to inform you that we currently have sufficient stock for all products.

            Regards,
            Your Company Name
            """

        product_list = "\n".join(
            [f"Product ID: {product_id}, Name: {name}, Quantity: {quantity}"
             for product_id, name, quantity in low_stock_products]  )
        return f"""
        Dear {to_name},

        We would like to inform you that the following products are running low in stock:

         {product_list}

        We kindly request that you supply these items at your earliest convenience. Thank you for your attention to this matter.

        Regards,
         Company Name
        """

    @staticmethod
    def print_email(msg):
        # Extracting email content
        email_body = msg.get_content()
        # Print email headers and formatted body
        print("Email Format:\n")
        print(f"To: {msg['To']}")
        print(f"From: {msg['From']}")
        print(f"Subject: {msg['Subject']}")
        print(f"Date: {msg['Date']}")
        print("\nBody:\n")
        print(email_body)

    @staticmethod
    def send_email(to_name, low_stock_products, subject, to_email, from_email='no-reply@example.com'):

        # Format the email body
        body = EmailService.format_email_body(to_name, low_stock_products)

        # Create the email
        msg = EmailService.create_email(subject, body, to_email, from_email)

        # Print the email for debugging (optional)
        EmailService.print_email(msg)


