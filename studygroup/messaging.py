from flask import render_template
from .application import meetup


def send_message(subject, recipient, text_body):
    response = meetup.post(
        '2/message',
        data={
            'subject': subject,
            'message': text_body,
            'member_id': long(recipient.meetup_member_id)
        },
    )
    return response


def send_join_notification(recipient, user, group):
    send_message(
        'BostonPython: {0} is joining you at {1}!'.format(user.full_name, group.name),
        recipient,
        render_template(
            'email/joined_group.txt',
            user=user,
            group=group
        )
    )
