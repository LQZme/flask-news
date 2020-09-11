from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length


#管理员表单验证
class UserForm(FlaskForm):

    username = StringField("管理员账号",
                           validators=[DataRequired(message="请输入管理员账号！"),
                                       Length(5, 12, message="账号长度要求5~12字符！")],
                           render_kw={"class": "form-control",
                                      "placeholder": "请输入管理员账号"})

    password = PasswordField("管理员密码",
                             validators=[DataRequired(message="请输入管理员密码！"),
                                         Length(6, 8, message="密码长度要求6~8字符！")],
                             render_kw={"class": "form-control",
                                        "placeholder": "请输入管理员密码"})

    repassword = PasswordField("确认密码",
                               validators=[DataRequired(message="请再次输入密码！"),
                                           EqualTo("password", message="两次密码不一致!")],
                               render_kw={"class": "form-control",
                                          "placeholder": "请再次输入密码！"})

    is_valid = BooleanField("是否启用")

    submit = SubmitField("提交", render_kw={"class": "btn btn-primary"})
