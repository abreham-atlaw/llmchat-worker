import os.path
import typing

from audiocraft.models import musicgen
import torch
import torchaudio

from datetime import datetime

from worker.file.file_processor import FileProcessor


class MusicGenProcessor(FileProcessor):

	class ModelType:
		small = "facebook/musicgen-small"
		medium = "facebook/musicgen-medium"
		melody = "facebook/musicgen-melody"
		large = "facebook/musicgen-large"

	MODEL_ID = "musicgen"

	def __init__(
			self,
			host: str,
			model_id: typing.Optional[str] = None,
			model_type: typing.Optional[str] = None,
			duration: int = 15,
			device: str="cuda",
			tmp_path: str="/tmp"
	):
		if model_id is None:
			model_id = self.MODEL_ID
		if model_type is None:
			model_type = self.ModelType.medium
		super().__init__(host, model_id=model_id)
		self._model = self.__prepare(model_type, duration, device)
		self.__tmp_path = tmp_path

	@staticmethod
	def __prepare(model_type: str, duration: int, device: str) -> musicgen.MusicGen:
		model = musicgen.MusicGen.get_pretrained(model_type, device=device)
		model.set_generation_params(duration=duration)
		return model

	@staticmethod
	def _generate_file_name() -> str:
		return f"{str(datetime.now().timestamp())}.wav"

	def processor_file(self, request: typing.Dict) -> str:
		query = request.get("query")
		audio = self._model.generate([query])
		file_path = os.path.join(self.__tmp_path, self._generate_file_name())
		torchaudio.save(file_path, audio[0].cpu(), 32000)
		return file_path

