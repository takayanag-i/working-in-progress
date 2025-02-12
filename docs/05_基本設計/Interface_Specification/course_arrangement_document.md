# Course Arrangement Document

## JSON Data Example

```json
{
  "id": "12345678",
  "docType": "course_arrangement",
  "ttid": "sry_2025_001",
  "curriculums": [
    {
      "homeroom": "2-4",
      "blocks": [
        {
          "name": "2-4共通",
          "lanes": [
            {
              "index": 1,
              "courses": ["2論国4", "2古探4"]
            },
          ]
        },
        {
          "name": "2-4歴史",
          "lanes": [
            {
              "index": 1,
              "courses": ["2世探"]
            },
            {
              "index": 2,
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

### Course Arrangement

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

| Key       | Business Name | Data Type       | Required | Description                                                               |
| --------- | ------------- | --------------- | -------- | ------------------------------------------------------------------------- |
| `index`   | Lane Index    | Number          | Y        | 1-indexed (starting from 1 within each block). Represents the lane order. |
| `courses` | Course List   | Array\<String\> | Y        | Contains at least one course ID.                                          |
| -         | Course ID     | String          | Y        |                                                                           |

---

