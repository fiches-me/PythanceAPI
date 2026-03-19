import random
import string

def create_api_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=64))

if __name__ == "__main__":
    print(create_api_key())