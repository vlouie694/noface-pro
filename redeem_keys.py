import json
import os
from datetime import datetime
from typing import Dict, List, Optional

REDEEM_KEYS_FILE = 'data/redeem_keys.json'
MAX_PROFILES_PER_KEY = 5


def ensure_data_directory():
    """Create data directory if it doesn't exist"""
    os.makedirs('data', exist_ok=True)


def load_redeem_keys() -> Dict:
    """Load redeem keys from file"""
    ensure_data_directory()
    if os.path.exists(REDEEM_KEYS_FILE):
        with open(REDEEM_KEYS_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_redeem_keys(keys: Dict):
    """Save redeem keys to file"""
    ensure_data_directory()
    with open(REDEEM_KEYS_FILE, 'w') as f:
        json.dump(keys, f, indent=2)


def create_redeem_key(key: str) -> bool:
    """Create a new redeem key"""
    keys = load_redeem_keys()
    if key in keys:
        return False
    keys[key] = {
        'created_at': datetime.now().isoformat(),
        'profiles_generated': 0,
        'max_profiles': MAX_PROFILES_PER_KEY,
        'profiles': []
    }
    save_redeem_keys(keys)
    return True


def validate_redeem_key(key: str) -> bool:
    """Check if redeem key is valid and has remaining profiles"""
    keys = load_redeem_keys()
    if key not in keys:
        return False
    return keys[key]['profiles_generated'] < keys[key]['max_profiles']


def get_remaining_profiles(key: str) -> int:
    """Get remaining profiles for a redeem key"""
    keys = load_redeem_keys()
    if key not in keys:
        return 0
    key_data = keys[key]
    return key_data['max_profiles'] - key_data['profiles_generated']


def add_profile_to_key(key: str, profile: Dict) -> bool:
    """Add a generated profile to a redeem key"""
    keys = load_redeem_keys()
    if key not in keys:
        return False
    
    if keys[key]['profiles_generated'] >= keys[key]['max_profiles']:
        return False
    
    keys[key]['profiles'].append(profile)
    keys[key]['profiles_generated'] += 1
    save_redeem_keys(keys)
    return True


def get_profiles_for_key(key: str) -> List[Dict]:
    """Get all profiles associated with a redeem key"""
    keys = load_redeem_keys()
    if key not in keys:
        return []
    return keys[key]['profiles']
