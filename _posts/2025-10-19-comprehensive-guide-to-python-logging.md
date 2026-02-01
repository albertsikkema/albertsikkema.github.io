---
layout: post
title: "A Comprehensive Guide to Python Logging: From Print Statements to Production"
date: 2025-10-19
categories: python development best-practices
description: "Complete Python logging guide from basics to production. Covers async-safe logging, structured logs, FastAPI patterns, and performance optimization."
keywords: "Python logging, FastAPI logging, async logging, structured logging, QueueHandler, production logging best practices"
---

In a current Fastapi project I got thinking about logging in Fastapi. Is the way I have been doing it (still) the correct way? I've been researching Python logging, and decided to share my findings in this guide. Maybe it is of use to you!

Every Python developer has been there—debugging with print statements scattered throughout the code, only to find them nearly impossible to disable or filter when you need to. While `print()` might work for quick scripts, production applications demand something more sophisticated.

This comprehensive guide takes you from basic logging concepts to production-ready implementations, including async-safe patterns and structured logging for modern applications.

## Table of Contents

1. [Why Not Just Use print()?](#why-not-just-use-print)
2. [Core Logging Approaches](#core-logging-approaches)
   - [Basic Logging](#1-basic-logging-simple-applications)
   - [Module-Level Logging](#2-module-level-logging-recommended-for-librariesapplications)
   - [dictConfig (Production)](#3-dictconfig-production-applications)
   - [Queue-Based Logging (Async)](#4-queue-based-logging-async-applications)
3. [Log Levels Explained](#log-levels-explained)
   - [DEBUG, INFO, WARNING, ERROR, CRITICAL](#debug-10---detailed-diagnostic-information)
   - [Choosing the Right Level](#choosing-the-right-level)
4. [Configuration Methods](#configuration-methods)
   - [Environment Variables](#1-environment-variables-recommended)
   - [Configuration Files (YAML/JSON)](#2-configuration-files-yamljson)
   - [Programmatic Configuration](#3-programmatic-configuration)
   - [Recommended Format Strings](#recommended-format-strings)
5. [Async-Safe Logging: The Critical Pattern](#async-safe-logging-the-critical-pattern)
   - [The Problem](#the-problem)
   - [The Solution: QueueHandler + QueueListener](#the-solution-queuehandler--queuelistener)
6. [Structured Logging for Production](#structured-logging-for-production)
   - [When to Use Structured Logging](#when-to-use-structured-logging)
7. [Best Practices](#best-practices)
8. [Common Patterns](#common-patterns)
   - [Request Logging Middleware](#pattern-1-request-logging-middleware-fastapi)
   - [Contextual Logging (Request ID)](#pattern-2-contextual-logging-request-id)
   - [Exception Logging at Boundaries](#pattern-3-exception-logging-at-boundaries)
   - [Conditional Debug Logging](#pattern-4-conditional-debug-logging)
   - [Migration from Print to Logging](#pattern-5-migration-from-print-to-logging)
9. [Testing Logging](#testing-logging)
10. [Quick Reference](#quick-reference)
11. [Resources](#resources)

## Why Not Just Use `print()`?

Let's start with why print statements fall short:

```python
# Problems with print statements:
print("Server starting...")                    # No timestamps
print(f"Processing user {user_id}")            # No severity levels
print(f"Warning: Rate limit approaching")      # Can't filter or disable
print(f"ERROR: Database failed: {error}")      # No structured output
```

**Key limitations**:
- ❌ No timestamp or context
- ❌ No severity/priority levels
- ❌ Cannot be disabled without code changes
- ❌ Not redirectable to files/services
- ❌ No structured data for analysis
- ❌ Mixes with stdout (test output, user messages)

Python's logging module solves all of these problems and more.

## Core Logging Approaches

### 1. Basic Logging (Simple Applications)

**When to use**: Scripts, small tools, learning projects

```python
import logging

# Quick setup - one liner
logging.basicConfig(level=logging.INFO)

# Use directly
logging.info("Application started")
logging.warning("Disk space low")
logging.error("Failed to connect")
```

**Pros**:
- ✅ Zero configuration
- ✅ Works immediately
- ✅ Good for scripts

**Cons**:
- ❌ Uses root logger (not modular)
- ❌ Hard to customize per-module
- ❌ No control over format

### 2. Module-Level Logging (Recommended for Libraries/Applications)

**When to use**: Any reusable code, libraries, applications

```python
import logging

# Get logger for this module
logger = logging.getLogger(__name__)

def process_data():
    logger.debug("Starting data processing")
    logger.info("Processed 1000 records")
    logger.warning("Skipped 5 invalid records")
```

**Pros**:
- ✅ Logger hierarchy (e.g., `myapp.utils.helpers`)
- ✅ Can configure different levels per module
- ✅ Doesn't pollute root logger
- ✅ Library-friendly

**Cons**:
- ⚠️ Requires configuration elsewhere

### 3. dictConfig (Production Applications)

**When to use**: Production apps, complex configurations

```python
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': 'INFO',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'app.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'detailed',
            'level': 'DEBUG',
        },
    },
    'loggers': {
        'myapp': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'myapp.database': {
            'level': 'WARNING',  # Only warnings for DB
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
```

**Pros**:
- ✅ Complete control over all aspects
- ✅ Supports multiple handlers (console + file)
- ✅ Different configs per module
- ✅ Can be loaded from JSON/YAML
- ✅ Industry standard

**Cons**:
- ⚠️ More complex setup
- ⚠️ Requires understanding of logging architecture

### 4. Queue-Based Logging (Async Applications)

**When to use**: FastAPI, asyncio apps, high-performance servers

This is crucial for async applications where blocking I/O can devastate performance.

```python
import logging
import logging.handlers
from queue import Queue

# Create queue and listener
log_queue = Queue()
queue_handler = logging.handlers.QueueHandler(log_queue)

# Configure actual handlers (run in separate thread)
console_handler = logging.StreamHandler()
file_handler = logging.handlers.RotatingFileHandler('app.log')

# Start listener in background thread
queue_listener = logging.handlers.QueueListener(
    log_queue,
    console_handler,
    file_handler,
    respect_handler_level=True
)
queue_listener.start()

# Configure root logger to use queue
root_logger = logging.getLogger()
root_logger.addHandler(queue_handler)
root_logger.setLevel(logging.INFO)

# Use normally in async code
logger = logging.getLogger(__name__)

async def handle_request():
    logger.info("Processing request")  # Non-blocking!
```

**Pros**:
- ✅ **Non-blocking** - critical for async applications
- ✅ 20-50% throughput improvement over synchronous logging
- ✅ Offloads I/O to background thread
- ✅ No event loop blocking

**Cons**:
- ⚠️ More complex setup
- ⚠️ Must start/stop listener properly
- ⚠️ Logs may be delayed slightly

**Performance Impact**:
- Synchronous logging: 20-50% throughput reduction in async apps
- QueueHandler pattern: <5% overhead

## Log Levels Explained

Python has 5 standard log levels (from least to most severe):

### DEBUG (10) - Detailed Diagnostic Information

**When to use**: Detailed execution flow, variable values, step-by-step processing

```python
logger.debug(f"Processing user_id={user_id}, role={role}")
logger.debug(f"Query parameters: {params}")
logger.debug(f"Entering function with args: {args}")
```

**Environment**: Development only (too verbose for production)

### INFO (20) - Confirmation of Expected Behavior

**When to use**: Normal operations, milestones, successful completions

```python
logger.info("Server started on port 8000")
logger.info("User authentication successful")
logger.info("Processed 1000 records in 2.3 seconds")
logger.info("Cache cleared")
```

**Environment**: All environments

### WARNING (30) - Something Unexpected (But Handled)

**When to use**: Deprecated features, unusual conditions, potential issues, client errors (400, 404)

```python
logger.warning("API rate limit approaching (80% used)")
logger.warning("Using deprecated configuration format")
logger.warning(f"File not found: {path}")  # 404
logger.warning("Retrying failed connection (attempt 2/3)")
```

**Environment**: All environments

### ERROR (40) - Serious Problem, Operation Failed

**When to use**: Failed operations, exceptions, server errors (500), data loss

```python
logger.error(f"Database connection failed: {e}", exc_info=True)
logger.error(f"Failed to write file: {path}")
logger.error("Payment processing failed", exc_info=True)
```

**Environment**: All environments

**Note**: Use `exc_info=True` to include full traceback

### CRITICAL (50) - Very Serious Error, Program May Stop

**When to use**: System failures, resource exhaustion, data corruption

```python
logger.critical("Database connection pool exhausted")
logger.critical("Out of disk space - cannot continue")
logger.critical("Configuration file missing - cannot start")
```

**Environment**: All environments

### Choosing the Right Level

```python
# Decision tree:
if "diagnostic information for developers":
    logger.debug()
elif "normal operation confirmation":
    logger.info()
elif "unexpected but handled" or "client error (400s)":
    logger.warning()
elif "operation failed" or "server error (500s)":
    logger.error()
elif "system is unusable":
    logger.critical()
```

## Configuration Methods

### 1. Environment Variables (Recommended)

**Advantage**: Change log level without code changes

```python
import os
import logging

# Simple approach
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level))

# With pydantic-settings (FastAPI style)
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
logging.basicConfig(level=settings.LOG_LEVEL)
```

**Usage**:
```bash
# Development
LOG_LEVEL=DEBUG python app.py

# Production
LOG_LEVEL=WARNING python app.py
```

### 2. Configuration Files (YAML/JSON)

**Advantage**: Complex configurations, version controlled

```yaml
# logging_config.yaml
version: 1
disable_existing_loggers: false

formatters:
  simple:
    format: '%(levelname)s - %(message)s'
  detailed:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'

handlers:
  console:
    class: logging.StreamHandler
    formatter: simple
    level: INFO

  file:
    class: logging.handlers.RotatingFileHandler
    filename: app.log
    maxBytes: 10485760
    backupCount: 5
    formatter: detailed
    level: DEBUG

loggers:
  myapp:
    level: DEBUG
    handlers: [console, file]
    propagate: false

root:
  level: INFO
  handlers: [console]
```

```python
import logging.config
import yaml

with open('logging_config.yaml', 'r') as f:
    config = yaml.safe_load(f)
    logging.config.dictConfig(config)
```

### 3. Programmatic Configuration

**Advantage**: Full control, dynamic configuration

```python
import logging
import logging.handlers

# Create logger
logger = logging.getLogger('myapp')
logger.setLevel(logging.DEBUG)

# Create handlers
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

file_handler = logging.handlers.RotatingFileHandler(
    'app.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
file_handler.setLevel(logging.DEBUG)

# Create formatters
console_format = logging.Formatter('%(levelname)-8s - %(message)s')
file_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)

# Attach formatters to handlers
console_handler.setFormatter(console_format)
file_handler.setFormatter(file_format)

# Attach handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
```

### Recommended Format Strings

**Simple (Console)**:
```python
'%(levelname)-8s - %(message)s'
# Output: INFO     - Server started
```

**Standard (File)**:
```python
'%(asctime)s - %(levelname)-8s - %(name)s - %(message)s'
# Output: 2025-10-19 10:30:45,123 - INFO     - myapp.server - Server started
```

**Detailed (Debugging)**:
```python
'%(asctime)s - %(levelname)-8s - %(name)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s'
# Output: 2025-10-19 10:30:45,123 - INFO     - myapp.server - main.py:42 - startup() - Server started
```

**Available Format Variables**:
- `%(asctime)s` - Timestamp
- `%(name)s` - Logger name (module path)
- `%(levelname)s` - Log level (DEBUG, INFO, etc.)
- `%(levelname)-8s` - Log level, left-aligned, 8 chars wide
- `%(message)s` - Log message
- `%(filename)s` - Source filename
- `%(lineno)d` - Line number
- `%(funcName)s` - Function name
- `%(pathname)s` - Full file path
- `%(process)d` - Process ID
- `%(thread)d` - Thread ID

## Async-Safe Logging: The Critical Pattern

### The Problem

**Synchronous logging blocks the event loop in async applications**:

```python
import asyncio
import logging

logging.basicConfig(
    filename='app.log',  # File I/O blocks!
    level=logging.INFO
)

async def handle_request():
    logger.info("Request started")  # BLOCKS the event loop!
    await asyncio.sleep(0.1)
    logger.info("Request completed")  # BLOCKS again!
```

**Performance Impact**:
- File I/O: 1-10ms per log write
- In busy async app: 20-50% throughput reduction
- Latency spikes: 99th percentile increases significantly

### The Solution: QueueHandler + QueueListener

**Architecture**:
```
[Async Code]
    ↓ logger.info() - fast, non-blocking
[QueueHandler] - adds to queue (microseconds)
    ↓
[Queue] - thread-safe buffer
    ↓
[QueueListener] - separate thread
    ↓
[Handlers] - File/Network I/O (blocking, but in background)
```

**FastAPI Implementation**:

```python
import logging
import logging.handlers
from queue import Queue
from contextlib import asynccontextmanager
from fastapi import FastAPI

# Global queue and listener
log_queue = Queue()
queue_listener = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Configure non-blocking logging on startup."""
    global queue_listener

    # Create handlers (these do blocking I/O)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter('%(levelname)-8s - %(message)s')
    )

    file_handler = logging.handlers.RotatingFileHandler(
        'app.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    )

    # Start listener in background thread
    queue_listener = logging.handlers.QueueListener(
        log_queue,
        console_handler,
        file_handler,
        respect_handler_level=True
    )
    queue_listener.start()

    # Configure root logger to use queue
    queue_handler = logging.handlers.QueueHandler(log_queue)
    root_logger = logging.getLogger()
    root_logger.addHandler(queue_handler)
    root_logger.setLevel(logging.INFO)

    logger = logging.getLogger(__name__)
    logger.info("Application started with non-blocking logging")

    yield

    # Shutdown
    logger.info("Application shutting down")
    if queue_listener:
        queue_listener.stop()

app = FastAPI(lifespan=lifespan)

# Use normally in async code
logger = logging.getLogger(__name__)

@app.get("/")
async def root():
    logger.info("Request received")  # Non-blocking!
    return {"status": "ok"}
```

**Performance Results**:
- QueueHandler overhead: <5%
- No event loop blocking
- Consistent latency (no spikes)

## Structured Logging for Production

### Standard Logging (String-Based)

```python
# Traditional approach
logger.info(f"User {user_id} logged in from {ip}")

# Output:
# 2025-10-19 10:30:45 - INFO - User 12345 logged in from 192.168.1.1
```

**Problems**:
- ❌ Hard to parse programmatically
- ❌ Can't filter by user_id or IP
- ❌ Inconsistent format across logs
- ❌ No support for log aggregation tools

### Structured Logging (JSON-Based)

```python
import structlog

logger = structlog.get_logger()

logger.info("user_login", user_id=12345, ip="192.168.1.1", duration_ms=245)

# Output (JSON):
# {
#   "event": "user_login",
#   "user_id": 12345,
#   "ip": "192.168.1.1",
#   "duration_ms": 245,
#   "timestamp": "2025-10-19T10:30:45.123Z",
#   "level": "info"
# }
```

**Advantages**:
- ✅ Machine-parseable (JSON)
- ✅ Easy to search/filter in log aggregation tools
- ✅ Consistent structure
- ✅ Rich context (nested data)
- ✅ Supports metrics extraction

### When to Use Structured Logging

**Use when**:
- ✅ Deploying to production with log aggregation (ELK, Datadog, Better Stack)
- ✅ Need to search/filter logs programmatically
- ✅ Building microservices (need request tracing)
- ✅ Collecting metrics from logs

**Don't use when**:
- ❌ Local development (JSON is hard to read)
- ❌ Simple scripts
- ❌ No log aggregation infrastructure

**Recommendation**: Start with standard logging, add structured logging when you need it.

## Best Practices

### 1. Use Module-Level Loggers

```python
# ✅ DO: Module-level logger
import logging
logger = logging.getLogger(__name__)

def process():
    logger.info("Processing started")

# ❌ DON'T: Root logger
import logging
logging.info("Processing started")  # Pollutes root logger
```

### 2. Use Lazy Formatting (this is an interesting one!)

```python
# ✅ DO: Lazy formatting (only formats if logged)
logger.debug("Processing user %s with data %s", user_id, data)

# ❌ DON'T: Eager formatting (always runs, even if not logged)
logger.debug(f"Processing user {user_id} with data {data}")
```

**Why**: If log level is INFO, debug messages aren't output. Lazy formatting avoids unnecessary string operations.

### 3. Include Exception Info

```python
# ✅ DO: Include traceback
try:
    risky_operation()
except Exception as e:
    logger.error("Operation failed", exc_info=True)
    # or
    logger.exception("Operation failed")  # Same as exc_info=True

# ❌ DON'T: Just log the message
except Exception as e:
    logger.error(f"Operation failed: {e}")  # No traceback!
```

### 4. Use Extra Context

```python
# ✅ DO: Add structured context
logger.info(
    "Request completed",
    extra={
        "request_id": "abc-123",
        "user_id": 456,
        "duration_ms": 45.2,
        "status_code": 200
    }
)

# ❌ DON'T: Embed in message
logger.info("Request abc-123 for user 456 completed in 45.2ms with status 200")
```

### 5. Log at the Right Level

```python
# ✅ DO: Use appropriate levels
logger.debug("Entering function with args: %s", args)
logger.info("User login successful")
logger.warning("File not found, using default")
logger.error("Database connection failed", exc_info=True)
logger.critical("Out of memory, shutting down")

# ❌ DON'T: Use wrong levels
logger.error("User logged in")  # Too severe
logger.info("Database crashed")  # Not severe enough
```

### 6. Don't Log Sensitive Data

```python
# ❌ DON'T: Log passwords, tokens, PII
logger.info(f"User login: {username}:{password}")
logger.debug(f"API token: {api_token}")
logger.info(f"SSN: {ssn}")

# ✅ DO: Redact or hash sensitive data
logger.info(f"User login: {username}:******")
logger.debug(f"API token: {api_token[:8]}...")
logger.info(f"User ID: {hash(ssn)}")
```

### 7. Configure Early, Log Everywhere

```python
# ✅ DO: Configure once at startup
# main.py
import logging
logging.basicConfig(level=logging.INFO)

# Then use in all modules
# utils.py
import logging
logger = logging.getLogger(__name__)
logger.info("Utils loaded")

# ❌ DON'T: Configure in every module
# utils.py
import logging
logging.basicConfig(level=logging.INFO)  # Overrides previous config!
```

### 8. Handle Logging Exceptions

```python
# ✅ DO: Catch logging errors in critical paths
try:
    risky_operation()
except Exception as e:
    try:
        logger.error("Operation failed", exc_info=True)
    except:
        pass  # Don't let logging crash the app

# Or use NullHandler for libraries
import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())  # No-op if not configured
```

### 9. Use Log Rotation

```python
# ✅ DO: Rotate logs to prevent disk fill
import logging.handlers

handler = logging.handlers.RotatingFileHandler(
    'app.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5            # Keep 5 old files
)

# Or time-based rotation
handler = logging.handlers.TimedRotatingFileHandler(
    'app.log',
    when='midnight',    # Rotate at midnight
    interval=1,         # Every 1 day
    backupCount=7       # Keep 7 days
)

# ❌ DON'T: Write to unbounded file
handler = logging.FileHandler('app.log')  # Will grow forever!
```

### 10. Environment-Specific Configuration

```python
# ✅ DO: Different configs per environment
import os

if os.getenv('ENV') == 'production':
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.handlers.RotatingFileHandler('app.log'),
            logging.StreamHandler()
        ]
    )
else:  # development
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)-8s - %(name)s - %(message)s'
    )
```

## Common Patterns

### Pattern 1: Request Logging Middleware (FastAPI)

```python
import time
import logging
from fastapi import Request

logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    logger.info(
        "Request started",
        extra={
            "method": request.method,
            "path": request.url.path,
            "client": request.client.host if request.client else None
        }
    )

    response = await call_next(request)

    duration_ms = (time.time() - start_time) * 1000

    logger.info(
        "Request completed",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "duration_ms": round(duration_ms, 2)
        }
    )

    return response
```

### Pattern 2: Contextual Logging (Request ID)

```python
import contextvars
import logging
import uuid

# Create context variable
request_id_var = contextvars.ContextVar('request_id', default=None)

class RequestIdFilter(logging.Filter):
    """Add request_id to all log records."""
    def filter(self, record):
        record.request_id = request_id_var.get() or 'no-request-id'
        return True

# Configure
logger = logging.getLogger()
logger.addFilter(RequestIdFilter())

# Format with request_id
formatter = logging.Formatter(
    '%(asctime)s - [%(request_id)s] - %(levelname)s - %(message)s'
)

# Use in middleware
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request_id_var.set(request_id)

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id

    return response

# All logs in this request will include request_id
logger.info("Processing payment")  # Will show request_id
```

### Pattern 3: Exception Logging at Boundaries

```python
# Repository layer - raise exceptions
class UserRepository:
    def get_user(self, user_id):
        try:
            return self.db.get(user_id)
        except DatabaseError as e:
            logger.error(f"Failed to get user {user_id}", exc_info=True)
            raise

# Service layer - propagate exceptions
class UserService:
    def get_user(self, user_id):
        return self.repo.get_user(user_id)  # Let exception propagate

# Router layer - catch and convert to HTTP
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    try:
        user = service.get_user(user_id)
        logger.info(f"User {user_id} retrieved successfully")
        return user
    except DatabaseError as e:
        logger.error(f"Failed to retrieve user {user_id}", exc_info=True)
        raise HTTPException(status_code=500, detail="Database error")
```

### Pattern 4: Conditional Debug Logging

```python
# Only compute expensive debug info if debug is enabled
if logger.isEnabledFor(logging.DEBUG):
    expensive_data = compute_debug_info()  # Expensive!
    logger.debug(f"Debug data: {expensive_data}")

# Lazy formatting achieves similar result
logger.debug("Debug data: %s", lambda: compute_debug_info())
```

### Pattern 5: Migration from Print to Logging

This pattern directly addresses the question: "Is my current logging approach correct?"

```python
# Step 1: Find all print statements
# grep -r "print(" backend/

# Step 2: Categorize by purpose
print("Server starting")           → logger.info()
print(f"Debug: {value}")           → logger.debug()
print(f"Warning: {msg}")           → logger.warning()
print(f"ERROR: {error}")           → logger.error()
print(traceback.format_exc())      → logger.exception()

# Step 3: Replace
# Before:
print(f"Processing user {user_id}")

# After:
logger.info("Processing user %s", user_id)

# Before:
try:
    risky()
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()

# After:
try:
    risky()
except Exception as e:
    logger.exception("Operation failed")
```

## Testing Logging

### Using pytest's caplog Fixture

```python
import logging
import pytest

def process_data(data):
    logger = logging.getLogger(__name__)
    if not data:
        logger.warning("No data provided")
        return None
    logger.info(f"Processing {len(data)} items")
    return data

def test_logging_no_data(caplog):
    """Test warning is logged when no data."""
    with caplog.at_level(logging.WARNING):
        result = process_data(None)

    assert result is None
    assert "No data provided" in caplog.text
    assert caplog.records[0].levelname == "WARNING"

def test_logging_with_data(caplog):
    """Test info is logged when processing data."""
    with caplog.at_level(logging.INFO):
        result = process_data([1, 2, 3])

    assert result == [1, 2, 3]
    assert "Processing 3 items" in caplog.text

def test_exception_logged(caplog):
    """Test exception is logged with traceback."""
    logger = logging.getLogger(__name__)

    with caplog.at_level(logging.ERROR):
        try:
            1 / 0
        except ZeroDivisionError:
            logger.exception("Math error")

    assert "Math error" in caplog.text
    assert caplog.records[0].exc_info is not None  # Traceback included
```

### Mocking Logging

```python
from unittest.mock import patch, MagicMock

def test_logging_called():
    """Verify specific log calls are made."""
    with patch('mymodule.logger') as mock_logger:
        process_data([1, 2, 3])

        # Verify specific call
        mock_logger.info.assert_called_once_with("Processing %s items", 3)

        # Verify error was logged
        mock_logger.error.assert_called()

        # Verify call count
        assert mock_logger.warning.call_count == 2
```

### Testing Log Configuration

```python
def test_log_level_from_env(monkeypatch):
    """Test log level is set from environment."""
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    # Re-import module to pick up env var
    import importlib
    import myapp
    importlib.reload(myapp)

    logger = logging.getLogger('myapp')
    assert logger.level == logging.DEBUG
```

## Quick Reference

### Common Setup Patterns

**Development (Console only, DEBUG level)**:
```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)-8s - %(name)s - %(message)s'
)
```

**Production (File + Console, INFO level)**:
```python
import logging.handlers

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.handlers.RotatingFileHandler(
            'app.log',
            maxBytes=10*1024*1024,
            backupCount=5
        )
    ]
)
```

**Async/FastAPI (Non-blocking with QueueHandler)**:
```python
import logging.handlers
from queue import Queue

log_queue = Queue()
queue_handler = logging.handlers.QueueHandler(log_queue)

console_handler = logging.StreamHandler()
queue_listener = logging.handlers.QueueListener(
    log_queue, console_handler
)
queue_listener.start()

root_logger = logging.getLogger()
root_logger.addHandler(queue_handler)
root_logger.setLevel(logging.INFO)
```

### Decision Matrix

| Scenario | Approach | Reason |
|----------|----------|--------|
| Simple script | `logging.basicConfig()` | Quick setup |
| Library/reusable code | Module-level logger | Configurable by users |
| Production app | `dictConfig` + env vars | Full control, environment-aware |
| Async/FastAPI app | QueueHandler pattern | Non-blocking I/O |
| Microservices | Structured logging (JSON) | Log aggregation, tracing |
| High-traffic API | QueueHandler + log rotation | Performance + disk management |
| Debugging | DEBUG level + detailed format | Maximum visibility |
| Production monitoring | INFO/WARNING + JSON + aggregation | Actionable insights |

## Conclusion

Python's logging module offers flexible solutions from simple print replacements to sophisticated structured logging systems. The key is to start simple and add complexity as needed.

For modern async applications like FastAPI, the QueueHandler pattern is essential to avoid blocking the event loop. For production deployments with log aggregation tools, structured logging provides the machine-parseable format you need for effective monitoring and debugging.

The patterns and practices covered here are used in production systems. Whether you're building a simple script or a high-performance microservice, Python's logging module has the capabilities you need—when configured correctly.

Remember: good logging is an investment. It pays dividends every time you need to debug an issue, analyze performance, or understand system behavior in production.

## Resources

### Official Documentation
- [Python Logging HOWTO](https://docs.python.org/3/howto/logging.html) - Official tutorial
- [Python logging module](https://docs.python.org/3/library/logging.html) - API reference
- [Python Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html) - Recipes and patterns
- [Python asyncio-dev Documentation](https://docs.python.org/3/library/asyncio-dev.html) - Async logging patterns
- [Uvicorn Settings](https://www.uvicorn.org/settings/) - Server configuration including logging

### FastAPI-Specific
- [Better Stack - Logging with FastAPI](https://betterstack.com/community/guides/logging/logging-with-fastapi/) - Comprehensive FastAPI guide
- [FastAPI Logging Strategy (Compile N Run)](https://www.compilenrun.com/docs/framework/fastapi/fastapi-best-practices/fastapi-logging-strategy/) - Best practices
- [Unify Logging for Gunicorn/Uvicorn/FastAPI](https://pawamoy.github.io/posts/unify-logging-for-a-gunicorn-uvicorn-app/) - Unified logging configuration
- [FastAPI Non-Blocking Logging](https://dev.to/behainguyen/python-fastapi-implementing-non-blocking-logging-with-built-in-queuehandler-and-queuelistener-classes-2ahi) - QueueHandler tutorial
- [FastAPI Logging Middleware](https://medium.com/@dhavalsavalia/fastapi-logging-middleware-logging-requests-and-responses-with-ease-and-style-201b9aa4001a) - Request logging patterns

### Async Logging
- [Super Fast Python - Asyncio Logging Best Practices](https://superfastpython.com/asyncio-logging-best-practices/) - Comprehensive async guide
- [Asyncio Logging Without Blocking](https://superfastpython.com/asyncio-log-blocking/) - Performance analysis
- [Martijn Pieters - Logging in asyncio](https://www.zopatista.com/python/2019/05/11/asyncio-logging/) - Deep dive

### Structured Logging
- [FastAPI Structured JSON Logging](https://www.sheshbabu.com/posts/fastapi-structured-json-logging/) - JSON logging tutorial
- [FastAPI Structlog Integration](https://wazaari.dev/blog/fastapi-structlog-integration) - Using structlog with FastAPI
- [Operations-Friendly Observability Guide](https://blog.greeden.me/en/2025/10/07/operations-friendly-observability-a-fastapi-implementation-guide-for-logs-metrics-and-traces-request-id-json-logs-prometheus-opentelemetry-and-dashboard-design/) - Complete observability implementation
- [Structlog Documentation](https://www.structlog.org/) - Official structlog docs

### General Best Practices
- [Real Python - Logging in Python](https://realpython.com/python-logging/) - Comprehensive guide
- [Python Logging Best Practices](https://middleware.io/blog/python-logging-best-practices/) - Industry patterns
- [When to use different log levels](https://stackoverflow.com/questions/2031163/when-to-use-the-different-log-levels) - Stack Overflow discussion

### Log Levels and Configuration
- [Python Log Levels Explained (Dash0)](https://www.dash0.com/faq/python-log-levels-explained) - Detailed log level guide
- [SigNoz - Set Logging Level from Command Line](https://signoz.io/guides/how-to-set-logging-level-from-command-line/) - CLI configuration patterns

---

*What's your approach to logging in Python applications? Have you encountered performance issues with async logging? I'd love to hear about your experiences—<a href="#" onclick="task1(); return false;">get in touch</a>.*
