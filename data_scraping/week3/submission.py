import re

def problem_1():
    return re.compile(r'-?\d+')

def problem_2():
    return re.compile(r'\d+\.?\d*')

def problem_3():
    return re.compile(r'(?:[01]?\d|2[0-3])(?::[0-5]\d){1,2}')

def problem_4():
    return re.compile(r'[12]\d{3,3}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])')

def problem_5():
    return re.compile(r'\b[a-zA-Z0-9_-]{3,16}\b')

def problem_6():
    return re.compile(r'[\w\.-]+@[\w\.-]+\.[\w\.-]+')

def problem_7():
    return re.compile(r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)')

def problem_8():
    return re.compile(r'(?:http://|https://)[\w\.-]+\.[\w\.-]+(?:/[\w\.-]*)*')
