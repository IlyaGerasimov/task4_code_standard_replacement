import os
import json
from math import log2
import random
from itertools import combinations
import calc


def get_max_speed(n, r, bandwidth):
    k = n - r
    if k <= 0:
        exit("Cannot build code. Message length cannot be zero or less.")
    speed = k / n
    while speed >= bandwidth:
        n = n - 1
        k = n - r
        if k <= 0:
            exit("Impossible to build code. Cannot achieve requirement for speed less than entropy.")
        speed = k / n
    return n, speed


def varshamov_gilbert(n, r):
    d = 0
    curr = 1
    bound = 1 << r
    combine = 1
    while curr < bound and d < r - 2:
        combine = calc.comb_next(n - 1, d, combine)
        d += 1
        curr += combine
    return d + 1


def get_h(r, n, d):
    set = [False for i in range(1, 1 << r)]
    h = [False for i in range(n)]
    i = n - 1
    while i >= n - r:
        h[i] = [(k == r + i - n) for k in range(r)]
        set[calc.bool_int(h[i]) - 1] = True
        i -= 1
    h[i] = [(k >= r - d + 1) for k in range(r)]
    set[calc.bool_int(h[i]) - 1] = True
    for j in range(2, d - 1):
        combos = combinations(h[i:n], j)
        combos = [calc.xor_tuple(elem, r) for elem in combos]
        for elem in combos:
            set[calc.bool_int(elem) - 1] = True
    i -= 1
    while i >= 0:
        h[i] = next(calc.int_bool(i + 1, r) for i in range((1 << r) - 1) if not set[i])
        set[calc.bool_int(h[i]) - 1] = True
        for j in range(2, d - 2):
            combos = combinations(h[(i + 1):n], d - 2)
            combos = [calc.xor_tuple(elem, r) for elem in combos]
            combos = [calc.xor_tuple([h[i], elem], r) for elem in combos]
            for elem in combos:
                set[calc.bool_int(elem) - 1] = True
        i -= 1
    return h


def get_g(g_0, k, n):
    g = [False for j in range(n)]
    i = 0
    while i < k:
        g[i] = [(j == i) for j in range(k)]
        i += 1
    while i < n:
        g[i] = [g_0[j][i - k] for j in range(k)]
        i += 1
    return g


def update_lead(pos_leader, w):
    n = len(pos_leader)
    i = n - 1
    while pos_leader[i] and i >= 0:
        i -= 1
    if i == 0:
        exit("error")
        return [False] + [True] + pos_leader[2:], w
    step = n - 1 - i
    if step == w:
        return [(i < w + 1) for i in range(n)], w + 1
    while not pos_leader[i] and i >= 0:
        i -= 1
    return pos_leader[:i] + [False] + [True] + [True] * step + [False] * (n - 2 - step - i), w


def get_s_p(k, n, g):
    messages = [calc.int_bool(i, k) for i in range(1 << k)]
    all_codes = [False for i in range(1 << n)]
    codes = [calc.mult_v_m(messages[i], g, n) for i in range(1 << k)]
    for code in codes:
        all_codes[calc.bool_int(code)] = True
    classes = [False for i in range((1 << (n - k)) - 1)]
    i = 0
    pos_leader = [True] + [False for i in range(n - 1)]
    w = 1
    while i < (1 << (n - k)) - 1:
        if not all_codes[calc.bool_int(pos_leader)]:
            temp = [calc.xor_tuple([pos_leader, code], n) for code in codes]
            classes[i] = temp
            i += 1
            for code in temp:
                all_codes[calc.bool_int(code)] = True
        pos_leader, w = update_lead(pos_leader, w)
    return [codes] + classes


def get_syndrome(s_p, k, n, h, t, r):
    res = dict()
    res['0' * r] = [calc.bool_str(elem) for elem in s_p[0] if calc.wt(elem) <= t]
    for i in range(1, len(s_p)):
        syn = calc.mult_m_v(h, s_p[i][0], n - k)
        res[calc.bool_str(syn)] = [calc.bool_str(elem) for elem in s_p[i] if calc.wt(elem) <= t]
    return res


def get_full_syndrome(s_p, k, n, h, t, r):
    res = dict()
    res['0' * r] = calc.bool_str(s_p[0][0])
    for i in range(1, len(s_p)):
        syn = calc.mult_m_v(h, s_p[i][0], n - k)
        res[calc.bool_str(syn)] = calc.bool_str(s_p[i][0])
    return res


def get_probability(s_p, p, t, n):
    wts = dict()
    for i in range(0, n):
        wts[i] = 0
    for elem in s_p:
        weight = calc.wt(elem[0])
        wts[weight] += 1
    res = 0
    for key, value in wts.items():
        res += (calc.pow(p, key) * calc.pow(1 - p, n - key)) * value
    return 1 - res


def write_h(h, r, n, f):
    for i in range(r):
        s = ""
        for j in range(n):
            s += str(int(h[j][i])) + " "
        f.write(s.strip(' '))
        f.write("\n")


def write_g(g, k, n, f):
    for i in range(k):
        s = ""
        for j in range(n):
            s += str(int(g[j][i])) + " "
        f.write(s.strip(' '))
        f.write("\n")


def write_s_p(s_p, f):
    s = ""
    for elem in s_p[0]:
        for element in elem:
            s += str(int(element))
        s += " "
    f.write(s.strip(' '))
    f.write("\n")
    for i in s_p[1:]:
        s = ""
        for elem in i:
            for element in elem:
                s += str(int(element))
            s += " "
        f.write(s.strip(' '))
        f.write("\n")


def gen(r, n, p):
    entropy = -(p * log2(p)) - (1 - p) * log2(1 - p)
    bandwidth = 1 - entropy
    print("\nCalculating max speed..")
    n, speed = get_max_speed(n, r, bandwidth)
    print("\nspeed:", speed)
    print("Done.")
    k = n - r
    print("\nCalculating d..")
    d = varshamov_gilbert(n, r)
    print("\nd:", d)
    print("Done.")
    t = int((d - 1) / 2)
    print("\nCalculating H..")
    h = get_h(r, n, d)
    print("Done.")
    g_0 = h[:(n - r)]
    print("\nCalculating G..")
    g = get_g(g_0, k, n)
    print("Done.")
    print("\nCalculating standard replacement..")
    s_p = get_s_p(k, n, g)
    print("Done.")
    print("\nCalculating syndrome..")
    syndrome = get_syndrome(s_p, k, n, h, t, r)
    print("Done.")
    print("\nForming standard placement for decoder.")
    syndrome_full = get_full_syndrome(s_p, k, n, h, t, r)
    print("\nCalculating probability..")
    print(d)
    pr = get_probability(s_p, p, t, n)
    print("Done.")
    print("Probability:", pr)
    index = sum([len(files) for r, d, files in os.walk("./codes")])
    path = "./codes/info{}".format(index)
    with open(path, "w") as f:
        f.write("r:\n")
        f.write(str(r))
        f.write("\nn:\n")
        f.write(str(n))
        f.write("\nprobability:\n")
        f.write(str(pr))
        f.write("\nd:\n")
        f.write(str(d))
        f.write("\nt:\n")
        f.write(str(t))
        f.write("\nH:\n")
        write_h(h, r, n, f)
        f.write("G:\n")
        write_g(g, k, n, f)
        f.write("Standard-replacement:\n")
        write_s_p(s_p, f)
    print("\nFull Code information has been written in {}".format(path))
    path = "./codes/code{}".format(index)
    with open(path, "w") as f:
        f.write("r:\n")
        f.write(str(r))
        f.write("\nn:\n")
        f.write(str(n))
        f.write("\nprobability:\n")
        f.write(str(pr))
        f.write("\nG:\n")
        write_g(g, k, n, f)
    print("\nCode process information has been written in {}".format(path))
    path = "./codes/decode{}".format(index)
    with open(path, "w") as f:
        f.write("r:\n")
        f.write(str(r))
        f.write("\nn:\n")
        f.write(str(n))
        f.write("\nprobability:\n")
        f.write(str(pr))
        f.write("\nH:\n")
        write_h(h, r, n, f)
        json.dump({"syndrome": syndrome, "standard_replacement": syndrome_full}, f, indent=4)
    print("\nDecode process information has been written in {}".format(path))
    return 0

gen(10, 12, 0.1)

