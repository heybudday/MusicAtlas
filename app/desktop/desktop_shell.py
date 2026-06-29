from __future__ import annotations


class DesktopShell:
    def __init__(self, application):
        self.application = application
        self.app = application
        self.services = application.services
        self.dispatcher = application.dispatcher

    def execute_command(self, raw: str):
        return self.dispatcher.dispatch(raw)

    def process_input(self, raw: str):
        raw = raw.strip()

        if not raw:
            return ""

        result = self.execute_command(raw)

        if isinstance(result, str) and result.startswith("opened:"):
            return result.replace("opened:", "opened: ", 1)

        return result

    def run_once(self, raw: str):
        result = self.process_input(raw)

        if isinstance(result, str) and result.startswith("opened: "):
            return result.replace("opened: ", "opened ", 1)

        return result

    def run(self, input_func=None, output_func=None):
        if input_func is None:
            return True

        while True:
            result = self.process_input(input_func("> "))

            if result is False:
                return True

            if output_func:
                output_func(result)