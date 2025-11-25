funcs = []
for i in range(3):
    def f():
        return i
    funcs.append(f)

print(funcs[0]())  # 2
print(funcs[1]())  # 2
print(funcs[2]())  # 2