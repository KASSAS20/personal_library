a = [1, 2, 3, 4]
a.append(a)

def w(a):
    e = a[-1]
    print(e)
    w(e)

w(a)