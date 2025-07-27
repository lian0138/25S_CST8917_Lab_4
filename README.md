# Project Report: Real-Time Trip Event Analysis (CST8917 Lab 4)

## 1. Architecture and Logic App Steps

This solution provides **real-time analysis of taxi trip events** to flag and notify about interesting or suspicious rides using Azure cloud components.

- **Event Hub** receives and ingests trip event data.
- **Logic App** orchestrates the workflow, calling the analysis function and sending notifications.
- **Azure Function** applies business logic to each trip event and determines “insights”.
- **Microsoft Teams** (via Adaptive Cards) receives notifications for operations staff.

**Workflow Overview:**

1. **Trigger:** Logic App triggers when new events are available in Event Hub (batched per minute).
2. **Decode Base64:** Decodes event data to string.
3. **Parse JSON:** Parses decoded string into trip fields (`vendorID`, `tripDistance`, `passengerCount`, `paymentType`).
4. **Analyze Trip:** Sends parsed trip to Azure Function (`analyze_trip`).
5. **For Each Trip:**
    - Check if `isInteresting` is true:
        - **Yes:**  
          - If "SuspiciousVendorActivity" in `insights`, notify as *Suspicious*  
          - Else, notify as *Interesting Trip*
        - **No:**  
          - Notify as *Trip Analyzed - No Issues*

**Workflow Diagram:**  
![Logic App Flowchart](https://raw.githubusercontent.com/lian0138/25S_CST8917_Lab_4/refs/heads/main/flowchart.png)

---

## 2. Azure Function Logic (`analyze_trip`)

- Receives a trip (or batch).
- Extracts trip data fields.
- Applies rules:
    - **LongTrip**: `tripDistance > 10`
    - **GroupRide**: `passengerCount > 4`
    - **CashPayment**: `paymentType == 2`
    - **SuspiciousVendorActivity**: cash payment (`2`) and `tripDistance < 1`
- Returns:  
  Each trip result includes `insights` (flags), `isInteresting` (bool), and a `summary`.

**Logic Excerpt:**
```python
if distance > 10:
    insights.append("LongTrip")
if passenger_count > 4:
    insights.append("GroupRide")
if payment == "2":
    insights.append("CashPayment")
if payment == "2" and distance < 1:
    insights.append("SuspiciousVendorActivity")
```

---

## 3. Example Input/Output

**Example Input** (from `send_to_eventhub.py` sending to Event Hub):
```json
{ "ContentData": { "vendorID": "V003", "tripDistance": "0.4", "passengerCount": "1", "paymentType": "2" } }
```

**Function Output:**
```json
[
  {
    "vendorID": "V003",
    "tripDistance": 0.4,
    "passengerCount": 1,
    "paymentType": "2",
    "insights": ["CashPayment", "SuspiciousVendorActivity"],
    "isInteresting": true,
    "summary": "2 flags: CashPayment, SuspiciousVendorActivity"
  }
]
```

**Sample Notification (Teams Adaptive Card):**

```
⚠️ Suspicious Vendor Activity Detected
- Vendor: V003
- Distance (mi): 0.4
- Passengers: 1
- Payment: 2
- Insights: CashPayment, SuspiciousVendorActivity
```

---

## 4. Extra Insights & Suggested Improvements

- **Cost Awareness:**  
  Logic App action-based pricing can add up in production—consider minimizing per-item actions and monitoring usage in Azure Cost Management.

**Files produced for this project:**
- `workFlow.json` – Logic App definition
- `send_to_eventhub.py` – Testing code for event generation
- `flowchart.png` – Flowchart of Logic App process

## 5. Youtube link
https://www.youtube.com/watch?v=TSRMwbwIPyM