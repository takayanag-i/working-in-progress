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

| Key        | Data Type      | Required |
| ---------- | -------------- | -------- |
| `id`       | String         | Y        |
| `docType`  | String         | Y        |
| `ttid`     | String         | Y        |
| `subjects` | Array<Object\> | Y        |

#### `id`
- Must be an 8-digit number.

#### `docType`
- Must be `"subject_schema"`.

#### `ttid`
- **Partition Key.**
- Must follow the pattern `^[a-z]{3}_[0-9]{4}_[0-9]{3}$`, representing {School Code}\_{Year}\_{Sequential Number}.

#### `subjects`
- Must contain at least one Subject object.

### Subject

| Key          | Data Type | Required |
| ------------ | --------- | -------- |
| `discipline` | String    | Y        |
| `grade`      | String    | Y        |
| `name`       | String    | Y        |
| `credits`    | Number    | Y        |

#### `discipline`
- Must be a non-empty string.

#### `grade`
- Must be a non-empty string.

#### `name`
- Must be a non-empty string.

#### `credits`
- Must be a positive integer.

---
