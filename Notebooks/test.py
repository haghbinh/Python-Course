counter = 1

def increment():
    return counter+1

for i in range(5):
    counter = increment()
    print(counter)