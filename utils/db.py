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
        self.connection = None

    async def connect(self):
        try:
            self.connection = await aioodbc.connect(dsn=self.connection_string, loop=asyncio.get_event_loop())
            print("Connection successful")
        except Exception as e:
            print(f"Error: {e}")

    async def disconnect(self):
        if self.connection:
            await self.connection.close()
            print("Connection closed")

    async def execute_query(self, query_object: SQLQuery):
        if not self.connection:
            await self.connect()
        try:
            async with self.connection.cursor() as cursor:
                if query_object.params:
                    await cursor.execute(query_object.query, query_object.params)
                else:
                    await cursor.execute(query_object.query)
                await self.connection.commit()
                return jsonify({'success': True, 'message': 'Entry created successfully'}), 201
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'success': False, 'message': str(e)}), 500
        finally:
            await self.disconnect();

    async def fetch_query(self, query_object: SQLQuery):
        if not self.connection:
            await self.connect()
        try:
            async with self.connection.cursor() as cursor:
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
            await self.disconnect()

    @staticmethod
    def row_to_dict(row, cursor):
        columns = [column[0] for column in cursor.description]
        return {columns[i]: row[i] for i in range(len(columns))}
