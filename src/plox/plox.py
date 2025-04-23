from pathlib import Path

from plox.scanner import Scanner


class Plox:
    def __init__(self):
        self.had_error: bool = False

    def run(self, source: str):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        for token in tokens:
            print(token)

            if self.had_error:
                return

    def run_file(self, source: Path):
        with source.open("r") as file:
            source = file.read()
        self.run(source)

    def run_prompt(self):
        while True:
            try:
                line = input("> ")
                if line.lower() == "exit":
                    break
                self.run(line)

                if self.had_error:
                    self.had_error = False

            except EOFError:
                break
            except KeyboardInterrupt:
                break

    def error(self, line: int, message: str):
        self.report(line, "", message)

    def report(self, line: int, where: str, message: str):
        print(f"[line {line}] Error {where}: {message}")
        self.had_error = True
