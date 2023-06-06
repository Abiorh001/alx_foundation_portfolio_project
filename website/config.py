from dotenv import load_dotenv
import os

# Specify the path to the .env file
dotenv_path = '/home/abiorh/malzahra-tech/.env'

# Load the environment variables from the .env file
load_dotenv(dotenv_path)



class Config:
    # Access the environment variables using os.getenv()
    # SECRET_KEY = os.getenv("SECRET_KEY")
    # SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SECRET_KEY=""

    SQLALCHEMY_DATABASE_URI=""

#creating my config for email sender
MAIL_SERVER = ""
MAIL_PORT = 587  
MAIL_USE_TLS = True 
MAIL_USERNAME = 
MAIL_PASSWORD = 

