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
              "courses": ["2世探"]
            },
            {
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

| Key           | Data Type       | Required |
| ------------- | --------------- | -------- |
| `id`          | String          | Y        |
| `docType`     | String          | Y        |
| `ttid`        | String          | Y        |
| `curriculums` | Array\<Object\> | Y        |

#### `id`
- Must be an 8-digit number.

#### `docType`
- Must be `"course_arrangement_schema"`.

#### `ttid`
- **Partition Key.**
- Must follow the pattern `^[a-z]{3}_[0-9]{4}_[0-9]{3}$`, representing {School Code}\_{Year}\_{Sequential Number}.

#### `curriculums`
- Must contain at least one Curriculum object.

### Curriculum

| Key        | Data Type       | Required |
| ---------- | --------------- | -------- |
| `homeroom` | String          | Y        |
| `blocks`   | Array\<Object\> | Y        |

#### `homeroom`
- Must be 5 characters or fewer, using only letters and hyphens (-).
#### `blocks`
- Must contain at least one Block object.

### Block

| Key     | Data Type       | Required |
| ------- | --------------- | -------- |
| `name`  | String          | Y        |
| `lanes` | Array\<Object\> | Y        |

#### `name`
- Must be 8 characters or fewer, using only letters and hyphens (-).

#### `lanes`
- Must contain at least one Lane object.

### Lane

| Key       | Data Type       | Required |
| --------- | --------------- | -------- |
| `courses` | Array\<String\> | Y        |

#### `courses`
- Must contain at least one course name.
- Each course name must be 5 characters or fewer and contain only letters (no symbols allowed).