from pathlib import Path

from plox import error
from plox.ast_printer import pretty_print
from plox.parser import Parser
from plox.scanner import Scanner


class Plox:
    def run(self, source: str):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()

        parser = Parser(tokens)
        expression = parser.parse()

        if error.had_error():
            return

        print(pretty_print(expression))

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

                if error.had_error():
                    error.set_error(False)

            except EOFError:
                break
            except KeyboardInterrupt:
                break
