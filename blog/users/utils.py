import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from blog import mail


def save_picture(form_picture):
    # use hex to generate image filename to replace the uploaded filename
    random_hex = secrets.token_hex(8)
    # filename, extension(.jpg .png or .jpeg)
    _, f_ext = os.path.splitext(form_picture.filename)
    # create unique filename to be stored in site.db
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # resize(scale down) the uploaded image
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


# function to send email with token to reset password
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
        sender='noreply@demo.com',
        recipients=[user.email])
    # the "_external=True" shows the ABSOULTE path, not relative path
    msg.body = f'''To reset your password, visit  the  following link:
{url_for('users.reset_token', token=token, _external=True)}
        
If you did not make this request, please ignore this email.
'''
    mail.send(msg)