def check_brackets(input_string):
    marks = [' ' for _ in input_string]
    stack = []

    for i, char in enumerate(input_string):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if stack:
                stack.pop()
            else:
                marks[i] = '?'

    for index in stack:
        marks[index] = 'x'

    marks_string = ''.join(marks)
    return input_string, marks_string

print("请输入字符串进行测试，输入'exit'退出程序。")

while True:
    user_input = input()  
    if user_input.lower() == 'exit':  
        break

    original, marks = check_brackets(user_input)
    print(marks)
