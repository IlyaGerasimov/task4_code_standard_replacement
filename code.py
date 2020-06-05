import calc
import random


def check_f(f, phrase, skip=True, is_float=False):
    if f.readline().strip('\n') != phrase:
        exit("Wrong format.")
    try:
        if is_float:
            res = float(f.readline().strip('\n'))
        else:
            res = int(f.readline().strip('\n'))
    except Exception:
        exit("Wrong format.")
    else:
        if not skip:
            return res


def get_g(f, k):
    res = [False for i in range(k)]
    if f.readline().strip('\n') != "G:":
        exit("Wrong format.")
    for i in range(k):
        s = f.readline().strip('\n').split(' ')
        res[i] = [bool(int(elem)) for elem in s]
    return res


def get_info(f):
    r = check_f(f, "r:", skip=False)
    n = check_f(f, "n:", skip=False)
    check_f(f, "probability:", is_float=True)
    g = get_g(f, n - r)
    return r, n, g


def code(f, m, e):
    r, n, g = get_info(f)
    if e is None:
        e = ""
        for i in range(n):
            e += str(random.choice(["0", "1"]))
    if len(e) != n:
        exit("Wrong error format.")
    if len(m) != n - r:
        exit("Wrong message format.")
    f.close()
    res = calc.mult_m_v(g, calc.str_bool(m), n)
    print(len(res))
    res = calc.xor_tuple([res, calc.str_bool(e)], len(res))
    print("Code result:", calc.bool_str(res))
    print("Error code:", e)
    return res, e

#code(open("./codes/code12", "r"), "01", "100010010100")