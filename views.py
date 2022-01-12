from flask import redirect, url_for, session
from app import app, oauth, db
from models import Main
from utils import get_slot, login_required
from datetime import datetime

from flask.templating import render_template

@app.route('/response')
@login_required
def response():
    user_data = dict(session)
    current_time = datetime.now()
    slot = get_slot(current_time)
    if slot:
        # insert into db.main
        entry = Main(
            name = user_data['profile']['name'],
            slot = slot
        )
        try:
            db.session.add(entry)
            db.session.commit()
            return render_template('response.html', user_data=user_data, slot=slot)

        except:
            db.session.rollback()
            db.session.flush()
            return "Entry exists"
    else:
        return "Sorry, mess closed. Try again later."


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