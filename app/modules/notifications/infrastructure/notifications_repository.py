from datetime import datetime, timezone
from typing import Any

from fastapi import Depends
from supabase import AsyncClient

from app.db.supabase_client import get_admin_client

SELECT_FIELDS = """
    id,
    user_id,
    notification_id,
    is_read,
    read_at,
    created_at,
    notification:notifications (
        *
    )
"""


class NotificationsRepositorySupabase:
    def __init__(self, admin_client: AsyncClient = Depends(get_admin_client)) -> None:
        self.client = admin_client

    async def get_user_notifications(self, user_id: str, limit: int = 20, offset: int = 0) -> tuple[list[Any], int]:
        try:
            response = await (
                self.client.from_("user_notifications")
                .select(SELECT_FIELDS, count="exact")
                .eq("user_id", user_id)
                .order("created_at", desc=True, foreign_table="notifications")
                .range(offset, offset + limit - 1)
                .execute()
            )
            count = getattr(response, "count", None)
            if count is None:
                count = len(response.data or [])
            return response.data or [], count
        except Exception as e:
            print(f"Error fetching notifications: {e}")
            raise e

    async def get_user_notification(self, notification_id: int, user_id: str):
        try:
            response = await (
                self.client.from_("user_notifications")
                .select(SELECT_FIELDS)
                .eq("notification_id", notification_id)
                .eq("user_id", user_id)
                .execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching notification: {e}")
            raise e

    async def mark_as_read(self, notification_id: int, user_id: str):
        try:
            payload = {
                "is_read": True,
                "read_at": datetime.now(timezone.utc).isoformat(),
            }
            response = await (
                self.client.from_("user_notifications")
                .update(payload)
                .eq("notification_id", notification_id)
                .eq("user_id", user_id)
                .execute()
            )
            return response.data
        except Exception as e:
            print(f"Error marking notification as read: {e}")
            raise e
