import json
import calc


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


def get_h(f, r):
    res = [False for i in range(r)]
    if f.readline().strip('\n') != "H:":
        exit("Wrong format.")
    for i in range(r):
        s = f.readline().strip('\n').split(' ')
        res[i] = [bool(int(elem)) for elem in s]
    return res


def get_info(f):
    r = check_f(f, "r:", skip=False)
    n = check_f(f, "n:", skip=False)
    pr = check_f(f, "probability:", skip=False, is_float=True)
    h = get_h(f, r)
    info = json.load(f)
    f.close()
    return r, n, pr, h, info


def decode(f, y_e):
    r, n, pr, h, info = get_info(f)
    syndrome = info["syndrome"]
    if len(y_e) != n:
        exit("Code message has wrong length.")
    y_e_bool = [bool(int(elem)) for elem in y_e]
    syndrome_y = calc.mult_v_m(y_e_bool, h, r)
    pos_e = syndrome[calc.bool_str(syndrome_y)]
    d_flag = False
    if len(pos_e) > 1:
        print("Warning: Found two suitable vectors for one syndrome. Using standard replacement.")
        d_flag = True
    elif len(pos_e) == 0:
        print("Warning: No suitable syndrome for the received code. Using standard replacement.")
        d_flag = True
    if d_flag:
        pos_e = [info["standard_replacement"][calc.bool_str(syndrome_y)]]
    res = calc.xor_tuple([calc.str_bool(pos_e[0]), y_e_bool], n)
    print("Decode result is: ", calc.bool_str(res))
    if d_flag:
        print("The error probability:", pr)
    else:
        print("The decode process is determined. The error is {} with weight {}".format(calc.bool_str(pos_e), calc.wt(pos_e)))
    return res[0:(n - r)], pr

#decode(open("./codes/decode12", "r"), "110010001011")
