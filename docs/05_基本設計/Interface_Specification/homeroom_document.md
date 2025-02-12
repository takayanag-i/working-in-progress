# Homeroom Document

## JSON Data Example

```json
{
  "id": "12345678",
  "docType": "homeroom",
  "ttid": "sry_2025_001",
  "homerooms": [
    {
      "name": "2-4",
      "schedule": {
          "Mon": 6,
          "Tues": 6,
          "Wednes": 5,
          "Thurs": 6,
          "Fri": 6
      }
    },
    {
      "name": "2-5",
      "schedule":{
        ...
      }
    }
  ]
}
```

## Object Structure

### Homeroom Schedule

| Key         | Business Name | Data Type       | Required | Description                            |
| ----------- | ------------- | --------------- | -------- | -------------------------------------- |
| `id`        | ID            | String          | Y        | Required by Cosmos DB.                 |
| `docType`   | Document Type | String          | Y        |                                        |
| `ttid`      | Timetable ID  | String          | Y        | **Partition Key**.                     |
| `homerooms` | Homeroom List | Array\<Object\> | Y        | Contains at least one homeroom object. |

### Homeroom

| Key        | Business Name | Data Type | Required | Description |
| ---------- | ------------- | --------- | -------- | ----------- |
| `name`     | Homeroom Name | String    | Y        |             |
| `schedule` | Schedule      | Object    | Y        |             |

### Schedule

| Key   | Business Name | Data Type | Required | Description |
| ----- | ------------- | --------- | -------- | ----------- |
| `Mon` | Monday        | Number    | N        |             |
| `Tue` | Tuesday       | Number    | N        |             |
| `Wed` | Wednesday     | Number    | N        |             |
| `Thu` | Thursday      | Number    | N        |             |
| `Fri` | Friday        | Number    | N        |             |
| `Sat` | Saturday      | Number    | N        |             |
| `Sun` | Sunday        | Number    | N        |             |

---
