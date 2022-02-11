from os import makedirs
from sqlite3 import connect, PARSE_COLNAMES
from pandas import read_sql
from pandas.io.sql import DatabaseError


class SQLite:
    __slots__ = {'__conn', '__cur', '__groups', 'name', '_backup_parent_dir'}

    def __init__(self, name, groups):
        self.name = name
        self.__conn = connect(
            f'{name}.db', isolation_level=None, detect_types=PARSE_COLNAMES
        )
        self.__cur = self.__conn.cursor()
        self.__groups = groups
        self.__create_users_tables()

    def __create_users_tables(self):
        for group_id in self.__groups:
            sql_command = f'''
            CREATE TABLE IF NOT EXISTS 'users{group_id}' (
            user_id INTEGER NOT NULL PRIMARY KEY, username TEXT, 
            messages INTEGER DEFAULT 0, replies INTEGER DEFAULT 0
            )
            '''
            self.__run_command(sql_command)

    def __clear_users_table(self, group_id):
        return self.__run_command(
            f"""DELETE FROM 'users{group_id}'"""
        )

    def __run_command(self, command):
        try:
            self.__cur.execute(command)
            self.__conn.commit()
        except Exception as e:
            return e

    @staticmethod
    def __dataset_clean(df):
        df["total"] = df['messages'] + df['replies']
        df = df[(df.username != "None") & (df.username != "0")]
        return df.sort_values('total', ascending=False).rename(
            columns={'username': 'name', 'messages': 'm', 'replies': 'r'}
        )

    @property
    def groups(self):
        return self.__groups

    def user_create(self, chat_id, user_id, username: str):
        return self.__run_command(
            f"""
            INSERT OR IGNORE INTO 'users{chat_id}' (user_id, username)
            VALUES ('{user_id}', '{username}')
            """
        )

    def user_create_signature(self, chat_id, user_id, signature):
        signature = signature if signature is not None else "0"
        new_id = f'{len(signature)}{ord(signature[-1])}'
        return self.__run_command(
            f"""
            INSERT OR IGNORE INTO 'users{chat_id}' (user_id, username)
            VALUES ('{new_id}', '{signature}')
            """
        )

    def user_delete(self, chat_id, user_id):
        return self.__run_command(
            f"""
            DELETE FROM 'users{chat_id}' 
            WHERE user_id='{user_id}'
            """
        )

    def increment_user_messages(cls, chat_id, user_id, signature=None):
        return cls.__run_command(f"""
        UPDATE 'users{chat_id}'
        SET messages = messages + 1 
        WHERE {f'user_id={user_id}' if not signature else f"username='{signature}'"}
        """)

    def increment_user_replies(cls, chat_id, user_id, signature=None):
        return cls.__run_command(f"""
        UPDATE 'users{chat_id}'
        SET replies = replies + 1 
        WHERE {f'user_id={user_id}' if not signature else f"username='{signature}'"}
        """)

    def backup_activity(self, group_id, path, date_time):
        db_df = read_sql(f"SELECT * FROM 'users{group_id}'", self.__conn)
        try:
            makedirs(path)
        except FileExistsError:
            pass
        finally:
            db_df = self.__dataset_clean(db_df)
            db_df.to_csv(f'{path}/Day {date_time[1]}.csv', index=False)
            self.__clear_users_table(group_id)

    def get_activity_today(self, group_id):
        try:
            db_df = read_sql(f"SELECT * FROM 'users{group_id}'", self.__conn)
        except DatabaseError:
            raise ValueError("Пожалуйста, введите ID группы.")
        else:
            return self.__dataset_clean(db_df).drop(
                columns=['user_id', 'total']
            ).to_markdown(index=False)
