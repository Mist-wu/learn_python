def mou_generater(x):
    a = 1
    while True:
        yield a*x
        a += 1


mou = mou_generater(2)


