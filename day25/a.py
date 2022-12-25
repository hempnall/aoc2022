from setuptools import SetuptoolsDeprecationWarning


f = open("input.txt","r")
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

def convert_to_snafu(num):
    digits=numberToBase(num,5)
    snafu_chars=[]
    for power in range(len(digits)):
        snafu_conv=snafus[digits[power]]
        snafu_chars.append(snafu_conv[0])
        if power < len(digits)-1:
            digits[power+1] += snafu_conv[1]
        else:
            if snafu_conv[1]==1:
                snafu_chars.append(str(snafu_conv[1]))
    return ''.join(snafu_chars[::-1])

conversions=[ convert_to_decimal(l) for l in lines]
print(conversions)
print(sum(conversions))
back_to_snafu=[ convert_to_snafu(l) for l in conversions]
print(back_to_snafu)
print(convert_to_snafu(sum(conversions)))





