
import json
import sqlite3
from pathlib import Path
from typing import Optional

import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "carecompass.db"
DATASET_PATH = BASE_DIR / "triage_dataset.jsonl"
CAREGIVERS_PATH = BASE_DIR / "caregivers.csv"

app = FastAPI(title="CareCompass AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Local prototype only
    allow_methods=["*"],
    allow_headers=["*"],
)

class IntakeRequest(BaseModel):
    user_input: str = Field(min_length=1, max_length=1500)
    language: str = "English"
    location: Optional[str] = None
    conversation_history: list = []

def get_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def initialize_database():
    connection = get_db()
    connection.execute("""
        CREATE TABLE IF NOT EXISTS triage_examples (
            id TEXT PRIMARY KEY,
            user_input TEXT,
            response_json TEXT
        )
    """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS caregivers (
            caregiver_id TEXT PRIMARY KEY,
            data_json TEXT
        )
    """)

    if DATASET_PATH.exists():
        with open(DATASET_PATH, encoding="utf-8") as file:
            for line in file:
                try:
                    item = json.loads(line)
                    request = item.get("request") or {}
                    response = item.get("response") or {}
                    item_id = str(item.get("id", ""))

                    if item_id:
                        connection.execute(
                            """INSERT OR REPLACE INTO triage_examples
                            (id, user_input, response_json)
                            VALUES (?, ?, ?)""",
                            (
                                item_id,
                                str(request.get("user_input", "")),
                                json.dumps(response, ensure_ascii=False),
                            ),
                        )
                except (json.JSONDecodeError, TypeError):
                    continue

    if CAREGIVERS_PATH.exists():
        try:
            data = pd.read_csv(CAREGIVERS_PATH).fillna("")
            for _, row in data.iterrows():
                record = row.to_dict()
                caregiver_id = str(record.get("caregiver_id", ""))
                if caregiver_id:
                    connection.execute(
                        "INSERT OR REPLACE INTO caregivers VALUES (?, ?)",
                        (
                            caregiver_id,
                            json.dumps(record, ensure_ascii=False, default=str),
                        ),
                    )
        except Exception as error:
            print("Caregiver import error:", error)

    connection.commit()
    connection.close()

EMERGENCY_TERMS = [
    "chest pain", "difficulty breathing", "shortness of breath",
    "can't breathe", "cannot breathe", "unconscious",
    "severe bleeding", "stroke", "seizure", "overdose",
    "सीने में दर्द", "सांस नहीं", "सांस लेने में दिक्कत",
    "बेहोश", "saans nahi", "saans lene mein dikkat",
    "seene mein dard", "behosh", "bahut khoon"
]

def get_demo_response(message):
    text = message.lower()

    if any(term in text for term in EMERGENCY_TERMS):
        return {
            "summary": "Possible emergency warning signs mentioned.",
            "guidance": (
                "If this is happening now in India, call 112 immediately. "
                "Do not wait for an app response."
            ),
            "urgency": "emergency",
            "care_type": "emergency_112",
            "next_steps": [
                "Call 112 if there is immediate danger.",
                "Follow the emergency operator's instructions."
            ]
        }

    if any(term in text for term in [
        "headache", "head ache", "head pain",
        "sir dard", "सिर दर्द", "सिरदर्द"
    ]):
        return {
            "summary": "You mentioned a headache.",
            "guidance": (
                "Headaches can have many causes. Rest somewhere quiet "
                "and drink water if appropriate. Seek professional advice "
                "if it persists, worsens, or concerns you. A sudden severe "
                "headache or headache with weakness, confusion, or speech "
                "or vision changes needs emergency assessment."
            ),
            "urgency": "routine_or_clinician_advice",
            "care_type": "general_guidance",
            "next_steps": [
                "Note when the headache started.",
                "Notice any other symptoms.",
                "Contact a qualified clinician if it persists or worsens."
            ]
        }

    if any(term in text for term in [
        "sleep", "insomnia", "can't sleep",
        "cannot sleep", "neend", "नींद"
    ]):
        return {
            "summary": "You asked about sleep.",
            "guidance": (
                "Try keeping a consistent sleep and wake time, reducing "
                "caffeine late in the day, and making your room quiet "
                "and dark. If sleep problems persist, consult a clinician."
            ),
            "urgency": "routine",
            "care_type": "wellbeing_guidance",
            "next_steps": [
                "Keep a regular sleep schedule.",
                "Reduce caffeine close to bedtime.",
                "Seek advice if sleep problems continue."
            ]
        }

    if any(term in text for term in [
        "stress", "anxiety", "anxious", "tension",
        "तनाव", "ghabra"
    ]):
        return {
            "summary": "You mentioned stress or anxiety.",
            "guidance": (
                "Consider taking a quiet pause, breathing comfortably, "
                "and talking to someone you trust. A mental-health "
                "professional may help if symptoms persist."
            ),
            "urgency": "routine",
            "care_type": "wellbeing_guidance",
            "next_steps": [
                "Take a short break in a calm place.",
                "Reach out to someone you trust.",
                "Seek urgent help if you may harm yourself."
            ]
        }

    return {
        "summary": "I need a little more information.",
        "guidance": (
            "What is your main symptom, when did it start, and is it "
            "getting worse? If this may be an emergency in India, call 112."
        ),
        "urgency": "needs_more_information",
        "care_type": "follow_up",
        "next_steps": [
            "Describe your main symptom.",
            "Mention when it began.",
            "Mention whether it is getting worse."
        ]
    }

@app.on_event("startup")
def startup():
    initialize_database()

@app.get("/")
def home():
    initialize_database()
    connection = get_db()
    examples = connection.execute(
        "SELECT COUNT(*) FROM triage_examples"
    ).fetchone()[0]
    caregivers = connection.execute(
        "SELECT COUNT(*) FROM caregivers"
    ).fetchone()[0]
    connection.close()

    return {
        "status": "running",
        "dataset_examples_loaded": examples,
        "caregivers_loaded": caregivers
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/dataset-status")
def dataset_status():
    return home()

@app.post("/navigate")
@app.post("/intake")
def navigate(payload: IntakeRequest):
    initialize_database()
    result = get_demo_response(payload.user_input)

    # Check whether the database has a broadly matching example.
    words = [
        word for word in payload.user_input.lower().split()
        if len(word) > 2
    ]
    connection = get_db()
    rows = connection.execute(
        "SELECT user_input FROM triage_examples"
    ).fetchall()
    connection.close()

    result["dataset_reference_found"] = any(
        any(word in (row["user_input"] or "").lower() for word in words)
        for row in rows
    )
    result["message"] = result["summary"]
    result["response"] = result["guidance"]
    result["advice"] = result["guidance"]
    result["resources"] = result["next_steps"]
    result["language"] = payload.language
    result["notice"] = (
        "Demo prototype only. Dataset is synthetic; this is not "
        "a validated medical triage system."
    )
    return result
