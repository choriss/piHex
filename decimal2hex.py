from decimal import Decimal
import math

def decimal_to_hex(decimal_value):
    # Decimal型を16進数文字列に変換
    hex_string = hex(int(decimal_value))
    
    # 小数部分がある場合は、小数点以下を16進数文字列に変換し、結合する
    if decimal_value % 1 != 0:
        decimal_part = decimal_value % 1
        decimal_part_hex = ''
        #桁数
        predit_digits = math.floor((len(str(decimal_part))-2)/1.205)
        while decimal_part % 1 != 0:
            decimal_part *= 16
            decimal_part_hex += hex(int(decimal_part))[2:]
            decimal_part %= 1
            if len(decimal_part_hex)==predit_digits:
                break

        hex_string += '.' + decimal_part_hex
    
    return hex_string