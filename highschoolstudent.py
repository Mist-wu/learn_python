class Student:
    def __init__(self, name, age, chinese, math, english):
        self.__name = name
        self.__age = age
        self.__chinese = chinese
        self.__math = math
        self.__english = english

    def get_name(self):
        return self.__name

    def get_age(self):
        return self.__age

    def get_maxScore(self):
        return max(self.__chinese, self.__math, self.__english)

    def get_totalScore(self):
        return self.__chinese + self.__math + self.__english

    # 给子类用的受保护接口
    def _get_scores(self):
        return [self.__chinese, self.__math, self.__english]


class HighSchoolStudent(Student):
    def __init__(self, name, age, chinese, math, english,
                 chemistry, physics, biology, history, politics):
        super().__init__(name, age, chinese, math, english)
        self.__chemistry = chemistry
        self.__physics = physics
        self.__biology = biology
        self.__history = history
        self.__politics = politics

    # (1) 计算并返回8门课程的平均分（四舍五入保留2位小数）
    def get_average(self):
        scores = self._get_scores() + [
            self.__chemistry, self.__physics, self.__biology,
            self.__history, self.__politics
        ]
        avg = sum(scores) / len(scores)
        return round(avg, 2)

    # 覆写：返回8门课程中的最高分
    def get_maxScore(self):
        scores = self._get_scores() + [
            self.__chemistry, self.__physics, self.__biology,
            self.__history, self.__politics
        ]
        return max(scores)


# -------- 主程序 --------
name = input("请输入姓名：")
age = int(input("请输入年龄："))

chinese = float(input("语文："))
math = float(input("数学："))
english = float(input("英语："))
chemistry = float(input("化学："))
physics = float(input("物理："))
biology = float(input("生物："))
history = float(input("历史："))
politics = float(input("政治："))

stu = HighSchoolStudent(name, age, chinese, math, english,
                        chemistry, physics, biology, history, politics)

print("姓名：", stu.get_name())
print("平均分：", stu.get_average())
print("最高分：", stu.get_maxScore())
