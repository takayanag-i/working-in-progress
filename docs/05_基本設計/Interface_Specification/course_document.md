# Course Document

## JSON Data Example

```json
{
  "id": "12345678",
  "docType": "course",
  "ttid": "sry_2025_001",
  "courses": [
    {
      "name": "3数Ⅲ7",
      "subject": "3数Ⅲ",
      "credits": 5,
      "courseDetails": [
        {
          "instructor": "高宮",
        },
        {
          "instructor": "伊達",
          "room": "予5"
        }
      ]
    },
    {
      "name": "3物理5",
      "subject": "3物理",
      "credits": 3,
      "courseDetails": [
        {
          "instructor": "滝沢",
          "room": "視聴覚"
        }
      ]
    }
  ]
}

```

## Object Structure

### Course Document

| Key       | Business Name | Data Type       | Required | Description                          |
| --------- | ------------- | --------------- | -------- | ------------------------------------ |
| `id`      | ID            | String          | Y        | Required by Cosmos DB.               |
| `docType` | Document Type | String          | Y        |                                      |
| `ttid`    | Timetable ID  | String          | Y        | **Partition Key**.                   |
| `courses` | Course List   | Array\<Object\> | Y        | Contains at least one course object. |

### Course

| Key       | Business Name | Data Type       | Required | Description                                 |
| --------- | ------------- | --------------- | -------- | ------------------------------------------- |
| `name`    | Course Name   | String          | Y        |                                             |
| `subject` | Subject       | String          | Y        |                                             |
| `credits` | Credits       | Number          | Y        |                                             |
| `details` | Details       | Array\<Object\> | Y        | Contains at least one course detail object. |

### Course Detail

| Key          | Business Name | Data Type | Required | Description |
| ------------ | ------------- | --------- | -------- | ----------- |
| `instructor` | Instructor    | String    | Y        |             |
| `room`       | Room          | String    | N        |             |

---
