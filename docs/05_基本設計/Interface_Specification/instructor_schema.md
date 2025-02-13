# Instructor Schema

## JSON Data Example

```json
{
{
  "id": "instructor_001",
  "docType": "instructor_schema",
  "ttid": "sry_2025_001",
  "instructors": [
    {
      "name": "中田",
      "discipline": "地歴公民",
      "classCount": 8,
      "attendance": [
        { "day": "mon", "period": 1, "available": true },
        { "day": "mon", "period": 2, "available": true },
        { "day": "mon", "period": 3, "available": true },
        { "day": "mon", "period": 4, "available": true },
        { "day": "mon", "period": 5, "available": false },
        { "day": "mon", "period": 6, "available": false },
        { "day": "mon", "period": 7, "available": false },
        { "day": "tue", "period": 1, "available": false },
        { "day": "tue", "period": 2, "available": false },
        ...
        { "day": "fri", "period": 6, "available": true }
      ]
    },
    {
      "name": "菅原",
      "discipline": "数学",
      "classCount": 17,
      "attendance": [
        ...
      ]
    }
  ]
}
```

## Object Structure

### Instructor Schema

| Key           | Business Name   | Data Type       | Required | Description                              |
| ------------- | --------------- | --------------- | -------- | ---------------------------------------- |
| `id`          | ID              | String          | Y        | Required by Cosmos DB.                   |
| `docType`     | Document Type   | String          | Y        |                                          |
| `ttid`        | Timetable ID    | String          | Y        | **Partition Key**.                       |
| `instructors` | Instructor List | Array\<Object\> | Y        | Contains at least one Instrcutor object. |

### Instructor

| Key          | Business Name         | Data Type       | Required | Description                 |
| ------------ | --------------------- | --------------- | -------- | --------------------------- |
| `name`       | Instructor Name       | String          | Y        |                             |
| `discipline` | Subject Name          | String          | Y        |                             |
| `classCount` | Class Count           | Number          | Y        | Number of Assigned Classes. |
| `attendance` | Instructor Attendance | Array\<Object\> | Y        |                             |

### Instructor Attendance

| Key         | Business Name | Data Type | Required | Description |
| ----------- | ------------- | --------- | -------- | ----------- |
| `day`       | Day of Week   | String    | Y        |             |
| `period`    | Period        | String    | Y        |             |
| `available` | Day of Week   | Boolean   | Y        |             |

---
