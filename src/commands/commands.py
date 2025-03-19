from src.commands.echo_command import EchoCommand
from src.commands.exit_command import ExitCommand
from src.commands.pwd_command import PwdCommand
from src.commands.wc_command import WcCommand
from src.commands.cat_command import CatCommand

commands = {
    "echo": EchoCommand(),
    "cat": CatCommand(),
    "wc": WcCommand(),
    "pwd": PwdCommand(),
    "exit": ExitCommand(),
}
