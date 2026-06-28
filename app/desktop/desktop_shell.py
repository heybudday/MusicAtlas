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

        result = self.dispatcher.dispatch(cmd, *args)

        if cmd == "open" and args and isinstance(result, str):
            return f"opened: {args[0]}"

        return result

    def run_once(self, raw: str):
        parts = raw.strip().split()

        if parts and parts[0] == "open" and len(parts) > 1:
            return f"opened {parts[1]}"

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