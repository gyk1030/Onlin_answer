# Author:gyk
from managers import models
from django.db.models import Q,F
import hashlib


# 加密
def take_md5(content):
    hash = hashlib.md5()    # 创建hash加密实例
    hash.update(content.encode())    # hash加密
    result = hash.hexdigest()  # 得到加密结果
    return result

def Role(role, user, pwd):
    pwd = take_md5(pwd)
    if role == 'student':
        stu = Stu_Pwd(user, pwd)
        return stu
    if role == 'teacher':
        tea = Tea_Pwd(user, pwd)
        return tea
    if role == 'manager':
        man = Man_Pwd(user, pwd)
        return man


def Stu_Pwd(user, pwd):
    print("****:Stu")
    try:
        obj = models.Student.objects.get(Q(studentNo=user) & Q(isDel=0))
        print("***:obj")
        if obj:
            password = obj.studentPwd
            if pwd and password == pwd:
                return 0
            else:
                return 1
    except:
        return 2


def Tea_Pwd(user, pwd):
    print("---***---")
    try:
        obj = models.Teacher.objects.get(Q(teacherNo=user) & Q(isDel=0))
        if obj:
            password = obj.teacherPwd
            if pwd and password == pwd:
                return 0
            else:
                return 1
    except:
        print("////")
        return 2

def Man_Pwd(user, pwd):
    try:
        obj = models.Manager.objects.get(Q(managerNo=user) & Q(isDel=0))
        if obj:
            password = obj.managerPwd
            if pwd and password == pwd:
                return 0
            else:
                return 1
    except:
        return 2


def User(id, user):
    if user == "student":
        obj = models.Student.objects.filter(Q(studentNo=id) & Q(isDel=0)).exists()
        if obj:
            return 1
        else:
            return 0
    if user == "teacher":
        obj = models.Teacher.objects.filter(Q(teacherNo=id) & Q(isDel=0)).exists()
        if obj:
            return 1
        else:
            return 0
