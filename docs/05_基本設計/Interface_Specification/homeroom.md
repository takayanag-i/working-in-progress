# Homeroom Schedule

## JSON Data Example

```json
{
  "id": "12345678",
  "docType": "homeroom_schedule",
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

| Key         | Business Name | Data Type       | Required | Description                                                                                 |
| ----------- | ------------- | --------------- | -------- | ------------------------------------------------------------------------------------------- |
| `id`        | ID            | String          | Y        | Required by Cosmos DB.                                                                      |
| `docType`   | Document Type | String          | Y        | Specifies the type of document. For homeroom schedules, this should be `homeroom_schedule`. |
| `ttid`      | Timetable ID  | String          | Y        | **Partition Key**. Identifies Timetable.                                                    |
| `homerooms` | Homeroom List | Array\<Object\> | Y        | Contains at least one homeroom object.                                                      |

### Homeroom

| Key        | Business Name | Data Type | Required | Description                       |
| ---------- | ------------- | --------- | -------- | --------------------------------- |
| `name`     | Homeroom Name | String    | Y        | Name of the homeroom.             |
| `schedule` | Schedule      | Object    | Y        | Weekly schedule for the homeroom. |

### Schedule

| Key   | Business Name | Data Type | Required | Description                     |
| ----- | ------------- | --------- | -------- | ------------------------------- |
| `Mon` | Monday        | Number    | N        | Number of periods on Monday.    |
| `Tue` | Tuesday       | Number    | N        | Number of periods on Tuesday.   |
| `Wed` | Wednesday     | Number    | N        | Number of periods on Wednesday. |
| `Thu` | Thursday      | Number    | N        | Number of periods on Thursday.  |
| `Fri` | Friday        | Number    | N        | Number of periods on Friday.    |
| `Sat` | Saturday      | Number    | N        | Number of periods on Saturday.  |
| `Sun` | Sunday        | Number    | N        | Number of periods on Sunday.    |

---
