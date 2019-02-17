from flask import Blueprint, render_template
from flask_login import login_required

live = Blueprint('live', __name__, url_prefix='/live')

@live.route('/')
@login_required
def index():
    return render_template('live/index.html')
