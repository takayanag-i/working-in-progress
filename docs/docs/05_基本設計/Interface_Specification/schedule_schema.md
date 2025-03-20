# Schedule Schema

## JSON Data Example

```json
{
  "id": "12345678",
  "docType": "schedule_schema",
  "ttid": "sry_2025_001",
  "days": [
    {
      "day": "mon",
      "available": true,
      "amPeriods": 4,
      "pmPeriods": 3
    },
    {
      "day": "tue",
      "available": true,
      "amPeriods": 4,
      "pmPeriods": 3
    },
    ...
  ]
}
```

## Object Structure

### Schedule Schema

| Key       | Data Type      | Required |
| --------- | -------------- | -------- |
| `id`      | String         | Y        |
| `docType` | String         | Y        |
| `ttid`    | String         | Y        |
| `days`    | Array<Object\> | Y        |

#### `id`
- Must be an 8-digit number.

#### `docType`
- Must be `"schedule_schema"`.

#### `ttid`
- **Partition Key.**
- Must follow the pattern `^[a-z]{3}_[0-9]{4}_[0-9]{3}$`, representing {School Code}\_{Year}\_{Sequential Number}.

#### `days`
- Must contain at least one Day object.

### Day

| Key         | Data Type | Required |
| ----------- | --------- | -------- |
| `day`      | String    | Y        |
| `available` | Boolean   | Y        |
| `amPeriods` | Number    | N        |
| `pmPeriods` | Number    | N        |

#### `day`
- Must be a valid day of the week abbreviation (e.g., "mon", "tue").

#### `available`
- Must be a boolean value.

#### `amPeriods`
- Must be a positive integer.

#### `pmPeriods`
- Must be a positive integer.

---
