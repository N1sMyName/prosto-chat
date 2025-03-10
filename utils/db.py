import asyncio
import os

import aioodbc
from dotenv import load_dotenv
from flask import jsonify

from utils.queries import SQLQuery


class Database:
    def __init__(self):
        load_dotenv()
        self.server = os.getenv('DB_SERVER')
        self.port = os.getenv('DB_PORT')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.database = 'master'
        self.connection_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={self.server},{self.port};UID={self.user};PWD={self.password};DATABASE={self.database}'

    async def connect(self):
        try:
            connection = await aioodbc.connect(dsn=self.connection_string, loop=asyncio.get_event_loop())
            print("Connection successful")
            return connection
        except Exception as e:
            print(f"Connection failed: {e}")
            return None

    async def disconnect(self, connection):
        if connection:
            await connection.close()
            print("Connection closed")

    async def execute_query(self, query_object: SQLQuery):
        connection = await self.connect()
        if not connection:
            return jsonify({'success': False, 'message': 'Failed to establish database connection'}), 500
        try:
            async with connection.cursor() as cursor:
                if query_object.params:
                    await cursor.execute(query_object.query, query_object.params)
                else:
                    await cursor.execute(query_object.query)
                await connection.commit()
                return jsonify({'success': True, 'message': query_object.message}), 201
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500
        finally:
            await self.disconnect(connection)

    async def fetch_query(self, query_object: SQLQuery):
        connection = await self.connect()
        if not connection:
            return jsonify({'success': False, 'message': 'Failed to establish database connection'}), 500
        try:
            async with connection.cursor() as cursor:
                if query_object.params:
                    await cursor.execute(query_object.query, query_object.params)
                else:
                    await cursor.execute(query_object.query)
                rows = await cursor.fetchall()
                data = [self.row_to_dict(row, cursor) for row in rows]
                return jsonify({'success': True, 'data': data}), 200
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500
        finally:
            await self.disconnect(connection)

    @staticmethod
    def row_to_dict(row, cursor):
        columns = [column[0] for column in cursor.description]
        return {columns[i]: row[i] for i in range(len(columns))}
