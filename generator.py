import smtplib
from email.message import EmailMessage
import openai

def read_credentials(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]


# Read API key and email password from the file
api_key, password,sender_email  = read_credentials('c:/Users/mohit/OneDrive/Desktop/prathu/py/emai/config.txt')
openai.api_key = api_key

def generate_email(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        temperature=0.7,
        n=1,
        stop=None,
        timeout=10
    )

    return response.choices[0].text.strip()

def generate_sick_leave_email():
    name = input("Enter your name: ")
    recipient_name = input("Enter the recipient's name: ")
    start_date = input("Enter the start date of your sick leave: ")
    end_date = input("Enter the end date of your sick leave: ")
    reason = input("Enter the Subject for email: ")

    prompt = f"make a {reason} email Request to Dear {recipient_name}, from {name}, will be unable to attend work from {start_date} to {end_date} ."

    generated_email = generate_email(prompt)
    print("\nGenerated Email:")
    print(generated_email)   

    # Sending the email
    recipient_email = input("Enter the recipient's email address: ")
   
    subject = reason
    email_content = f"Subject: {subject}\n\n{generated_email} "

    msg = EmailMessage()
    msg.set_content(email_content)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
            print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print("Error sending the email:", e)

# Example usage
generate_sick_leave_email()
