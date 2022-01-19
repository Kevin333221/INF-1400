
x = 5

# Prints 5
print(x)

def change_value(number):
    number = number + 1

    # Må returnere
    return number

# Må re-assign her for å forandre 'x'
x = change_value(x)

# Prints 6
print(x)



y = 5

# Prints 5
print(y)

def change_value_2(y):
    y = y + 1

change_value(y)

# Still prints 5, vil ha 6
print(y)
