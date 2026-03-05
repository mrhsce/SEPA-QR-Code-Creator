"""
SEPA QR Code Creator
A user-friendly GUI application to generate SEPA QR codes (BCD format)
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import qrcode
import re


class PaymentQRCodeCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("SEPA QR Code Creator")
        self.root.geometry("800x750")
        self.root.resizable(True, True)

        self.qr_image_tk = None
        self.current_qr_image = None

        # All fields data (hidden from UI but used in QR code)
        self.all_fields = {
            "IBAN": "",
            "BIC": "",
            "Name": "",
            "Amount": "",
            "Purpose": "",
            "Structured Reference": "",
            "Unstructured Remittance": "",
            "Info": ""
        }

        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title = ttk.Label(main_frame, text="SEPA QR Code Generator (BCD Format)",
                         font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=10)

        # Payment Information section - Only visible fields
        payment_frame = ttk.LabelFrame(main_frame, text="Payment Information", padding="10")
        payment_frame.grid(row=1, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))

        # Visible input fields with paste buttons
        self.fields = {}
        row = 0

        visible_field_configs = [
            ("IBAN", "Required", True),
            ("BIC", "Optional", False),
            ("Name", "Required", True),
            ("Amount", "Optional (€)", False),
            ("Unstructured Remittance", "Optional", False),
        ]

        for field_name, requirement, is_required in visible_field_configs:
            # Label with requirement indicator
            label_text = f"{field_name} ({requirement})"
            ttk.Label(payment_frame, text=label_text, font=("Arial", 10)).grid(
                row=row, column=0, sticky=tk.W, pady=5
            )

            # Entry field
            entry = ttk.Entry(payment_frame, width=40)
            entry.grid(row=row, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

            # Paste button
            paste_btn = ttk.Button(
                payment_frame,
                text="Paste",
                command=lambda e=entry, f=field_name: self.paste_from_clipboard(e, f)
            )
            paste_btn.grid(row=row, column=2, padx=5, pady=5)

            self.fields[field_name] = {
                "entry": entry,
                "required": is_required
            }
            row += 1

        payment_frame.columnconfigure(1, weight=1)

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=15, sticky=(tk.W, tk.E))

        # Generate button
        generate_btn = ttk.Button(
            button_frame,
            text="Generate QR Code",
            command=self.generate_qr_code
        )
        generate_btn.pack(side=tk.LEFT, padx=5)

        # Reset button
        reset_btn = ttk.Button(
            button_frame,
            text="Reset",
            command=self.reset_fields
        )
        reset_btn.pack(side=tk.LEFT, padx=5)

        # Save button (initially disabled)
        self.save_btn = ttk.Button(
            button_frame,
            text="Save QR Code",
            command=self.save_qr_code,
            state=tk.DISABLED
        )
        self.save_btn.pack(side=tk.LEFT, padx=5)

        # QR Code display frame
        qr_frame = ttk.LabelFrame(main_frame, text="Generated QR Code", padding="10")
        qr_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

        # QR Code image label
        self.qr_label = ttk.Label(qr_frame, background="white", relief=tk.SUNKEN)
        self.qr_label.pack(padx=10, pady=10)

        # Configure grid weights for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

    def paste_from_clipboard(self, entry_widget, field_name):
        """Paste content from clipboard to the entry field and clean it"""
        try:
            clipboard_content = self.root.clipboard_get()

            # Clean up: Remove leading/trailing whitespace
            cleaned_content = clipboard_content.strip()

            # Remove all trailing non-alphanumeric characters
            # Keep alphanumeric, spaces, hyphens, dots, @, +, and / symbols
            while cleaned_content and not cleaned_content[-1].isalnum() and cleaned_content[-1] not in ' -.@+/':
                cleaned_content = cleaned_content[:-1]

            # Remove trailing whitespace again
            cleaned_content = cleaned_content.rstrip()

            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, cleaned_content)
        except tk.TclError:
            messagebox.showwarning("Clipboard Error", "Could not read from clipboard")

    def validate_inputs(self):
        """Validate required fields"""
        errors = []

        for field_name, field_data in self.fields.items():
            value = field_data["entry"].get().strip()

            if field_data["required"] and not value:
                errors.append(f"{field_name} is required")

        # Validate IBAN format
        iban = self.fields["IBAN"]["entry"].get().strip()
        if iban and not self.validate_iban(iban):
            errors.append("IBAN format appears invalid")

        # Validate amount if provided
        amount = self.fields["Amount"]["entry"].get().strip()
        if amount:
            try:
                float_amount = float(amount.replace(",", "."))
                if float_amount <= 0:
                    errors.append("Amount must be greater than 0")
            except ValueError:
                errors.append("Amount must be a valid number")

        return errors

    def validate_iban(self, iban):
        """Basic IBAN validation"""
        iban = iban.replace(" ", "").upper()
        # Check format: 2 letters (country), 2 digits (check digits), then alphanumeric
        return bool(re.match(r"^[A-Z]{2}[0-9]{2}[A-Z0-9]{1,30}$", iban))

    def generate_qr_code(self):
        """Generate the QR code using SEPA BCD format"""
        errors = self.validate_inputs()

        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return

        try:
            # Collect visible data from UI
            iban = self.fields["IBAN"]["entry"].get().strip()
            bic = self.fields["BIC"]["entry"].get().strip()
            name = self.fields["Name"]["entry"].get().strip()
            amount = self.fields["Amount"]["entry"].get().strip()
            unstructured_rem = self.fields["Unstructured Remittance"]["entry"].get().strip()

            # Build SEPA QR code data (BCD format - FULL STRUCTURE)
            # Line 1-4: Standard header
            # Line 5: BIC
            # Line 6: Name
            # Line 7: IBAN
            # Line 8: Amount
            # Line 9: Purpose (empty)
            # Line 10: Structured reference (empty)
            # Line 11: Unstructured remittance
            # Line 12: Info (empty)

            qr_lines = [
                "BCD",                              # Line 1: Service tag
                "002",                              # Line 2: Version
                "1",                                # Line 3: Encoding (UTF-8)
                "SCT",                              # Line 4: Identification
                bic if bic else "",                 # Line 5: BIC
                name,                               # Line 6: Beneficiary name
                iban.replace(" ", "").upper(),      # Line 7: IBAN
                amount if amount else "",           # Line 8: Amount
                "",                                 # Line 9: Purpose (always empty)
                "",                                 # Line 10: Structured reference (always empty)
                unstructured_rem if unstructured_rem else "",  # Line 11: Unstructured remittance
                ""                                  # Line 12: Info (always empty)
            ]

            qr_data = "\n".join(qr_lines)

            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)

            # Create PIL image
            img = qr.make_image(fill_color="black", back_color="white")
            self.current_qr_image = img

            # Display QR code in GUI
            self.display_qr_code(img)

            # Enable save button
            self.save_btn.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {str(e)}")

    def display_qr_code(self, img):
        """Display the QR code in the GUI"""
        # Resize image for display
        display_img = img.copy()

        # Maximum display size
        max_size = 400
        display_img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

        # Convert to PhotoImage
        self.qr_image_tk = ImageTk.PhotoImage(display_img)
        self.qr_label.config(image=self.qr_image_tk)

    def save_qr_code(self):
        """Save the QR code to a file"""
        if self.current_qr_image is None:
            messagebox.showwarning("No QR Code", "Generate a QR code first")
            return

        try:
            # Ask user for file location
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                initialfile="sepa_qr_code.png"
            )

            if file_path:
                self.current_qr_image.save(file_path)
                messagebox.showinfo("Saved", f"QR code saved successfully to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save QR code: {str(e)}")

    def reset_fields(self):
        """Clear all input fields"""
        for field_data in self.fields.values():
            field_data["entry"].delete(0, tk.END)

        self.qr_label.config(image="")
        self.qr_image_tk = None
        self.current_qr_image = None
        self.save_btn.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = PaymentQRCodeCreator(root)
    root.mainloop()

