import random

def random_str(randomlength=8):
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    length = len(chars) - 1
    random2 = random.Random()
    randomstr = ''.join(random2.choices(chars, k=randomlength))
    return randomstr

if __name__ == '__main__':
    print(random_str())