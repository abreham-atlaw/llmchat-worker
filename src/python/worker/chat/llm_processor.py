import typing
from abc import ABC, abstractmethod

from worker import RequestProcessor


class LLMProcessor(RequestProcessor, ABC):

	@abstractmethod
	def chat(self, query: str) -> str:
		pass

	def handle(self, params) -> typing.Any:
		return self.chat(params.get("query"))
