from django.db import models

# Create your models here.

class Student(models.Model):
    studentNo = models.IntegerField(primary_key=True)
    professionNos = models.ForeignKey('Profession', on_delete=models.CASCADE)
    studentName = models.CharField(null=False, blank=False, max_length=20)
    studentPwd = models.CharField(null=False, blank=False, max_length=20)
    studentEmail = models.EmailField()
    askCount = models.IntegerField(null=False, default=0)
    del_choices = ((0, '未删除'), (1, '已删除'))
    isDel = models.IntegerField(null=False, default=0, choices=del_choices)

    # def __str__(self):
    #     return str(self.studentNo)

class Teacher(models.Model):
    teacherNo = models.IntegerField(primary_key=True)
    professionNos = models.ForeignKey('Profession', on_delete=models.CASCADE)
    teacherName = models.CharField(null=False, blank=False, max_length=20)
    teacherPwd = models.CharField(null=False, blank=False, max_length=20)
    teacherEmail = models.EmailField()
    answerCount = models.IntegerField(null=False, default=0)
    del_choices = ((0, '未删除'), (1, '已删除'))
    isDel = models.IntegerField(null=False, default=0, choices=del_choices)

    # def __str__(self):
    #     return self.teacherNo

class Manager(models.Model):
    managerNo = models.CharField(max_length=20, primary_key=True)
    managerPwd = models.CharField(null=False, max_length=20)
    del_choices = ((0, '未删除'), (1, '已删除'))
    isDel = models.IntegerField(null=False, default=1, choices=del_choices)

    def __str__(self):
        return self.managerNo

class Profession(models.Model):
    professionNo = models.AutoField(default=None, primary_key=True)
    name = models.CharField(null=False, max_length=20)
    del_choices = ((0, '未删除'), (1, '已删除'))
    isDel = models.IntegerField(null=False, default=0, choices=del_choices)

    # def __str__(self):
    #     return self.professionNo

class Ask(models.Model):
    askNo = models.AutoField(default=None, primary_key=True)
    studentNos = models.ForeignKey('Student', on_delete=models.CASCADE)
    askTypes = models.ForeignKey('Profession', on_delete=models.CASCADE)
    askTopic = models.CharField(null=False, blank=False, max_length=50)
    askContent = models.TextField(max_length=1000)
    askTime = models.DateField()
    status_choices = ((0, '未解决'), (1, '已解决'))
    status = models.IntegerField(null=False, default=0, choices=status_choices)
    del_choices = ((0, '未删除'),(1, '已删除'))
    isDel = models.IntegerField(null=False, default=0, choices=del_choices)

    # def __str__(self):
    #     return self.askNo

class Answer(models.Model):
    answerNo = models.AutoField(default=None, primary_key=True)
    askNos = models.OneToOneField('Ask', default=None, on_delete=models.CASCADE)
    teacherNos = models.ForeignKey('Teacher',on_delete=models.CASCADE)
    answerContent = models.TextField(max_length=1000)
    answerTime = models.DateField()
    status_choices = ((0, '未解决'), (1, '已解决'))
    status = models.IntegerField(null=False, default=0, choices=status_choices)
    del_choices = ((0, '未删除'), (1, '已删除'))
    isDel = models.IntegerField(null=False, default=0, choices=del_choices)

    # def __str__(self):
    #     return self.answerNo