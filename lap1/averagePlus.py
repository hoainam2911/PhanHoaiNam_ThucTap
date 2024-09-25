def create_avg():
    total = 0
    count = 0
    def avg(n):
        nonlocal total, count  
        total += n
        count += 1
        return total / count
    return avg

avg = create_avg()
print(avg(3))  
print(avg(5))  
print(avg(7))  
print(avg(26)) 

