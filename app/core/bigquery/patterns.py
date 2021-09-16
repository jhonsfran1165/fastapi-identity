import re

var_pattern = re.compile(
    r'(?P<dblquote>"[^"]+")|'
    r"(?P<quote>\'[^\']+\')|"
    r"(?P<lead>[^:]):(?P<var_name>[\w-]+)(?P<trail>[^:]?)"
)
"""
Pattern: Identifies variable definitions in SQL code.
"""
