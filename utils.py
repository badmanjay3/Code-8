import subprocess
from pathlib import Path

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

def run_python(path:str):
    result = subprocess.run(["python", path], capture_output=True, text=True)
    return f"{result.args[0]} \"{result.args[1]}\"\n{result.stdout}\nReturn code: {result.returncode}" if not result.stderr else \
        f"{result.args[0]} \"{result.args[1]}\"\n{result.stderr}\nReturn code: {result.returncode}"

def run_cpp(path):
    exe_path = Path(path).with_suffix('.exe')  # e.g., "main.cpp" → "main.exe"

    compile_result = subprocess.run(["g++", path, "-o", str(exe_path)], capture_output=True, text=True)

    if compile_result.returncode != 0:
        return compile_result.stderr  # Compilation error

    # Step 2: Run
    run_result = subprocess.run([str(exe_path)], capture_output=True, text=True)
    return run_result.stdout + run_result.stderr

def new(path):
    with open(path, "w") as file:
        file.write("")

def extension(path: str) -> tuple[str, str]:
    p = Path(path)
    file_name = p.stem
    extension_ = p.suffix

    return file_name, extension_

def run(path):
    result = ''
    ext = extension(path)[1]
    if ext == ".py":
        result =  run_python(path)
    elif ext == ".cpp":
        result = run_cpp(path)
    return result


if __name__ == '__main__':
    #print(run_python('testroom.py'))
    print(run("testroom.py"))
