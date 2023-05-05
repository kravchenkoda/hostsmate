from pathlib import Path
from logging import Logger

from src.hostsmate.sources.sources import Sources
from src.utils.os_utils import OSUtils
from src.hostsmate.logger import HostsLogger


class BlacklistSources(Sources):

    def __init__(self):
        self.logger: Logger = HostsLogger().create_logger(__class__.__name__)

    @property
    def sources_json_path(self) -> Path:
        """
        Returns the path to the JSON file that contains the list of
        blacklisted domains sources.
        """
        project_root: Path = OSUtils.get_project_root()
        return project_root / 'resources' / 'blacklist_sources.json'

    def add_url_to_sources(self, new_source: str) -> None:
        """
        Adds a new URL to the list of sources of the blacklisted domains.
        Extends Sources.add_url_to_sources() with the print statement.

        Args:
            new_source: A string representing the new URL to add to the
            list of blacklist sources.
        """
        super().add_url_to_sources(new_source)
        print(f'"{new_source}" has been added to blacklist sources.')

    def remove_url_from_sources(self, source_to_remove: str) -> None:
        """
        Removes a URL from the list of sources of the blacklisted domains.
        Extends Sources.remove_url_from_sources() with the print statement.

        Args:
            source_to_remove: A string representing the URL to remove from the
            list of blacklist sources.
        """
        super().remove_url_from_sources(source_to_remove)
        print(f'"{source_to_remove}" has been removed from blacklist sources.')

    def fetch_source_contents(self, url: str) -> str:
        """
         Fetches the contents of a source containing whitelisted domains.
         Extends Sources.remove_url_from_sources() with the print statement.

         Args:
             url: A string representing the URL to fetch the contents from.

         Returns:
             A string representing the contents of the URL.
         """
        print(f'Fetching blacklisted domains from {url}')
        return super().fetch_source_contents(url)
