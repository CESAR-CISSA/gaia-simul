from scapy.all import sniff, IP, TCP, Raw
from scapy.contrib.mqtt import MQTT
from net_helper import NetworkInterfaceManager
from sender import EventSender
import numpy as np
import logging
import time
import pandas as pd

import csv
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
        

        print(data)
        out_cep_scaled = scaler.transform(data)

        print(out_cep_scaled)
        model_pred = model.predict(out_cep_scaled)

        print(model_pred)
        
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

class MQTTSniffer:
    def __init__(self, log_file, iface, sport, dport):
        self.log_file = log_file
        self.iface = iface
        self.dport = dport
        self.sport = sport
        #self.sender = sender

        log_array = []
        self.log_array = log_array

        logging.basicConfig(filename=self.log_file, level=logging.INFO, format='%(message)s')
        logging.info("Iniciando o MQTTSniffer...")
        logging.info("Timestamp\t Source IP\t Destination IP\t MQTT Type\t MQTT Length\t MQTT QoS")

    def packet_callback(self, packet):
        if IP in packet and TCP in packet and (packet[TCP].sport == self.sport or packet[TCP].dport == self.dport) and MQTT in packet:
            sipaddr = packet[IP].src
            dipaddr = packet[IP].dst
            tcp_time = str(packet[TCP].time)
            mqtt_type = packet[MQTT].type
            mqtt_qos = packet[MQTT].QOS

            

            #exclude_types = [2, 8, 9, 12, 13, 14]  # Exclude these MQTT types

            try:
                mqtt_length = packet[MQTT].length
                
                
                try:
                    mqtt_passwd = packet[MQTT].passwordflag
                except:
                    mqtt_passwd = 0

                self.siddhi_sender.send_event([str(tcp_time), str(sipaddr), str(dipaddr), mqtt_type, mqtt_length, mqtt_qos,  mqtt_passwd])

                print('passou do SIDHI')

                # if mqtt_type == 3:
                #data = [mqtt_type, mqtt_length, mqtt_passwd]
                #model_pred, is_attack = analisys_packet(data, model, IP_ATTACKER, scaler, sipaddr)

                #data_output = [sipaddr, dipaddr, mqtt_type, mqtt_length, mqtt_qos, model_pred, is_attack]

                #data_output = [model_pred, is_attack]
                #write_output_analisys(FILE_OUTPUT_CSV, data_output)

                #self.log_array.append((tcp_time, sipaddr, dipaddr, mqtt_type, mqtt_length, mqtt_qos))

                #print(f"{tcp_time}\t {sipaddr}\t {dipaddr}\t {mqtt_type}\t {mqtt_length}\t {mqtt_qos}")
                #logging.info(f"{tcp_time}\t {sipaddr}\t {dipaddr}\t {mqtt_type}\t {mqtt_length}\t {mqtt_qos}")
            except AttributeError:
                None

           
                
    
    
    def start_sniffing(self, sender: EventSender):
        self.siddhi_sender = sender

        print(sender)
        print(f"Capturando pacotes da interface {self.iface} na porta {self.dport} e registrando em {self.log_file}...")
        try:
            print('entra')
            sniff(iface=self.iface, filter=f"tcp and port {self.dport}", prn=self.packet_callback)
            print('testeando')
        except KeyboardInterrupt:
            print("\nCaptura interrompida.")
            logging.info("Captura interrompida pelo usuário.")
        finally:
            nparray = np.array(self.log_array)
            logging.info("Finalizando a captura.")


# def main(log_file, iface, sport, dport):
#     sniffer = MQTTSniffer(log_file, iface, sport, dport)
#     sniffer.start_sniffing()


# if __name__ == "__main__":
#     manager = NetworkInterfaceManager()
#     selected_interface = manager.choose_interface_cli()

#     log_file = "captura_scapy.log"
#     iface = selected_interface
#     sport = 1883
#     dport = 1883
#     main(log_file, iface, sport, dport)