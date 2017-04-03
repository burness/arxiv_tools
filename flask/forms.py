# pythonspot.com
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import fcntl

USER_INFO_FILE = './static/user_info.csv'
# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '213949948595995'
 
class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])
    subject = TextField('Subject:', validators=[validators.required()])
 

def write_file(**user_info):
    # write the file with amend mode
    with open(USER_INFO_FILE,'a') as fwrite:
        # file_no = fwrite.fileno()
        # add the lock of the file when you write the content to the file
        # fcntl.lockf(file_no,fcntl.LOCK_EX|fcntl.LOCK_NB)
        temp_line = user_info['name'] +',' +user_info['subject']+',' + user_info['email']+'\n'
        fwrite.write(temp_line)


@app.route("/", methods=['GET', 'POST'])
def register_email():
    form = ReusableForm(request.form)
    print form.errors
    if request.method == 'POST':
        name = request.form['name']
        subject = request.form['subject']
        subject = '\t'.join([temp.strip(' ') for temp in subject.split(',')])
        print subject
        email = request.form['email']

        
        if form.validate():
            # Save the comment here.
            flash('Thanks for registration ' + name)
            user_info = {'name': name, 'subject': subject, 'email': email}
            # write the info of the user to a file
            write_file(**user_info)
        else:
            flash('Error: All the form fields are required. ')

    return render_template('hello.html', form=form)
 
if __name__ == "__main__":
    app.run()
