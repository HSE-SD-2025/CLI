from typing import List


class CommandInterface:

    def execute(self, args: List[str]) -> int:
        pass
