from lib.file_storage import PCloudClient, DropboxClient
from lib.network import NetworkApiClient

from worker.config import PCLOUD_PATH, PCLOUD_API_KEY, DROPBOX_API_KEY, DROPBOX_FOLDER


class UtilsProviders:

	@staticmethod
	def provide_file_storage():
		return DropboxClient(DROPBOX_API_KEY, DROPBOX_FOLDER)

