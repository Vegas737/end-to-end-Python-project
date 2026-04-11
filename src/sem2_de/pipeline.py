import os
import json
import subprocess
import argparse 
from datetime import datetime

PYTHON_PATH = r"D:\Games\Anaconda\python.exe"
STATE_FILE = "data/state/state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"last_year": 0, "status": "new"}
    return {"last_year": 0, "status": "new"}

def save_state(state_dict):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state_dict, f, indent=4)

def run_step(command, step_name):
    print(f"--- Запуск этапа: {step_name} ---")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f" Ошибка на этапе {step_name}")
        return False
    return True

def main():
    parser = argparse.ArgumentParser(description="Pipeline CLI")
    parser.add_argument("--config", required=True, help="Путь к конфигу")
    parser.add_argument("--mode", choices=["full", "incremental"], default="incremental", 
                        help="Режим: full (все заново) или incremental (только новое)")
    args = parser.parse_args()

    current_year = 2025 
    
    if args.mode == "full":
        print(" Режим FULL: игнорируем старое состояние.")
        state = {"last_year": 0, "status": "none"}
    else:
        state = load_state()
        print(f" Режим INCREMENTAL. Watermark: {state.get('last_year')}")

    is_done = state.get("last_year") >= current_year and state.get("status") == "success"
    
    if is_done and args.mode == "incremental":
        print(f" Год {current_year} уже успешно обработан. Пропускаю Extract.")
    else:
        if not run_step(f"{PYTHON_PATH} src/sem2_de/extract.py --config {args.config}", "Extract"):
            return

    if not run_step(f"{PYTHON_PATH} src/sem2_de/transform.py", "Transform"):
        return

    if not run_step(f"{PYTHON_PATH} src/sem2_de/load.py", "Load"):
        return

    new_state = {
        "variant": 20,
        "last_year": current_year, 
        "status": "success",
        "last_run": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mode": args.mode
    }
    save_state(new_state)
    print(f" Пайплайн завершен успешно! Состояние (watermark) обновлено до {current_year}.")

if __name__ == "__main__":
    main()
