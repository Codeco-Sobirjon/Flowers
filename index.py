def factorial(num):
    if num < 0:
        return None
    elif num == 0 or num == 1:
        return 1
    else:
        result = 1
        for i in range(1, num + 1):
            result *= i
        return result


number = 5
result = factorial(number)
print(result)