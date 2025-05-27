import argparse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A6
from reportlab.lib.units import inch
import re

def create_hour_grid_pdf(filename="hour_grid.pdf", heading_text="Hourly Grid", grid_size=20, cell_hour_value=0.5):
    """
    Generates a PDF with an N x N grid representing hours, with a header row on top.
    The page size is A6 (palm size). All N*N cells are numbered sequentially.
    Borders are solid black. Reverted text spacing and centering.
    Default filename is derived from heading_text if not specified via command line.
    """
    c = canvas.Canvas(filename, pagesize=A6)
    page_width, page_height = A6

    # Margins
    margin = 0.5 * inch
    
    # Usable area
    usable_width = page_width - 2 * margin
    
    grid_structure_top_y_abs = page_height - margin
    grid_render_area_height = grid_structure_top_y_abs - margin
    grid_render_area_width = usable_width

    data_rows = grid_size
    data_cols = grid_size
    layout_total_rows = data_rows + 1 

    cell_w, cell_h = 0, 0
    
    _cell_w_candidate = grid_render_area_width / data_cols
    _cell_h_candidate_if_square = _cell_w_candidate
    
    if layout_total_rows * _cell_h_candidate_if_square <= grid_render_area_height:
        cell_w = _cell_w_candidate
        cell_h = _cell_h_candidate_if_square
    else:
        _cell_h_candidate = grid_render_area_height / layout_total_rows
        _cell_w_candidate_if_square = _cell_h_candidate
        cell_h = _cell_h_candidate
        cell_w = _cell_w_candidate_if_square
        
    actual_grid_content_width = data_cols * cell_w
    actual_grid_content_height = layout_total_rows * cell_h
    
    grid_offset_x = (grid_render_area_width - actual_grid_content_width) / 2
    grid_offset_y = (grid_render_area_height - actual_grid_content_height) / 2

    grid_final_start_x = margin + grid_offset_x
    grid_final_top_y_coord = grid_structure_top_y_abs - grid_offset_y

    # 1. Draw Header Row
    header_font_size = max(min(cell_h * 0.35, 10), 5) # Reverted font size
    c.setFont("Helvetica-Bold", header_font_size)
    
    header_cell_bl_x = grid_final_start_x
    header_cell_bl_y = grid_final_top_y_coord - cell_h
    header_cell_width = data_cols * cell_w
    
    c.setStrokeColorRGB(0, 0, 0) # Black border
    c.rect(header_cell_bl_x, header_cell_bl_y, header_cell_width, cell_h, stroke=1, fill=0)
    
    c.setFillColorRGB(0,0,0) 
    text_width_header = c.stringWidth(heading_text, "Helvetica-Bold", header_font_size)
    
    text_x_header = header_cell_bl_x + (header_cell_width - text_width_header) / 2 # Reverted centering
    text_y_header = header_cell_bl_y + (cell_h - header_font_size) / 2 + (header_font_size * 0.15) # Reverted centering

    if text_y_header < header_cell_bl_y + 2 : text_y_header = header_cell_bl_y + 2
    c.drawString(text_x_header, text_y_header, heading_text)

    # 2. Draw Data Grid and Fill Numbers
    current_hour_value = 0.0
    cells_to_fill = data_rows * data_cols
    cells_filled_count = 0
    font_size_cell_text = max(min(cell_h * 0.3, 7), 4) # Reverted font size

    data_grid_area_top_y = grid_final_top_y_coord - cell_h

    for r in range(data_rows):
        for col in range(data_cols):
            cell_x_bl = grid_final_start_x + col * cell_w
            cell_y_bl = data_grid_area_top_y - (r + 1) * cell_h

            c.setStrokeColorRGB(0, 0, 0) # Black border
            c.rect(cell_x_bl, cell_y_bl, cell_w, cell_h, stroke=1, fill=0)

            if cells_filled_count < cells_to_fill:
                current_hour_value += cell_hour_value
                text_content = f"{current_hour_value:.1f}"
                
                c.setFillColorRGB(0,0,0)
                c.setFont("Helvetica", font_size_cell_text)
                text_width_cell = c.stringWidth(text_content, "Helvetica", font_size_cell_text)
                
                text_x = cell_x_bl + (cell_w - text_width_cell) / 2 # Reverted centering
                text_y = cell_y_bl + (cell_h - font_size_cell_text) / 2 + (font_size_cell_text * 0.1) # Reverted centering
                
                if text_y < cell_y_bl + 1: text_y = cell_y_bl + 1
                c.drawString(text_x, text_y, text_content)
                cells_filled_count += 1
    
    c.save()
    total_hours_represented = cells_filled_count * cell_hour_value
    print(f"PDF '{filename}' (A6 size) created successfully.")
    print(f"Page Size: A6 ({A6[0]}pt x {A6[1]}pt approx. 4.1in x 5.8in)")
    print(f"Header Text: '{heading_text}'")
    print(f"Data grid dimensions: {data_rows} rows x {data_cols} cols.")
    print(f"Cell size (for data and header): {cell_w:.2f}pt width x {cell_h:.2f}pt height.")
    print(f"Cells numbered: {cells_filled_count} (representing {total_hours_represented:.1f}hrs at {cell_hour_value}hr/cell).")
    print(f"Note: Font sizes reverted. Header font: ~{header_font_size:.1f}pt, Cell font: ~{font_size_cell_text:.1f}pt.")
    print("Borders are black. Text spacing and centering reverted. Default filename derived from heading.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a PDF hour grid with a header row on an A6 (palm size) page.")
    parser.add_argument("heading", type=str, help="The text for the header row (also used for default filename).")
    parser.add_argument("grid_size", type=int, help="The size of the data grid (e.g., 10 for a 10x10 grid).")
    parser.add_argument("--filename", type=str, default=None, help="Output PDF filename. If not provided, it's derived from the heading text (e.g., 'My Heading' -> 'My_Heading.pdf').")
    parser.add_argument("--cell_value", type=float, default=0.5, help="Hour value per cell (default: 0.5).")
    
    args = parser.parse_args()

    actual_filename = args.filename
    if actual_filename is None:
        # Generate filename from heading
        # Replace spaces with underscores
        safe_heading = args.heading.replace(" ", "_")
        # Remove characters not suitable for filenames (keep alphanumeric, underscore, hyphen)
        safe_heading = re.sub(r'[^\w\-_]', '', safe_heading)
        # If the heading becomes empty after sanitization or is just underscores/hyphens, use a fallback
        if not safe_heading or all(c in '_-' for c in safe_heading):
            safe_heading = "hour_grid" 
        actual_filename = f"{safe_heading}.pdf"

    create_hour_grid_pdf(
        filename=actual_filename,
        heading_text=args.heading,
        grid_size=args.grid_size,
        cell_hour_value=args.cell_value
    )
