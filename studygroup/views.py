from flask import (g, request, redirect, render_template,
                   session, url_for, jsonify, Blueprint)

from models import db, User, Group
from application import meetup
from auth import login_required
from forms import GroupForm

studygroup = Blueprint("studygroup", __name__, static_folder='static')

@studygroup.before_request
def load_user():
    user_id = session.get('user_id')
    if user_id:
        g.user = User.query.filter_by(id=user_id).first()
    else:
        g.user = None


@studygroup.route('/')
def index():
    return render_template('index.html')

@studygroup.route('/groups')
@login_required
def show_groups():
    g.groups = Group.all_with_memberships()
    return render_template('groups.html')

@studygroup.route('/group/<id>')
def show_group(id):
    g.group = Group.query.filter_by(id=id).first()
    return render_template('show_group.html')

@studygroup.route('/group/new', methods=('GET', 'POST'))
def new_group():
    form = GroupForm()
    if form.validate_on_submit():
        group = form.save()
        return redirect(url_for('.show_group', id=group.id))
    return render_template('new_group.html', form=form)

@studygroup.route('/join_group', methods=('POST',))
def join_group():
    pass


@studygroup.route('/members')
@studygroup.route('/members/<int:offset>')
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
    # return redirect(url_for('.login'))


@studygroup.route('/send_message/<int:member_id>', methods=['GET', 'POST'])
def send_message(member_id):
    if 'meetup_token' not in session:
        return redirect(url_for('.login'))

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

@studygroup.route('/boom')
def boom():
    raise Exception('BOOM')


@studygroup.route('/login')
def login():
    return meetup.authorize(callback=url_for('.authorized', _external=True))


@studygroup.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('.index'))


@studygroup.route('/login/authorized')
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
    return redirect(url_for('.index'))


@meetup.tokengetter
def get_meetup_oauth_token():
    return session.get('meetup_token')
