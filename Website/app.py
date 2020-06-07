# IMPORTS FOR FLASK

from flask import Flask, render_template, session, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, Email # CHECK THE INPUT TO HAVE NOT BE BLANK
# IMPORTS FOR DES

from Crypto.Cipher import DES


app = Flask(__name__) # Create out Flask application

app.config["SECRET_KEY"] = 'DEVA-VADA-31419DE-97315934153579' # Configuration key for CSRF security

# FORMS

class EncryptForm(FlaskForm):

    key = TextAreaField('Enter a key:', validators=[DataRequired()])
    decoded_message = TextAreaField(validators=[DataRequired])
    submit = SubmitField('Submit')

class DecryptForm(FlaskForm):

    key = TextAreaField('Enter a key:', validators=[DataRequired()])
    encoded_message = TextAreaField(validators=[DataRequired])
    submit = SubmitField('Submit', validators=[DataRequired()])

# DES PROGRAM FUNCTIONS

def pad(message): # This is the padding function that allows users to enter any len string as a message by adding the remainder for mess/8
    while len(message) % 8 != 0:
        message = message + ' '  # Adds a space to message
    return bytes(message, encoding='ascii')

# ROUTING FUNCTIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    
    encrypt_form = EncryptForm()

    if encrypt_form.validate_on_submit(): # ONCE THEY SUBMIT FORM

        session['key'] = bytes(encrypt_form.key.data, 'ascii') # GRABS WHAT THE USER PROVIDED
        session['decoded_message'] = encrypt_form.decoded_message.data

        # DES ENCRYPTION LOGIC
        des = DES.new(session['key'], DES.MODE_ECB)
        session['decoded_message'] = pad(session['decoded_message'])
        session['decoded_message'] = des.encrypt(session['decoded_message'])

        return redirect(url_for('en_results')) # ONLY HAPPEND WHEN SUBMISSION
    return render_template('encrypt.html', encrypt_form=encrypt_form)

@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():

    decrypt_form = DecryptForm()

    if decrypt_form.validate_on_submit(): # ONCE THEY SUBMIT FORM

        session['key'] = decrypt_form.key.data
        session['encoded_message'] = decrypt_form.encoded_message.data

        return redirect(url_for('de_results', decrypt_form=decrypt_form))
    return render_template('decrypt.html', decrypt_form=decrypt_form)

@app.route('/decryption-results')
def de_results():
    return render_template('de_results.html')

@app.route('/encryption-results')
def en_results():
    return render_template('en_results.html')

if __name__ == "__main__":
    app.run() # RUN THE APPLICATION