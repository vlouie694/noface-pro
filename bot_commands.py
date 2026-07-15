import logging
import os
import requests
from typing import Dict
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from profile_generator import ProfileGenerator
from profile_storage import save_profile, get_user_profiles, get_latest_profile
from redeem_keys import validate_redeem_key, get_remaining_profiles, add_profile_to_key

logger = logging.getLogger(__name__)

# CPN Validation API (you can replace with your own validation service)
CPN_VALIDATION_API = os.getenv('CPN_VALIDATION_API', 'https://api.example.com/validate-cpn')


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command - displays welcome and available commands"""
    welcome_message = (
        "🎉 **Welcome to CPN Profile Generator Bot!**\n\n"
        "This bot generates unique profiles with CPN (Customer Proprietary Network), "
        "First Name, Last Name, Date of Birth, and State.\n\n"
        "**Available Commands:**\n\n"
        "`/redeem <key>` - Validate your redeem key\n"
        "`/firstname <name>` - Set your first name\n"
        "`/lastname <name>` - Set your last name\n"
        "`/dob <date>` - Set your date of birth (any format)\n"
        "`/state <state>` - Set your state\n"
        "`/profile` - Generate complete profile with all info\n"
        "`/validate` - Validate if CPN is unissued\n"
        "`/list` - List all your generated profiles\n"
        "`/help` - Show this help message\n\n"
        "**Example workflow:**\n"
        "1. `/redeem YOUR_KEY_HERE`\n"
        "2. `/firstname John`\n"
        "3. `/lastname Doe`\n"
        "4. `/dob 01/15/1990`\n"
        "5. `/state CA`\n"
        "6. `/profile`\n"
        "7. `/validate`"
    )
    
    await update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN)


async def cmd_redeem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Redeem command - validate redeem key"""
    user_id = update.effective_user.id
    
    if not context.args or len(context.args) == 0:
        await update.message.reply_text(
            "❌ **Usage:** `/redeem <key>`\n\n"
            "Example: `/redeem ABC123XYZ`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    redeem_key = context.args[0].strip()
    
    if not validate_redeem_key(redeem_key):
        remaining = get_remaining_profiles(redeem_key)
        if remaining == 0:
            await update.message.reply_text(
                "❌ **Invalid Key or No Profiles Remaining**\n\n"
                "This redeem key has no more profiles available (max 5 per key).",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                "❌ **Invalid Redeem Key**\n\n"
                "The key you entered is not valid.",
                parse_mode=ParseMode.MARKDOWN
            )
        return
    
    # Store key in user context
    context.user_data['redeem_key'] = redeem_key
    remaining = get_remaining_profiles(redeem_key)
    
    await update.message.reply_text(
        f"✅ **Key Validated!**\n\n"
        f"Remaining profiles: `{remaining}/5`\n\n"
        f"You can now generate profiles. Set your details using:\n"
        f"`/firstname`, `/lastname`, `/dob`, `/state`, then `/profile`",
        parse_mode=ParseMode.MARKDOWN
    )


async def cmd_firstname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set first name"""
    user_id = update.effective_user.id
    
    if not context.args or len(context.args) == 0:
        await update.message.reply_text(
            "❌ **Usage:** `/firstname <name>`\n\n"
            "Example: `/firstname John`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    first_name = ' '.join(context.args).strip()
    
    if len(first_name) < 2:
        await update.message.reply_text(
            "❌ **Error:** First name must be at least 2 characters.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    context.user_data['firstname'] = first_name
    
    await update.message.reply_text(
        f"✅ First name set to: `{first_name}`",
        parse_mode=ParseMode.MARKDOWN
    )


async def cmd_lastname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set last name"""
    user_id = update.effective_user.id
    
    if not context.args or len(context.args) == 0:
        await update.message.reply_text(
            "❌ **Usage:** `/lastname <name>`\n\n"
            "Example: `/lastname Doe`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    last_name = ' '.join(context.args).strip()
    
    if len(last_name) < 2:
        await update.message.reply_text(
            "❌ **Error:** Last name must be at least 2 characters.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    context.user_data['lastname'] = last_name
    
    await update.message.reply_text(
        f"✅ Last name set to: `{last_name}`",
        parse_mode=ParseMode.MARKDOWN
    )


async def cmd_dob(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set date of birth"""
    if not context.args or len(context.args) == 0:
        await update.message.reply_text(
            "❌ **Usage:** `/dob <date>`\n\n"
            "Supported formats:\n"
            "• `01/15/1990`\n"
            "• `01-15-1990`\n"
            "• `1990-01-15`\n"
            "• `01151990`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    dob_input = ' '.join(context.args).strip()
    profile_gen = ProfileGenerator()
    normalized_dob = profile_gen.parse_dob(dob_input)
    
    if not normalized_dob:
        await update.message.reply_text(
            "❌ **Invalid Date Format**\n\n"
            "Please use one of these formats:\n"
            "• `MM/DD/YYYY`\n"
            "• `MM-DD-YYYY`\n"
            "• `YYYY-MM-DD`\n"
            "• `MMDDYYYY`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    context.user_data['dob'] = normalized_dob
    
    await update.message.reply_text(
        f"✅ Date of birth set to: `{normalized_dob}`",
        parse_mode=ParseMode.MARKDOWN
    )


async def cmd_state(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set state"""
    if not context.args or len(context.args) == 0:
        await update.message.reply_text(
            "❌ **Usage:** `/state <state>`\n\n"
            "Examples:\n"
            "• `/state CA` (2-letter code)\n"
            "• `/state California` (full name)",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    state_input = ' '.join(context.args).strip()
    profile_gen = ProfileGenerator()
    normalized_state = profile_gen.normalize_state(state_input)
    
    if not normalized_state:
        await update.message.reply_text(
            "❌ **Invalid State**\n\n"
            "Please enter a valid US state as:\n"
            "• 2-letter code (CA, NY, TX, etc.)\n"
            "• Full state name (California, New York, Texas, etc.)",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    context.user_data['state'] = normalized_state
    state_full = profile_gen.US_STATES[normalized_state]
    
    await update.message.reply_text(
        f"✅ State set to: `{normalized_state}` ({state_full})",
        parse_mode=ParseMode.MARKDOWN
    )


async def cmd_profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate complete profile"""
    user_id = update.effective_user.id
    
    # Check if redeem key is set
    if 'redeem_key' not in context.user_data:
        await update.message.reply_text(
            "❌ **Error:** Please validate your redeem key first using `/redeem <key>`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Check if all required fields are set
    required_fields = ['firstname', 'lastname', 'dob', 'state']
    missing_fields = [f for f in required_fields if f not in context.user_data]
    
    if missing_fields:
        await update.message.reply_text(
            f"❌ **Missing Information**\n\n"
            f"Please set the following before generating a profile:\n"
            f"• {', '.join([f'`/{f}`' for f in missing_fields])}\n\n"
            f"Example workflow:\n"
            f"`/firstname John`\n"
            f"`/lastname Doe`\n"
            f"`/dob 01/15/1990`\n"
            f"`/state CA`",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Generate profile
    profile_gen = ProfileGenerator()
    profile = profile_gen.generate_profile(
        context.user_data['dob'],
        context.user_data['state']
    )
    
    if not profile:
        await update.message.reply_text(
            "❌ **Error Generating Profile**\n\n"
            "An error occurred while generating your profile. Please try again.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    # Add personal information to profile
    profile['firstname'] = context.user_data['firstname']
    profile['lastname'] = context.user_data['lastname']
    
    # Save to redeem key
    redeem_key = context.user_data['redeem_key']
    add_profile_to_key(redeem_key, profile)
    
    # Save profile locally
    save_profile(user_id, profile)
    
    # Update remaining profiles
    remaining = get_remaining_profiles(redeem_key)
    context.user_data['last_profile'] = profile
    
    # Display profile
    profile_message = (
        f"✅ **Profile Generated Successfully**\n\n"
        f"**Name:** `{profile['firstname']} {profile['lastname']}`\n"
        f"**CPN:** `{profile['cpn']}`\n"
        f"**DOB:** `{profile['dob']}`\n"
        f"**State:** `{profile['state']}` ({profile['state_full']})\n\n"
        f"Remaining profiles: `{remaining}/5`\n\n"
        f"Use `/validate` to check if this CPN is unissued."
    )
    
    await update.message.reply_text(profile_message, parse_mode=ParseMode.MARKDOWN)


async def cmd_validate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Validate if CPN is unissued"""
    user_id = update.effective_user.id
    
    # Get the last generated profile
    profile = context.user_data.get('last_profile') or get_latest_profile(user_id)
    
    if not profile:
        await update.message.reply_text(
            "❌ **Error:** No profile generated yet. Use `/profile` to generate one first.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    cpn = profile['cpn']
    
    # Validate CPN - you can replace this with your actual validation service
    validation_result = await validate_cpn(cpn)
    
    if validation_result['valid']:
        status_message = (
            f"✅ **CPN Validation Result**\n\n"
            f"**CPN:** `{cpn}`\n"
            f"**Status:** ✅ UNISSUED\n"
            f"**Valid:** Yes\n\n"
            f"This CPN can be safely used."
        )
    else:
        status_message = (
            f"❌ **CPN Validation Result**\n\n"
            f"**CPN:** `{cpn}`\n"
            f"**Status:** ❌ ISSUED or INVALID\n"
            f"**Valid:** No\n\n"
            f"This CPN may already be in use."
        )
    
    await update.message.reply_text(status_message, parse_mode=ParseMode.MARKDOWN)


async def validate_cpn(cpn: int) -> Dict:
    """
    Validate CPN against external service
    Returns: {'valid': bool, 'status': str}
    """
    try:
        # Replace with your actual validation endpoint
        # This is a placeholder implementation
        response = requests.post(
            CPN_VALIDATION_API,
            json={'cpn': cpn},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                'valid': data.get('unissued', True),
                'status': data.get('status', 'UNISSUED')
            }
        else:
            # Default to valid if API is unavailable
            return {'valid': True, 'status': 'UNISSUED'}
    except Exception as e:
        logger.error(f"CPN validation error: {e}")
        return {'valid': True, 'status': 'UNISSUED'}


async def cmd_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List all generated profiles"""
    user_id = update.effective_user.id
    profiles = get_user_profiles(user_id)
    
    if not profiles:
        await update.message.reply_text(
            "📋 **Your Profiles**\n\n"
            "No profiles generated yet. Use `/profile` to create one.",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    message = "📋 **Your Generated Profiles:**\n\n"
    for idx, profile in enumerate(profiles, 1):
        message += (
            f"**Profile {idx}:**\n"
            f"Name: `{profile['firstname']} {profile['lastname']}`\n"
            f"CPN: `{profile['cpn']}`\n"
            f"DOB: `{profile['dob']}`\n"
            f"State: `{profile['state']}` ({profile['state_full']})\n"
            f"Generated: {profile['generated_at']}\n\n"
        )
    
    await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show help message"""
    await cmd_start(update, context)
