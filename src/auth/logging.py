"""
Audit logging module.

Handles security event logging for authentication.
"""

import logging
from datetime import datetime

from src.auth.config import PermissionLevel

# Configure auth logger
logger = logging.getLogger("auth")
logger.setLevel(logging.INFO)

# Memory handler for UI display
log_buffer = []


class ListHandler(logging.Handler):
    """Handler that stores log records in a list."""

    def emit(self, record):
        log_entry = self.format(record)
        log_buffer.append(log_entry)
        # Keep only last 1000 logs
        if len(log_buffer) > 1000:
            log_buffer.pop(0)


# Add handlers if not already configured
if not logger.handlers:
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(console_handler)

    # List handler for UI
    list_handler = ListHandler()
    list_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(list_handler)


def get_recent_logs(limit: int = 50) -> list[str]:
    """Get recent log entries."""
    return log_buffer[-limit:]


def log_auth_event(email: str, oid: str, permission: PermissionLevel) -> None:
    """
    Log successful authentication.

    Args:
        email: User's email address
        oid: User's Object ID
        permission: Assigned permission level
    """
    timestamp = datetime.now().isoformat()
    logger.info(
        f"AUTH_SUCCESS | timestamp={timestamp} | email={email} | "
        f"oid={oid} | permission={permission.name}"
    )


def log_auth_failure(reason: str) -> None:
    """
    Log authentication failure without sensitive details.

    Args:
        reason: Generic reason for failure (no sensitive data)
    """
    timestamp = datetime.now().isoformat()
    logger.warning(f"AUTH_FAILURE | timestamp={timestamp} | reason={reason}")


def log_logout(email: str) -> None:
    """
    Log user logout.

    Args:
        email: User's email address
    """
    timestamp = datetime.now().isoformat()
    logger.info(f"LOGOUT | timestamp={timestamp} | email={email}")


def log_access_denied(user_oid: str, resource: str, required: PermissionLevel) -> None:
    """
    Log access denial.

    Args:
        user_oid: User's Object ID
        resource: Requested resource identifier
        required: Required permission level
    """
    timestamp = datetime.now().isoformat()
    logger.warning(
        f"ACCESS_DENIED | timestamp={timestamp} | oid={user_oid} | "
        f"resource={resource} | required={required.name}"
    )
