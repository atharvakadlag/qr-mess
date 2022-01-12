from logging import error
from flask import redirect, url_for, session
from app import app, oauth, db
from models import Main
from utils import get_slot, login_required
from datetime import datetime
from sqlalchemy import exc

from flask.templating import render_template

@app.route('/entries')
def entries():
    # get all the entries from the database
    entries = Main.query.all()
    print(Main.query.count())
    for entry in entries:
        print(entry.name)
        print(entry.slot)
        print(entry.date)
    return render_template('entries.html', entries=entries)

@app.route('/response')
@login_required
def response():
    user_data = dict(session)
    current_time = datetime.now()
    slot = get_slot(current_time)
    name = user_data['profile']['name']
    if slot:
        # insert into db.main
        entry = Main(
            name = name,
            slot = slot
        )
        try:
            db.session.add(entry)
            db.session.commit()
            return render_template('response.html', name=name, slot=slot)

        except exc.IntegrityError:
            db.session.rollback()
            db.session.flush()
            return render_template('error.html', error="Entry already exists!")
        except Exception as e:
            print(e)
            return render_template('error.html', error="Something went wrong!")
    else:
        return render_template('error.html', error="Sorry, mess closed. Try again later!")


@app.route('/')
@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    session['profile'] = user_info
    session.permanent = True
    return redirect('/response')


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')