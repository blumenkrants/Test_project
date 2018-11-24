one = 'Learn'
two = 'Python'
def get_summ(one, two, delimiter='&'):
    return (str(one) + str(delimiter) + str(two)).upper()
sum_string = get_summ(one, two)
print(sum_string)