# NOTE: This is just a copy of the example code. it works, I'm not going to worry about redoing it.

import json
from logging import Logger, StreamHandler
from os import environ as env
from typing import Any, Optional

import dotenv
from aiohttp import ClientSession

from novelai_api import NovelAIAPI
from novelai_api.utils import get_encryption_key

class API:
	_username: str
	_password: str
	_session: ClientSession

	logger: Logger
	api: Optional[NovelAIAPI]

	def __init__(self, base_address: Optional[str] = None):
		dotenv.load_dotenv()

		if "NAI_USERNAME" not in env or "NAI_PASSWORD" not in env:
			raise RuntimeError("Please ensure that NAI_USERNAME and NAI_PASSWORD are set in your environment")

		# Just a test, but I doubt I will continue messing with this.
		self._token = env["NAI_TOKEN"]
		self._username = env["NAI_USERNAME"]
		self._password = env["NAI_PASSWORD"]

		self.logger = Logger("NovelAI")
		self.logger.addHandler(StreamHandler())

		self.api = NovelAIAPI(logger=self.logger)
		if base_address is not None:
			self.api.BASE_ADDRESS = base_address

	# Look into how this'll work with Persistent Token
	@property
	def encryption_key(self):
		return get_encryption_key(self._username, self._password)

	async def __aenter__(self):
		self._session = ClientSession()
		await self._session.__aenter__()

		self.api.attach_session(self._session)
		await self.api.high_level.login(self._username, self._password)

		return self

	async def __aexit__(self, exc_type, exc_val, exc_tb):
		await self._session.__aexit__(exc_type, exc_val, exc_tb)

class JSONEncoder(json.JSONEncoder):
	"""
	Extended JSON encoder to support bytes
	"""

	def default(self, o: Any) -> Any:
		if isinstance(o, bytes):
			return o.hex()

		return super().default(o)


def dumps(e: Any) -> str:
	"""
	Shortcut to a configuration of json.dumps for consistency
	"""

	return json.dumps(e, indent=4, ensure_ascii=False, cls=JSONEncoder)