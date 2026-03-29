
# PDF Text Search and Replace with PyMuPDF

This script allows you to search and replace text in a PDF file using the PyMuPDF library. It reads a CSV file containing the mapping of old text to new text and applies these replacements to the PDF.

## Prerequisites

- Python 3.x
- PyMuPDF
- CSV file with text replacements

## Installation

1. Clone this repository or download the script.
2. Install the required library using pip:
    ```sh
    pip install .
    ```

## Usage

1. Prepare a CSV file with two columns: the first column contains the text to be replaced, and the second column contains the new text.
2. Run the script with the following command:
    ```bash
    python search_replace_pymupdf.py <input_pdf_path> --output <output_directory> --mapping <mapping_csv_file>
    ```

### Command Line Arguments

- Path to the input PDF file.
- `--output`: Directory path to save the redacted PDF.
- `--mapping`: Path to the CSV file containing the text replacements.

### Example

```sh
python search_replace_pymupdf.py raw_data/confidencial.pdf --output redacted/output --mapping raw_data/pii.csv
```

## CSV File Format

The CSV file should have two columns:
- Column 1: Text to be replaced
- Column 2: New text

Example:
```csv
old text 1,new text 1
old text 2,new text 2
```
