import psycopg2

class Database:
    def __init__(self, settings: dict) -> None:
        self.__host = settings["host"]
        self.__port = settings["port"]
        self.__user = settings["user"]
        self.__password = settings["password"]
        self.__database = settings["database"]

    def __connect(self):
        try:
            return psycopg2.connect(host=self.__host, port=self.__port, user=self.__user, password=self.__password, database=self.__database)
        except:
            raise NameError("Could not connect to database")

    def __query(self, query: int) -> str:
        try:
            with open(f"src/config/map.sql", "r") as f:
                return f.readlines()[query - 1].strip()
        except:
            raise NameError(f"Error reading line {query} of query map")

    def get(self, query: int, payload: list=[]) -> list:
        connection = self.__connect()
        cursor = connection.cursor()
        query = self.__query(query=query)

        try:
            cursor.execute(query, payload)
            result = cursor.fetchall()
        except:
            raise NameError(f"Error getting {payload} from line {query} of query map")

        cursor.close()
        connection.close()
        return result

    def execute(self, query: int, payload: list=[]) -> None:
        connection = self.__connect()
        cursor = connection.cursor()
        query = self.__query(query=query)

        try:
            cursor.execute(query, payload)
        except:
            raise NameError(f"Error executing line {query} of query map with payload {payload}")

        connection.commit()
        cursor.close()
        connection.close()
