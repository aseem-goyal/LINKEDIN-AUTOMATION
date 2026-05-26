"""
LinkedIn Recruiter Email Automation System

Developed By: Aseem Goyal

Tech Stack:
- Python
- Selenium
- Regex
- SMTP
- ChromeDriver
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import re
import smtplib
from email.message import EmailMessage


# LINKEDIN LOGIN DETAILS


LINKEDIN_EMAIL = "LinkedIN_EMAIL"
LINKEDIN_PASSWORD = "LINKEDIN_PASSWORD"

# GMAIL DETAILS

GMAIL_EMAIL = "GMAIL_EMAIL"

# Use Gmail App Password here
GMAIL_PASSWORD = "GMAIL_APP_PASSWORD"

# CHROME SETUP

options = Options()

# Open browser maximized
options.add_argument("--start-maximized")

# ChromeDriver setup
service = Service("chromedriver.exe")

# Start browser
driver = webdriver.Chrome(service=service, options=options)

# OPEN LINKEDIN LOGIN PAGE

driver.get("https://www.linkedin.com/login")

time.sleep(3)

# ENTER EMAIL

email = driver.find_element(By.ID, "username")
email.send_keys(LINKEDIN_EMAIL)

# ENTER PASSWORD

password = driver.find_element(By.ID, "password")
password.send_keys(LINKEDIN_PASSWORD)

# CLICK LOGIN BUTTON

login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
login_button.click()

print("LinkedIn Login Successful")

time.sleep(5)

# OPEN SEARCH PAGE

driver.get("https://www.linkedin.com/search/results/content/?keywords=java%20developer%20contract")

print("Search Results Opened")

time.sleep(8)

# GET PAGE SOURCE

page_source = driver.page_source

# FIND EMAILS USING REGEX

emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+",page_source)

# Remove duplicate emails
emails = list(set(emails))

print("\nEmails Found:\n")

for mail in emails:
    print(mail)

# SAVE EMAILS TO FILE

with open("emails.txt", "w") as file:
    for mail in emails:
        file.write(mail + "\n")

print("\nEmails saved to emails.txt")

# SEND EMAIL USING GMAIL SMTP

if len(emails) > 0:
    receiver = emails[0]
    print("\nSending email to:", receiver)

    # Create Email
    msg = EmailMessage()

    msg["Subject"] = "Application for Java Developer Contract Role"

    msg["From"] = GMAIL_EMAIL

    msg["To"] = receiver

    msg.set_content(
        """
Hello,

I hope you are doing well.

I came across your requirement for a Java Developer Contract role.

Please find my resume attached for your consideration.

Thank you.

Best Regards,
Aseem Goyal
"""
    )

    # ATTACH RESUME
    
    with open(r"C:\Users\Aseem\Downloads\Aseem_Goyal_Resume.pdf", "rb") as f:
        file_data = f.read()
        file_name = f.name

    msg.add_attachment(
        file_data,
        maintype="application",
        subtype="pdf",
        filename=file_name
    )

    # CONNECT TO GMAIL SERVER
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

        smtp.login(GMAIL_EMAIL, GMAIL_PASSWORD)

        smtp.send_message(msg)

    print("\nEmail Sent Successfully")

else:

    print("\nNo emails found")

# WAIT BEFORE CLOSING

time.sleep(10)

# CLOSE BROWSER

driver.quit()