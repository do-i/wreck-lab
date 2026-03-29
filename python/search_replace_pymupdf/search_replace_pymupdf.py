import argparse
import fitz  # PyMuPDF
import csv
import sys
from pathlib import Path


def hex_to_rgb(hex_code):
    """Converts #RRGGBB to an RGB tuple (0.0 to 1.0)."""
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) / 255.0 for i in (0, 2, 4))

def search_and_replace_text(input_path, output_dir, mapping_file):
    """
    Search and replace text in a PDF using PyMuPDF.

    Args:
        input_path (str): Path to the input PDF.
        output_path (str): Dir Path to save the redacted PDF.
        mapping_file (dict): Dictionary of {old_text: new_text}.
    """
    doc = fitz.open(input_path)

    # Read the mapping file
    mapping_path = Path(input_path).parent / Path(mapping_file)
    with open(mapping_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        replacements = [row for row in reader if len(row) == 2]

    for page in doc:
        # Search for each target text
        for old_text, new_text in replacements:
            # Search for the text in the page
            text_instances = page.search_for(old_text)

            # Replace each instance
            for inst in text_instances:

                page.add_redact_annot(inst, fill=(1, 1, 1)) # White background
                page.apply_redactions()

                page.insert_text(inst.bl, new_text, fontsize=8, color=(0, 0, 0))

                # Add red box (50% opacity)
                # 'fill' is the color, 'color' is the border color
                # 'fill_opacity' controls the transparency (0.0 to 1.0)
                page.draw_rect(inst,
                           color=hex_to_rgb("#0a6432"),
                           fill=hex_to_rgb("#0a6432"),
                           fill_opacity=0.4,
                           width=2)

        page.apply_redactions()

    # Save the redacted PDF
    output_path = Path(output_dir) / Path(input_path).name
    doc.save(output_path)
    doc.close()

    print(f"✅ Redacted PDF saved to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search and replace text in a PDF using PyMuPDF.")
    parser.add_argument("input_path", type=str, help="Path to the input PDF.")
    parser.add_argument("--output_path", type=str, default="redacted", help="Path to save the redacted PDF.")
    parser.add_argument("--mapping_path", type=str, default="pii.csv", help="Path to the mapping CSV.")
    args = parser.parse_args()

    search_and_replace_text(args.input_path, args.output_path, args.mapping_path)