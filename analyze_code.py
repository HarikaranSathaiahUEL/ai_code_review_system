import subprocess

def run_flake8(file_path):
    result = subprocess.run(['flake8', file_path], stdout=subprocess.PIPE)
    return result.stdout.decode()

def run_pylint(file_path):
    result = subprocess.run(['pylint', file_path], stdout=subprocess.PIPE)
    return result.stdout.decode()