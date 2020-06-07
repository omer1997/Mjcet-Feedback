import smtplib
from email.mime.text import MIMEText


def send_mail(student, Professor, rating, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = 'b9eb596410196c'
    password = '9bd57e8cd5642b'
    message = f"<h3>New Feedback Submission</h3><ul><li>Student Name: {student}</li><li>Professor Name: {Professor}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>"

    sender_email = 'omerbinali311@gmail.com'
    receiver_email = 'omerbinali678@gmail.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Professor Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())