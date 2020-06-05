def pow(x, y, n=None):
    if n:
        if y == 0:
            return 1
        if y == 1:
            return x % n
        res = 1
        while y:
            if y & 1 == 1:
                res = res * x % n
            x = x * x % n
            y = y // 2
    else:
        if y == 0:
            return 1
        if y == 1:
            return x
        res = 1
        while y:
            if y & 1 == 1:
                res = res * x
            x = x * x
            y = y // 2
    return res


def int_bool(n, r):
    return [bool(n & (1 << j)) for j in range(r - 1, -1, -1)]


def bool_int(b):
    n = 0
    for elem in b:
        n = n << 1
        if elem:
            n += int(elem)
    return n


def xor_tuple(a, r):
    res = [False for i in range(r)]
    for elem in a:
        res = [res[i] ^ elem[i] for i in range(r)]
    return res


def comb_next(n, k, combin):
    return round(combin * ((n - k) / (k + 1)))


def mult_m_v(m, v, l):
    r = len(v)
    res = [False for i in range(l)]
    for i in range(l):
        elem = False
        for j in range(r):
            elem ^= m[j][i] and v[j]
        res[i] = elem
    return res


def mult_v_m(v, m, l):
    r = len(v)
    res = [False for i in range(l)]
    for i in range(l):
        elem = False
        for j in range(r):
            elem ^= m[i][j] and v[j]
        res[i] = elem
    return res


def bool_str(b):
    res = [str(int(elem)) for elem in b]
    return "".join(res)


def str_bool(s):
    return [bool(int(elem)) for elem in s]


def wt(v):
    return sum(1 for elem in v if elem)
