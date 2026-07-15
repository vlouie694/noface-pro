# CPN Profile Generator Bot

A Telegram bot for generating secure customer proprietary network (CPN) profiles with first name, last name, date of birth, and state information.

## Features

- 🔑 **Redeem Key System**: Users can generate up to 5 profiles per redeem key
- 👤 **Profile Information**: Collect first name, last name, DOB, and state
- 🔢 **CPN Generation**: Generates valid CPNs using the Luhn algorithm
- ✅ **Validation**: Check if generated CPNs are unissued
- 📋 **Profile Management**: View all previously generated profiles

## Setup

### Prerequisites

- Python 3.8+
- Telegram Bot Token (from BotFather)

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export CPN_VALIDATION_API="https://your-api.com/validate-cpn"  # Optional
```

3. Run the bot:
```bash
python bot_main.py
```

## Usage

### Commands

| Command | Description | Example |
|---------|-------------|----------|
| `/start` | Show welcome message and available commands | `/start` |
| `/redeem` | Validate your redeem key | `/redeem ABC123XYZ` |
| `/firstname` | Set your first name | `/firstname John` |
| `/lastname` | Set your last name | `/lastname Doe` |
| `/dob` | Set your date of birth | `/dob 01/15/1990` |
| `/state` | Set your state | `/state CA` or `/state California` |
| `/profile` | Generate complete profile with CPN | `/profile` |
| `/validate` | Check if CPN is unissued | `/validate` |
| `/list` | List all your generated profiles | `/list` |
| `/help` | Show help message | `/help` |

### Workflow Example

```
1. /start
2. /redeem YOUR_REDEEM_KEY
3. /firstname John
4. /lastname Doe
5. /dob 01/15/1990
6. /state CA
7. /profile
8. /validate
9. /list
```

## DOB Format Support

The bot accepts dates in multiple formats:
- `01/15/1990`
- `01-15-1990`
- `1990-01-15`
- `01151990`

## State Support

Enter states as either:
- 2-letter abbreviation: `CA`, `NY`, `TX`
- Full state name: `California`, `New York`, `Texas`

## File Structure

```
.
├── bot_main.py              # Main bot entry point
├── bot_commands.py          # Command handlers
├── profile_generator.py     # Profile generation logic
├── profile_storage.py       # Profile persistence
├── redeem_keys.py          # Redeem key management
├── main.py                 # Original CPN generator
├── luhn_algorithm.py       # Luhn checksum validation
├── constants.py            # Constants
├── utils.py                # Utility functions
├── requirements.txt        # Dependencies
└── data/                   # Data directory (created at runtime)
    ├── profiles.json       # Stored profiles
    └── redeem_keys.json    # Redeem key data
```

## Redeem Key Management

Redeem keys are stored in `data/redeem_keys.json` with the following structure:

```json
{
  "ABC123XYZ": {
    "created_at": "2024-01-15T10:30:00",
    "profiles_generated": 2,
    "max_profiles": 5,
    "profiles": [...]
  }
}
```

## CPN Validation

The bot can validate CPNs against an external API. Set the `CPN_VALIDATION_API` environment variable to your validation endpoint.

Expected API response:
```json
{
  "unissued": true,
  "status": "UNISSUED"
}
```

## Security Notes

- Store redeem keys securely
- Keep `TELEGRAM_BOT_TOKEN` private
- Profile data is stored locally in JSON files
- Consider implementing database storage for production use

## Error Handling

The bot includes comprehensive error handling:
- Invalid redeem keys are rejected
- Incomplete profiles cannot be generated
- Invalid date formats are caught and reported
- Invalid states are rejected with suggestions

## License

MIT License - See LICENSE file for details
