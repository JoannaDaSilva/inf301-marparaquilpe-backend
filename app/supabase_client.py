from supabase import create_client
from app.config import SUPABASE_URL, SUPABASE_KEY
import functools
import httpx

# Configure httpx client with timeout and connection limits
def create_http_client():
    return httpx.Client(
        timeout=30.0,  # 30 second timeout
        limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
    )

# Use a lazy initialization pattern for serverless environments
@functools.lru_cache(maxsize=1)
def get_supabase_client():
    return create_client(
        SUPABASE_URL, 
        SUPABASE_KEY,
        options={
            "timeout": 30,
            "connection_timeout": 10,
            "read_timeout": 30,
            "write_timeout": 30
        }
    )

# Keep the original interface for backwards compatibility
def get_supabase():
    return get_supabase_client()

# For backward compatibility
supabase = get_supabase()
