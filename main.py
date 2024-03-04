import bbp
import gmpy2
import picalc_and_search

class PiHex():
    def __init__(self,start,end):
        self.start = start
        self.end = end
        self.decimal = self.__toDecimal()

    def __toDecimal(self):
        #toHex
        digits = self.end-self.start

        #
        fpprec = len(str(self.start)) + 4 * digits + 20
        gmpy2.get_context().precision = fpprec
        #

        rss = bbp.bbpmpgmp(self.start,digits)
        irss = int(gmpy2.floor(rss * (16 ** (digits))))
        self.decimal = irss

        return irss

    def __int__(self):
        return self.decimal
    
    def toHex(self):
        hex_num = hex(self.decimal)
        return hex_num
    
    def __add__(self,other):
        add_result = self.decimal+other.decimal
        result_start,result_end = self.toPiHex(add_result)
        return PiHex(result_start,result_end)
    
    def __sub__(self,other):
        add_result = self.decimal-other.decimal
        if add_result<0:
            raise ValueError("PiHex is not support negative number!")
        result_start,result_end = self.toPiHex(add_result)
        return PiHex(result_start,result_end)
    
    def toVisible(self):
        return f"PiHex({self.start},{self.end})"
    
    def toPiHex(self,num:int):
        result_start,result_end = picalc_and_search.main_search(hex(num)[2:])
        return result_start,result_end



#
if __name__ == '__main__':
    a = PiHex(1,3)
    b = PiHex(2,4)
    c = a+b
    print(c.toVisible())
    

