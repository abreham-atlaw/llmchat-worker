from lib.file_storage import PCloudClient
from lib.network import NetworkApiClient

from worker.config import PCLOUD_PATH, PCLOUD_API_KEY


class UtilsProviders:

	@staticmethod
	def provide_file_storage():
		return PCloudClient(PCLOUD_API_KEY, PCLOUD_PATH)
