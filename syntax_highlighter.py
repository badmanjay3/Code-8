from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import QRegularExpression
import json


class HighlightRule:
    def __init__(self, pattern, fmt):
        self.pattern = QRegularExpression(pattern)
        self.format = fmt


class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.rules = []
        self.format_map = {}

    def set_language(self, language_extension):
        self.rules = []
        try:
            with open("languages.json", "r") as f:
                data = json.load(f)

            lang = data["languages"].get(language_extension)
            if not lang:
                return

            for fmt_name, fmt_props in data["formats"].items():
                fmt = QTextCharFormat()
                if "color" in fmt_props:
                    fmt.setForeground(QColor(fmt_props["color"]))
                if "bold" in fmt_props and fmt_props["bold"]:
                    fmt.setFontWeight(QFont.Bold)
                if "italic" in fmt_props and fmt_props["italic"]:
                    fmt.setFontItalic(True)
                self.format_map[fmt_name] = fmt

            for rule in lang["patterns"]:
                pattern = rule["regex"]
                fmt_name = rule["format"]
                fmt = self.format_map.get(fmt_name)
                if fmt:
                    self.rules.append(HighlightRule(pattern, fmt))
        except Exception as e:
            print(f"Error loading syntax highlighting rules: {e}")

    def highlightBlock(self, text):
        for rule in self.rules:
            match_iterator = rule.pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                start = match.capturedStart()
                length = match.capturedLength()
                self.setFormat(start, length, rule.format)
