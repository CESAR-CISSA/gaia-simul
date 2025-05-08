from PySiddhi.core.SiddhiManager import SiddhiManager
from mqtt_stream import MQTTStream, SiddhiType
from net_helper import NetworkInterfaceManager
from scapy_sniffer import MQTTSniffer
from query_callback import QueryCallbackImpl
from siddhi_query import SiddhiQuery
from sender import EventSender
from time import sleep
import asyncio

async def main():
    # Instancia o stream MQTT
    mqtt_stream = MQTTStream("cseEventStream")
    mqtt_stream.add_mqtt_attribute("sniff_ts", SiddhiType.STRING)
    mqtt_stream.add_mqtt_attribute("srcAddr", SiddhiType.STRING)
    mqtt_stream.add_mqtt_attribute("dstAddr", SiddhiType.STRING)
    mqtt_stream.add_mqtt_attribute("mqtt_messagetype", SiddhiType.INT)
    mqtt_stream.add_mqtt_attribute("mqtt_messagelength", SiddhiType.LONG)
    mqtt_stream.add_mqtt_attribute("mqtt_flag_qos", SiddhiType.INT)

    # Define a query Siddhi
    query = SiddhiQuery(
        name="query1",
        query_string="@info(name = 'query1') " +
                    #  "from (cseEventStream[mqtt_messagetype == 2])#window.time(0.5 sec) " +
                     "from (cseEventStream[mqtt_messagetype == 3]) " +
                     "select sniff_ts, srcAddr, dstAddr, mqtt_messagetype, mqtt_messagelength, mqtt_flag_qos, count() as msgCount " +
                     "group by srcAddr " +
                     "having msgCount >= 10 " +
                     "insert into outputStream;"
    )

    siddhi_manager = SiddhiManager()
    siddhi_app = str(mqtt_stream) + " " + str(query)
    siddhi_runtime = siddhi_manager.createSiddhiAppRuntime(siddhi_app)

    # Define os nomes das colunas na ordem usada na stream
    column_names = mqtt_stream.get_attribute_names()

    # Adiciona callback com os nomes reais
    # siddhi_runtime.addCallback(query.name, QueryCallbackImpl(column_names=column_names))
    siddhi_runtime.addCallback(query.name, QueryCallbackImpl())
    input_handler = siddhi_runtime.getInputHandler(mqtt_stream.stream_name)

    sender = EventSender(input_handler, mqtt_stream)
    siddhi_runtime.start()

    manager = NetworkInterfaceManager()
    selected_interface = manager.choose_interface_cli()


    sniffer = MQTTSniffer(interface=selected_interface)
    sniffer.start_sniffing(selected_interface, sender)


    # await sender.send_event_from_csv("./data/eventos.csv") # when not containerized
    # await sender.send_event_from_csv("./app/data/eventos.csv") # when containerized

    sleep(5)
    siddhi_manager.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
