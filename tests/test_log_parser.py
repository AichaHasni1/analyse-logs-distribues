# Ce script contient une fonction pour analyser une ligne de log au format commun.
# Il extrait l'adresse IP, la date et le message principal de la ligne.
# Un test unitaire vérifie que l'IP est correctement extraite et que le message contient "index.html".

import unittest

def parse_log_line(line):
    parts = line.split(" ")
    return {
        "ip": parts[0],
        "date": parts[3][1:] if len(parts) > 3 else "",
        "message": " ".join(parts[5:]) if len(parts) > 5 else ""
    }

class TestLogParser(unittest.TestCase):
    def test_parse_line(self):
        line = '127.0.0.1 - - [12/May/2025:12:34:56] "GET /index.html HTTP/1.1"'
        parsed = parse_log_line(line)
        self.assertEqual(parsed["ip"], "127.0.0.1")
        self.assertIn("index.html", parsed["message"])

if __name__ == '__main__':
    unittest.main()
