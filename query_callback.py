import csv
import os
import numpy as np
from PySiddhi.core.query.output.callback.QueryCallback import QueryCallback
from PySiddhi.core.util.EventPrinter import PrintEvent


class QueryCallbackImpl(QueryCallback):
    def receive(self, timestamp, inEvents, outEvents):
        for event in inEvents:
            raw_data = event.getData()
            np_array = np.array(raw_data)  # converte para numpy.ndarray
            print(f"Evento em NumPy: {np_array}")