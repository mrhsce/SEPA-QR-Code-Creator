# SEPA QR Code Creator

A user-friendly GUI application to generate SEPA QR codes in BCD format compatible with most banking and payment apps.

## Features

- **Easy-to-use Interface**: Clean tkinter-based GUI with minimal, essential fields only
- **Clipboard Integration**: Paste buttons for each field to quickly populate data from clipboard
- **Automatic Cleanup**: Non-alphanumeric characters at the end of pasted text are automatically removed
- **Input Validation**: 
  - IBAN format validation
  - Amount validation (must be positive number)
  - Required fields enforcement
- **QR Code Generation**: Creates standard SEPA QR codes (BCD format) with full structure
- **Save Functionality**: Save generated QR codes as PNG files with custom naming
- **Reset Function**: Clear all fields and start over

## SEPA QR Code Format (BCD) - Full Structure

The application generates QR codes with the complete SEPA BCD format (12 lines):

```
BCD                                     # Line 1: Service tag
002                                     # Line 2: Version
1                                       # Line 3: Encoding (UTF-8)
SCT                                     # Line 4: Identification
{BIC}                                   # Line 5: BIC
{Name}                                  # Line 6: Beneficiary name
{IBAN}                                  # Line 7: IBAN
{Amount}                                # Line 8: Amount
(blank)                                 # Line 9: Purpose
(blank)                                 # Line 10: Structured reference
{Unstructured Remittance}              # Line 11: Message/Reference
(blank)                                 # Line 12: Info
```

**Example:**
```
BCD
002
1
SCT
PCHQBEBB
Inningscentrum
BE39679200229319
2.20


+++123456789+++

```

## Visible UI Fields (Minimal Interface)

Only 5 essential fields are shown in the UI:

| Field | Required | Description |
|-------|----------|-------------|
| **IBAN** | ✅ Yes | Beneficiary's International Bank Account Number |
| **BIC** | ❌ No | Beneficiary's Bank Identifier Code |
| **Name** | ✅ Yes | Beneficiary's name or company name |
| **Amount** | ❌ No | Payment amount in euros (e.g., 2.20) |
| **Unstructured Remittance** | ❌ No | Payment reference or message (e.g., `+++123456789+++`) |

**Hidden Fields** (always empty in QR code):
- Purpose (Line 9)
- Structured Reference (Line 10)
- Info (Line 12)

## Requirements

- Python 3.6+
- tkinter (usually included with Python)
- PIL/Pillow
- qrcode

## Installation

1. Clone or download this project
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Option 1: Double-click the launcher (Easiest) 🚀
Simply double-click the `run.sh` file to launch the application.

### Option 2: Run from terminal
```bash
./run.sh
```

### Option 3: Manual Python execution
```bash
python main.py
```

## Generating a SEPA QR Code

1. **Fill in the required payment details:**
   - **IBAN** - The beneficiary's account number
   - **Name** - The beneficiary's name or company name

2. **Optionally add:**
   - **BIC** - Bank Identifier Code
   - **Amount** - Payment amount in euros
   - **Unstructured Remittance** - Payment reference or message

3. **Use the "Paste" buttons** to quickly populate fields from clipboard
   - Non-alphanumeric characters at the end are automatically cleaned up
   - This prevents encoding errors from extra characters

4. **Click "Generate QR Code"** to create the QR code
   - The QR code displays instantly (no popup)
   - Full SEPA BCD format is generated (12 lines)

5. **Click "Save QR Code"** to export it as PNG
   - Choose your desired file location
   - Ready to print or share

6. **Scan with any SEPA-compatible banking app**
   - All details are pre-filled
   - Ready to process payment

## Clipboard Cleanup Feature

When you paste text using the "Paste" buttons, the application automatically:
- ✅ Removes leading and trailing whitespace
- ✅ Removes trailing non-alphanumeric characters
- ✅ Preserves hyphens, dots, @, +, and / symbols (needed for IBANs and references)
- ✅ Cleans up all trailing special characters in one pass

This is useful when copying from sources that might add extra characters.

## Compatibility

This format is compatible with banking and payment apps supporting SEPA transfers:
- ✅ Most European banking apps
- ✅ ING, ABN AMRO, Bunq, KBC, Argenta
- ✅ Wise, Revolut, N26
- ✅ Most SEPA-compatible payment apps

## License

Free to use and modify for personal or commercial purposes.



