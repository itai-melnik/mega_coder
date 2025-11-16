"""
Code detection module for identifying code in OCR'd text.

This module provides heuristic-based detection to determine if text extracted
from screenshots contains programming code. The logic is abstracted here to
allow easy modification without changing the main application.
"""

import re
from typing import Set


# Common programming keywords across popular languages
PYTHON_KEYWORDS: Set[str] = {
    'def', 'class', 'import', 'from', 'if', 'elif', 'else', 'for', 'while',
    'try', 'except', 'finally', 'with', 'return', 'yield', 'lambda', 'async',
    'await', 'pass', 'break', 'continue', 'raise', 'assert', 'None', 'True',
    'False', 'and', 'or', 'not', 'in', 'is', 'as', 'global', 'nonlocal'
}

OTHER_KEYWORDS: Set[str] = {
    'function', 'const', 'let', 'var', 'public', 'private', 'static',
    'void', 'int', 'string', 'boolean', 'interface', 'namespace', 'package',
    'struct', 'enum', 'typedef', 'sizeof', 'template', 'typename'
}

ALL_KEYWORDS = PYTHON_KEYWORDS | OTHER_KEYWORDS


def has_code_keywords(text: str, threshold: int = 2) -> bool:
    """
    Check if text contains programming keywords.
    
    Args:
        text: The text to analyze
        threshold: Minimum number of keywords required
        
    Returns:
        True if text contains at least threshold keywords
    """
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    keyword_count = sum(1 for word in words if word in ALL_KEYWORDS)
    return keyword_count >= threshold


def has_code_structure(text: str) -> bool:
    """
    Check if text has code-like structure (brackets, operators, etc.).
    
    Args:
        text: The text to analyze
        
    Returns:
        True if text appears to have code structure
    """
    # Count various code indicators
    indicators = {
        'parentheses': text.count('(') + text.count(')'),
        'brackets': text.count('[') + text.count(']'),
        'braces': text.count('{') + text.count('}'),
        'operators': text.count('=') + text.count('==') + text.count('!='),
        'semicolons': text.count(';'),
        'colons': text.count(':'),
        'dots': text.count('.'),
    }
    
    # If we have significant structural elements, likely code
    total_indicators = sum(indicators.values())
    return total_indicators >= 5


def has_indentation_pattern(text: str) -> bool:
    """
    Check if text has consistent indentation (common in code).
    
    Args:
        text: The text to analyze
        
    Returns:
        True if text shows indentation patterns
    """
    lines = text.split('\n')
    if len(lines) < 3:
        return False
    
    indented_lines = 0
    for line in lines:
        if line and (line.startswith('    ') or line.startswith('\t')):
            indented_lines += 1
    
    # If at least 30% of lines are indented, likely code
    return indented_lines >= len(lines) * 0.3


def has_function_or_class_definition(text: str) -> bool:
    """
    Check if text contains function or class definitions.
    
    Args:
        text: The text to analyze
        
    Returns:
        True if text contains function/class definitions
    """
    # Common patterns for function/class definitions
    patterns = [
        r'\bdef\s+\w+\s*\(',           # Python function
        r'\bclass\s+\w+',               # Class definition
        r'\bfunction\s+\w+\s*\(',       # JavaScript function
        r'\w+\s*=\s*function\s*\(',     # Function expression
        r'\w+\s*=>\s*{',                # Arrow function
        r'\b(public|private|protected)\s+\w+\s+\w+\s*\(',  # Java/C# method
    ]
    
    for pattern in patterns:
        if re.search(pattern, text):
            return True
    return False


def has_comments(text: str) -> bool:
    """
    Check if text contains code comments.
    
    Args:
        text: The text to analyze
        
    Returns:
        True if text contains comment patterns
    """
    comment_patterns = [
        r'#.*',           # Python comments
        r'//.*',          # C-style single line
        r'/\*.*?\*/',     # C-style multi-line
        r'""".*?"""',     # Python docstrings
        r"'''.*?'''",     # Python docstrings
    ]
    
    for pattern in comment_patterns:
        if re.search(pattern, text):
            return True
    return False


def is_code(text: str, min_length: int = 20) -> bool:
    """
    Determine if the given text appears to be code using multiple heuristics.
    
    This function uses several heuristics to detect code:
    - Presence of programming keywords
    - Code structure (brackets, operators, etc.)
    - Indentation patterns
    - Function/class definitions
    - Code comments
    
    Args:
        text: The text to analyze
        min_length: Minimum text length to consider (default: 20)
        
    Returns:
        True if the text appears to be code, False otherwise
    """
    # Filter out very short text
    if not text or len(text.strip()) < min_length:
        return False
    
    # Count how many heuristics pass
    checks = [
        has_code_keywords(text),
        has_code_structure(text),
        has_indentation_pattern(text),
        has_function_or_class_definition(text),
        has_comments(text),
    ]
    
    # If at least 2 heuristics pass, consider it code
    passed_checks = sum(checks)
    return passed_checks >= 2


def get_code_confidence(text: str) -> float:
    """
    Get a confidence score (0.0 to 1.0) for how likely the text is code.
    
    Args:
        text: The text to analyze
        
    Returns:
        Confidence score between 0.0 and 1.0
    """
    if not text or len(text.strip()) < 20:
        return 0.0
    
    checks = [
        has_code_keywords(text),
        has_code_structure(text),
        has_indentation_pattern(text),
        has_function_or_class_definition(text),
        has_comments(text),
    ]
    
    return sum(checks) / len(checks)

