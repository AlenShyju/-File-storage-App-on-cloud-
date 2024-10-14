from flask import Flask, request, render_template, send_from_directory, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required to use sessions

# Ensure the 'uploads' folder exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Hardcoded credentials
CREDS = {'Admin':'Admin001',
         'Alen':'alen123',
         'yash':'yash123',
         'amar':'amar123',
         'mohammed':'mohammed123'}

# Route for the login page
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if(username in CREDS):
            if password == CREDS[username]:
                session['user'] = username
                return redirect(url_for('index'))
            else:
                return 'Invalid credentials, please try again.'
    return render_template('login.html')

# Route for the homepage (after login)
@app.route('/index')
def index():
    if 'user' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

# Route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'user' in session:
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        
        os.makedirs(f"{app.config['UPLOAD_FOLDER']}/{session['user']}", exist_ok=True)
        
        filename = os.path.join(f"{app.config['UPLOAD_FOLDER']}/{session['user']}", file.filename)
        file.save(filename)
        return "<h3 style = 'font-size:20px; color:green' align = 'center'>File uploaded successfully!</h3>"
    return redirect(url_for('login'))

# Route to view uploaded files
@app.route('/uploads')
def list_files():
    if 'user' in session:
        try:
            files = os.listdir(f"{app.config['UPLOAD_FOLDER']}/{session['user']}")
        except FileNotFoundError:
            files = ["no file found."]
        return render_template('uploads.html', files=files)
        
    return redirect(url_for('login'))

# Route to handle file downloads
@app.route('/download/<filename>')
def download_file(filename):
    if 'user' in session:
        return send_from_directory(f"{app.config['UPLOAD_FOLDER']}/{session['user']}", filename)
    return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# Route for the About page
@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
