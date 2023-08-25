import typing

from bark import SAMPLE_RATE, generate_audio, preload_models
import torchaudio

import os
from datetime import datetime

from worker.file.file_processor import FileProcessor


class BarkProcessor(FileProcessor):

	MODEL_ID = "bark"

	def __init__(
			self,
			host: str,
			model_id: typing.Optional[str] = None,
			tmp_path: str = "/tmp"
	):
		if model_id is None:
			model_id = model_id
		super().__init__(host, model_id)
		self.__tmp_path = tmp_path

	@staticmethod
	def __prepare():
		preload_models()

	@staticmethod
	def _generate_file_name() -> str:
		return f"{str(datetime.now().timestamp())}.wav"

	def processor_file(self, request: typing.Any) -> str:
		query = request.get("query")
		audio = generate_audio(query)
		file_path = os.path.join(self.__tmp_path, self._generate_file_name())
		torchaudio.save(file_path, audio.cpu(), SAMPLE_RATE)
		return file_path

