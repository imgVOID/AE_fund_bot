hello_message_group = """
✨ Приветствуем в увлекательной и волшебной галактике Фонда аказуальной эмерджентности! ✨

В одном из самых увлекательных магических чатов мы шутим, играем в Minecraft, обсуждаем новости, философию, оккультизм, язычество и другие интересные темы. 
Мы рады приветствовать представителей всех традиций и направлений, расскажите о себе - и добро пожаловать в Фонд!

🌾 А в целом, порой мы просто так раздаём деньги в чате))
Наш канал: https://t.me/+DStS5X95A2kxZWYy
Проекты партнёров: https://t.me/hill_sidhe_wicca/264
https://t.me/mudrostvbezumii
"""

hello_message_bot = """
Добро пожаловать, {}!
Я - бот Фонда. Меня еще разрабатывают ;)
Напишите символ слеша, чтобы увидеть доступные команды.
"""


def get_hello_message_group():
    return hello_message_group


def get_hello_message_bot():
    return hello_message_bot


if __name__ == "__main__":
    print(hello_message_group)
    print(hello_message_bot)
