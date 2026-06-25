import os
import re
import shutil
from datetime import datetime


# =====================================================
# Folder Utilities
# =====================================================

def create_folder(folder_path):
    """
    Create folder if it doesn't exist.
    """
    os.makedirs(folder_path, exist_ok=True)


def clear_folder(folder_path):
    """
    Delete all files inside a folder.
    """
    if not os.path.exists(folder_path):
        return

    for filename in os.listdir(folder_path):

        file_path = os.path.join(folder_path, filename)

        try:

            if os.path.isfile(file_path):
                os.remove(file_path)

            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

        except Exception as e:
            print(e)


# =====================================================
# File Utilities
# =====================================================

def allowed_file(filename):

    return "." in filename and \
           filename.lower().endswith(".pdf")


def get_file_size(file_path):

    size = os.path.getsize(file_path)

    return round(size / (1024 * 1024), 2)


# =====================================================
# String Utilities
# =====================================================

def clean_text(text):

    if text is None:
        return ""

    text = text.replace("\n", " ")

    text = text.replace("\t", " ")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def clean_amount(amount):

    if amount is None:
        return ""

    amount = amount.replace(",", "")

    amount = amount.replace("₹", "")

    amount = amount.strip()

    return amount


# =====================================================
# Date Utilities
# =====================================================

def format_date(date_string):

    if not date_string:
        return ""

    formats = [

        "%d-%m-%Y",
        "%d/%m/%Y",
        "%d-%b-%y",
        "%d-%b-%Y",
        "%d/%b/%Y",
        "%d.%m.%Y"

    ]

    for fmt in formats:

        try:

            dt = datetime.strptime(date_string.strip(), fmt)

            return dt.strftime("%d-%m-%Y")

        except:

            pass

    return date_string


# =====================================================
# Number Extraction
# =====================================================

def find_first_amount(text):

    matches = re.findall(

        r"\d[\d,]*\.\d{2}",

        text

    )

    if matches:

        return clean_amount(matches[0])

    return ""


# =====================================================
# Safe Dictionary
# =====================================================

def blank_invoice():

    return {

        "vendor": "",

        "po": "",

        "invoice_no": "",

        "invoice_date": "",

        "base_amount": "",

        "igst": "",

        "cgst": "",

        "sgst": "",

        "other": "",

        "total": ""

    }


# =====================================================
# Debug
# =====================================================

def print_header(title):

    print("\n")

    print("=" * 70)

    print(title)

    print("=" * 70)


def print_success(msg):

    print(f"[SUCCESS] {msg}")


def print_error(msg):

    print(f"[ERROR] {msg}")
