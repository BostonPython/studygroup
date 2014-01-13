from flask import (
    Flask, redirect, url_for, session,
    request, jsonify, render_template)
from flask_oauthlib.client import OAuth
import settings


app = Flask(__name__)
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

meetup = oauth.remote_app(
    'meetup',
    consumer_key=settings.MEETUP_OAUTH_KEY,
    consumer_secret=settings.MEETUP_OAUTH_SECRET,
    request_token_params={'scope': 'messaging'},
    base_url='https://api.meetup.com/',
    access_token_method='POST',
    access_token_url='https://secure.meetup.com/oauth2/access',
    authorize_url='https://secure.meetup.com/oauth2/authorize'
)


@app.route('/')
def index():
    if 'meetup_token' not in session:
        return redirect(url_for('login'))

    group = meetup.get('2/group/%s' % settings.MEETUP_GROUP_ID)
    return render_template('index.html', group=group.data)

@app.route('/members')
@app.route('/members/<int:offset>')
def members(offset=None):
    if 'meetup_token' in session:
        if offset is None:
            offset = 0

        me = meetup.get(
            '2/members',
            data={
                'group_id': settings.MEETUP_GROUP_ID,
                'page': 20,
                'offset': offset
            })

        return render_template(
            'members.html',
            members=me.data['results'],
            next_offset=offset + 1)

    return redirect(url_for('login'))


@app.route('/send_message/<int:member_id>', methods=['GET', 'POST'])
def send_message(member_id):
    if 'meetup_token' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        member = meetup.get('2/member/%s' % member_id)
        return render_template("send_message.html", member=member.data)
    elif request.method == 'POST':
        response = meetup.post(
            '2/message',
            data={
                'subject': request.form['subject'],
                'message': request.form['message'],
                'member_id': request.form['member_id']
            })
        return jsonify(response.data)
    else:
        return "Invalid Request", 500


@app.route('/login')
def login():
    return meetup.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    session.pop('meetup_token', None)
    return redirect(url_for('index'))


@app.route('/login/authorized')
@meetup.authorized_handler
def authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['meetup_token'] = (resp['access_token'], '')
    me = meetup.get('activity')
    return jsonify(me.data)


@meetup.tokengetter
def get_meetup_oauth_token():
    return session.get('meetup_token')


if __name__ == '__main__':
    app.run(debug=True, port=80)