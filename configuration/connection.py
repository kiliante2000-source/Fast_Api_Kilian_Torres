import mysql 


class DatabaseConnection:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.my_db = None     # store the connection object

    async def connect(self):
        if self.my_db is None:
            self.database = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database = self.database
        )
        return self.database