# Homeroom Schema

## JSON Data Example

```json
{
  "id": "12345678",
  "docType": "homeroom_schema",
  "ttid": "sry_2025_001",
  "homerooms": [
    {
      "name": "2-4",
      "schedule": [
        {
          "day": "mon",
          "lastPeriod": 6
        },
        {
          "day": "tue",
          "lastPeriod": 7
        }
      ]
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

### Homeroom Schema

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

| Key          | Business Name   | Data Type | Required | Description |
| ------------ | --------------- | --------- | -------- | ----------- |
| `day`        | Day of the Week | String    | Y        |             |
| `lastPeriod` | Last Period     | Number    | Y        |             |

---
````
