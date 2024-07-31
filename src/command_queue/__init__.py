"""
Command Queue written in Python
"""

import queue
import time
import threading
from dataclasses import dataclass

from loguru import logger

from .commands import BaseCommand as _BaseCommand


__version__ = "0.0.1"


@dataclass
class CommandQueueOptions:
    maxsize: int = 0
    overruntime: float = 1  # seconds


class CommandQueue:
    def __init__(self, options: CommandQueueOptions = CommandQueueOptions()) -> None:
        self.options = options
        self._queue: queue.Queue[_BaseCommand] = queue.Queue(self.options.maxsize)
        logger.info("Created command queue")

    def run(
        self,
        quantity: int = 1,
    ) -> None:
        """
        Run the next function in the command queue
        """

        for _ in range(quantity):
            if self._queue.qsize() != 0:
                item = self._queue.get_nowait()
                if not isinstance(item, _BaseCommand):
                    logger.warning(
                        "Attempted to run a non-command in the command queue."
                        "If you are trying to add a function, wrap it in the FunctionCommand class instead."
                        f"Type: {str(type(item))}: {item}"
                    )

                item.launch()  # Run command

    def spin(self, loop_rate: int, until_empty=False):
        """
        Run the command queue.
        Attempt to run at a constant rate.
        If the command takes too long, a warning will be produced.
        This will run indefenitely if `until_empty` is `False`
        """
        while True:
            """
            Run one iteration of the command scheduler.
            Attempt to run at a constant rate.
            If the command takes too long, a warning will be produced.
            """
            start_time = time.time()
            self.run()
            end_time = time.time()
            if loop_rate > 0:
                time.sleep(1 / (loop_rate - (end_time - start_time)))
            if until_empty and (self._queue.qsize() == 0):
                break

    def run_in_background(self, loop_rate: int):
        """
        Run the command queue inside a new thread.
        Attempt to run at a constant rate.
        If the command takes too long, a warning will be produced.
        """
        thread = threading.Thread(
            target=self.spin,
            name=f"Command Queue background process for 0x{self.__hash__():015X}",
            args=(loop_rate,),
            daemon=True,
        )
        thread.start()
        return thread

    def add_command(self, command: _BaseCommand):
        self._queue.put_nowait(command)
