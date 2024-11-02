import secrets
import string

def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password


"""
a = generate_random_password()
print(a) # Output: something like: 9!@#aBcD
"""