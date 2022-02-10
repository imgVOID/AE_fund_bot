from aiosqlite import connect


class SQLiteAsync:
    @staticmethod
    async def __run_command(command):
        try:
            async with connect("activity.db") as database:
                await database.execute(command)
                await database.commit()
        except Exception as e:
            return e

    @classmethod
    async def create_new_user(cls, chat_id, user_id, username=None, signature=None):
        username = signature if not username else username
        await cls.__run_command(f"""
        INSERT OR IGNORE INTO 'users{chat_id}' (user_id, username)
        VALUES ('{user_id}', '{username}')
        """)

    @classmethod
    async def increment_user_messages(cls, chat_id, user_id, signature=None):
        return await cls.__run_command(f"""
        UPDATE 'users{chat_id}'
        SET messages = messages + 1 
        WHERE {f'user_id={user_id}' if not signature else f"username='{signature}'"}
        """)

    @classmethod
    async def increment_user_replies(cls, chat_id, user_id, signature=None):
        return await cls.__run_command(f"""
        UPDATE 'users{chat_id}'
        SET replies = replies + 1 
        WHERE {f'user_id={user_id}' if not signature else f"username='{signature}'"}
        """)

    @classmethod
    async def delete_user(cls, chat_id, user_id):
        return await cls.__run_command(f"""
        DELETE FROM 'users{chat_id}' 
        WHERE user_id='{user_id}'
        """)
