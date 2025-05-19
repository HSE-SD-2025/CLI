from src.commands.echo_command import EchoCommand
from src.commands.pwd_command import PwdCommand
from src.commands.wc_command import WcCommand
from src.commands.cat_command import CatCommand
from src.commands.exit_command import ExitCommand
from src.commands.grep_command import GrepCommand
from src.commands.ls_command import LsCommand
from src.commands.cd_command import CdCommand

commands = {
    "echo": EchoCommand,
    "cat": CatCommand,
    "wc": WcCommand,
    "pwd": PwdCommand,
    "exit": ExitCommand,
    "grep": GrepCommand,
    "ls": LsCommand,
    "cd": CdCommand,
}
