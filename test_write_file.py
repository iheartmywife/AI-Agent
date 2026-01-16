from functions.write_file import write_file

print("Result for 'wait, this isn't lorem ipsum' written to 'lorem.txt'")
print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))

print("Result for 'lorem ipsum dolor sit amet' written to 'pkg/morelorem.txt'")
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))

print("Result for 'this should not be allowed' to '/tmp/temp.txt'")
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))