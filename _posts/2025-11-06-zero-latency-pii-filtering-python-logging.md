---
layout: post
title: "Zero-Latency PII Filtering in Python Logging: GDPR Compliance Without the Performance Hit"
date: 2025-11-06
categories: python security best-practices gdpr
---

While implementing centralized logging for a FastAPI service using Axiom for logging, I ran into a challenge: how do you filter PII (Personal Identifiable Information, like email, phone number etc.) from logs without slowing down your application?

The obvious solution—sanitizing logs during the log call itself—added 1-2ms to every request:

```python
logger.info(sanitize_pii(f"User {email} logged in"))  # Blocks main thread!
```

This blocks the main thread for every single log entry. With Python running on a single thread by default and regex-based PII filtering taking 1-2ms per log, this creates a real performance problem. And more filtering will follow, so this is potentially huge.

<figure>
  <img src="/assets/images/gdpr-logging-diagram.png" alt="GDPR-Compliant Python Logging Architecture">
  <figcaption>This is what AI thinks an image for this blog should look like...</figcaption>
</figure>

## The Solution: Background Thread Filtering

Most modern log aggregation libraries (axiom-py, datadog, logstash) buffer logs and send them in batches every 5-10 seconds using a background thread. So what if we could use that? And **sanitize during the flush, not during the log call itself**. So I basically extended the Axiomhandler:

```python
from axiom_py.logging import AxiomHandler

class SafeAxiomHandler(AxiomHandler):
    """Custom handler with automatic PII filtering in background thread."""

    def flush(self):
        """Override flush to sanitize before sending to Axiom."""
        if len(self.buffer) == 0:
            return

        # Sanitize all buffered logs (runs on background thread!)
        sanitized_buffer = [
            self._sanitize_event(event)
            for event in self.buffer
        ]

        self.buffer = []
        self.client.ingest_events(self.dataset, sanitized_buffer)

    def _sanitize_event(self, event_dict: dict) -> dict:
        """Redact PII from log event."""
        sanitized = {}
        for key, value in event_dict.items():
            if isinstance(value, str):
                # Use your sanitization function
                value = sanitize_string(value)
            sanitized[key] = value
        return sanitized
```

## Why This Works

The `flush()` method runs on a background thread (via Timer) in axiom-py and similar libraries. By moving PII filtering there:

- **Main thread**: 0.01ms overhead (just dict conversion)
- **Background thread**: 1-2ms for regex filtering
- **Request latency impact**: 0ms

The logs get sanitized 5 seconds later when the background thread flushes the buffer. For production logging, that delay is perfectly acceptable.

## How Method Overriding Works

When you inherit from a class and define a method with the same name as the parent class, you **override** that method. Python's method resolution looks for methods in the child class first:

```python
# Parent class (axiom-py library)
class AxiomHandler:
    def flush(self):
        """Original: just send buffer to Axiom"""
        if len(self.buffer) > 0:
            self.client.ingest_events(self.dataset, self.buffer)
            self.buffer = []

# Your child class
class SafeAxiomHandler(AxiomHandler):
    def flush(self):
        """Override: sanitize BEFORE sending"""
        # This completely replaces parent's flush()
        sanitized_buffer = [self._sanitize_event(e) for e in self.buffer]
        self.buffer = []
        self.client.ingest_events(self.dataset, sanitized_buffer)
```

**The execution flow:**

```
Background Thread (Timer) calls flush():
    ↓
Is flush() defined in SafeAxiomHandler?
    ↓ YES
SafeAxiomHandler.flush() executes:
    1. Sanitize all events in buffer (YOUR CODE)
    2. Send sanitized events to Axiom (YOUR CODE)
    ↓
Done! Main thread was never blocked.
```

The brilliance: **the background thread calling pattern doesn't change**. When axiom-py's Timer fires and calls `self.flush()`, Python automatically routes it to your override. The library doesn't know you've customized it—it just works.

You have access to all parent class attributes:
- `self.buffer` - inherited from AxiomHandler
- `self.client` - inherited from AxiomHandler
- `self.dataset` - inherited from AxiomHandler

As an extra: If you wanted to keep parent behavior and add to it, use `super()`:
```python
def flush(self):
    # Sanitize first
    self.buffer = [self._sanitize_event(e) for e in self.buffer]
    # Then call parent's flush
    super().flush()  # Calls AxiomHandler.flush()
```

## Implementation Tips

**1. Identify Sensitive Keys**

Some data should be completely redacted:

```python
SENSITIVE_KEYS = {
    "questionnaire", "questions", "answers",
    "chat_history", "password", "api_key"
}

if key in SENSITIVE_KEYS:
    sanitized[key] = "[REDACTED]"
```

**2. Use Proper PII Detection Libraries**

For emails, regex works fine. For phone numbers, use [Google's phonenumbers library](https://github.com/daviddrysdale/python-phonenumbers) for accurate international detection:

```python
import re
import phonenumbers

# Email: regex is sufficient
EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
)

def sanitize_string(text: str) -> str:
    """Sanitize PII from text."""
    # Redact emails
    text = EMAIL_PATTERN.sub("[REDACTED]", text)

    # Redact phone numbers using Google's library (more accurate for GDPR)
    for match in phonenumbers.PhoneNumberMatcher(text, None):
        text = text.replace(match.raw_string, "[REDACTED]")

    return text
```

**Why phonenumbers over regex?** GDPR compliance requires accurate detection. Phone number formats vary wildly across countries—Google's library handles all international formats correctly.

## Edge Cases to Consider

**Buffer Overflow**: If your app logs faster than the flush interval (>1000 logs in 5 seconds), `flush()` might run on the main thread. Monitor buffer size in production. 

**Performance Consideration**: The `phonenumbers` library is more thorough than regex but slightly slower. In production, this trade-off is worth it for GDPR accuracy, especially since filtering happens on the background thread.

**Testing**: Mock the client to test without real API calls:

```python
from unittest.mock import MagicMock

def test_pii_filtering():
    mock_client = MagicMock()
    handler = SafeAxiomHandler(client=mock_client, dataset="test")

    logger = logging.getLogger("test")
    logger.addHandler(handler)

    logger.info("User john@example.com logged in")
    handler.flush()

    # Verify email was redacted
    sent_events = mock_client.ingest_events.call_args[0][1]
    assert "[REDACTED]" in sent_events[0]["msg"]
    assert "john@example.com" not in sent_events[0]["msg"]
```

## Trade-offs

**Benefits:**
- Zero request latency impact
- Automatic protection (developers can't forget)
- GDPR compliant by default
- Easy to test and maintain

**Costs:**
- Logs delayed by 5-10 seconds
- Slight memory overhead (buffer storage)
- Pattern only works with buffered/batched handlers

## When to Use This Pattern

This pattern is essential for:
- Production APIs with strict SLAs (<3s response time)
- GDPR/CCPA compliance requirements
- High-volume logging (>100 logs/second)
- User-generated content that might contain PII

Don't use it for:
- Development/local logging (console handlers don't buffer)
- Low-traffic apps where 1-2ms overhead is acceptable
- Real-time log streaming (no buffering)

## The Result

In our production FastAPI service:
- **Before**: 1-2ms added to request time for PII filtering
- **After**: 0ms request overhead, filtering happens in background
- **GDPR compliance**: Automatic, no developer action needed

By leveraging the background thread that already exists in modern logging libraries, we achieved GDPR-compliant logging without sacrificing performance. The key was recognizing that log delivery doesn't need to be synchronous—and that's where the opportunity lives.

## Resources

### Python Logging
- [Python Logging Documentation](https://docs.python.org/3/library/logging.html) - Official docs
- [Logging Best Practices](https://docs.python-guide.org/writing/logging/) - The Hitchhiker's Guide to Python
- [Python Logging Handlers](https://docs.python.org/3/library/logging.handlers.html) - Handler reference

### GDPR & PII
- [GDPR Official Text](https://gdpr-info.eu/) - Full regulation text
- [GDPR Logging Requirements](https://www.enterprisenetworkingplanet.com/security/gdpr-logging-requirements/) - Compliance guide
- [Google phonenumbers Library](https://github.com/daviddrysdale/python-phonenumbers) - Accurate international phone number detection
- [PII Detection Patterns](https://github.com/microsoft/presidio) - Microsoft's PII detection library

### Log Aggregation Services
- [Axiom Documentation](https://axiom.co/docs) - Axiom logging service
- [Datadog Logging](https://docs.datadoghq.com/logs/) - Datadog logs
- [Better Stack](https://betterstack.com/logs) - Modern logging platform

### Background Processing
- [Python Threading](https://docs.python.org/3/library/threading.html) - Threading documentation
- [Queue Module](https://docs.python.org/3/library/queue.html) - Thread-safe queues
- [AsyncIO Logging](https://docs.python.org/3/library/asyncio-dev.html#logging) - Async logging patterns

---

*How do you handle PII in your logging? Found other patterns that work? I'd love to hear about your approach—connect with me on [LinkedIn](https://www.linkedin.com/in/albert-sikkema/).*
