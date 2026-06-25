import re


class InvoiceParser:

    def __init__(self):

        self.invoice_patterns = [

            r'Invoice\s*No\.?\s*[:\-]?\s*(.+)',

            r'Invoice\s*Number\s*[:\-]?\s*(.+)',

            r'Inv\s*No\.?\s*[:\-]?\s*(.+)',

            r'Bill\s*No\.?\s*[:\-]?\s*(.+)'

        ]

        self.po_patterns = [

            r'Buyer.?s\s*Order\s*No\.?\s*[:\-]?\s*(.+)',

            r'Purchase\s*Order\s*No\.?\s*[:\-]?\s*(.+)',

            r'\b(PO[/A-Z0-9\-]+)',

            r'\b(WO[/A-Z0-9\-]+)',

            r'\b(SO[/A-Z0-9\-]+)'

        ]

        self.date_patterns = [

            r'Dated\s*[:\-]?\s*([0-9]{1,2}[-/][A-Za-z]{3}[-/][0-9]{2,4})',

            r'Invoice\s*Date\s*[:\-]?\s*(.+)',

            r'Date\s*[:\-]?\s*(.+)'

        ]

    # ---------------------------------

    def search_patterns(self, patterns, text):

        for pattern in patterns:

            match = re.search(

                pattern,

                text,

                flags=re.IGNORECASE

            )

            if match:

                return match.group(1).strip()

        return ""

    # ---------------------------------

    def extract_amount_after_label(

        self,

        label,

        text

    ):

        pattern = (

            label +

            r'.{0,80}?([0-9,]+\.\d{2})'

        )

        match = re.search(

            pattern,

            text,

            flags=re.IGNORECASE | re.DOTALL

        )

        if match:

            return match.group(1)

        return ""

    # ---------------------------------

    def extract_vendor(self, text):

        lines = text.splitlines()

        for line in lines:

            line = line.strip()

            if len(line) > 5:

                if any(

                    word in line.upper()

                    for word in

                    [

                        "PRIVATE",

                        "LIMITED",

                        "LTD",

                        "SERVICES",

                        "ENGINEERING",

                        "ENTERPRISE",

                        "INDUSTRIES"

                    ]

                ):

                    return line

        return ""

    # ---------------------------------

    def parse(self, text):

        result = {}

        result["vendor"] = self.extract_vendor(text)

        result["invoice_no"] = self.search_patterns(

            self.invoice_patterns,

            text

        )

        result["po"] = self.search_patterns(

            self.po_patterns,

            text

        )

        result["invoice_date"] = self.search_patterns(

            self.date_patterns,

            text

        )

        result["base_amount"] = self.extract_amount_after_label(

            "Taxable",

            text

        )

        result["igst"] = self.extract_amount_after_label(

            "IGST",

            text

        )

        result["cgst"] = self.extract_amount_after_label(

            "CGST",

            text

        )

        result["sgst"] = self.extract_amount_after_label(

            "SGST",

            text

        )

        result["other"] = self.extract_amount_after_label(

            "CESS",

            text

        )

        total = self.extract_amount_after_label(

            "Grand Total",

            text

        )

        if total == "":

            total = self.extract_amount_after_label(

                "Total",

                text

            )

        result["total"] = total

        return result
