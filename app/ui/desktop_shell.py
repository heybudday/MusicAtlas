from __future__ import annotations


class DesktopShell:
    def __init__(self, app):
        self.application = app
        self.services = app.services
        self.dispatcher = app.dispatcher

    def execute_command(self, name, *args):
        return self.dispatcher.dispatch(name, *args)

    def process_input(self, raw: str):
        parts = raw.strip().split()

        if not parts:
            return ""

        cmd = parts[0]
        args = parts[1:]

        return self.dispatcher.dispatch(cmd, *args)

    def run_once(self, raw: str):
        return self.process_input(raw)

    def run(self, input_func=input, output_func=print):
        while True:
            try:
                user_input = input_func("> ")
            except (EOFError, OSError):
                return True

            result = self.process_input(user_input)

            if result is False:
                return True

            output_func(result)