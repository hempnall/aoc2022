from setuptools import SetuptoolsDeprecationWarning


f = open("day25/input.txt","r")
lines=[ l.strip() for l in f.readlines()]
nums={
    '0':0,
    '1':1,
    '2':2,
    '-':-1,
    '=':-2    
}
snafus={
    0:('0',0),
    1:('1',0),
    2:('2',0),
    3:('=',1),
    4:('-',1),
    5:('0',1)
}
def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits

def convert_to_decimal(line,power_of_5=0):
    if len(line)==0:
        return 0
    num=nums[line[-1]]
    return (num * (5 ** power_of_5)) + convert_to_decimal(line[:-1],power_of_5+1)

def convert_to_snafu(digits,curr_chars):
    if len(digits)==0:
        return ''.join(curr_chars[::-1])
    else:
        snafu_conv=snafus[digits[0]]
        curr_chars.append(snafu_conv[0])
        if len(digits)>1:
            digits[1] += snafu_conv[1]
        else:
            if snafu_conv[1]==1:
                curr_chars.append(str(snafu_conv[1]))
        return convert_to_snafu(digits[1:],curr_chars)

conversions=[ convert_to_decimal(l) for l in lines]
print(conversions)
print(sum(conversions))
back_to_snafu=[ convert_to_snafu(numberToBase(l,5),[]) for l in conversions]
print(back_to_snafu)
sum_conversions=sum(conversions)
digits=numberToBase(sum_conversions,5)
print(convert_to_snafu(digits,[]))





