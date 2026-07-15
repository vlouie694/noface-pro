import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

PROFILES_FILE = 'data/profiles.json'

logger = logging.getLogger(__name__)


def ensure_data_directory():
    """Create data directory if it doesn't exist"""
    os.makedirs('data', exist_ok=True)


def load_profiles() -> Dict:
    """Load all profiles from file"""
    ensure_data_directory()
    if os.path.exists(PROFILES_FILE):
        with open(PROFILES_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_profiles(profiles: Dict):
    """Save profiles to file"""
    ensure_data_directory()
    with open(PROFILES_FILE, 'w') as f:
        json.dump(profiles, f, indent=2)


def save_profile(user_id: int, profile: Dict) -> bool:
    """Save a user's generated profile"""
    profiles = load_profiles()
    
    if str(user_id) not in profiles:
        profiles[str(user_id)] = []
    
    profiles[str(user_id)].append(profile)
    save_profiles(profiles)
    return True


def get_user_profiles(user_id: int) -> List[Dict]:
    """Get all profiles for a user"""
    profiles = load_profiles()
    return profiles.get(str(user_id), [])


def get_latest_profile(user_id: int) -> Optional[Dict]:
    """Get the most recently generated profile for a user"""
    profiles = get_user_profiles(user_id)
    if profiles:
        return profiles[-1]
    return None


def clear_user_session(user_id: int):
    """Clear temporary session data for a user"""
    # This could be expanded to clear session files
    pass
