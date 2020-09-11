from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.User import User
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from common.forms import UserForm
from application import db

admin_route = Blueprint('admin', __name__)


def admin_login_require(f):
    # 使用functools.wraps装饰器装饰内函数wrapper，从而可以保留被修饰的函数属性
    @wraps(f)
    def wrapper(*args, **kwargs):
        # 判断是否登录
        if 'isLogged' not in session or session['isLogged'] != 1:
            # 如果session中没有isLogged的键名，则重定向到登录页
            return redirect(url_for('.login'))
        return f(*args, **kwargs)
    return wrapper


@admin_route.route('/')
@admin_login_require
def index():
    return render_template('/admin/index.html')


@admin_route.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, is_valid=1).first()
        if user and check_password_hash(user.passwd, password):
            session['isLogged'] = 1
            session['userid'] = user.id
            session['username'] = username
            return redirect(url_for(".index"))
        else:
            flash("账号或密码错误！")
    return render_template('/admin/login.html')


# 退出
@admin_route.route('/logout')
def logout():
    session.pop('userid', None)
    session.pop('username', None)
    return redirect(url_for(".login"))


# 新闻列表
@admin_route.route('/article/')
@admin_route.route('/article/<int:page>')
@admin_login_require
def article_index(page=None):
    return render_template('/admin/article/index.html')


# 新增新闻
@admin_route.route('/article/add', methods=['GET', 'POST'])
@admin_login_require
def article_add():
    return render_template('/admin/article/add.html')


# 编辑新闻
@admin_route.route('/article/edit/<int:pk>', methods=['GET', 'POST'])
@admin_login_require
def article_edit(pk):
    return render_template('/admin/article/edit.html')


# 删除单个新闻
@admin_route.route('/article/delete/<int:pk>')
@admin_login_require
def article_delete(pk):
    pass


# 管理员列表
@admin_route.route('/user')
@admin_route.route('/user/<int:page>')
@admin_login_require
def user_index(page=None):
    if page is None:
        page = 1
    keyword = request.args.get("search")
    if keyword:
        users = User.query.filter(User.username.contains(keyword)).order_by(User.id).paginate(page, per_page=1)
        condition = "?search=" + keyword
        return render_template('/admin/user/index.html', users=users, condition=condition)
    else:
        users = User.query.order_by(User.username).paginate(page=page, per_page=1)
        return render_template('/admin/user/index.html', users=users)


# 新增管理员
@admin_route.route('/user/add', methods=['GET', 'POST'])
@admin_login_require
def user_add():
    form = UserForm()
    if form.validate_on_submit():
        try:
            user = User(form.username.data,
                        form.password.data,
                        form.is_valid.data)
            db.session.add(user)
            db.session.commit()
            flash("成功添加管理员!")
            return redirect(url_for('.user_index'))
        except:
            flash("添加管理员失败!", category="error")

    return render_template('/admin/user/add.html', form=form)


# 编辑管理员
@admin_route.route('/user/edit/<int:pk>', methods=['GET', 'POST'])
@admin_login_require
def user_edit(pk):
    user = User.query.get(pk)
    if user is None:
        return redirect(url_for('.user_index'))
    form = UserForm(obj=user)
    if form.validate_on_submit():
        try:
            user.username = form.username.data
            user.passwd = generate_password_hash(form.password.data)
            user.is_valid = form.is_valid.data
            db.session.add(user)
            db.session.commit()
            flash("管理员编辑成功！")
            return redirect(url_for('.user_index'))
        except:
            flash("管理员编辑失败！", category="error")

    return render_template('/admin/user/edit.html', form=form)


# 删除单个管理员
@admin_route.route('/user/delete/<int:pk>')
@admin_login_require
def user_delete(pk):
    user = User.query.get(pk)
    if user is None:
        return redirect(url_for('.user_index'))
    try:
        db.session.delete(user)
        db.session.commit()
        flash("管理员删除成功！")
    except:
        flash("管理员删除失败！", category="error")
    return redirect(url_for('.user_index'))
