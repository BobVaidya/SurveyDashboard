from __future__ import annotations

import os
from typing import Callable

from botbuilder.core import BotFrameworkAdapterSettings, TurnContext
from botbuilder.core.bot_framework_adapter import BotFrameworkAdapter


def create_adapter() -> BotFrameworkAdapter:
	app_id = os.getenv("MICROSOFT_APP_ID", "")
	app_password = os.getenv("MICROSOFT_APP_PASSWORD", "")
	settings = BotFrameworkAdapterSettings(app_id, app_password)
	adapter = BotFrameworkAdapter(settings)

	async def on_error(context: TurnContext, error: Exception):
		await context.send_activity("The bot encountered an error or bug.")
		await context.send_activity("To continue to run this bot, please fix the bot source code.")

	adapter.on_turn_error = on_error
	return adapter


