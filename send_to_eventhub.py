from azure.eventhub import EventHubProducerClient, EventData
import json
import time



events = [
    {"ContentData": {"vendorID": "V001", "tripDistance": "2", "passengerCount": "2", "paymentType": "1"}},
    {"ContentData": {"vendorID": "V002", "tripDistance": "15.2", "passengerCount": "6", "paymentType": "1"}},
    {"ContentData": {"vendorID": "V003", "tripDistance": "0.4", "passengerCount": "1", "paymentType": "2"}}
]

producer = EventHubProducerClient.from_connection_string(CONNECTION_STR, eventhub_name=EVENTHUB_NAME)
try:
    for i, evt in enumerate(events):
        batch = producer.create_batch()
        batch.add(EventData(json.dumps(evt)))
        producer.send_batch(batch)
        print(f"✅ Already sent message {i+1}: {json.dumps(evt, ensure_ascii=False, indent=2)}")
        if i < len(events) - 1:
            time.sleep(3) # Sleep for 3 seconds between messages
    print("✅ All meesages sent successfully.")
except Exception as e:
    print("❌ Messages sent failure", str(e))
finally:
    producer.close()