import logging
import os
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

from bot_commands import (
    cmd_start,
    cmd_redeem,
    cmd_firstname,
    cmd_lastname,
    cmd_dob,
    cmd_state,
    cmd_profile,
    cmd_validate,
    cmd_list,
    cmd_help
)

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    """Start the bot with all commands"""
    # Get token from environment variable
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")
    
    # Create application
    application = Application.builder().token(token).build()
    
    # Add command handlers
    application.add_handler(CommandHandler('start', cmd_start))
    application.add_handler(CommandHandler('help', cmd_help))
    application.add_handler(CommandHandler('redeem', cmd_redeem))
    application.add_handler(CommandHandler('firstname', cmd_firstname))
    application.add_handler(CommandHandler('lastname', cmd_lastname))
    application.add_handler(CommandHandler('dob', cmd_dob))
    application.add_handler(CommandHandler('state', cmd_state))
    application.add_handler(CommandHandler('profile', cmd_profile))
    application.add_handler(CommandHandler('validate', cmd_validate))
    application.add_handler(CommandHandler('list', cmd_list))
    
    # Start the bot
    logger.info("Starting CPN Profile Generator Bot...")
    logger.info("Available commands:")
    logger.info("  /start - Show welcome message")
    logger.info("  /redeem <key> - Validate redeem key")
    logger.info("  /firstname <name> - Set first name")
    logger.info("  /lastname <name> - Set last name")
    logger.info("  /dob <date> - Set date of birth")
    logger.info("  /state <state> - Set state")
    logger.info("  /profile - Generate complete profile")
    logger.info("  /validate - Validate if CPN is unissued")
    logger.info("  /list - List all generated profiles")
    
    application.run_polling()


if __name__ == '__main__':
    main()
