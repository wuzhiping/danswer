import abc
from collections.abc import Iterator

from langchain.chat_models.base import BaseChatModel
from langchain.schema.language_model import LanguageModelInput

from danswer.llm.utils import message_generator_to_string_generator
from danswer.utils.logger import setup_logger


logger = setup_logger()


class LLM(abc.ABC):
    """Mimics the LangChain LLM / BaseChatModel interfaces to make it easy
    to use these implementations to connect to a variety of LLM providers."""

    @abc.abstractmethod
    def invoke(self, input: LanguageModelInput) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def stream(self, input: LanguageModelInput) -> Iterator[str]:
        raise NotImplementedError


class LangChainChatLLM(LLM, abc.ABC):
    @property
    @abc.abstractmethod
    def llm(self) -> BaseChatModel:
        raise NotImplementedError

    def _log_model_config(self) -> None:
        logger.debug(
            f"Model Class: {self.llm.__class__.__name__}, Model Config: {self.llm.__dict__}"
        )

    def invoke(self, input: LanguageModelInput) -> str:
        self._log_model_config()
        return self.llm.invoke(input).content

    def stream(self, input: LanguageModelInput) -> Iterator[str]:
        self._log_model_config()
        yield from message_generator_to_string_generator(self.llm.stream(input))
