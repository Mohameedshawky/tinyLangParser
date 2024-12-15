import re

class Scanner:
    def _init_(self, tiny_code=""):
        self.tiny_code = tiny_code  # Accept TINY code directly as an argument
        self.tokens_list = []
        self.code_list = []

    def set_tiny_code(self, tiny_code):
        """Sets the TINY language code to be scanned."""
        self.tiny_code = tiny_code

    def remove_comments(self, code):
        """Removes comments enclosed in curly brackets."""
        return re.sub(r"\{.*?\}", "", code, flags=re.DOTALL)

    def scan(self):
        """Tokenizes the TINY code."""
        # Define token patterns
        TOKEN_PATTERNS = [
            ("SEMICOLON", r";"),
            ("IF", r"if"),
            ('ELSE',r"else"),
            ("THEN", r"then"),
            ("END", r"end"),
            ("REPEAT", r"repeat"),
            ("UNTIL", r"until"),
            ("READ", r"read"),
            ("WRITE", r"write"),
            ("ASSIGN", r":="),
            ("NOT_EQUAL", r"!="),
            ("LESSTHAN", r"<"),
            ("GREATERTHAN", r">"),
            ("EQUAL", r"="),
            ("PLUS", r"\+"),
            ("MINUS", r"-"),
            ("MULT", r"\*"),
            ("DIV", r"/"),
            ("OPENBRACKET", r"\("),
            ("CLOSEDBRACKET", r"\)"),
            ("NUMBER", r"\d+"),
            ("IDENTIFIER", r"[a-zA-Z][a-zA-Z0-9]*"),
            ("WHITESPACE", r"\s+"),  # Add whitespace pattern
        ]

        token_pattern = "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_PATTERNS)
        pattern = re.compile(token_pattern)

        self.tokens_list = []
        self.code_list = []

        # Remove comments and scan
        code = self.remove_comments(self.tiny_code)
        found_end = False  # Track if end is found
        for match in pattern.finditer(code):
            token_type = match.lastgroup
            token_value = match.group(token_type)

            # Skip whitespace tokens
            if token_type == "WHITESPACE" :
                continue

            self.tokens_list.append((token_value, token_type))
            self.code_list.append(token_value)

            # Check for the 'end' token
            if token_type == "END":
                found_end = True

        # Add UNKNOWN tokens for anything unmatched
        remaining_code = re.sub(token_pattern, "", code).strip()
        for unknown in remaining_code.split():
            self.tokens_list.append((unknown, "UNKNOWN"))
            self.code_list.append(unknown)

        # Raise an error if end is not found
        if not found_end:
            raise ValueError("Code does not contain the 'end' token.")

    def createOutputFile(self, filename):
        """Save the tokens to a file."""
        if not self.tokens_list:
            print("No tokens to save. Run the scan method first.")
            return

        try:
            with open(filename, 'w') as out:
                out.write("Token Value\tToken Type\n")
                for token_value, token_type in self.tokens_list:
                    out.write(f"{token_value:<12}\t{token_type}\n")
            print(f"Tokens successfully written to {filename}")
        except Exception as e:
            print(f"Error writing to file: {e}")