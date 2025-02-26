# Subject Schema

## JSON Data Example

```json
{
  "id": "12345678",
  "docType": "subject_schema",
  "ttid": "sry_2025_001",
  "subjects": [
    {
      "discipline": "理科",
      "grade": "1",
      "name": "化基",
      "credits": 2
    },
    {
      "discipline": "理科",
      "grade": "2",
      "name": "化基",
      "credits": 1
    }
  ]
}

```

## Object Structure

### Subject Schema

| Key        | Business Name | Data Type       | Required | Description                           |
| ---------- | ------------- | --------------- | -------- | ------------------------------------- |
| `id`       | ID            | String          | Y        | Required by Cosmos DB.                |
| `docType`  | Document Type | String          | Y        |                                       |
| `ttid`     | Timetable ID  | String          | Y        | **Partition Key**.                    |
| `subjects` | Subject List  | Array\<Object\> | Y        | Contains at least one subject object. |

### Subject

| Key          | Business Name     | Data Type | Required | Description                                       |
| ------------ | ----------------- | --------- | -------- | ------------------------------------------------- |
| `discipline` | Discipline Name   | String    | Y        |                                                   |
| `grade`      | Grade             | String    | Y        |                                                   |
| `name`       | Subject Name      | String    | Y        | Combination of `grade` and `name` must be unique. |
| `credits`    | Number of Credits | Number    | Y        |                                                   |

---
