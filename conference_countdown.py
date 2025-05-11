from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import argparse
import re

def parse_date(date_str):
    """Parse date string in YYYY-MM-DD format and convert AoE deadline to IST."""
    try:
        # Parse the date
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        # Create AoE deadline (23:59:59 AoE)
        aoe = timezone(timedelta(hours=-12))  # UTC-12
        aoe_deadline = datetime.combine(date, datetime.max.time()).replace(tzinfo=aoe)
        # Convert to IST (UTC+5:30)
        ist = ZoneInfo("Asia/Kolkata")
        ist_deadline = aoe_deadline.astimezone(ist)
        return ist_deadline
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format. Please use YYYY-MM-DD format.")

def sanitize_filename(name):
    """Convert event name to a valid filename."""
    # Replace spaces and special characters with underscores
    return re.sub(r'[^a-zA-Z0-9]', '_', name)

def generate_weekly_calendar(event_name, full_paper_date, abstract_date=None, current_date=None):
    styles = getSampleStyleSheet()
    
    # Set up timezone info
    ist = ZoneInfo("Asia/Kolkata")  # UTC+5:30
    
    # Get current date in IST
    current_date = current_date or datetime.now(ist).date()
    
    # Define single event with deadlines
    event = {
        "name": event_name,
        "deadlines": {
            "Full Paper": full_paper_date
        }
    }
    
    # Add abstract deadline if provided
    if abstract_date:
        event["deadlines"]["Abstract"] = abstract_date
    
    # Find the latest deadline
    max_target_date = max(dt.date() for dt in event["deadlines"].values())
    
    # Start from today instead of Monday of current week
    start_date = current_date
    
    # Calculate end date to include the last event
    end_date = max_target_date + timedelta(days=(6 - max_target_date.weekday()))
    
    # Generate all dates in calendar view
    delta = (end_date - start_date).days + 1
    all_dates = [start_date + timedelta(days=i) for i in range(delta)]
    
    # Group dates into weeks, starting from any day
    weeks = []
    current_week = []
    
    for date in all_dates:
        if not current_week and date.weekday() > 0:
            # Fill beginning of first week with empty strings
            current_week.extend([""] * date.weekday())
        
        current_week.append(date)
        
        if date.weekday() == 6:  # End of week (Sunday)
            # Only add the week if it has future dates
            has_future_dates = any(
                (not isinstance(d, str) and d >= current_date) 
                for d in current_week
            )
            if has_future_dates:
                weeks.append(current_week)
            current_week = []
    
    # Handle last partial week
    if current_week:
        # Only add the last week if it has future dates
        has_future_dates = any(
            (not isinstance(d, str) and d >= current_date) 
            for d in current_week
        )
        if has_future_dates:
            current_week.extend([""] * (7 - len(current_week)))
            weeks.append(current_week)

    # Create output filename using event name
    output_filename = f"{sanitize_filename(event_name)}_countdown.pdf"

    # Create PDF document with adjusted size based on number of weeks
    page_height = 30 + (len(weeks) + 1) * 100  # Header + weeks * height_per_week
    doc = SimpleDocTemplate(
        output_filename, 
        pagesize=(letter[0], min(page_height, letter[1])),  # Adjust height, but don't exceed letter size
        leftMargin=15,    # Smaller margins
        rightMargin=15,
        topMargin=20,
        bottomMargin=20
    )
    elements = []

    # Create calendar data with title
    calendar_data = []
    
    # Add title row with larger font and correct format
    title = Paragraph(
        f"""<para align="center">
            <font size="18" color="#2C3E50"><b>{event['name']}-{max_target_date.year}</b></font>
        </para>""",
        styles["Normal"]
    )
    calendar_data.append([title])

    # Add day headers
    header = ["Monday", "Tuesday", "Wednesday", "Thursday", 
            "Friday", "Saturday", "Sunday"]
    calendar_data.append(header)

    # Define colors for different deadline types
    deadline_colors = {
        "Abstract": '#3498DB',     # Light blue for abstract
        "Full Paper": '#2980B9'    # Dark blue for full paper
    }

    # Define background colors for target dates (lighter shades)
    deadline_bg_colors = {
        "Abstract": '#D6EAF8',    # Very light blue for abstract
        "Full Paper": '#D4E6F1'    # Light blue for full paper
    }

    for week in weeks:
        week_row = []
        for day in week:
            if day == "":
                week_row.append("")
                continue
                
            # Skip dates after the full paper deadline
            if event["deadlines"]["Full Paper"].date() < day:
                week_row.append("")
                continue

            cell_content = []
            
            # Show date in Day-Month-Year format with larger font
            if day == current_date:
                date_str = f"<font color='#E67E22' size='11'><b>{day.strftime('%d-%b-%Y')}</b></font>"
            else:
                date_str = f"<font size='11'><b>{day.strftime('%d-%b-%Y')}</b></font>"

            # Add date at the top
            cell_content.append(Paragraph(date_str, styles["Normal"]))
            
            # Check if this is an abstract deadline day
            is_abstract_day = ("Abstract" in event["deadlines"] and 
                             event["deadlines"]["Abstract"].date() == day and 
                             event["deadlines"]["Abstract"].date() >= current_date)

            # Process Abstract deadline - only show on the day
            if is_abstract_day:
                deadline_time = event["deadlines"]["Abstract"].strftime("%I:%M %p")
                cell_content.append(Paragraph(
                    f"<br/><font size='12' color='{deadline_colors['Abstract']}'>"
                    f"<b>⭐ Abstract ({deadline_time})</b></font>",
                    styles["Normal"]
                ))
            else:
                # Process Full Paper deadline - show countdown
                if event["deadlines"]["Full Paper"].date() >= current_date:
                    days_remaining = (event["deadlines"]["Full Paper"].date() - day).days
                    if day == event["deadlines"]["Full Paper"].date():
                        deadline_time = event["deadlines"]["Full Paper"].strftime("%I:%M %p")
                        cell_content.append(Paragraph(
                            f"<br/><font size='12' color='{deadline_colors['Full Paper']}'>"
                            f"<b>⭐ Full Paper ({deadline_time})</b></font>",
                            styles["Normal"]
                        ))
                    elif days_remaining > 0:
                        cell_content.append(Paragraph(
                            f"<br/><font size='28' color='{deadline_colors['Full Paper']}'>"
                            f"<b>{days_remaining}</b></font>",
                            styles["Normal"]
                        ))

                # Add week countdown box if there's a nearest deadline (not on abstract day)
                if not is_abstract_day:
                    days_until_target = (event["deadlines"]["Full Paper"].date() - day).days
                    if days_until_target >= 0:
                        weeks_remaining = days_until_target // 7
                        cell_content.insert(1, Paragraph(
                            f"""<font size='9' color='{deadline_colors['Full Paper']}'><b>W{weeks_remaining}</b></font>""",
                            styles["Normal"]
                        ))

            week_row.append(cell_content)
        
        # Only add the week if it has any content
        if any(cell != "" for cell in week_row):
            calendar_data.append(week_row)

    # Create and style table with adjusted dimensions
    table = Table(calendar_data, 
                 colWidths=[82]*7,
                 rowHeights=[40, 25] + [70]*(len(calendar_data)-2))  # Adjusted row heights

    table.setStyle(TableStyle([
        # Add span for title row
        ('SPAN', (0,0), (-1,0)),
        # Style for title
        ('BACKGROUND', (0,0), (-1,0), colors.white),
        # Style for day headers
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#2C3E50')),
        ('TEXTCOLOR', (0,1), (-1,1), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,0), 'MIDDLE'),
        ('VALIGN', (0,2), (-1,-1), 'TOP'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,1), (-1,1), 10),  # Header font size
        ('GRID', (0,0), (-1,-1), 0.25, colors.HexColor('#BDC3C7')),  # Thinner grid lines
        ('BACKGROUND', (0,2), (-1,-1), colors.HexColor('#ECF0F1')),
        ('ROWBACKGROUNDS', (0,2), (-1,-1), [
            colors.transparent, 
            colors.HexColor('#F8F9F9')
        ]),
        ('TOPPADDING', (0,2), (-1,-1), 2),    # Slightly increased top padding
        ('BOTTOMPADDING', (0,2), (-1,-1), 2),  # Slightly increased bottom padding
        ('LEFTPADDING', (0,0), (-1,-1), 3),    # Slightly increased left padding
        ('RIGHTPADDING', (0,0), (-1,-1), 3),   # Slightly increased right padding
    ]))

    # Add background colors for target dates
    for row_idx, week in enumerate(weeks):
        for col_idx, day in enumerate(week):
            for deadline_type, target_date in event["deadlines"].items():
                if target_date.date() == day and target_date.date() >= current_date:
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (col_idx, row_idx + 2), (col_idx, row_idx + 2), 
                         colors.HexColor(deadline_bg_colors[deadline_type]))
                    ]))

    elements.append(table)
    doc.build(elements)
    return output_filename

def main():
    parser = argparse.ArgumentParser(
        description='Generate a weekly calendar PDF for conference submission deadlines.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate calendar for AAAI with both abstract and full paper deadlines
  python calendar_plot.py "AAAI" --full-paper 2025-08-01 --abstract 2025-07-25

  # Generate calendar for a conference with only full paper deadline
  python calendar_plot.py "ICML" --full-paper 2025-06-15

Note: Dates should be in YYYY-MM-DD format. All deadlines are considered as AoE (Anywhere on Earth) 
and will be converted to IST (UTC+5:30). For example, a deadline of 2025-08-01 AoE means 
2025-08-02 17:29:59 IST.
        """
    )
    
    parser.add_argument('event_name', 
                      help='Name of the conference/event')
    
    parser.add_argument('--full-paper', 
                      type=parse_date,
                      required=True,
                      help='Full paper submission deadline (YYYY-MM-DD) in AoE timezone')
    
    parser.add_argument('--abstract',
                      type=parse_date,
                      help='Abstract submission deadline (YYYY-MM-DD) in AoE timezone')
    
    args = parser.parse_args()
    
    output_file = generate_weekly_calendar(
        event_name=args.event_name,
        full_paper_date=args.full_paper,
        abstract_date=args.abstract
    )
    print(f"Calendar generated: {output_file}")

if __name__ == "__main__":
    main()
