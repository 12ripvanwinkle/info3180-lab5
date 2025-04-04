"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app ,db
from flask import render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import os
from .forms import MovieForm
from .models import Movie
from app import csrf
from flask_wtf.csrf import generate_csrf
###
# Routing for your application.
###

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


@app.route('/api/v1/movies', methods=['POST'])
@csrf.exempt  # Disable CSRF for this API route
def movies():
    # Debugging statements
    print("Request files:", request.files)  # See what files are being sent
    print("Request form data:", request.form)  # See other form fields being sent

    if 'poster' not in request.files:
        return jsonify({"errors": ["Poster file is missing"]}), 400  # <-- File not found in request

    title = request.form.get('title')
    description = request.form.get('description')
    file = request.files.get('poster')  # <-- Fetch file from request

    # Validate form data
    if not title or not description or not file:
        return jsonify({"errors": ["Title, Description, and Poster are required"]}), 400

    # Validate file type and save it
    if file.filename == '':  
        return jsonify({"errors": ["No selected file"]}), 400  # <-- Check if filename is empty

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        return jsonify({"errors": ["Invalid file type"]}), 400

    # Save movie to database
    new_movie = Movie(title=title, description=description, poster=filename)
    db.session.add(new_movie)
    db.session.commit()

    return jsonify({
        "message": "Movie Successfully added",
        "title": title,
        "poster": filename,
        "description": description
    }), 201

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
 return jsonify({'csrf_token': generate_csrf()})

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404