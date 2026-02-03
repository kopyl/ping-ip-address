from supabase import create_client, Client
from tenacity import retry, stop_after_attempt, wait_exponential
from postgrest import APIResponse
import os
import datetime


SUPABASE_PROJECT_ID = os.getenv("SUPABASE_PROJECT_ID")
SUPABASE_URL = f"https://{SUPABASE_PROJECT_ID}.supabase.co"
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=10))
def send_get_last_status_request(ip_address: str, port: int) -> APIResponse:
    response = (
        supabase.table("ping_statuses")
        .select("status", "created_at")
        .eq("ip_address", ip_address)
        .eq("port", port)
        .order("created_at", desc=True).limit(1).execute()
    )
    return response


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=10))
def write_status(
    is_success: bool,
    ip_address: str,
    port: int,
    timestamp: datetime.datetime
) -> None:
    
    supabase.table("ping_statuses").insert({
        "ip_address": ip_address,
        "port": port,
        "status": is_success,
        "created_at": timestamp.isoformat()
    }).execute()


def get_last_status(ip_address: str, port: int) -> dict:
    response = send_get_last_status_request(ip_address, port)
    data = response.data
    if not data:
        return {
            "status": None,
            "timestamp": None
        }
    return {
        "status": data[0]["status"],
        "timestamp": datetime.datetime.fromisoformat(data[0]["created_at"])
    }