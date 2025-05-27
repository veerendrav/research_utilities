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

# Hour Challenge PDF Generator (`hour_challenge.py`)

This Python script generates a PDF document with a grid, typically used for tracking hours or tasks. The grid is palm-sized (A6 page format) and features a header row with a title, followed by a data grid where each cell is numbered sequentially.

## Prerequisites

1.  **Python 3**: Ensure you have Python 3 installed on your system.
2.  **ReportLab Library**: This script uses the ReportLab library to generate PDFs. If you don't have it installed, you can install it using pip:
    ```bash
    pip install reportlab
    ```

## How to Run

You can run the script from your command line terminal.

### Basic Usage

The script requires two positional arguments:
1.  `heading`: The text you want to display in the header row of the grid. This will also be used to generate the default PDF filename if not specified.
2.  `grid_size`: An integer specifying the dimensions of the data grid (e.g., `10` for a 10x10 grid).

**Example:**
```bash
python hour_challenge.py "My Daily Tasks" 10
```
This command will:
*   Create a PDF with the header "My Daily Tasks".
*   The data grid will be 10 rows by 10 columns.
*   Each cell in the data grid will be numbered sequentially, starting from 0.5 and incrementing by 0.5.
*   The output PDF filename will be automatically generated as `My_Daily_Tasks.pdf` (spaces replaced by underscores, special characters removed).

### Command-Line Options

You can customize the output using the following optional arguments:

*   `--filename <OUTPUT_FILENAME.pdf>`
    *   Specifies a custom name for the output PDF file.
    *   If not provided, the filename is derived from the `heading` text (e.g., "Project X" becomes `Project_X.pdf`).
    *   **Example:** `python hour_challenge.py "Sprint Goals" 15 --filename sprint_tracker.pdf`

*   `--cell_value <FLOAT_VALUE>`
    *   Sets the numerical increment for each cell in the data grid.
    *   Defaults to `0.5`.
    *   **Example:** `python hour_challenge.py "Quarterly Milestones" 20 --cell_value 1.0` (each cell will increment by 1.0)

### Detailed Examples

1.  **Generate a 5x5 grid for "Quick Wins", saved as `Quick_Wins.pdf`, with default 0.5hr cells:**
    ```bash
    python hour_challenge.py "Quick Wins" 5
    ```

2.  **Generate a 20x20 grid for "Long Term Project", saved as `long_project_plan.pdf`, with 0.25hr cells:**
    ```bash
    python hour_challenge.py "Long Term Project" 20 --filename long_project_plan.pdf --cell_value 0.25
    ```

3.  **Generate a 12x12 grid for "12 Week Challenge", saved as `12_Week_Challenge.pdf`, with cells representing 1 unit each:**
    ```bash
    python hour_challenge.py "12 Week Challenge" 12 --cell_value 1.0
    ```

## Output PDF Features

*   **Page Size**: A6 (105mm x 148mm, approximately 4.1in x 5.8in).
*   **Layout**:
    *   A header row spanning the width of the grid, containing the `heading` text.
    *   A data grid of `grid_size` x `grid_size` cells below the header.
*   **Cell Numbering**: Data cells are numbered sequentially, starting from `cell_value` and incrementing by `cell_value`.
*   **Styling**:
    *   Solid black borders for all cells.
    *   Text is dynamically sized to fit within cells, with font sizes adjusted for readability.
    *   Text is centered within cells.

## Script Location

Ensure `hour_challenge.py` is in your current directory when running the commands, or provide the full path to the script.
