from datetime import datetime
from typing import Dict, Optional
import re

from main import ProfileNumberGenerator
from utils import is_valid_number
from luhn_algorithm import calculate_luhn_check_digit


class ProfileGenerator:
    """Generate complete profiles with Profile Number, DOB, and State"""
    
    US_STATES = {
        'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
        'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
        'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
        'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
        'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
        'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
        'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
        'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
        'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
        'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
        'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
        'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
        'WI': 'Wisconsin', 'WY': 'Wyoming'
    }
    
    def __init__(self):
        self.profile_gen = ProfileNumberGenerator()
    
    @staticmethod
    def normalize_state(state_input: str) -> Optional[str]:
        """
        Normalize state input to 2-letter abbreviation
        Accepts: 2-letter code or full state name
        Returns: 2-letter code or None if invalid
        """
        state_input = state_input.strip().upper()
        
        if len(state_input) == 2 and state_input in ProfileGenerator.US_STATES:
            return state_input
        
        for code, name in ProfileGenerator.US_STATES.items():
            if name.upper() == state_input:
                return code
        
        return None
    
    @staticmethod
    def parse_dob(dob_input: str) -> Optional[str]:
        """
        Parse DOB in any common format and return standardized format (MM/DD/YYYY)
        """
        dob_input = dob_input.strip()
        cleaned = re.sub(r'[/-]', '', dob_input)
        
        formats_to_try = [
            '%m%d%Y',
            '%m%d%y',
            '%d%m%Y',
            '%d%m%y',
        ]
        
        for fmt in formats_to_try:
            try:
                date_obj = datetime.strptime(cleaned, fmt)
                return date_obj.strftime('%m/%d/%Y')
            except ValueError:
                continue
        
        for separator in ['/', '-']:
            parts = dob_input.split(separator)
            if len(parts) == 3:
                try:
                    if len(parts[2]) == 4:
                        month, day, year = int(parts[0]), int(parts[1]), int(parts[2])
                        if 1 <= month <= 12 and 1 <= day <= 31:
                            return f"{month:02d}/{day:02d}/{year}"
                    elif len(parts[0]) == 4:
                        year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
                        if 1 <= month <= 12 and 1 <= day <= 31:
                            return f"{month:02d}/{day:02d}/{year}"
                except (ValueError, IndexError):
                    continue
        
        return None
    
    def generate_profile(self, dob: str, state: str) -> Optional[Dict]:
        """
        Generate a complete profile with Profile Number, DOB, and State
        """
        normalized_state = self.normalize_state(state)
        if not normalized_state:
            return None
        
        normalized_dob = self.parse_dob(dob)
        if not normalized_dob:
            return None
        
        profile_number = self.profile_gen.generate_unique_random_profile_number()
        
        if not is_valid_number(profile_number, calculate_luhn_check_digit):
            return None
        
        return {
            'profile_number': profile_number,
            'dob': normalized_dob,
            'state': normalized_state,
            'state_full': self.US_STATES[normalized_state],
            'generated_at': datetime.now().isoformat()
        }
    
    @staticmethod
    def format_profile_display(profile: Dict) -> str:
        """Format profile for display"""
        return (
            f"✅ **Profile Generated**\n\n"
            f"Profile Number: `{profile['profile_number']}`\n"
            f"DOB: `{profile['dob']}`\n"
            f"State: {profile['state']} ({profile['state_full']})\n"
            f"Generated: {profile['generated_at']}"
        )
