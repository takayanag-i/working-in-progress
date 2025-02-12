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
          "mon": 6,
          "tue": 6,
          "wed": 5,
          "thu": 6,
          "fri": 6
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

### Homeroom Document

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
| `mon` | Monday        | Number    | N        |             |
| `tue` | Tuesday       | Number    | N        |             |
| `wed` | Wednesday     | Number    | N        |             |
| `thu` | Thursday      | Number    | N        |             |
| `fri` | Friday        | Number    | N        |             |
| `sat` | Saturday      | Number    | N        |             |
| `sun` | Sunday        | Number    | N        |             |

---
