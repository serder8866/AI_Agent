import os
from functions.get_file_content import get_file_content

result = get_file_content("calculator", "lorem.txt")
text, trunc_message = result.split("...")
print(f"The length of the content was {len(text)} characters\nThe truncation message: {trunc_message}")

print(get_file_content("calculator", "main.py"))


print(get_file_content("calculator", "pkg/calculator.py"))


print(get_file_content("calculator", "/bin/cat"))


print(get_file_content("calculator", "pkg/does_not_exist.py"))