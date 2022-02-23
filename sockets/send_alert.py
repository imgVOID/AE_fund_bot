from loader import bot, config


async def send_alert_vandals(vandal_name, region_name):
    for chat_id in config.groups_alarm:
        await bot.send_message(chat_id=chat_id, text=f"{vandal_name} пришел сюда: {region_name}")
