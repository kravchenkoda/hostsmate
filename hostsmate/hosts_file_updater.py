from hostsmate.formatter import Formatter
from hostsmate.raw_hosts_collector import RawHostsCollector
from hostsmate.utils.os_utils import OSUtils
from hostsmate.utils.data_utils import DataUtils
from hostsmate.system_hosts_file import SystemHostsFile


class HostsFileUpdater:
    """
    Managing class that updates the system Hosts file by downloading raw
    sources of domain entries, formatting them, removing duplicates, and
    writing the resulting entries, along with the header, to the hosts file.

    """

    @staticmethod
    def run() -> None:
        """
        Collects domain entries from raw sources, formats them, removes
        duplicates, and writes the resulting entries to the hosts file.
        """
        temp_file: str = OSUtils().mk_tmp_hex_file()
        blacklist_sources = DataUtils().extract_sources_from_json(blacklist=True)

        RawHostsCollector().process_sources_concurrently(
            temp_file,
            blacklist_sources
        )
        Formatter().format_raw_lines(temp_file)
        SystemHostsFile().build()
