from decimal import *
import re

import decimal2hex

def my_sqrt(X,prc):

    getcontext().Emax = MAX_EMAX 
    getcontext().Emin = MIN_EMIN

    
    getcontext().prec = prc

    
    A = Decimal('1')/Decimal(str(X))  
    xn = A.sqrt()


    # 漸化式を計算
    while True:
        hn = Decimal(1) - A * xn**2
        xn = xn * (Decimal(1) + hn * (Decimal(str(1/2)) + hn * (Decimal(str(3/8)) + hn * (Decimal(str(5/16)) + hn * (Decimal(str(35/128)) + hn * Decimal(str(63/256)))))))
        try:
            if before_xn == xn:
                break
        except:
            pass
        before_xn = xn
    return xn

def find_first_occurrence(pattern, text):
    match = re.search(pattern, text)
    if match:
        return match.start()
    else:
        return -1  # If pattern not found

    


def search_from_pi(pi,value:str):
    #toHex
    hex_pi = decimal2hex.decimal_to_hex(pi)
    
    #検索する
    start_place = find_first_occurrence(value,str(hex_pi)[2:])
    
    return start_place-1


def match_strings(string1, string2):
    match = ""
    for char1, char2 in zip(string1, string2):
        if char1 == char2:
            match += char1
        else:
            break
    return match
    

def Gauss_Legendre(prc,search_num):
    getcontext().prec = prc
    a = Decimal('1')
    b = Decimal('1') / my_sqrt(Decimal('2'),prc)
    t = Decimal('1') / Decimal('4')
    p = Decimal('1')
    pi = Decimal('0')
    pin = Decimal('3')
    i = 0
    
    while pi != pin:
        pi = pin
        an = (a + b) / 2
        bn = my_sqrt((a * b),prc)
        getcontext().prec = prc
        tn = t - p * (a - an) ** 2
        pn = 2 * p
        pin = ((a + b) ** 2) / (4 * t)
        a = an
        b = bn
        t = tn
        p = pn
        i += 1
        
        right_pi = str(match_strings(str(pi),str(pin)))
        if right_pi != "":
            
            result = search_from_pi(Decimal(right_pi),search_num)
            
        
            if result != -2:
                #見つかったときの処理
                return result
    return pin


def main_search(search_num,limit=10000):
    final_result = Gauss_Legendre(limit,search_num)
    return final_result,final_result+len(search_num)


