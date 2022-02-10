from aiogram.utils.markdown import hlink
from utils.api_minecraft import MinecraftInfo
from loader import bot, config


# scheduled action, more information in the app.py file
async def get_minecraft_info(*args):
    minecraft_data = MinecraftInfo.get_data_message_info()
    message_config = {
        "template": "{}\n\n{} {} с Minecraft версии {}\n✨ {}, пинг {} мс",
        "hello": "✨ Хочешь на сервер?\n✨ Подключайся по адресу",
        "map": "http://23.88.80.152:8123/?worldname=world&mapname=surface&zoom=6&x=-530&y=64&z=380",
    }
    for chat_id in config.groups:
        await bot.send_message(chat_id=chat_id, text=message_config["template"].format(
            minecraft_data["players"], message_config["hello"], minecraft_data["ip"], minecraft_data["version"],
            hlink('Карта сервера', message_config["map"]), minecraft_data["ping"],
        ), parse_mode="html")
