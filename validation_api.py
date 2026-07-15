"""
CPN Validation API Module
Validates CPN (Critical Profile Numbers) for format, Luhn check digit, and issuance status
"""

from typing import Dict, Union, Optional
import json
import os
from datetime import datetime

from constants import MIN_PROFILE_NUMBER, MAX_PROFILE_NUMBER, PROFILE_NUMBER_LENGTH
from luhn_algorithm import calculate_luhn_check_digit
from profile_storage import load_profiles


class CPNValidator:
    """Validates Critical Profile Numbers (CPNs) against multiple criteria"""
    
    def __init__(self):
        self.min_number = MIN_PROFILE_NUMBER
        self.max_number = MAX_PROFILE_NUMBER
        self.required_length = PROFILE_NUMBER_LENGTH
    
    def validate_format(self, cpn: Union[int, str]) -> Dict[str, Union[bool, str]]:
        """
        Validate CPN format
        
        Args:
            cpn (Union[int, str]): The CPN to validate
            
        Returns:
            Dict with format_valid (bool) and format_message (str)
        """
        try:
            cpn_str = str(cpn).strip()
            
            # Check if it's numeric
            if not cpn_str.isdigit():
                return {
                    "format_valid": False,
                    "format_message": "CPN must contain only digits"
                }
            
            # Check length
            if len(cpn_str) != self.required_length:
                return {
                    "format_valid": False,
                    "format_message": f"CPN must be exactly {self.required_length} digits long"
                }
            
            cpn_int = int(cpn_str)
            
            # Check range
            if not (self.min_number <= cpn_int <= self.max_number):
                return {
                    "format_valid": False,
                    "format_message": f"CPN must be between {self.min_number} and {self.max_number}"
                }
            
            return {
                "format_valid": True,
                "format_message": "CPN format is valid"
            }
            
        except Exception as e:
            return {
                "format_valid": False,
                "format_message": f"Invalid CPN format: {str(e)}"
            }
    
    def validate_luhn_check_digit(self, cpn: Union[int, str]) -> Dict[str, Union[bool, str]]:
        """
        Validate CPN Luhn check digit
        
        Args:
            cpn (Union[int, str]): The CPN to validate
            
        Returns:
            Dict with luhn_valid (bool) and luhn_message (str)
        """
        try:
            check_digit = calculate_luhn_check_digit(cpn)
            
            if check_digit == 0:
                return {
                    "luhn_valid": True,
                    "luhn_message": "Luhn check digit is valid"
                }
            else:
                return {
                    "luhn_valid": False,
                    "luhn_message": f"Luhn check digit validation failed (check digit: {check_digit})"
                }
        except Exception as e:
            return {
                "luhn_valid": False,
                "luhn_message": f"Error validating Luhn check digit: {str(e)}"
            }
    
    def check_issuance_status(self, cpn: Union[int, str]) -> Dict[str, Union[bool, str]]:
        """
        Check if CPN has been issued/used
        
        Args:
            cpn (Union[int, str]): The CPN to check
            
        Returns:
            Dict with is_issued (bool), issued_status (str), and issued_message (str)
        """
        try:
            cpn_int = int(str(cpn).strip())
            profiles = load_profiles()
            
            # Check all user profiles for this CPN
            for user_id, user_profiles in profiles.items():
                if isinstance(user_profiles, list):
                    for profile in user_profiles:
                        if isinstance(profile, dict) and profile.get('profile_number') == cpn_int:
                            return {
                                "is_issued": True,
                                "issued_status": "ISSUED",
                                "issued_message": f"CPN {cpn_int} has already been issued"
                            }
            
            return {
                "is_issued": False,
                "issued_status": "UNUSED",
                "issued_message": f"CPN {cpn_int} is unused and available"
            }
            
        except Exception as e:
            return {
                "is_issued": None,
                "issued_status": "UNKNOWN",
                "issued_message": f"Error checking issuance status: {str(e)}"
            }
    
    def validate_cpn(self, cpn: Union[int, str]) -> Dict:
        """
        Comprehensive CPN validation
        Validates format, Luhn check digit, and issuance status
        
        Args:
            cpn (Union[int, str]): The CPN to validate
            
        Returns:
            Dict containing all validation results and overall status
        """
        # Format validation
        format_result = self.validate_format(cpn)
        
        if not format_result["format_valid"]:
            return {
                "cpn": cpn,
                "valid": False,
                "status": "INVALID_FORMAT",
                "message": format_result["format_message"],
                "format_validation": format_result,
                "luhn_validation": None,
                "issuance_check": None,
                "timestamp": datetime.now().isoformat()
            }
        
        # Luhn check digit validation
        luhn_result = self.validate_luhn_check_digit(cpn)
        
        if not luhn_result["luhn_valid"]:
            return {
                "cpn": int(str(cpn).strip()),
                "valid": False,
                "status": "INVALID_LUHN",
                "message": luhn_result["luhn_message"],
                "format_validation": format_result,
                "luhn_validation": luhn_result,
                "issuance_check": None,
                "timestamp": datetime.now().isoformat()
            }
        
        # Issuance status check
        issuance_result = self.check_issuance_status(cpn)
        
        if issuance_result["is_issued"]:
            return {
                "cpn": int(str(cpn).strip()),
                "valid": False,
                "status": "ALREADY_ISSUED",
                "message": issuance_result["issued_message"],
                "format_validation": format_result,
                "luhn_validation": luhn_result,
                "issuance_check": issuance_result,
                "timestamp": datetime.now().isoformat()
            }
        
        # All validations passed
        return {
            "cpn": int(str(cpn).strip()),
            "valid": True,
            "status": "VALID_UNUSED",
            "message": "CPN is valid and unused",
            "format_validation": format_result,
            "luhn_validation": luhn_result,
            "issuance_check": issuance_result,
            "timestamp": datetime.now().isoformat()
        }


# Utility function for quick validation
def validate_cpn(cpn: Union[int, str]) -> Dict:
    """
    Quick validation function for CPN
    
    Args:
        cpn (Union[int, str]): The CPN to validate
        
    Returns:
        Dict with validation results
    """
    validator = CPNValidator()
    return validator.validate_cpn(cpn)
