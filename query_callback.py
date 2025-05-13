import csv
import os
import numpy as np
from PySiddhi.core.query.output.callback.QueryCallback import QueryCallback
from PySiddhi.core.util.EventPrinter import PrintEvent


import pandas as pd
import pickle

IP_ATTACKER = '172.20.0.6'
FILE_OUTPUT_CSV = 'output_cep_analysis.csv'
MODEL_FILE_PATH = 'model/model.pickle'

def load_model_and_scaler(path):

    with open(path, 'rb') as handle:
        pickle_obj = pickle.load(handle)

    return pickle_obj['model'], pickle_obj['scaler']


model, scaler = load_model_and_scaler('model/model.pickle')

def analisys_packet(data, model, ip_attacker, scaler, srcAddr):
        


        data = pd.DataFrame([data], columns=['mqtt_messagetype', 'mqtt_messagelength', 'mqtt_flag_passwd'])
        

        #print(data)
        out_cep_scaled = scaler.transform(data)

        #print(out_cep_scaled)
        model_pred = model.predict(out_cep_scaled)

        #   print(model_pred)
        
        model_pred = [1 if p == -1 else 0 for p in model_pred]

        if ip_attacker == srcAddr:
            is_attack = 1
        else:
            is_attack = 0

        return model_pred[0], is_attack


def write_output_analisys(filename, data):
        try:
            with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(data) 
        except Exception as e:
            print(f"Erro ao adicionar dados ao arquivo CSV: {e}")


class QueryCallbackImpl(QueryCallback):
    def receive(self, timestamp, inEvents, outEvents):
        
        print('Event In')
        if inEvents is not None:
            for event in inEvents:
                raw_data = event.getData()
                np_array = np.array(raw_data)  # converte para numpy.ndarray
                print(f"Evento em NumPy: {np_array}")

        print('Event Out')

        if outEvents is not None:
            for event in outEvents:
                raw_data = event.getData()
                np_array = np.array(raw_data)  # converte para numpy.ndarray
                print(f"Evento em NumPy: {np_array}")
        else:
            pass