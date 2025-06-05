# Data Ingestion API System

A RESTful API system designed to accept and process ingestion requests in batches, prioritize based on urgency, and respect rate limits — all with real-time status tracking.

### Features

1. Ingest a list of IDs with assigned priority (HIGH, MEDIUM, LOW)  
2. Automatically splits requests into batches of 3 IDs  
3. Processes one batch every 5 seconds (rate-limited)  
4. Prioritizes ingestion by priority and creation time  
5. Provides live status updates for each batch  

### How to Run Locally

1. Clone the repo  

git clone https://github.com/tanika04/Data_Ingestion_API_System.git
cd Data_Ingestion_API_System

2. Intall dependencies
pip install -r requirements.txt

3. Run the server
uvicorn main:app --reload

4. Run tests
python test_api.py

### API Endpoints
POST /ingest

Submit ingestion request with JSON body:

{

  "ids": [1, 2, 3, 4, 5],
  
  "priority": "HIGH"
  
}

Response:

{

  "ingestion_id": "your-generated-id"

  
}


GET /status/{ingestion_id}
 
Check ingestion status. Response example:

{

  "ingestion_id": "your-generated-id",
  
  "status": "triggered",
  
  "batches": [
    {"batch_id": "uuid1", "ids": [1, 2, 3], "status": "completed"},
    {"batch_id": "uuid2", "ids": [4, 5], "status": "triggered"}
  ]
}


