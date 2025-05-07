import csv
import os
from PySiddhi.core.query.output.callback.QueryCallback import QueryCallback

class QueryCallbackImpl(QueryCallback):
    def __init__(self, output_file='output/resultados.csv', column_names=None):
        super().__init__()
        self.output_file = output_file
        self.column_names = column_names or []
        self.header_written = False

        # Garante que o diretório de saída exista
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)

    def receive(self, timestamp, inEvents, outEvents):
        if outEvents:
            with open(self.output_file, mode='a', newline='') as csvfile:
                writer = csv.writer(csvfile)

                for event in outEvents:
                    data = event.getData()
                    row = [timestamp] + list(data)

                    if not self.header_written:
                        header = ['timestamp'] + self.column_names
                        writer.writerow(header)
                        self.header_written = True

                    writer.writerow(row)
