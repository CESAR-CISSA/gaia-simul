import csv
from PySiddhi.DataTypes.LongType import LongType
import asyncio
# from typing import Dict

from mqtt_stream import MQTTStream

class EventSender:
    def __init__(self, input_handler, stream: MQTTStream):
        self.input_handler = input_handler
        self.stream = stream

    def _get_attribute_order(self):
        return [name for name in self.stream.get_attributes().keys()]

    def _format_event(self, attribute_order, values):
        """Formata um evento de acordo com os tipos definidos."""
        event = []
        for idx, attr_name in enumerate(attribute_order):
            tipo = self.stream.get_attributes()[attr_name]
            val = values[idx]
            if tipo == "long":
                if val == '':
                    continue
                else:
                    event.append(LongType(int(float(val))))
            else:
                event.append(val)
        return event

    async def send_event_from_csv(self, csv_path: str):
        """
        Lê o CSV linha por linha de forma assíncrona e envia eventos ao Siddhi.
        """
        attribute_order = self._get_attribute_order()

        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                values = [row[field] for field in attribute_order]
                event = self._format_event(attribute_order, values)
                self.input_handler.send(event)
                await asyncio.sleep(0)  # Yield para o event loop

    def _count_records(self, csv_path: str) -> int:
        """Conta o número de registros no CSV, ignorando o cabeçalho."""
        with open(csv_path, newline='') as csvfile:
            return sum(1 for _ in csvfile) - 1
