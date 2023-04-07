import subprocess
import sys
from pathlib import Path
from logging import Logger

from hostsmate.cli.ask_user import AskUser
from hostsmate.utils.data_utils import OSUtils
from hostsmate.logger import HostsLogger


class Autorunner:
    """A class responsible for setting up automatic update of the system's
     Hosts file.

    Attributes:
        hostsmate_app (Path) = path to the hostsmate.py file.
        job_setter_sh (Path) = path to the anacron_job_setter.sh which sets up
        an anacron job for Linux (bash only).

    """
    hostsmate_app: Path = OSUtils.get_project_root() / 'hostsmate.py'
    job_setter_sh: Path = OSUtils.get_project_root() / 'anacron_job_setter.sh'

    def __init__(self):
        self.ensure_os_compatibility()
        self.logger: Logger = HostsLogger().create_logger(__class__.__name__)

    @staticmethod
    def ensure_os_compatibility() -> None:
        """Ensure that the current operating system is compatible with the
        autorunner feature (Linux and FreeBSD), exit if it is not.

        Raises:
            SystemExit: If the current operating system is not in the list of
            allowed platforms.
        """
        platform: str = sys.platform
        allowed_platforms: list[str] = ['linux', 'freebsd']

        if platform not in allowed_platforms:
            raise SystemExit('This feature in not supported for your '
                             'operating system.')

    def check_anacron_dependency(self) -> None:
        """
        Verify whether anacron package is installed on the system, exit if not.
        """
        try:
            anacron: subprocess.CompletedProcess = subprocess.run(
                ['which', 'anacron'],
                capture_output=True
            )
        except subprocess.SubprocessError as e:
            print('Operation failed.')
            self.logger.error(f'Operation failed: {e}')

        if not anacron.stdout:
            exit("Please install 'anacron' dependency and try again.")

    def add_exec_permissions(self) -> None:
        """Add executable permissions to the anacron job setter bash script."""
        try:
            subprocess.run(
                ['chmod',
                 '+x',
                 self.job_setter_sh
                 ]
            )
            self.logger.debug(f'executable permissions added to '
                              f'{self.job_setter_sh}')
        except subprocess.SubprocessError as e:
            print('Operation failed.')
            self.logger.error(f'Operation failed: {e}')

    def set_anacron_job(self) -> None:
        """Run the anacron_job_setter.sh script."""

        self.check_anacron_dependency()
        autorun_frequency: str = AskUser().ask_autorun_frequency()
        self.add_exec_permissions()
        try:
            subprocess.run(['bash',
                            self.job_setter_sh,
                            autorun_frequency,
                            f'python3 {self.hostsmate_app} --go'
                            ])
        except subprocess.SubprocessError as e:
            print('Operation failed.')
            self.logger.error(f'Operation failed: {e}')