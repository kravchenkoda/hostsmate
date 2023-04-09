import ctypes
import pathlib
import subprocess
import sys
from os import getuid
from os.path import join
from pathlib import Path
from tempfile import gettempdir
from uuid import uuid4

from hostsmate.utils.utils import Utils
import hostsmate.logger as l


class OSUtils(Utils):
    """
    This class contains utility methods for operating system-related tasks.

    Methods:
        ensure_root_privileges(): Ensure that the application is running with
        root/administrator privileges. Exit if it is not.

        get_project_root(): Return the root directory of the project.

        mk_tmp_hex_file(): Create a temporary file path using a random
        hexadecimal UUID.

        path_to_hosts(): Return the path to the hosts file on the current system.
    """

    def __init__(self):
        self.ensure_root_privileges()
        self.logger = l.HostsLogger().create_logger('Utils')

    @staticmethod
    def ensure_root_privileges():
        """
        Ensure that the application is running with root/administrator privileges. Exit if it is not.

        Raises:
        SystemExit: If the application is not running with root/administrator privileges.
        """
        try:
            root: bool = getuid() == 0
        except AttributeError:
            root: bool = ctypes.windll.shell32.IsUserAnAdmin() != 0

        if not root:
            exit('Please run the application as a '
                 'root/administrator to continue.')

    @staticmethod
    def get_project_root() -> pathlib.Path:
        """
        Return the root directory of the project.

        The root directory is defined as the parent directory of the directory containing
        the module that this method is called from.

        Returns:
            pathlib.Path: The root directory of the project.
        """
        project_root: pathlib.Path = Path(__file__).resolve().parents[2]
        return project_root

    def mk_tmp_hex_file(self) -> str:
        """Create a temporary file path using a random hexadecimal UUID.

        Returns:
            str: The absolute path of the temporary file.
        """
        tmp: str = join(gettempdir(), uuid4().hex)
        self.logger.info(f'Temporary file: path: {tmp}')
        return tmp

    def path_to_hosts(self) -> Path:
        """Return the path to the hosts file on the current system.

        Returns:
            Path: The path to the hosts file.
        """
        platform: str = sys.platform

        if platform.startswith(('linux', 'freebsd', 'darwin')):
            hosts_path: Path = Path('/etc/hosts')
            return hosts_path
        elif platform.startswith('win'):
            root_drive: str = Path(sys.executable).anchor
            hosts_path: Path = Path(root_drive + r'Windows\System32\drivers\etc\hosts')
        else:
            exit('This operating system is not supported.')
        self.logger.info(f'path to the hosts file is {hosts_path}')
        return hosts_path

    @staticmethod
    def ensure_linux_or_bsd() -> bool:
        """Ensure that the current operating system is compatible with the
        feature (Linux and FreeBSD), exit if it is not.

        Returns:
            bool: True if

        Raises:
            SystemExit: If the current operating system is not in the list of
            allowed platforms.
        """
        platform: str = sys.platform
        allowed_platforms: list[str] = ['linux', 'freebsd']

        if platform not in allowed_platforms:
            raise SystemExit('This feature in not supported for your '
                             'operating system.')
        else:
            return True

    def add_exec_permissions(self, program_name) -> bool:
        """Add executable permissions to the anacron job setter bash script."""
        try:
            command = subprocess.run(
                ['chmod',
                 '+x',
                 program_name
                 ]
            )
            self.logger.debug(f'executable permissions added to '
                              f'{program_name}')
        except subprocess.SubprocessError as e:
            self.logger.error(f'Operation failed: {e}')
            raise SystemExit('Operation failed.')
        return command.returncode == 0

    def execute_sh_command_as_root(
            self,
            program: str | Path,
            cli_args: list
    ) -> bool:
        """
        Execute a shell command as root user using sudo.

        Args:
            program (str): The name of the shell command to execute.
            cli_args (list): A list of string arguments to pass to the command.

        Returns:
            bool: True if the command was executed with 0 return code;
            False otherwise.

        Raises:
            SystemExit: if there is the error while executing command.
        """
        command = ['sudo', program]
        command.extend(cli_args)
        try:
            process: subprocess.CompletedProcess = subprocess.run(command)
        except subprocess.SubprocessError as e:
            self.logger.error(f'Operation failed: {e}')
            raise SystemExit('Operation failed.')
        return process.returncode == 0

    def is_shell_dependency_installed(self, dependency: str) -> bool:
        """Verify whether the dependency is installed on the system.

        Args:
            dependency (str): dependency name to be verified.

        Returns:
            bool: True if the command was executed with 0 return code;
            False otherwise.
        """
        try:
            command: subprocess.CompletedProcess = subprocess.run(
                ['which', dependency],
                capture_output=True
            )
        except subprocess.SubprocessError as e:
            self.logger.error(f'Operation failed: {e}')
            raise SystemExit('Operation failed.')
        return command.returncode == 0
