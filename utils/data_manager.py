import json
from pathlib import Path
from datetime import datetime

DATA_PATH = Path("data/founders.json")


def load_data():
    if DATA_PATH.exists():
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_data(data):
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def register_answer(founder_id, startup, founder_name, step, answer_text):
    data = load_data()

    if founder_id not in data:
        data[founder_id] = {
            "startup": startup,
            "founder_name": founder_name,
            "step": step,
            "last_update": str(datetime.now()),
            "answers": {step: answer_text},
        }
    else:
        data[founder_id]["step"] = step
        data[founder_id]["last_update"] = str(datetime.now())
        data[founder_id]["answers"][step] = answer_text

    save_data(data)
