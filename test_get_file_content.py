from functions.get_file_content import get_file_content

print("Result for current directory:")
print(get_file_content("calculator", "lorem.txt"))

print("Result for main.py:")
print(get_file_content("calculator", "main.py"))

print("Result for pkg/calculator.py:")
print(get_file_content("calculator", "pkg/calculator.py"))

print("Result for /bin/cat:")
print("(should return an error)")
print(get_file_content("calculator", "/bin/cat"))

print("result for pkg/does_not_exist.py:")
print("(should return an error)")
print(get_file_content("calculator", "pkg/does_not_exist.py"))