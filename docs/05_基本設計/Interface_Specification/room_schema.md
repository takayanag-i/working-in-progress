# Room Schema

## JSON Data Example

```json
{
  "id": "12345678",
  "docType": "room_schema",
  "ttid": "sry_2025_001",
  "rooms": [
    {
      "discipline": "芸術",
      "name": "書道室",
      "consectiveChange": false
    },
    {
      "name": "予5",
      "consectiveChange": true
    }
  ]
}
```

## Object Structure

### Room Schema

| Key       | Data Type      | Required |
| --------- | -------------- | -------- |
| `id`      | String         | Y        |
| `docType` | String         | Y        |
| `ttid`    | String         | Y        |
| `rooms`   | Array<Object\> | Y        |

#### `id`
- Must be an 8-digit number.

#### `docType`
- Must be `"room_schema"`.

#### `ttid`
- **Partition Key.**
- Must follow the pattern `^[a-z]{3}_[0-9]{4}_[0-9]{3}$`, representing {School Code}\_{Year}\_{Sequential Number}.

#### `rooms`
- Must contain at least one Room object.

### Room

| Key                | Data Type | Required |
| ------------------ | --------- | -------- |
| `discipline`       | String    | N        |
| `name`             | String    | Y        |
| `consectiveChange` | Boolean   | Y        |

#### `discipline`
- Must be a non-empty string if provided.

#### `name`
- Must be a non-empty string.

#### `consectiveChange`
- Must be a boolean value.

---
