# Profile Generator Bot

A Telegram bot for generating and managing user profiles with personal information.

## Features

- 🔑 **Redeem Key System**: Users can generate up to 5 profiles per redeem key
- 👤 **Profile Information**: Collect first name, last name, DOB, and state
- 🔢 **Profile Number Generation**: Generates valid profile numbers using the Luhn algorithm
- ✅ **Validation**: Validate profile numbers
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
export PROFILE_VALIDATION_API="https://your-api.com/validate-profile"  # Optional
```

3. Run the bot:
```bash
python bot_main.py
```

## Usage

### Commands

| Command | Description | Example |
|---------|-------------|----------|
| `/start` | Show welcome message | `/start` |
| `/redeem` | Validate your redeem key | `/redeem ABC123XYZ` |
| `/firstname` | Set your first name | `/firstname John` |
| `/lastname` | Set your last name | `/lastname Doe` |
| `/dob` | Set your date of birth | `/dob 01/15/1990` |
| `/state` | Set your state | `/state CA` or `/state California` |
| `/profile` | Generate profile | `/profile` |
| `/validate` | Validate profile | `/validate` |
| `/list` | List your profiles | `/list` |
| `/help` | Show help | `/help` |

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

- `01/15/1990`
- `01-15-1990`
- `1990-01-15`
- `01151990`

## State Support

- 2-letter abbreviation: `CA`, `NY`, `TX`
- Full state name: `California`, `New York`, `Texas`

## File Structure

```
.
├── bot_main.py
├── bot_commands.py
├── profile_generator.py
├── profile_storage.py
├── redeem_keys.py
├── main.py
├── luhn_algorithm.py
├── constants.py
├── utils.py
├── requirements.txt
└── data/
    ├── profiles.json
    └── redeem_keys.json
```

## Redeem Key Management

Redeem keys are stored in `data/redeem_keys.json`:

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
