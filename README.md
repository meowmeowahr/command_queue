# A Command Queue for Python

Run commands (which can be regular functions) in a FIFO queue. Can be run in a background thread.

## Usage examples

Simple filling and running of the queue

```python
from command_queue import CommandQueue
from command_queue.commands import FunctionCommand
import functools


example_queue = CommandQueue()

# Add example commands
for i in range(100):
    example_queue.add_command(
        FunctionCommand(functools.partial(print, f"Running loop iteration {i}"))
    )

# Attempt to run command queue at 60 commands per second
# Stop running once queue empties
example_queue.spin(60, until_empty=True)
```

Example of ParallelCommandGroups

```python
from command_queue import CommandQueue
from command_queue.commands import FunctionCommand, ParallelCommandGroup
import functools
import time


def do_something():
    print(f"Something happended on {time.time()}")
    time.sleep(0.05)


def do_something_2():
    print(f"Something_2 happended on {time.time()}")
    time.sleep(0.05)


example_queue = CommandQueue()

# Add example non-parallel commands
# These commands will run sequentially
for i in range(2):
    example_queue.add_command(FunctionCommand(functools.partial(do_something)))

# These commands will run at the same time using threads

# Add example parallel command
# These commands will run at the same time
example_queue.add_command(
    ParallelCommandGroup(
        FunctionCommand(functools.partial(do_something_2)),
        FunctionCommand(functools.partial(do_something_2)),
        FunctionCommand(functools.partial(do_something_2)),
        FunctionCommand(functools.partial(do_something_2)),
        FunctionCommand(functools.partial(do_something_2)),
        FunctionCommand(functools.partial(do_something_2)),
    )
)

# Attempt to run command queue at 10 commands per second
# Stop running once queue empties
example_queue.spin(10, until_empty=True)
```