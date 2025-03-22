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
      "credits": 8,
      "days": [
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
      "credits": 17,
      "days": [
        ...
      ]
    }
  ]
}
```

## Object Structure

### Instructor Schema

| Key           | Data Type      | Required |
| ------------- | -------------- | -------- |
| `id`          | String         | Y        |
| `docType`     | String         | Y        |
| `ttid`        | String         | Y        |
| `instructors` | Array<Object\> | Y        |

#### `id`
- Must be an 8-digit number.

#### `docType`
- Must be `"instructor_schema"`.

#### `ttid`
- **Partition Key.**
- Must follow the pattern `^[a-z]{3}_[0-9]{4}_[0-9]{3}$`, representing {School Code}\_{Year}\_{Sequential Number}.

#### `instructors`
- Must contain at least one Instructor object.

### Instructor

| Key          | Data Type      | Required |
| ------------ | -------------- | -------- |
| `name`       | String         | Y        |
| `discipline` | String         | Y        |
| `credits`    | Number         | Y        |
| `days`      | Array<Object\> | Y        |

#### `name`
- Must be a non-empty string.

#### `discipline`
- Must be a non-empty string.

#### `credits`
- Must be a positive integer.

#### `days`
- Must contain at least one Day object.

### Day

| Key         | Data Type | Required |
| ----------- | --------- | -------- |
| `day`       | String    | Y        |
| `period`    | Number    | Y        |
| `available` | Boolean   | Y        |

#### `day`
- Must be a valid day of the week abbreviation (e.g., "mon", "tue").

#### `period`
- Must be a positive integer.

#### `available`
- Must be a boolean value.

---
