from io import BytesIO
from flask import Blueprint, redirect, render_template, request, flash, send_file, url_for
from flask_login import current_user, login_required
from .models import File, Link
from . import db

views = Blueprint('views', __name__)

@views.route('/flash')
def flash_test():
    
    flash('Flash test!')

    flash('Flash test 2!')

    return redirect('/')

@views.route('/')
def index():
    return render_template('index.html', current_user = current_user)

@views.route('/files', methods=['GET', 'POST'])
@login_required
def files():

    if request.method == 'GET':

        return render_template('files.html', user = current_user)
    
    if request.method == 'POST':

        files = request.files.getlist('file')

        public = request.form.get('public')

        if not files:

            flash('Please upload a file!')

            return render_template('files.html', user = current_user)
        
        for file in files:

            new_file = File(file.filename, file.read(), public == 'True', current_user.id)

            db.session.add(new_file)

            db.session.commit()

            flash(f'{file.filename} uploaded!')

        return render_template('files.html', user = current_user)

@views.route('/download/<file_id>')
def download(file_id):

    file = File.query.filter_by(id = file_id).first()

    if not file:
            
        flash('File does not exist!')

        if current_user.is_authenticated:

            return render_template('files.html', current_user = current_user)
        
        return render_template('index.html', current_user = current_user)
    
    if file.public:

        return send_file(BytesIO(file.data), download_name=file.name, as_attachment=True)
    
    if not current_user.is_authenticated:

        flash('You do not have access to that file!')

        return render_template('index.html', current_user = current_user)

    if file.user_id != current_user.id:

        flash('You do not have access to that file!')

        return render_template('files.html', current_user = current_user)

    return send_file(BytesIO(file.data), download_name=file.name, as_attachment=True)

@views.route('/delete/file/<file_id>')
@login_required
def delete_file(file_id):

    file = File.query.filter_by(id = file_id).first()

    if not file:
            
        flash('File does not exist!')

        return render_template('files.html', current_user = current_user)

    if file.user_id != current_user.id:

        flash('You do not have access to that file!')

        return render_template('files.html', current_user = current_user)

    db.session.delete(file)

    db.session.commit()

    flash('File deleted!')

    return redirect(url_for('views.files'))

@views.route('/links', methods=['GET', 'POST'])
@login_required
def links():

    if request.method == 'GET':

        return render_template('links.html', current_user = current_user)

    if request.method == 'POST':

        link = request.form.get('link')

        public = request.form.get('public')

        if not link or not link.startswith('http') and not link.startswith('https'):

            flash('Please enter a valid link! (Starts with http:// or https://)')

            return render_template('links.html', current_user = current_user)

        new_link = Link(link, public == 'True', current_user.id)

        db.session.add(new_link)

        db.session.commit()

        flash('Link created!')

        return render_template('links.html', current_user = current_user)
    
@views.route('/link/<link_id>')
def link(link_id):

    link = Link.query.filter_by(id = link_id).first()

    if not link:

        if current_user.is_authenticated:

            flash('Link does not exist!')

            return render_template('links.html', current_user = current_user)
            
        return render_template('index.html', current_user = current_user)
    
    if link.public:

        return redirect(link.url)
    
    if not current_user.is_authenticated:

        flash('You do not have access to that link!')

        return render_template('index.html', current_user = current_user)

    if link.user_id != current_user.id:

        flash('You do not have access to that link!')

        return render_template('links.html', current_user = current_user)

    return redirect(link.url)

@views.route('/delete/link/<link_id>')
@login_required
def delete_link(link_id):

    link = Link.query.filter_by(id = link_id).first()

    if not link:
            
        flash('Link does not exist!')

        return render_template('links.html', current_user = current_user)

    if link.user_id != current_user.id:

        flash('You do not have access to that link!')

        return render_template('links.html', current_user = current_user)

    db.session.delete(link)

    db.session.commit()

    flash('Link deleted!')

    return redirect(url_for('views.links'))