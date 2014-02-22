from flask import (g, request, redirect, render_template,
                   session, url_for, jsonify)

from application import app, meetup
from models import db, User, Group
from auth import login_required
from forms import GroupForm

@app.before_request
def load_user():
    user_id = session.get('user_id')
    if user_id:
        g.user = User.query.filter_by(id=user_id).first()
    else:
        g.user = None


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/groups')
@login_required
def show_groups():
    g.groups = Group.all_with_memberships()
    return render_template('groups.html')

@app.route('/group/<id>')
def show_group(id):
    g.group = Group.query.filter_by(id=id).first()
    return render_template('show_group.html')

@app.route('/group/new', methods=('GET', 'POST'))
def new_group():
    form = GroupForm()
    if form.validate_on_submit():
        group = form.save()
        return redirect(url_for('show_group', id=group.id))
    return render_template('new_group.html', form=form)

@app.route('/join_group', methods=('POST',))
def join_group():
    pass


@app.route('/members')
@app.route('/members/<int:offset>')
@login_required
def show_members(offset=None):
    g.users = User.query.all()
    return render_template('members.html')

    # if 'meetup_token' in session:
    #     if offset is None:
    #         offset = 0
    #
    #     me = meetup.get(
    #         '2/members',
    #         data={
    #             'group_id': settings.MEETUP_GROUP_ID,
    #             'page': 20,
    #             'offset': offset
    #         })
    #
    #     return render_template(
    #         'members.html',
    #         members=me.data['results'],
    #         next_offset=offset + 1)
    #
    # return redirect(url_for('login'))


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

@app.route('/boom')
def boom():
    raise Exception('BOOM')


@app.route('/login')
def login():
    return meetup.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    session.clear()
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

    meetup_response = meetup.get('2/member/self')
    member_details = meetup_response.data
    member_id = str(member_details['id'])

    user = User.query.filter_by(meetup_member_id=member_id).first()
    if not user:
        user = User(
            full_name=member_details['name'],
            meetup_member_id=member_id
        )
        db.session.add(user)
        db.session.commit()

    session['user_id'] = user.id
    return redirect(url_for('index'))


@meetup.tokengetter
def get_meetup_oauth_token():
    return session.get('meetup_token')
