import re
from typing import Any, Dict


def redact_sensitive_data(data: Any) -> Any:
    """
    Recursively redacts sensitive information from data structures before logging.
    """
    if isinstance(data, dict):
        redacted = {}
        for key, value in data.items():
            # Redact keys that might contain sensitive info
            if any(sensitive in key.lower() for sensitive in [
                'password', 'api_key', 'token', 'secret', 'credential',
                'authorization', 'auth', 'app_password'
            ]):
                redacted[key] = "***REDACTED***"
            else:
                redacted[key] = redact_sensitive_data(value)
        return redacted
    
    elif isinstance(data, list):
        return [redact_sensitive_data(item) for item in data]
    
    elif isinstance(data, str):
        # Redact API keys in strings (pattern: alphanumeric strings > 20 chars)
        if len(data) > 20 and re.match(r'^[a-zA-Z0-9_-]+$', data):
            return f"{data[:4]}...{data[-4:]}"
        return data
    
    else:
        return data


def safe_log_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Returns a safe-to-log version of a dictionary with sensitive data redacted.
    """
    return redact_sensitive_data(data)
