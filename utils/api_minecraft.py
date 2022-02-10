from mcstatus import MinecraftServer
from typing import Tuple


class MinecraftInfo:
    __ip = "23.88.80.152"
    __port = "25565"
    __server = MinecraftServer.lookup(f"{__ip}:{__port}")
    _server_status = None

    @classmethod
    def __set_server_status(cls):
        cls._server_status = cls.__server.status()

    @classmethod
    def _get_online_players_info(cls):
        players_count = cls._server_status.players.online

        if players_count:
            players_count = f"{' '.join(cls._plural(players_count, ('игрок', 'игрока', 'игроков')))}"
            return f"Онлайн {players_count}:\n{', '.join(cls.__server.query().players.names)}"
        else:
            return f"На сервере никого нет, лишь зомби сидят в уютных могилках("

    @staticmethod
    def _plural(n: int, words: Tuple[str, str, str]):
        if n % 10 == 1 and n % 100 != 11:
            p = 0
        elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
            p = 1
        else:
            p = 2
        return str(n), words[p]

    @classmethod
    def get_data_message_info(cls):
        cls.__set_server_status()

        return {
            "players": cls._get_online_players_info(), "version": "1.15.2", "ip": cls.__ip,
            "ping": round(cls._server_status.latency),
            "map": "http://23.88.80.152:8123/?worldname=world&mapname=surface&zoom=6&x=-530&y=64&z=380",
        }
