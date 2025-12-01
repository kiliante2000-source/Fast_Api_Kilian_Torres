import mysql 


class DatabaseConnection:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    async def connect(self):
        if self.database is None:
            self.database = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
        return self.database