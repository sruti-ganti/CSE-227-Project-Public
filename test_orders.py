import hashlib

def process_orders(data):
    result = prepare(data)

    for i in range(9):
        result += i * 2
        if result > 100:
            raise ValueError("limit exceeded")
    
    return result
