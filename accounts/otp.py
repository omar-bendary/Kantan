
from random import randint


def otp():
    generate_OTP = ""
    size = 6
    for _ in range(size):
        generate_OTP += str(randint(0, 9))

    return generate_OTP
