from __future__ import annotations

import asyncio
from typing import Dict, Iterable, List, Optional, Set

from botbuilder.schema import ConversationReference


class SubscriptionStore:
	"""In-memory mapping of survey_id -> set of ConversationReference.

	Thread-safe via asyncio.Lock for async web servers.
	"""

	def __init__(self) -> None:
		self._survey_id_to_refs: Dict[str, Set[str]] = {}
		self._ref_id_to_ref: Dict[str, ConversationReference] = {}
		self._lock = asyncio.Lock()

	@staticmethod
	def _make_ref_id(ref: ConversationReference) -> str:
		# Unique key per conversation (channelId + conversation.id + serviceUrl + bot.id)
		parts: List[str] = [
			getattr(ref, "channel_id", ""),
			getattr(ref.conversation, "id", "") if getattr(ref, "conversation", None) else "",
			getattr(ref, "service_url", ""),
			getattr(ref.bot, "id", "") if getattr(ref, "bot", None) else "",
		]
		return "|".join(parts)

	async def add_subscription(self, survey_id: str, ref: ConversationReference) -> None:
		ref_id = self._make_ref_id(ref)
		async with self._lock:
			refs = self._survey_id_to_refs.setdefault(survey_id, set())
			refs.add(ref_id)
			self._ref_id_to_ref[ref_id] = ref

	async def remove_subscription(self, survey_id: str, ref: ConversationReference) -> None:
		ref_id = self._make_ref_id(ref)
		async with self._lock:
			if survey_id in self._survey_id_to_refs:
				self._survey_id_to_refs[survey_id].discard(ref_id)
				if not self._survey_id_to_refs[survey_id]:
					self._survey_id_to_refs.pop(survey_id, None)

	async def remove_conversation_everywhere(self, ref: ConversationReference) -> int:
		"""Remove a conversation from all survey subscriptions. Returns count removed."""
		ref_id = self._make_ref_id(ref)
		removed_count = 0
		async with self._lock:
			for survey_id, refs in list(self._survey_id_to_refs.items()):
				if ref_id in refs:
					refs.remove(ref_id)
					removed_count += 1
					if not refs:
						self._survey_id_to_refs.pop(survey_id, None)
			self._ref_id_to_ref.pop(ref_id, None)
		return removed_count

	async def list_subscriptions_for_conversation(self, ref: ConversationReference) -> List[str]:
		ref_id = self._make_ref_id(ref)
		async with self._lock:
			return [sid for sid, refs in self._survey_id_to_refs.items() if ref_id in refs]

	async def get_subscribers(self, survey_id: str) -> List[ConversationReference]:
		async with self._lock:
			ref_ids = list(self._survey_id_to_refs.get(survey_id, set()))
			return [self._ref_id_to_ref[rid] for rid in ref_ids if rid in self._ref_id_to_ref]



