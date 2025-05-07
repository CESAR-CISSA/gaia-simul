from scapy.all import sniff, IP, TCP, Raw
from scapy.contrib.mqtt import MQTT
from datetime import datetime
import logging

CONTROL_PACKET_TYPE = {
    1: 'CONNECT',
    2: 'CONNACK',
    3: 'PUBLISH',
    4: 'PUBACK',
    5: 'PUBREC',
    6: 'PUBREL',
    7: 'PUBCOMP',
    8: 'SUBSCRIBE',
    9: 'SUBACK',
    10: 'UNSUBSCRIBE',
    11: 'UNSUBACK',
    12: 'PINGREQ',
    13: 'PINGRESP',
    14: 'DISCONNECT',
    15: 'AUTH'  # Added in v5.0
}


QOS_LEVEL = {
    0: 'At most once delivery',
    1: 'At least once delivery',
    2: 'Exactly once delivery'
}


class MQTTSniffer:
    def __init__(self, log_file="captura_scapy.log", interface="br-a506fe339fbf"):
        self.log_file = log_file
        #logging.basicConfig(filename=self.log_file, level=logging.INFO, format='[%(asctime)s] - %(message)s')
        logging.basicConfig(filename=self.log_file, level=logging.INFO, format='%(message)s')
        logging.info("Iniciando o MQTTSniffer...")
        logging.info("Timestamp\t Source IP\t Destination IP\t MQTT Type\t MQTT Length\t MQTT QoS")
    

    def packet_callback(self, packet):
        if IP in packet and TCP in packet and (packet[TCP].dport == 1883 or packet[TCP].sport == 1883) and MQTT in packet:
            #timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

            '''
            # Obtém o endereço IP de origem e destino
            # Obtém o timestamp do pacote TCP
            '''
            sipaddr = packet[IP].src
            dipaddr = packet[IP].dst
            tcp_time = str(packet[TCP].time)
            
            '''
            # Informações sobre o pacote MQTT
            # Obtém o tipo do pacote MQTT
            # Obtém o tamanho do pacote MQTT
            # Obtém o QoS do pacote MQTT
            '''
            mqtt_type = packet[MQTT].type # Obtém o tipo do pacote MQTT                  
            
            # Ignora os pacotes sem length (tipos 2, 8, 9, 12, 13 e 14)
            if mqtt_type not in [2,8,9,12,13,14]:
                mqtt_length = packet[MQTT].length
                mqtt_qos = packet[MQTT].QOS

                print(f"{tcp_time}\t {sipaddr}\t {dipaddr}\t {mqtt_type}\t {mqtt_length}\t {mqtt_qos}")
                logging.info(f"{tcp_time}\t {sipaddr}\t {dipaddr}\t {mqtt_type}\t {mqtt_length}\t {mqtt_qos}")
    

    def start_sniffing(self, iface):
        print(f"Capturando pacotes da interface {iface} na porta 1883 e registrando em {self.log_file}...")
        try:
            sniff(iface=iface, filter="tcp and port 1883", prn=self.packet_callback)
        except KeyboardInterrupt:
            print("\nCaptura interrompida.")
            logging.info("Captura interrompida pelo usuário.")


# def main(iface):
#     sniffer = MQTTSniffer(interface=iface)
#     sniffer.start_sniffing(iface)


# if __name__ == "__main__":
#     # iface = "br-f07280c660ff"  
#     iface = "br-a506fe339fbf" 
#     main(iface)