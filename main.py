from pathlib import Path
import csv
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

CSV_PATH = Path(__file__).with_name("q-fastapi.csv")

with CSV_PATH.open("r", newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    students = [
        {"studentId": int(row["studentId"]), "class": row["class"]}
        for row in reader
    ]

@app.get("/api")
def get_students(class_: list[str] | None = Query(default=None, alias="class")):
    if class_:
        selected_classes = set(class_)
        filtered = [student for student in students if student["class"] in selected_classes]
    else:
        filtered = students
    return {"students": filtered}
