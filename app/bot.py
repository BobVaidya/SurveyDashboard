from __future__ import annotations

from typing import List

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ConversationReference

from .storage import SubscriptionStore


def _generate_quota_name(quota: dict) -> str:
	"""Generate a meaningful quota name from criteria"""
	criteria = quota.get('criteria', [])
	if not criteria:
		return quota.get('quota_title', 'General Quota')
	
	# Extract key criteria information
	parts = []
	for criterion in criteria:
		qualification_name = criterion.get('qualification_name', '')
		condition_names = criterion.get('condition_names', [])
		
		if qualification_name == 'Gender':
			if condition_names:
				parts.append(condition_names[0])
		elif qualification_name == 'Age':
			range_sets = criterion.get('range_sets', [])
			if range_sets:
				age_range = range_sets[0]
				from_age = age_range.get('from', '')
				to_age = age_range.get('to', '')
				if from_age and to_age:
					parts.append(f"{from_age}-{to_age} yr")
		elif qualification_name == 'Children':
			if condition_names:
				child_condition = condition_names[0]
				if 'no children' in child_condition.lower():
					parts.append('No Children')
				elif 'children' in child_condition.lower():
					parts.append('Has Children')
	
	if parts:
		return ', '.join(parts)
	
	# Fallback to quota title or ID
	return quota.get('quota_title') or f"Quota {quota.get('ps_quota_id', '')[:8]}"


def format_survey_status_for_teams(survey: dict, survey_id: str) -> str:
	"""
	Format basic survey status for Teams display
	"""
	title = survey.get('title', 'Untitled Survey')
	status = survey.get('status', 'Unknown')
	completes = survey.get('completes', 0)
	target = survey.get('target', 0)
	cpi = survey.get('cpi', 0)
	incidence = survey.get('incidence', 0)
	loi = survey.get('loi', 0)
	current_cost = survey.get('currentCost', 0)
	
	# Calculate progress
	progress_pct = (completes / target * 100) if target > 0 else 0
	
	# Create progress bar
	bar_length = 15
	filled_length = int(bar_length * progress_pct / 100)
	progress_bar = "=" * filled_length + "-" * (bar_length - filled_length)
	
	message_parts = [
		f"**Survey {survey_id} Status**",
		f"**Title:** {title}",
		f"**Status:** {status}",
		f"**Progress:** {completes}/{target} ({progress_pct:.1f}%)",
		f"**Progress Bar:** [{progress_bar}]",
		f"**CPI:** ${cpi:.2f}",
		f"**Incidence:** {incidence:.1%}",
		f"**LOI:** {loi} minutes",
		f"**Current Cost:** ${current_cost:.2f}",
		"",
		f"Use `quotas {survey_id}` for detailed quota breakdown"
	]
	
	return "\n".join(message_parts)


def format_quotas_for_teams(quotas: list, survey_id: str) -> str:
	"""
	Format quota data for Teams display, similar to the dashboard view
	"""
	if not quotas:
		return f"No quota data available for survey {survey_id}"
	
	# Group quotas by category/type
	grouped_quotas = {}
	
	for quota in quotas:
		# Extract category from quota name or type
		category = quota.get('group_key', quota.get('quota_category', 'General'))
		if category not in grouped_quotas:
			grouped_quotas[category] = []
		grouped_quotas[category].append(quota)
	
	# Build the formatted message
	message_parts = [f"**Quota Details for Survey {survey_id}**\n"]
	
	for category, category_quotas in grouped_quotas.items():
		message_parts.append(f"**{category}**")
		
		for quota in category_quotas:
			# Generate meaningful quota name from criteria
			name = _generate_quota_name(quota)
			fielded = quota.get('achieved', 0)
			goal = quota.get('required_count', 0)
			current_target = quota.get('current_target', 0)
			currently_open = quota.get('currently_open', 0)
			in_progress = quota.get('in_progress', 0)
			
			# Calculate progress percentage
			progress_pct = (fielded / goal * 100) if goal > 0 else 0
			
			# Create a simple progress bar
			bar_length = 20
			filled_length = int(bar_length * progress_pct / 100)
			progress_bar = "=" * filled_length + "-" * (bar_length - filled_length)
			
			quota_line = f"  • **{name}**\n"
			quota_line += f"    Fielded: {fielded}/{goal} ({progress_pct:.1f}%)\n"
			quota_line += f"    Progress: [{progress_bar}] {progress_pct:.1f}%\n"
			quota_line += f"    Target: {current_target} | Open: {currently_open} | In Progress: {in_progress}"
			
			message_parts.append(quota_line)
		
		message_parts.append("")  # Empty line between categories
	
	# Add summary if we have multiple categories
	if len(grouped_quotas) > 1:
		total_fielded = sum(q.get('fielded', 0) for quota_list in grouped_quotas.values() for q in quota_list)
		total_goal = sum(q.get('goal', 0) for quota_list in grouped_quotas.values() for q in quota_list)
		overall_progress = (total_fielded / total_goal * 100) if total_goal > 0 else 0
		
		message_parts.append(f"**Overall Progress: {total_fielded}/{total_goal} ({overall_progress:.1f}%)**")
	
	return "\n".join(message_parts)


class SurveyBot(ActivityHandler):
	def __init__(self, store: SubscriptionStore, adapter) -> None:
		self._store = store
		self._adapter = adapter

	async def on_message_activity(self, turn_context: TurnContext):
		text = (turn_context.activity.text or "").strip()
		ref: ConversationReference = TurnContext.get_conversation_reference(turn_context.activity)

		if not text:
			await turn_context.send_activity("Say 'help' to see available commands.")
			return

		lower = text.lower()
		if lower.startswith("help"):
			await turn_context.send_activity(
				"Commands:\n• subscribe <surveyId> - Subscribe to survey updates\n• unsubscribe <surveyId> - Unsubscribe from survey\n• list - Show your subscriptions\n• status <surveyId> - Show survey status and basic metrics\n• quotas <surveyId> - Show detailed quota information\n• update <surveyId> key=value - Manual update (e.g., update 12345 status=live completes=50)\n• help - Show this help"
			)
			return

		if lower.startswith("subscribe "):
			survey_id = text.split(" ", 1)[1].strip()
			if not survey_id:
				await turn_context.send_activity("Usage: subscribe <surveyId>")
				return
			await self._store.add_subscription(survey_id, ref)
			await turn_context.send_activity(f"Subscribed this conversation to survey {survey_id}.")
			return

		if lower.startswith("unsubscribe "):
			survey_id = text.split(" ", 1)[1].strip()
			if not survey_id:
				await turn_context.send_activity("Usage: unsubscribe <surveyId>")
				return
			await self._store.remove_subscription(survey_id, ref)
			await turn_context.send_activity(f"Unsubscribed this conversation from survey {survey_id}.")
			return

		if lower == "list":
			sids: List[str] = await self._store.list_subscriptions_for_conversation(ref)
			if not sids:
				await turn_context.send_activity("No subscriptions for this conversation.")
			else:
				await turn_context.send_activity("Subscribed surveys: " + ", ".join(sorted(sids)))
			return

		if lower.startswith("status "):
			survey_id = text.split(" ", 1)[1].strip()
			if not survey_id:
				await turn_context.send_activity("Usage: status <surveyId>")
				return
			
			try:
				from .scraper import PureSpectrumScraper
				import aiohttp
				import os
				
				# Get credentials from environment
				username = os.getenv("PURESPECTRUM_USERNAME", "")
				password = os.getenv("PURESPECTRUM_PASSWORD", "")
				
				if not username or not password:
					await turn_context.send_activity("❌ PureSpectrum credentials not configured. Please set PURESPECTRUM_USERNAME and PURESPECTRUM_PASSWORD environment variables.")
					return
				
				scraper = PureSpectrumScraper(username, password)
				
				async with aiohttp.ClientSession() as session:
					if not await scraper.login(session):
						await turn_context.send_activity("❌ Authentication failed. Please check your credentials or update your auth token.")
						return
					
					survey_data = await scraper.get_survey_data(session, survey_id)
					
					if not survey_data or survey_id not in survey_data:
						await turn_context.send_activity(f"❌ Survey {survey_id} not found")
						return
					
					survey = survey_data[survey_id]
					
					# Format and send survey status
					status_text = format_survey_status_for_teams(survey, survey_id)
					await turn_context.send_activity(status_text)
					
			except Exception as e:
				await turn_context.send_activity(f"❌ Error fetching survey status: {str(e)}")
			return

		if lower.startswith("quotas "):
			survey_id = text.split(" ", 1)[1].strip()
			if not survey_id:
				await turn_context.send_activity("Usage: quotas <surveyId>")
				return
			
			try:
				from .scraper import PureSpectrumScraper
				import aiohttp
				import os
				
				# Get credentials from environment
				username = os.getenv("PURESPECTRUM_USERNAME", "")
				password = os.getenv("PURESPECTRUM_PASSWORD", "")
				
				if not username or not password:
					await turn_context.send_activity("❌ PureSpectrum credentials not configured. Please set PURESPECTRUM_USERNAME and PURESPECTRUM_PASSWORD environment variables.")
					return
				
				scraper = PureSpectrumScraper(username, password)
				
				async with aiohttp.ClientSession() as session:
					if not await scraper.login(session):
						await turn_context.send_activity("❌ Authentication failed. Please check your credentials or update your auth token.")
						return
					
					quotas = await scraper.get_survey_quotas(session, survey_id)
					
					if not quotas:
						await turn_context.send_activity(f"❌ No quota data found for survey {survey_id}")
						return
					
					# Format and send quota information
					quota_text = format_quotas_for_teams(quotas, survey_id)
					await turn_context.send_activity(quota_text)
					
			except Exception as e:
				await turn_context.send_activity(f"❌ Error fetching quotas: {str(e)}")
			return

		if lower.startswith("update "):
			# Manual update command: "update 12345 status=live completes=50 target=100"
			try:
				parts = text.split(" ", 1)[1].strip()
				survey_id = parts.split(" ")[0]
				update_data = {}
				
				# Parse key=value pairs
				for pair in parts.split()[1:]:
					if "=" in pair:
						key, value = pair.split("=", 1)
						update_data[key] = value
				
				# Send update to all subscribers
				refs = await self._store.get_subscribers(survey_id)
				
				if refs:
					message = f"Manual update for Survey {survey_id}: " + " | ".join([f"{k}={v}" for k, v in update_data.items()])
					
					for ref in refs:
						async def send_proactive(turn_context):
							await turn_context.send_activity(message)
						
						await self._adapter.continue_conversation(ref, send_proactive)
					
					await turn_context.send_activity(f"Update sent to {len(refs)} subscribers of survey {survey_id}")
				else:
					await turn_context.send_activity(f"No subscribers found for survey {survey_id}")
					
			except Exception as e:
				await turn_context.send_activity(f"Error processing update: {str(e)}")
			return

		await turn_context.send_activity("Unknown command. Say 'help' for options.")


