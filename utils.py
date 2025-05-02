import subprocess

def save(content:str,path:str) -> None | str:
    try:
        with open(path, 'w', encoding="utf-8") as file:
            file.write(content)
    except FileNotFoundError:
        return "The given path was not found"
    except PermissionError:
        return ""
    except Exception as e:
        return f"Unexpected error: {e}"

def load_file(path:str) -> None | str:
    try:
        if not path:
            return
        with open(path, 'r', encoding="utf-8") as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return "The given path was not found."
    except PermissionError:
        return "You do not have permission to open this file."
    except Exception as e:
        return f"Unexpected error: {e}"

def run(path:str):
    result = subprocess.run(["python", path], capture_output=True, text=True)
    return f"{result.args[0]} \"{result.args[1]}\"\n{result.stdout}\nReturn code: {result.returncode}" if not result.stderr else \
        f"{result.args[0]} \"{result.args[1]}\"\n{result.stderr}\nReturn code: {result.returncode}"

def new(path):
    with open(path, "w") as file:
        file.write("")

if __name__ == '__main__':
    result = run("C:\\Users\\Jason Chundusu\\Desktop\\c8\\text.py")
    print(result)

