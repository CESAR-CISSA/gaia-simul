# Gaia CEP App

A real-time Complex Event Processing (CEP) application built with PySiddhi for MQTT event stream analysis.

## Overview

This application processes MQTT event streams using the Siddhi CEP engine to detect patterns and anomalies in real-time. It's designed to identify potential security threats like brute force attacks by analyzing MQTT message patterns.

## Architecture

The application consists of several key components:

- **MQTT Stream Definition**: Defines the structure of MQTT events to be processed
- **Siddhi Query Engine**: Processes event streams using CEP queries
- **Event Sender**: Reads events from CSV files and sends them to the Siddhi runtime
- **Query Callback**: Handles the results of processed queries

## Key Components

### MQTTStream

Defines the structure of MQTT events with typed attributes.

### SiddhiQuery

Encapsulates Siddhi CEP queries with validation.

### EventSender

Reads events from CSV files and sends them to the Siddhi runtime for processing.

### StreamSchema

Base interface for stream definitions.

## Current Implementation

The current implementation:

1. Defines an MQTT stream with attributes for source address, message type, message length, and QoS flag
2. Creates a Siddhi query that detects when a source sends 50+ messages with message type 2 within a 0.5 second window
3. Processes events from a CSV file
4. Reports detected patterns through a callback mechanism

## Requirements

- Python 3.6+
- PySiddhi 5.1.0
- Additional dependencies listed in requirements.txt

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/gaia-cep.git
cd gaia-cep
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure you have Java installed (required by PySiddhi)

## Usage

1. Prepare your event data in CSV format in the `data/eventos.csv` file
2. Run the application:
```bash
python app.py
```

## Configuration

You can modify the Siddhi query in `app.py` to detect different patterns or adjust the detection window.

Example query (currently implemented):
```
@info(name = 'query1')
from cseEventStream[mqtt_messagetype == 2]#window.time(0.5 sec)
select srcAddr, mqtt_messagetype, mqtt_messagelength, mqtt_flag_qos, count() as msgCount
group by srcAddr
having msgCount >= 50
insert into outputStream;
```

## Data Format

The CSV file should contain columns matching the attribute names defined in the MQTT stream:
- srcAddr
- mqtt_messagetype
- mqtt_messagelength
- mqtt_flag_qos

## Project Structure

```
gaia-cep-app/
├── app.py                 # Main application entry point
├── mqtt_stream.py         # MQTT stream definition
├── stream_schema.py       # Base stream schema interface
├── sender.py              # Event sender implementation
├── siddhi_query.py        # Siddhi query definition
├── query_callback.py      # Callback for query results
├── data/
│   └── eventos.csv        # Event data in CSV format
└── requirements.txt       # Project dependencies
```

## License

[Specify your license here]

## Contributors

[List contributors here]