import typing

from ctransformers import AutoModelForCausalLM
import ctransformers

from .llm_processor import LLMProcessor


class Llama2Processor(LLMProcessor):

	class ModelType:
		LLAMA2_7B = "TheBloke/Llama-2-7B-GGML"
		LLAMA2_7B_CHAT = "TheBloke/Llama-2-7B-chat-GGML"
		LLAMA2_13B = "TheBloke/Llama-2-13B-GGML"
		LLAMA2_13_CHAT = "TheBloke/Llama-2-13B-chat-GGML"

	MODEL_ID = "llama_2"

	def __init__(
			self,
			host: str,
			llama_model_type: typing.Optional[str] = None,
			model_id: typing.Optional[str] = None,
			config: typing.Dict[str, typing.Any] = None
	):
		if model_id is None:
			model_id = self.MODEL_ID
		if llama_model_type is None:
			llama_model_type = self.ModelType.LLAMA2_13_CHAT
		if config is None:
			config = {}
		super().__init__(host, model_id)
		self._model = self.__load_model(llama_model_type, config)

	def __load_model(self, model_type: str, config: typing.Dict) -> ctransformers.llm.LLM:
		return AutoModelForCausalLM.from_pretrained(
			model_type,
			model_type="llama",
			gpu_layers=130,
			**config
		)

	def chat(self, query: str) -> str:
		query = f"Question: {query}\nAnswer: "
		return self._model(query)
