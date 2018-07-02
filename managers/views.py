from django.shortcuts import render, redirect, HttpResponse
from managers import models, form
import time
import hashlib
from django.db.models import Q, F


'''
# def test(req):
#     models.Profession.objects.create(name='网络工程',)
#     models.Profession.objects.create(name='计算机',)
#     models.Profession.objects.create(name='电气',)
#     models.Profession.objects.create(name='信工',)
#     models.Profession.objects.create(name='会计',)
#     models.Profession.objects.create(name='物流',)
#     return HttpResponse('test.html')
'''

# 加密
def take_md5(content):
    hash = hashlib.md5()    # 创建hash加密实例
    hash.update(content.encode())    # hash加密
    result = hash.hexdigest()  # 得到加密结果
    return result

# 注销
def login_out(req):
    del req.session['user_info']  # 删除session
    return redirect('/login')

# session验证
def auth_json(func):
    def inner(req, *args, **kwargs):

        user_info = req.session.get('user_info')
        if user_info:
            return func(req, *args, **kwargs)
        tip = "请登录"
        return redirect("/login", {'error': tip})

    return inner

# 查询问题信息集合
def check_ask(ask_list):
    # 取到所有问题集合
    # 定义两个列表用来存放数据集和编号
    gatherValue = []
    gatherNo = []
    count = 1
    # 遍历所有问题，取出问题序列号、问题编号、主题、内容、提问学生、提问时间、是否解决、回答时间、回答教师、回答内容
    for i in ask_list:
        askNo = i.askNo
        askTopic = i.askTopic
        askContent = i.askContent
        studentName = i.studentNos.studentName
        askTime = i.askTime
        status_choices = i.get_status_display()
        isDel = i.get_isDel_display()
        # 将取到的一行数据集写成一个字典
        obj_list = {"askNo": askNo,
                    "count": count,
                    "askTopic": askTopic,
                    "askContent": askContent,
                    "studentName": studentName,
                    "askTime": askTime,
                    "status_choices": status_choices,
                    "isDel": isDel
                    }
        # 若已被回答，则有回答，并将时间加入列表
        try:
            answerObj = models.Answer.objects.get(askNos__askNo=askNo)
            answerTime = answerObj.answerTime
            teacherName = answerObj.teacherNos.teacherName
            answerContent = answerObj.answerContent
            if answerObj:
                obj_list.setdefault("answerTime", answerTime)
                obj_list.setdefault("teacherName", teacherName)
                obj_list.setdefault("answerContent", answerContent)
        except:
            pass
        # 将一行数据集追和下标值加到列表中
        gatherValue.append(obj_list)
        gatherNo.append(count)
        count += 1
    # 将两集合合并为一个字典
    data_list = dict(zip(gatherNo, gatherValue))
    return data_list

# 查询单个问题信息
def check_single_ask(count):
    askObj = models.Ask.objects.get(askNo=count)
    askNo = askObj.askNo
    askTopic = askObj.askTopic
    askContent = askObj.askContent
    askTime = askObj.askTime
    studentName = askObj.studentNos.studentName
    status = askObj.status
    status_choice = askObj.get_status_display()
    isDel = askObj.isDel
    print("******",":",isDel)
    data_list = {"askNo": askNo,
                 "askTopic": askTopic,
                 "askContent": askContent,
                 "askTime": askTime,
                 "studentName": studentName,
                 "status_choice": status_choice,
                 "status": status,
                 "isDel": isDel
                 }
    try:
        answerObj = models.Answer.objects.get(askNos__askNo=count)
        teacherName = answerObj.teacherNos.teacherName
        answerTime = answerObj.answerTime
        answerContent = answerObj.answerContent
        if answerObj:
            data_list.setdefault("teacherName", teacherName)
            data_list.setdefault("answerTime", answerTime)
            data_list.setdefault("answerContent", answerContent)
    except: pass

    return data_list

# 查询回复信息集合
def check_answer(answer_list):
    count = 1
    gatherValue = []
    gatherNo = []
    for i in answer_list:
        answerNo = i.answerNo
        askTopic = i.askNos.askTopic
        askContent = i.askNos.askContent
        studentName = i.askNos.studentNos.studentName
        askTime = i.askNos.askTime
        status_choices = i.askNos.get_status_display()
        answerObj = models.Answer.objects.get(answerNo=answerNo)
        answerTime = answerObj.answerTime
        teacherName = answerObj.teacherNos.teacherName
        answerContent = answerObj.answerContent
        obj_list = {
            "count": count,
            "answerNo": answerNo,
            "askTopic": askTopic,
            "askContent": askContent,
            "studentName": studentName,
            "askTime": askTime,
            "status_choices": status_choices,
            "answerTime": answerTime,
            "teacherName": teacherName,
            "answerContent": answerContent,
        }
        gatherValue.append(obj_list)
        gatherNo.append(count)
        count += 1
    data_list = dict(zip(gatherNo, gatherValue))
    return data_list

# **************登录/注册**************
# 系统主页
def index(req):
    ask_list = models.Ask.objects.filter(Q(isDel=0))[0:20]
    data_list = check_ask(ask_list)
    return render(req, "index.html", {"data_list": data_list})

# 登录
def login(req):
    # a = verify_code()
    if req.method == 'POST':
        user = req.POST.get("user")
        pwd = req.POST.get("pwd")
        role = req.POST.get("role")

        status = form.Role(role, user, pwd)
        if status == 0:
            print("***:status")
            req.session['user_info'] = {'id': user}  # 设置session
            req.session.set_expiry(2000)
            if role == "student":
                return redirect('/student_index')
            elif role == "teacher":
                return redirect('/teacher_index')
            elif role == "manager":
                return redirect('/manager')
        if status == 1:
            error = "密码错误！"
            return render(req, "login.html", {"error":error})
        if status == 2:
            error = "用户名不存在！"
            return render(req, "login.html", {"error":error})

    return render(req,"login.html",)

# 注册用户验证
def register_auth(req):
    if req.method == "POST":
        id = req.POST.get("id")
        user = req.POST.get("user")
        print("id and user:",id,user)
        status = form.User(id, user)
        print("status:",status)
        return HttpResponse(status)

# 学生注册
def student_register(req):
    if req.method == 'POST':
        name = req.POST.get("name")
        id = req.POST.get("id")
        profession = req.POST.get("profession")
        Email = req.POST.get("Email")
        pwd = req.POST.get("pwd")
        rpwd = req.POST.get("rpwd")
        if name and id and profession and Email and pwd and rpwd:
            a = models.Student.objects.filter(studentNo=id)
            # 判断学号是否已经存在
            if not a:
                b = models.Student.objects.filter(studentEmail=Email)
                # 判断Email是否已经存在
                if not b:
                    if pwd == rpwd:
                        dic = {
                            "studentName": name,
                            "studentNo": id,
                            "professionNos_id":profession,
                            "studentEmail": Email,
                            "studentPwd": take_md5(pwd)
                        }
                        models.Student.objects.create(**dic)
                        message = '您已成功注册！'
                        return render(req, 'student_register.html',{'message':message})
                    else:
                        tip1 = '两次密码不一致！'
                        return render(req, 'student_register.html',{'tip':tip1})
                else:
                    tip2 = '邮箱已被注册！'
                    return render(req, 'student_register.html', {'tip': tip2})
            else:
                tip3 = '学号已被注册！'
                return render(req, 'student_register.html', {'tip': tip3})
        else:
            tip4 = '请填写完整信息！'
            return render(req,'student_register.html', {'tip': tip4})
    return render(req, 'student_register.html')

# 教师注册
def teacher_register(req):
    if req.method == 'POST':
        name = req.POST.get('name')
        id = req.POST.get("id")
        profession = req.POST.get("profession")
        Email = req.POST.get("Email")
        pwd = req.POST.get("pwd")
        rpwd = req.POST.get("rpwd")
        if name and id and profession and Email and pwd and rpwd:
            a = models.Teacher.objects.filter(teacherNo=id)
            if not a:
                b = models.Teacher.objects.filter(teacherEmail=Email)
                if not b:
                    if pwd == rpwd:
                        dic = {"teacherName": name, "teacherNo": id, "professionNos_id": profession,
                               "teacherEmail": Email,"teacherPwd": pwd}
                        models.Teacher.objects.create(**dic)
                        message = '您已成功注册！'
                        return render(req, 'teacher_register.html', {'message': message})
                    else:
                        tip1 = '两次密码不一致！'
                        return render(req, 'teacher_register.html', {'tip': tip1})
                else:
                    tip2 = '邮箱已被注册！'
                    return render(req, 'teacher_register.html', {'tip': tip2})
            else:
                tip3 = '工号已被注册！'
                return render(req, 'teacher_register.html', {'tip': tip3})
        else:
            tip4 = '请填写完整信息！'
            return render(req, 'teacher_register.html', {'tip': tip4})
    return render(req, 'teacher_register.html')

# ***************主页******************
# 学生主页
@auth_json
def student_index(req):
    user = req.session.get('user_info')['id']
    # 显示个人和问题信息
    if user:
        studentName = models.Student.objects.get(studentNo=user).studentName
        # studentName = models.Student.objects.filter(studentNo=user).values("studentName")[0]['studentName']
        # 通过用户名取到问题的集合
        ask_list = models.Ask.objects.filter(Q(studentNos__studentNo=user) & Q(isDel=0))
        data_list = check_ask(ask_list)
        return render(req, 'student_index.html', {"data_list": data_list, "studentName": studentName})
    else:
        return redirect("/login")

# 教师主页
@auth_json
def teacher_index(req):
    user = req.session.get('user_info')['id']
    # 显示个人和问题信息
    if user:
        teacherName = models.Teacher.objects.get(teacherNo=user).teacherName
        # 通过用户名取到问题的集合
        answer_list = models.Answer.objects.filter(Q(teacherNos__teacherNo=user) & Q(isDel=0))
        data_list = check_answer(answer_list)
        return render(req, 'teacher_index.html', {"data_list": data_list, "teacherName": teacherName})
    else:
        return redirect("/login")

# 管理员主页
@auth_json
def manager(req):
    user = req.session.get('user_info')['id']
    if user:
        return render(req, "manager.html")
    else:
        return redirect("/login")

# ************学生操作***************
# 提问
@auth_json
def ask(req):
    user = req.session.get('user_info')['id']
    if user:
        studentName = models.Student.objects.get(studentNo=user).studentName
        if req.method == "POST":
            user = req.session.get('user_info')['id']
            print("ask:",user)
            ask_topic = req.POST.get("ask_topic")
            ask_content = req.POST.get("ask_content")
            profession = req.POST.get("profession")
            print(user)
            if ask_topic:
                # print("zzzzzz:",ask_topic,ask_content,profession,user)
                dic={
                    # "askNo":3,
                    "askTopic": ask_topic,
                    "askContent": ask_content,
                    "askTime": time.strftime("%F"),
                    # "status":1,
                    # "isDel":1,
                    "askTypes_id": profession,
                    "studentNos_id": user
                }
                models.Ask.objects.create(**dic)
                models.Student.objects.filter(studentNo=user).update(askCount=F("askCount")+1)
                print("shujuku添加成功")
                success_add = "问题添加成功"
                return render(req,'ask.html', {"success_add":success_add, "studentName": studentName})
            else:
                failed_add = "请填写正确的概要！"
                return render(req, 'ask.html', {"failed_add": failed_add, "studentName": studentName})
        else:
            return render(req,'ask.html', {"studentName": studentName})
    else:
        return redirect('/login')

# 学生修改资料
@auth_json
def stu_InfoUp(req):
    user = req.session.get('user_info')['id']
    if user:
        studentName = models.Student.objects.get(studentNo=user).studentName
        person_massage = models.Student.objects.get(studentNo=user)
        if req.method == "POST":
            oldPwd = req.POST.get("oldPwd")
            newPwd = req.POST.get("newPwd")
            renewPwd = req.POST.get("renewPwd")
            newEmail = req.POST.get("newEmail")
            print("完成第一步")
            # 输入验证
            if oldPwd and ((newPwd and renewPwd) or newEmail):
                oldPwd = take_md5(oldPwd)
                oldPwds = models.Student.objects.filter(studentNo=user)[0].studentPwd
                if oldPwds == oldPwd:
                    # 改密码
                    if newPwd or renewPwd:
                        newPwd = take_md5(newPwd)
                        renewPwd = take_md5(renewPwd)
                        if newPwd == renewPwd:
                            models.Student.objects.filter(studentNo=user).update(studentPwd=newPwd)
                        else:
                            tip1 = '两次密码不一致！'
                            return render(req, "stu_InfoUp.html", {"tip": tip1, "studentName":studentName})
                    # 改邮箱
                    if newEmail:
                        models.Student.objects.filter(studentNo=user).update(studentEmail=newEmail)
                else:
                    tip2 = '原密码错误！'
                    return render(req, 'stu_InfoUp.html', {"person_massage": person_massage,
                                                           "tip": tip2,
                                                           "studentName":studentName})
            else:
                tip3 = "请填写完整修改信息！"
                return render(req, "stu_InfoUp.html", {"person_massage": person_massage,
                                                       "tip": tip3,
                                                       "studentName":studentName})
            massage = '信息修改成功！'
            return render(req, "stu_InfoUp.html", {"person_massage": person_massage,
                                                   "massage": massage,
                                                   "studentName":studentName})

        return render(req, 'stu_InfoUp.html', {"person_massage": person_massage, "studentName":studentName})
    else:
        return redirect("/login")

# 标记解决
@auth_json
def ask_solve(req, count):
    user = req.session.get('user_info')['id']
    if user:
        status = models.Ask.objects.filter(Q(askNo=count) & Q(isDel=0)).values("status")[0]["status"]
        print(status)
        if status == 1:
            models.Ask.objects.filter(Q(askNo=count) & Q(isDel=0)).update(status=0)
            print("改为“未解决”", status)
        else:
            models.Ask.objects.filter(Q(askNo=count) & Q(isDel=0)).update(status=1)
            print("改为“已解决”", status)
        return redirect('/student_index')
    else:
        return redirect('/login')

# 问题删除
@auth_json
def ask_del(req, count):
    user = req.session.get('user_info')['id']
    if user:
        models.Ask.objects.filter(Q(askNo=count)&Q(isDel=0)).update(isDel=1)
        print("修改成功")
        return redirect('/student_index')
    else:
        return redirect('/login')

# ***************教师操作*****************
# 教师修改资料
@auth_json
def tea_InfoUp(req):
    user = req.session.get('user_info')['id']
    if user:
        teacherName = models.Teacher.objects.filter(teacherNo=user).values("teacherName")[0]['teacherName']
        person_massage = models.Teacher.objects.filter(teacherNo=user)[0]
        if req.method == "POST":
            oldPwd = req.POST.get("oldPwd")
            newPwd = req.POST.get("newPwd")
            renewPwd = req.POST.get("renewPwd")
            newEmail = req.POST.get("newEmail")
            print("完成第一步")
            # 输入验证
            if oldPwd and ((newPwd and renewPwd) or newEmail):
                oldPwd = take_md5(oldPwd)
                oldPwds = models.Teacher.objects.filter(teacherNo=user)[0].teacherPwd
                if oldPwds == oldPwd:
                    # 改密码
                    if newPwd or renewPwd:
                        newPwd = take_md5(newPwd)
                        renewPwd = take_md5(renewPwd)
                        if newPwd == renewPwd:
                            models.Teacher.objects.filter(teacherNo=user).update(teacherPwd=newPwd)
                        else:
                            tip1 = '两次密码不一致！'
                            return render(req, "tea_InfoUp.html", {"tip": tip1, "teacherName": teacherName})
                    # 改邮箱
                    if newEmail:
                        models.Student.objects.filter(teacherNo=user).update(teacherEmail=newEmail)
                else:
                    tip2 = '原密码错误！'
                    return render(req, 'tea_InfoUp.html', {"person_massage": person_massage,
                                                           "tip": tip2,
                                                           "teacherName": teacherName})
            else:
                tip3 = "请填写完整修改信息！"
                return render(req, "tea_InfoUp.html", {"person_massage": person_massage,
                                                       "tip": tip3,
                                                       "teacherName": teacherName})
            massage = '信息修改成功！'
            return render(req, "tea_InfoUp.html", {"person_massage": person_massage,
                                                   "massage": massage,
                                                   "teacherName": teacherName})

        return render(req, 'tea_InfoUp.html', {"person_massage": person_massage, "teacherName": teacherName})
    else:
        return redirect("/login")

# 回复删除
@auth_json
def ans_del(req, count):
    user = req.session.get('user_info')['id']
    if user:
        models.Answer.objects.filter(Q(answerNo=count)&Q(isDel=0)).update(isDel=1)
        print("修改成功")
        return redirect('/teacher_index')
    else:
        return redirect('/login')

# 回复
@auth_json
def answer(req, count):
    print("count111:", count)
    user = req.session.get('user_info')['id']
    if user:
        teacherName = models.Teacher.objects.filter(teacherNo=user).values("teacherName")[0]["teacherName"]
        ask_list = models.Ask.objects.filter(askNo=count)[0]
        # print("askTopic:",ask_list.askTopic)
        if req.method == "POST":
            answerContent = req.POST.get("answerContent")
            if answerContent:
                al_mark = 0
                try:
                    al_mark = models.Answer.objects.get(askNos_id=count)
                except:
                    pass
                if not al_mark:
                    dic = {
                        "answerContent": answerContent,
                        "answerTime": time.strftime("%F"),
                        "askNos_id": count,
                        "teacherNos_id": user,
                    }
                    models.Answer.objects.create(**dic)
                    models.Teacher.objects.filter(teacherNo=user).update(answerCount=F("answerCount") + 1)
                    massage = "回复已成功提交！"
                    return render(req, 'answer.html', {"massage": massage})
                else:
                    tip1 = "该问题已经被回答！"
                    return render(req, 'tea_search.html', {"tip": tip1})
            else:
                tip2 = "请填写完成信息！"
                return render(req, 'tea_search.html', {"tip": tip2})
        return render(req, 'answer.html', {"ask_list": ask_list, "teacherName": teacherName, "count":count})
    else:
        return redirect('/login')

# 教师搜索
@auth_json
def tea_search(req):
    user = req.session.get('user_info')['id']
    # print("第一步")
    if user:
        # 取到所有问题集合
        teacherName = models.Teacher.objects.filter(teacherNo=user).values("teacherName")[0]["teacherName"]
        ask_list = models.Ask.objects.filter(Q(isDel=0) & Q(status=0))
        data_list = check_ask(ask_list)
        return render(req, "tea_search.html", {"data_list": data_list, "teacherName": teacherName,})
    else:
        return redirect('/login')

# *************************管理员操作*************************
# 问题管理
@auth_json
def admin_question(req):
    user = req.session.get('user_info')['id']
    if user:
        # 取到所有问题集合
        ask_list = models.Ask.objects.all().reverse()[1:11]
        data_list = check_ask(ask_list)
        return render(req, "admin_question.html",{"data_list": data_list,})
    return redirect("/login")

# 学生管理
@auth_json
def admin_student(req):
    user = req.session.get('user_info')['id']
    if user:
        # 取到所有学生信息集合集合
        stu_list = models.Student.objects.all()
        return render(req, "admin_student.html", {"stu_list": stu_list, })
    return redirect("/login")

# 教师管理
@auth_json
def admin_teacher(req):
    user = req.session.get('user_info')['id']
    if user:
        # 取到所有学生信息集合集合
        tea_list = models.Teacher.objects.all()
        return render(req, "admin_teacher.html", {"tea_list": tea_list, })
    return redirect("/login")

# 问题修改页面
@auth_json
def admin_askUp(req, count):
    user = req.session.get('user_info')['id']
    if user:
        if req.method == "POST":

            askTopic = req.POST.get("askTopic")
            askContent = req.POST.get("askContent")
            solve_status = req.POST.get("solve_status")
            answerContent = req.POST.get("answerContent")
            print("****************",askTopic,askContent,solve_status,answerContent)
            if askTopic:
                models.Ask.objects.filter(askNo=count).update(askTopic=askTopic)
            if askContent:
                models.Ask.objects.filter(askNo=count).update(askContent=askContent)
            if solve_status:
                models.Ask.objects.filter(askNo=count).update(status=solve_status)
            if answerContent:
                models.Answer.objects.filter(askNos__askNo=count).update(answerContent=answerContent)
        data_list = check_single_ask(count)
        return render(req, "admin_askUp.html", {"data_list": data_list})
    return redirect("/login")

# 学生修改页面
def admin_stuUp(req, count):
    user = req.session.get('user_info')['id']
    if user:
        if req.method == "POST":
            print("******++++++*******:", user,count)
            # newNo = req.POST.get("newNo")
            newName = req.POST.get("newName")
            newEmail = req.POST.get("newEmail")
            newProfession = req.POST.get("newProfession")
            del_flag = req.POST.get("del_flag")
            if newName:
                models.Student.objects.filter(studentNo=count).update(studentName=newName)
            if newEmail:
                models.Student.objects.filter(studentNo=count).update(studentEmail=newEmail)
            if newProfession:
                models.Student.objects.filter(studentNo=count).update(professionNos_id=newProfession)
            if del_flag:
                models.Student.objects.filter(studentNo=count).update(isDel=del_flag)
            print("修改成功......")
            return redirect('/admin_stuUp/%s' % count)
        person_massage = models.Student.objects.get(studentNo=count)
        print("*+*+*+*+*+**+")
        return render(req, "admin_stuUp.html", {"person_massage": person_massage})
    return redirect("/login")

# 教师修改页面
def admin_teaUp(req, count):
    user = req.session.get('user_info')['id']
    if user:
        if req.method == "POST":
            print("******++++++*******:", user,count)
            # newNo = req.POST.get("newNo")
            newName = req.POST.get("newName")
            newEmail = req.POST.get("newEmail")
            newProfession = req.POST.get("newProfession")
            del_flag = req.POST.get("del_flag")
            if newName:
                models.Teacher.objects.filter(teacherNo=count).update(teacherName=newName)
            if newEmail:
                models.Teacher.objects.filter(teacherNo=count).update(teacherEmail=newEmail)
            if newProfession:
                models.Teacher.objects.filter(teacherNo=count).update(professionNos_id=newProfession)
            if del_flag:
                models.Teacher.objects.filter(teacherNo=count).update(isDel=del_flag)
            print("修改成功......")
            return redirect('/admin_teaUp/%s'%count)
        person_massage = models.Teacher.objects.get(teacherNo=count)
        return render(req, "admin_teaUp.html", {"person_massage": person_massage})
    return redirect("/login")

# 问题删除
@auth_json
def admin_askDel(req, count):
    user = req.session.get('user_info')['id']
    if user:
        models.Ask.objects.filter(Q(askNo=count)).update(isDel=1)
        print("修改成功")
        return redirect('/admin_question')
    else:
        return redirect('/login')

# 重置密码(学生)
@auth_json
def reset_pwd1(req, count):
    user = req.session.get('user_info')['id']
    if user:
        password = take_md5(count)
        models.Student.objects.filter(studentNo=count).update(studentPwd=password)
        return redirect('/admin_stuUp/%s'%count)
    else:
        return redirect('/login')

# 重置密码(教师)
@auth_json
def reset_pwd2(req, count):
    user = req.session.get('user_info')['id']
    if user:
        password = take_md5(count)
        models.Teacher.objects.filter(teacherNo=count).update(teacherPwd=password)
        return redirect('/admin_teaUp/%s'%count)
    else:
        return redirect('/login')