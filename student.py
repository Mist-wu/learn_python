class Student:
    def __init__(self, name, age, chinese, math, english):
        self.__name = name
        self.__age = age
        self.__chinese = chinese
        self.__math = math
        self.__english = english

    # (1) 获取姓名
    def get_name(self):
        return self.__name

    # (2) 获取年龄
    def get_age(self):
        return self.__age

    # (3) 返回最高分
    def get_maxScore(self):
        return max(self.__chinese, self.__math, self.__english)

    # (4) 返回总成绩
    def get_totalScore(self):
        return self.__chinese + self.__math + self.__english


# -------- 主程序 --------
name = input("请输入姓名：")
age = int(input("请输入年龄："))
chinese = float(input("请输入语文成绩："))
math = float(input("请输入数学成绩："))
english = float(input("请输入英语成绩："))

stu = Student(name, age, chinese, math, english)

print("姓名：", stu.get_name())
print("年龄：", stu.get_age())
print("最高分：", stu.get_maxScore())
print("总成绩：", stu.get_totalScore())
