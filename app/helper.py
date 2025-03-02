import re

def extract_java_files(stack_trace):
    java_files = re.findall(r'(?:/[\w/\\.-]+|[\w/\\.-]+)\.java', stack_trace)
    return java_files