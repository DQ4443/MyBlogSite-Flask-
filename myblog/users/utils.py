import os
import secrets
from PIL import Image
from flask import url_for
from myblog import app, mail # importing from package imports from init file
from flask_mail import Message

# function for saving pictures
def save_picture(form_picture):
    # generates 8 byte hex
    random_hex = secrets.token_hex(8)
    # get name and ext of file
    _, f_ext = os.path.splitext(form_picture.filename)
    # concatenate
    picture_fn = random_hex + f_ext
    # get full path of picture location 
    picture_path = os.path.join(app.root_path, 'static/flask profile pictures', picture_fn)

    # resize image with Pillow before saving
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    # returns file name
    return picture_fn

# method for sending a reset password email to the given user
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender=os.environ.get('EMAIL_USER'), recipients=[user.email])
    msg.body = f'''To Reset your password, visit the following link: {url_for('reset_token', token=token, _external=True)}
    
    If you did not make this request, simply ignore this email and no changes will be made.
    '''
    # mail.send(msg)
    # this function does not work as no smtp account is linked with this project