from supabase import Client


class SupabaseRepository:

    def __init__(self, client: Client) -> None:
        self.client = client
