# Course Schema

## JSON Data Example

```json
{
  "id": "12345678",
  "docType": "course_schema",
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

### Course Schema

| Key       | Data Type      | Required |
| --------- | -------------- | -------- |
| `id`      | String         | Y        |
| `docType` | String         | Y        |
| `ttid`    | String         | Y        |
| `courses` | Array<Object\> | Y        |

#### `id`
- Must be an 8-digit number.

#### `docType`
- Must be `"course_schema"`.

#### `ttid`
- **Partition Key.**
- Must follow the pattern `^[a-z]{3}_[0-9]{4}_[0-9]{3}$`, representing {School Code}\_{Year}\_{Sequential Number}.

#### `courses`
- Must contain at least one Course object.

### Course

| Key       | Data Type      | Required |
| --------- | -------------- | -------- |
| `name`    | String         | Y        |
| `subject` | String         | Y        |
| `credits` | Number         | Y        |
| `details` | Array<Object\> | Y        |

#### `name`
- Must be 5 characters or fewer, using only letters and numbers.

#### `subject`
- Must be 5 characters or fewer, using only letters and numbers.

#### `credits`
- Must be a positive integer.

#### `details`
- Must contain at least one Course Detail object.

### Course Detail

| Key          | Data Type | Required |
| ------------ | --------- | -------- |
| `instructor` | String    | Y        |
| `room`       | String    | N        |

#### `instructor`
- Must be a non-empty string.

#### `room`
- Must be a non-empty string if provided.

---
