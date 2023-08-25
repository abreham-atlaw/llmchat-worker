import os.path
import typing
from abc import ABC, abstractmethod

from worker import RequestProcessor
from worker.di.utils_di import UtilsProviders


class FileProcessor(RequestProcessor, ABC):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__file_processor = UtilsProviders.provide_file_storage()

	@abstractmethod
	def processor_file(self, request: typing.Any) -> str:
		pass

	def handle(self, request) -> typing.Any:
		file_path = self.processor_file(request)
		self.__file_processor.save(file_path)
		url = self.__file_processor.get_url(os.path.basename(file_path))
		return url


