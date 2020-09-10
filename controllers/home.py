from flask import Blueprint, render_template
from models.Article import Article

home_route = Blueprint('home', __name__)


@home_route.route('/')
def index():
    news = Article.query.filter_by(is_valid=1).all()
    return render_template("home/index.html", news=news)


# 分类页
@home_route.route('/type/<name>')
def type(name):
    news = Article.query.filter_by(types=name).all()
    return render_template("home/type.html", news=news, name=name)


# 详情页
@home_route.route('/detail/<int:pk>')
def detail(pk):
    news = Article.query.get(pk)
    return render_template("home/detail.html", news=news)


# 推荐页
@home_route.route('/recommend/')
def recommend():
    news = Article.query.filter_by(is_recommend=1).all()
    return render_template("home/recommend.html", news=news)
