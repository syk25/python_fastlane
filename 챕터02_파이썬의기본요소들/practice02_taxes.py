""" 문제 3: 입력값 저장하기 """

my_income = int(input("나의 수입: "))
tax_rate = float(input("세율: "))


def calculate_tax(my_income: int, tax_rate: float) -> int:
    return my_income * tax_rate


def after_tax_income(my_income, tax):
    return my_income - tax


""" 문제 1: 세금 계산하기 """
my_tax = calculate_tax(my_income, tax_rate)
print("세금: ", int(my_tax), "원", sep="")

""" 문제 2: 세금 제외 소득 """
my_real_income = after_tax_income(my_income, my_tax)
print("실소득:", int(my_real_income), "원", sep="")
