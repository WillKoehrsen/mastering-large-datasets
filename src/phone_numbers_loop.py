import re

phone_numbers = ["(123) 456-7890", "1234567890", "123.456.7890", "+1 123 456-7890"]

new_numbers = []

exp = re.compile(r"\d")

for number in phone_numbers:
    digits = exp.findall(number)
    area_code = "".join(digits[-10:-7])
    first_three = "".join(digits[-7:-4])
    last_four = "".join(digits[-4 : len(digits)])

    pretty_format = f"({area_code}) {first_three}-{last_four}"
    new_numbers.append(pretty_format)
