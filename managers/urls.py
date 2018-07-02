# Author:gyk

from django.conf.urls import url
from managers import views

urlpatterns = [
    # url(r'^test/$', views.test),
    # base
    url(r'^$', views.index, name=""),
    url(r'^login/$', views.login, name="login"),
    url(r'^login_out/$', views.login_out, name="login_out"),
    url(r'^register_auth/$', views.register_auth, name="register_auth"),

    # 学生
    url(r'^student_register/$', views.student_register, name="student_register"),
    url(r'^student_index/$', views.student_index, name="student_index"),
    url(r'^ask/$', views.ask, name="ask"),
    url(r'^stu_InfoUp/$', views.stu_InfoUp, name="stu_InfoUp"),
    url(r'^ask_solve/(\d+)$', views.ask_solve, name="ask_solve"),
    url(r'^ask_del/(\d+)$', views.ask_del, name="ask_del"),

    # 教师
    url(r'^teacher_register/$', views.teacher_register, name="teacher_register"),
    url(r'^teacher_index/$', views.teacher_index, name="teacher_index"),
    url(r'^answer/(\d+)$', views.answer, name="answer"),
    url(r'^tea_InfoUp/$', views.tea_InfoUp, name="tea_InfoUp"),
    url(r'^ans_del/(\d+)$', views.ans_del, name="ans_del"),
    url(r'^tea_search/$', views.tea_search, name="tea_search"),

    # 管理员
    url(r'^manager/$', views.manager, name="manager"),
    url(r'^admin_question/$', views.admin_question, name="admin_question"),
    url(r'^admin_student/$', views.admin_student, name="admin_student"),
    url(r'^admin_teacher/$', views.admin_teacher, name="admin_teacher"),
    url(r'^admin_askUp/(\d+)$', views.admin_askUp, name="admin_askUp"),
    url(r'^admin_askDel/(\d+)$', views.admin_askDel, name="admin_askDel"),
    url(r'^admin_stuUp/(\d+)$', views.admin_stuUp, name="admin_stuUp"),
    url(r'^reset_pwd1/(\d+)$', views.reset_pwd1, name="reset_pwd1"),
    url(r'^admin_teaUp/(\d+)$', views.admin_teaUp, name="admin_teaUp"),
    url(r'^reset_pwd2/(\d+)$', views.reset_pwd2, name="reset_pwd2"),
]
