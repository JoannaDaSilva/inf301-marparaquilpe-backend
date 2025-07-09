from supabase import create_client
from app.config import SUPABASE_URL, SUPABASE_KEY
import functools

# Use a lazy initialization pattern for serverless environments
@functools.lru_cache(maxsize=1)
def get_supabase_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

# Keep the original interface for backwards compatibility
def get_supabase():
    return get_supabase_client()

# For backward compatibility
supabase = get_supabase()
