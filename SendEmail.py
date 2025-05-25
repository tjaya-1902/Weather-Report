import smtplib, ssl
import os
from pyhtml2pdf import converter

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def SendWeatherReport(Email):

    Subject = "Automated Weather Report"
    Body = "Hello, here is your custom weather prediction"
    Sender = "xxx@gmail.com"
    Receiver = Email
    Password = "xxx"

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = Sender
    message["To"] = Receiver
    message["Subject"] = Subject

    # Add body to email
    message.attach(MIMEText(Body, "plain"))

    # Convert HTML file to PDF format
    path = os.path.abspath('WeatherPrediction.html')
    converter.convert(f'file:///{path}', 'WeatherPrediction.pdf', print_options={"landscape": True, "paperHeight": 13, "paperWidth": 10})
    filename = "WeatherPrediction.pdf" 

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    print("Sending Email")

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(Sender, Password)
        server.sendmail(Sender, Receiver, text)

    print("Email sent")