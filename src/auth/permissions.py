"""
Permission service module.

Maps group OIDs to permission levels and manages permission caching.
"""

from dataclasses import dataclass
from typing import List, Optional, TYPE_CHECKING

from src.auth.config import PermissionLevel, AuthConfig

if TYPE_CHECKING:
    from src.auth.graph_client import GraphAPIClient

SESSION_PERMISSION_KEY = "user_permission"


@dataclass
class UserPermission:
    """User permission data for session storage."""

    user_oid: str
    permission_level: PermissionLevel
    group_oids: List[str]

    def to_dict(self) -> dict:
        """Serialize for session storage."""
        return {
            "user_oid": self.user_oid,
            "permission_level": int(self.permission_level),
            "group_oids": self.group_oids,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "UserPermission":
        """Deserialize from session storage."""
        return cls(
            user_oid=data["user_oid"],
            permission_level=PermissionLevel(data["permission_level"]),
            group_oids=data["group_oids"],
        )


class PermissionService:
    """Service for managing user permissions."""

    def __init__(
        self, config: AuthConfig, graph_client: Optional["GraphAPIClient"] = None
    ):
        self.config = config
        self.graph_client = graph_client

    def map_groups_to_permission(self, group_oids: List[str]) -> PermissionLevel:
        """
        Map group OIDs to highest permission level.

        This iterates through the user's groups and checks if any match
        the mappings defined in secrets.toml. It returns the highest
        permission level found.

        Args:
            group_oids: List of group OIDs the user belongs to

        Returns:
            Highest permission level from matched groups, or VIEWER if none match
        """
        matched_levels = []

        for oid in group_oids:
            if oid in self.config.group_mappings:
                matched_levels.append(self.config.group_mappings[oid])

        return self.resolve_highest_permission(matched_levels)

    def resolve_highest_permission(
        self, levels: List[PermissionLevel]
    ) -> PermissionLevel:
        """
        Return the highest permission level from a list.

        Args:
            levels: List of permission levels

        Returns:
            Highest permission level, or VIEWER if list is empty
        """
        if not levels:
            return PermissionLevel.VIEWER
        return max(levels)

    async def determine_user_permission(self, user_oid: str) -> UserPermission:
        """
        Determine user's permission level from their groups.

        Args:
            user_oid: User's Object ID

        Returns:
            UserPermission with resolved permission level
        """
        group_oids = []

        if self.graph_client:
            try:
                group_oids = await self.graph_client.get_user_groups(user_oid)
            except Exception:
                # On failure, assign default VIEWER permission
                pass

        permission_level = self.map_groups_to_permission(group_oids)

        return UserPermission(
            user_oid=user_oid,
            permission_level=permission_level,
            group_oids=group_oids,
        )

    def cache_permission(self, permission: UserPermission) -> None:
        """Cache permission in session state."""
        import streamlit as st

        st.session_state[SESSION_PERMISSION_KEY] = permission.to_dict()

    def get_cached_permission(self) -> Optional[UserPermission]:
        """Get cached permission from session state."""
        import streamlit as st

        data = st.session_state.get(SESSION_PERMISSION_KEY)
        if data:
            return UserPermission.from_dict(data)
        return None


def has_permission(required: PermissionLevel) -> bool:
    """
    Check if current user has required permission level.

    Args:
        required: The minimum required permission level

    Returns:
        True if user has sufficient permission, False otherwise
    """
    current = get_current_permission()
    if current is None:
        return False
    return current >= required


def get_current_permission() -> Optional[PermissionLevel]:
    """
    Get current user's permission level from session state.

    Returns:
        Current permission level, or None if not set
    """
    import streamlit as st

    data = st.session_state.get(SESSION_PERMISSION_KEY)
    if data:
        return PermissionLevel(data["permission_level"])
    return None
