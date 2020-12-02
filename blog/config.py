import os

# =========================================================================
# To allow python to get environment variables, run in terminal, not VScode
# =========================================================================
class Config:
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db' # 3 slashes for absolute path
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

'''
Generate the environment variables
1. open .bash_profile 
2. export EMAIL_USER=<your_email>, export EMAIL_PASS=<password>
'''