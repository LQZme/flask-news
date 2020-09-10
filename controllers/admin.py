from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.User import User
from werkzeug.security import check_password_hash

admin_route = Blueprint('admin', __name__)


@admin_route.route('/')
def index():
    return render_template('/admin/test.html')


@admin_route.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, is_valid=1).first()
        if user and check_password_hash(user.passwd, password):
            session['isLogged'] = 1
            session['username'] = username
            return redirect(url_for(".index"))
        else:
            flash("账号或密码错误！")
    return render_template('/admin/login.html')
