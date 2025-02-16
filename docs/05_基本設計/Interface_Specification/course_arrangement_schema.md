# Course Arrangement Schema

## JSON Data Example

```json
{
  "id": "12345678",
  "docType": "course_arrangement_schema",
  "ttid": "sry_2025_001",
  "curriculums": [
    {
      "homeroom": "2-4",
      "blocks": [
        {
          "name": "2-4共通",
          "lanes": [
            {
              "courses": ["2論国4", "2古探4"]
            },
          ]
        },
        {
          "name": "2-4歴史",
          "lanes": [
            {
              "name": "世界史",
              "courses": ["2世探"]
            },
            {
              "name": "日本史",
              "courses": ["2日探34"]
            }
          ]
        }
      ]
    },
    {
      "homeroom": "2-5",
      "blocks": [
        ...
      ]
    }
  ]
}
```

## Object Structure

### Course Arrangement Schema

| Key           | Business Name   | Data Type       | Required | Description                              |
| ------------- | --------------- | --------------- | -------- | ---------------------------------------- |
| `id`          | ID              | String          | Y        | Required by Cosmos DB.                   |
| `docType`     | Document Type   | String          | Y        |                                          |
| `ttid`        | Timetable ID    | String          | Y        | **Partition Key**. I                     |
| `curriculums` | Curriculum List | Array\<Object\> | Y        | Contains at least one curriculum object. |

### Curriculum

| Key        | Business Name | Data Type       | Required | Description                         |
| ---------- | ------------- | --------------- | -------- | ----------------------------------- |
| `homeroom` | Homeroom      | String          | Y        |                                     |
| `blocks`   | Block List    | Array\<Object\> | Y        | Contains at least one Block object. |

### Block

| Key     | Business Name | Data Type       | Required | Description                        |
| ------- | ------------- | --------------- | -------- | ---------------------------------- |
| `name`  | Block Name    | String          | Y        |                                    |
| `lanes` | Lane List     | Array\<Object\> | Y        | Contains at least one lane object. |

### Lane

| Key       | Business Name | Data Type       | Required | Description                      |
| --------- | ------------- | --------------- | -------- | -------------------------------- |
| `name`    | Lane Name     | String          | N        |                                  |
| `courses` | Course List   | Array\<String\> | Y        | Contains at least one course ID. |
| -         | Course ID     | String          | Y        |                                  |

---

