
# Conference Deadline Calendar Generator

This utility generates a weekly calendar PDF showing countdown to conference submission deadlines. It's particularly useful for tracking paper submission deadlines with proper timezone handling.

## Features

- Generates a weekly calendar view from current date to the deadline
- Shows countdown in days and weeks to the deadline
- Properly handles AoE (Anywhere on Earth) deadlines and converts them to IST
- Supports both abstract and full paper deadlines
- Highlights current date and deadline dates
- Generates a PDF named after the conference

## Requirements

- Python 3.6 or higher
- Required packages:
  - reportlab
  - zoneinfo

Install required packages:
```bash
pip install reportlab
```

## Usage

Basic usage with full paper deadline:
```bash
python conference_countdown.py "CONFERENCE_NAME" --full-paper YYYY-MM-DD
```

With both abstract and full paper deadlines:
```bash
python conference_countdown.py "CONFERENCE_NAME" --full-paper YYYY-MM-DD --abstract YYYY-MM-DD
```

### Arguments

- `CONFERENCE_NAME`: Name of the conference (required)
- `--full-paper`: Full paper submission deadline in YYYY-MM-DD format (required)
- `--abstract`: Abstract submission deadline in YYYY-MM-DD format (optional)

### Timezone Handling

The script handles deadlines in the following way:
- Input dates are considered as AoE (Anywhere on Earth, UTC-12) deadlines
- These are automatically converted to IST (UTC+5:30)
- For example:
  - If deadline is 2025-08-01 AoE (23:59:59 UTC-12)
  - It will be converted to 2025-08-02 17:29:59 IST

### Output

- Generates a PDF file named `{CONFERENCE_NAME}_countdown.pdf`
- The calendar shows:
  - Current date highlighted in orange
  - Abstract deadline (if provided) with exact IST time
  - Full paper deadline with exact IST time
  - Countdown in days to the deadline
  - Week countdown (W0, W1, etc.) to the deadline

## Examples

1. Generate calendar for AAAI with both deadlines:
```bash
python conference_countdown.py "AAAI" --full-paper 2025-08-01 --abstract 2025-07-25
```

2. Generate calendar for ICML with only full paper deadline:
```bash
python conference_countdown.py "ICML" --full-paper 2025-06-15
```

## Notes

- All dates should be in YYYY-MM-DD format
- The calendar will show dates from today until the latest deadline
- The generated PDF will be named after the conference (e.g., "AAAI_countdown.pdf")
- Special characters in conference names will be replaced with underscores in the filename
