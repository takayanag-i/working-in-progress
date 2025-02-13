# Room Schema

## JSON Data Example

```json
{
  "id": "12345678",
  "docType": "room_schema",
  "ttid": "sry_2025_001",
  "rooms": [
    {
      "discipline": "芸術",
      "name": "書道室",
      "consectiveChange": false
    },
    {
      "name": "予5",
      "consectiveChange": true
    }
  ]
}
```

## Object Structure

### Room Schema

| Key       | Business Name | Data Type       | Required | Description                        |
| --------- | ------------- | --------------- | -------- | ---------------------------------- |
| `id`      | ID            | String          | Y        | Required by Cosmos DB.             |
| `docType` | Document Type | String          | Y        |                                    |
| `ttid`    | Timetable ID  | String          | Y        | **Partition Key**.                 |
| `rooms`   | Room List     | Array\<Object\> | Y        | Contains at least one room object. |

### Room

| Key                | Business Name           | Data Type | Required | Description                          |
| ------------------ | ----------------------- | --------- | -------- | ------------------------------------ |
| `discipline`       | Discipline              | String    | N        | Discipline associated with the room. |
| `name`             | Room Name               | String    | Y        | Name of the room.                    |
| `consectiveChange` | Consecutive Room Change | Boolean   | Y        | Indicates if the room is continuous. |

---
