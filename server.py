import socket
import math


HOST = "127.0.0.1"
# HOST = "192.168.1.115"
PORT = 7000

Operators = {'+', '-', '*', '/', '^', '%'}
Priority = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2, '^': 3}

# Stack class
class Stack:
    def __init__(self, size):
        self.stack = []
        self.size = size

    def push(self, item):
        if len(self.stack) < self.size:
            self.stack.append(item)

    def pop(self):
        result = -99999

        if self.stack != []:
            result = self.stack.pop()

        return result

    def display(self):
        if self.stack == []:
            print("Stack is empty!")
        else:
            print("Stack data:")
            for item in reversed(self.stack):
                print(item)

    def isEmpty(self):
        return self.stack == []

    def topChar(self):
        result = -99999

        if self.stack != []:
            result = self.stack[len(self.stack) - 1]

        return result

def isOperator(c):
    return c in Operators

def arithmetic(num1, num2, op):
    if op == '+':
        return num1 + num2
    elif op == '-':
        return num1 - num2
    elif op == '*':
        return num1 * num2
    elif op == '/':
        if int(num2) == 0:
            return 0
        return num1 / num2
    elif op == '^':
        return math.pow(num1, num2)
    elif op == '%':
        return num1 % num2
    else: 
        print("Invalid Operator")
        return 0

def infixToPostfix(expr):
    result = ""
    idx = 0
    stack = Stack(15)
    
    for char in expr:
        if char.isnumeric():
            result += char
        elif isOperator(char):
            
            while True:
                if(char=='-'):
                    if(idx == 0):
                        result+=char
                        break
                    elif((isOperator(expr[idx-1])or expr[idx-1]=='(')):
                        result+=char
                        break
                topChar = stack.topChar()
                result += " "
                if stack.isEmpty() or topChar == '(':
                    stack.push(char)
                    break
                else:
                    if Priority[char] > Priority[topChar]:
                        stack.push(char)
                        break
                    else:
                        result += stack.pop()

        elif char == '(':
            stack.push(char)
        elif char == ')':
            cpop = stack.pop()

            while cpop != '(':
                result += " "
                result += cpop
                cpop = stack.pop()

        idx += 1

    while not stack.isEmpty():
        result += " "
        cpop = stack.pop()
        result += cpop
        
    return result

def postfixCalc(expr):
    stack = Stack(15)
    num = ''
    idx = 0
    for char in expr:
        if char == '-' and (idx+1) < len(expr):
            if expr[idx+1].isnumeric():
                num+=char
                continue
        if char.isnumeric():
            num +=char
        elif char == ' ':
            if num != '':
                stack.push(float(num))
            num = ''
        elif isOperator(char):
            try:
                num2 = stack.pop()
                num1 = stack.pop()
            except:
                return "invalid input"
            if(num1 == -99999 or num2 == -99999):
                return "invalid input"
            result = arithmetic(num1, num2, char)
            if(num2 ==0 and char == '/'):
                return "NULL"
            stack.push(result)
        idx += 1
    result = stack.pop()
    result = ("{:.2f}".format(result))
    return result

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)

end = "q"
while True:
    print("Waiting for connection...")
    conn, addr = s.accept()
    print("Connection")
    while True:
        mode = conn.recv(1024)
        mode = mode.decode("utf-8")
        if mode == end:
            print("Quit calling~")
            print("Connection close!")
            s.close()
            break
        elif mode == "1":
            print("now is mode 1")
            while True:
                line = conn.recv(1024)
                line = line.decode("utf-8")
                if line == end:
                    print("Quit mode 1~")
                    break
                else:
                    postfixData = infixToPostfix(line)
                    postfixResult = postfixCalc(postfixData)
                    if type(postfixResult) == str:
                        print('Send to Client: ',postfixResult)
                        conn.send(postfixResult.encode("utf-8"))
                    else:
                        print('Send to Client: ',postfixResult)
                        conn.send(str(postfixResult).encode("utf-8"))

        elif mode == "2":
            print("now is mode 2")
            answers = []
            while True:
                line = conn.recv(1024)
                line = line.decode("utf-8")
                if line == end:
                    f = open("ANS.txt", "w")
                    for answer in answers:
                        f.write(str(answer)+"\n")
                    f.close()
                    print("Quit mode 2~")
                    break
                else:
                    postfixData = infixToPostfix(line)
                    postfixResult = postfixCalc(postfixData)
                    if type(postfixResult) == str:
                        result = "ANS = " + postfixResult
                    else:
                        result = "ANS = " + str(postfixResult)
                    print(result)
                    conn.send(result.encode("utf-8"))
                    answers.append(result)
    break

