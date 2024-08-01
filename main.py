from datetime import time, date
import streamlit as st
import pandas as pd
import smtplib
import email.message
import pandas as pd
import random
from email_validator import validate_email, EmailNotValidError

st.title('Automated Huawei Exam Appointment Emailer Demo Using Streamlit')
st.write('Fill these fields and put your email to test')

# Setting Name and Email variables 
name = st.text_input("Your name", key="name")
email_input = st.text_input("Your email", key="email")

# Setting the Exam DataFrame
df = pd.DataFrame({
    'exam column':
    ["HCIA Exam", "HCIP Exam", "HCIE Exam", "HCCDA and HCCDP Exams"],
})

# Creating the SelectBox of dataframe exam column
exam_type = st.selectbox('Which exam do you want to take?', df['exam column'])
today = date.today()
start_date = st.slider(
    "When do you want to schedule your exam?",
    value=today,
    format="MM/DD/YY",
    min_value=today,  # Setting the minimal date as today() 
    max_value=date(2024, 12, 31))  # Setting the max date limit.

# Creating a time slider of appointment
appointment = st.slider("Schedule your exam appointment:",
                        value=(time(11, 30), time(12, 45)))

# Name validation using streamlit st error message
def validate_name():
  if not name.strip():
    st.error("Invalid name, please enter a valid name")
    st.stop()
    return False
  return True


if st.button("Send Email"):
  # Validar o e-mail
  validate_name() # Using here the function validate_name created 
  try:
  
    validate_email(email_input) # Using the email-validator lib
  except EmailNotValidError as e:
    st.error(f"Invalid email: {str(e)}")
    st.stop()

  exam_number = random.randint(0, 1000000) # Random number to generate the exam number.

  # Here is the content of the email message formated with informations generates with the slider and input.
  corpo_email = f""" 
    <p> Dear, {name} </p>

    <p>This is your exam number {exam_number}.</p>

    <p>Your exam informations: </p>

    <p>Exam type: {exam_type}</p>
    <p>Exam Date: {start_date.strftime("%Y-%m-%d")} {appointment[0]} to {appointment[1]}</p>

    <p>This is Huawei Cloud Courses that can help you on learning for exam: </p>
    <p>https://edu.huaweicloud.com/intl/en-us/courses/</p>
    <p> Best Regards. </p>

    <p>Leandro Ramos - Huawei Cloud</p>
    <p> TAM Team </p>
    """

  msg = email.message.Message()
  msg['Subject'] = f'{exam_type} Appointment'  # Assunto do E-mail
  msg['From'] = 'xxxxxx@gmail.com'  # E-mail que vai enviar
  msg['To'] = email_input
  password = 'xxxx xxxx xxxx xxxx' # Set here the password with the "App passwords of Google"
  msg.add_header('Content-Type', 'text/html')
  msg.set_payload(corpo_email)

  s = smtplib.SMTP('smtp.gmail.com: 587') # Setting the SMTP protocol
  s.starttls()

  # Login Credentials send emailer
  s.login(msg['From'], password)
  s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
  st.success("Email sent successfully!")
