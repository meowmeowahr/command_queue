import threading
from typing import Callable

from loguru import logger


class BaseCommand:
    """
    The base command class for the command queue, does nothing if used directly.
    """

    def __init__(self) -> None:
        self._command = lambda: logger.warning(
            "A BaseCommand was called directly. Nothing will happen"
        )

    @property
    def command(self) -> Callable:
        return self._command

    @command.setter
    def command(self, callback: Callable) -> None:
        self._command = callback

    def launch(self):
        self._command()

    @property
    def as_function(self):
        return self._command


class ThreadedCommand(BaseCommand):
    def launch(self):
        threading.Thread(target=self._command, daemon=True).start()


class FunctionCommand(BaseCommand):
    def __init__(self, func: Callable) -> None:
        super().__init__()
        self.command = func


class ParallelCommandGroup(BaseCommand):
    def __init__(self, *args: BaseCommand) -> None:
        super().__init__()
        self.commands = args
        self.command = self.launch

    def launch(self):
        threads: list[threading.Thread] = []

        for command in self.commands:
            thread = threading.Thread(target=command.launch, name=f"ParallelCommandGroup thread for {command}")
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
