# Author:gyk

# import hashlib
#
# def take_md5(content):
#     hash = hashlib.md5()    # 创建hash加密实例
#     hash.update(content.encode())    # hash加密
#     result = hash.hexdigest()  # 得到加密结果
#     return result
#
# a = take_md5("")
# print(a)



# a = "654321"
# b = ""
# q = input('请输入原密码：')
# w = input('请输入邮箱：')
#
# if q and w:
#     print("进来了")
#     if a == q:
#         print("hello")
# print("end")



a = {
    "aa":321321,
    "bb":654,
    "cc":"hello"
}

a.setdefault("dd",444)

print(a)