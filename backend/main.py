import logging
import json
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any

# Configure structured logging
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger_name": record.name,
            "filename": record.filename,
            "lineno": record.lineno,
            "module": record.module,
            "funcName": record.funcName,
            "process": record.process,
            "thread": record.thread,
            **getattr(record, 'extra', {}) # Include any extra attributes
        }
        return json.dumps(log_record)

# Set up logger
logger = logging.getLogger("agent_console_backend")
logger.setLevel(logging.INFO)

# Check if handlers already exist to prevent duplicate logging
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = JsonFormatter(datefmt="%Y-%m-%dT%H:%M:%S%z")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

app = FastAPI()

class LogMessage(BaseModel):
    message: str
    data: Dict[str, Any] = {}

@app.get("/")
async def read_root():
    logger.info("Root endpoint accessed", extra={"endpoint": "/", "method": "GET"})
    return {"message": "Hello World from Agent Console Backend!"}

@app.post("/log")
async def write_log(log_message: LogMessage):
    logger.info(log_message.message, extra=log_message.data)
    return {"status": "success", "message": "Log received"}

