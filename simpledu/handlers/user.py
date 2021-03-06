from flask import Blueprint, render_template
from simpledu.models import User

user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/<username>')
def user_index(username):
    date = User.query.filter_by(username=username).first()
    return render_template('detail.html',date=date)
