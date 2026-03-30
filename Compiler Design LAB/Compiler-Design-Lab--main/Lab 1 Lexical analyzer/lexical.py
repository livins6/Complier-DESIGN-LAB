import re

# Token definitions (type, regex pattern)
TOKEN_PATTERNS = [
    ('KEYWORD',    r'\b(if|else|while|for|return|int|float|char|void|do|break|continue)\b'),
    ('FLOAT',      r'\b\d+\.\d+\b'),
    ('INTEGER',    r'\b\d+\b'),
    ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    ('OPERATOR',   r'[+\-*/=<>!&|]{1,2}'),
    ('DELIMITER',  r'[(){};,\[\]]'),
    ('STRING',     r'"[^"]*"'),
    ('WHITESPACE', r'\s+'),
    ('UNKNOWN',    r'.'),
]

# Compile all patterns
master_pattern = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_PATTERNS)
compiled = re.compile(master_pattern)

def tokenize(source_code):
    tokens = []
    for match in compiled.finditer(source_code):
        token_type = match.lastgroup
        token_value = match.group()
        if token_type == 'WHITESPACE':
            continue  # Skip whitespace
        tokens.append((token_type, token_value))
    return tokens

def display_tokens(tokens):
    print(f"{'TOKEN TYPE':<15} {'VALUE'}")
    print("-" * 35)
    for token_type, value in tokens:
        print(f"{token_type:<15} {value}")

# ---- Test the Lexer ----
if __name__ == "__main__":
    source_code = """
    int main() {
        int x = 10;
        float y = 3.14;
        if (x > 5) {
            return x + y;
        }
    }
    """

    print("Source Code:")
    print(source_code)
    print("Tokens Found:")
    tokens = tokenize(source_code)
    display_tokens(tokens)
    print(f"\nTotal tokens: {len(tokens)}")