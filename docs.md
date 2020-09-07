# API Documentation

## Download Counter

### Get Download Counters

#### Request

```
GET /download_counter
```

#### Response Format

```ts
{
    [key:app_slug]: number
}
```

The number is the count.

#### Example Response

```json
{
  "kaidiremote": 1,
  "osm-map": 6
}
```

### Increase Download Counter

#### Request

```
GET /download_counter/count/<appid_slug>
```

Replace `<appid_slug>` by the filename of the app in the appid.
In `data.json` this id is found under `app.slug`.

#### Response

```text
OK
```
