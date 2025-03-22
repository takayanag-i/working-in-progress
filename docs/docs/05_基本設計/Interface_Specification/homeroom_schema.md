# Homeroom Schema

## JSON Data Example

```json
{
  "id": "12345678",
  "docType": "homeroom_schema",
  "ttid": "sry_2025_001",
  "homerooms": [
    {
      "homeroom": "2-4",
      "days": [
        {
          "day": "mon",
          "lastPeriod": 6
        },
        {
          "day": "tue",
          "lastPeriod": 7
        }
      ]
    },
    {
      "homeroom": "2-5",
      "days":{
        ...
      }
    }
  ]
}
```

## Object Structure

### Homeroom Schema

| Key         | Data Type      | Required |
| ----------- | -------------- | -------- |
| `id`        | String         | Y        |
| `docType`   | String         | Y        |
| `ttid`      | String         | Y        |
| `homerooms` | Array<Object\> | Y        |

#### `id`
- Must be an 8-digit number.

#### `docType`
- Must be `"homeroom_schema"`.

#### `ttid`
- **Partition Key.**
- Must follow the pattern `^[a-z]{3}_[0-9]{4}_[0-9]{3}$`, representing {School Code}\_{Year}\_{Sequential Number}.

#### `homerooms`
- Must contain at least one Homeroom object.

### Homeroom

| Key        | Data Type      | Required |
| ---------- | -------------- | -------- |
| `homeroom`     | String         | Y        |
| `days` | Array<Object\> | Y        |

#### `name`
- Must be 5 characters or fewer, using only letters and hyphens (-).

#### `days`
- Must contain at least one Day object.

### Day

| Key          | Data Type | Required |
| ------------ | --------- | -------- |
| `day`        | String    | Y        |
| `lastPeriod` | Number    | Y        |

#### `day`
- Must be a valid day of the week abbreviation (e.g., "mon", "tue").

#### `lastPeriod`
- Must be a positive integer.

---
