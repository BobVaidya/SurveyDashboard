from __future__ import annotations

from typing import Optional, List

from pydantic import BaseModel, Field, computed_field


class QuotaData(BaseModel):
	"""Represents quota information for a survey"""
	name: Optional[str] = None
	category: Optional[str] = None
	fielded: Optional[int] = 0
	goal: Optional[int] = 0
	current_target: Optional[int] = 0
	currently_open: Optional[int] = 0
	in_progress: Optional[int] = 0
	
	@computed_field
	@property
	def progress_percentage(self) -> float:
		"""Calculate progress percentage"""
		if self.goal and self.goal > 0:
			return (self.fielded / self.goal) * 100
		return 0.0


class PureSpectrumEvent(BaseModel):
	"""Represents a minimal PureSpectrum webhook payload.

	Adjust fields to match the actual webhook schema from PureSpectrum.
	"""

	surveyId: str = Field(alias="surveyId")
	event: Optional[str] = None
	status: Optional[str] = None
	completes: Optional[int] = None
	target: Optional[int] = None
	incidence: Optional[float] = None
	cpi: Optional[float] = None
	updatedAt: Optional[str] = None

	class Config:
		populate_by_name = True
		arbitrary_types_allowed = True


def format_event_as_text(event: PureSpectrumEvent) -> str:
	"""Create a human-readable update message for Teams."""
	parts = [
		f"Survey {event.surveyId}",
		f"event={event.event}" if event.event else None,
		f"status={event.status}" if event.status else None,
		f"completes={event.completes}" if event.completes is not None else None,
		f"target={event.target}" if event.target is not None else None,
		f"incidence={event.incidence}" if event.incidence is not None else None,
		f"cpi={event.cpi}" if event.cpi is not None else None,
		f"updatedAt={event.updatedAt}" if event.updatedAt else None,
	]
	parts = [p for p in parts if p]
	return " | ".join(parts) if parts else f"Survey {event.surveyId} update"



