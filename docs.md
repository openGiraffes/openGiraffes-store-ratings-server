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

## Ratings

### Create user

#### Request

```
POST /createuser
```

parameters are to be provided via the request body in the `application/json` mime format.

```ts
{
 "username":string,
 "logintoken":string
}
```

the login token is basically the password used for requests

#### Response

```ts
{ success: true }
// or
{ success: false, error: "username is already taken" }
```

### Check Whether user exists

#### Request

```
POST /checkuser
```

parameters are to be provided via the request body in the `application/json` mime format.

```ts
{
 "username":string,
 "logintoken":string
}
```

#### Response

```ts
{ success: true }
// or
{ success: false, error: "user not found" }
```

### Create Rating For An App

#### Request

```
POST /ratings/<appid_slug>/add
```

parameters are to be provided via the request body in the `application/json` mime format.

```ts
{
 "username": string,
 "logintoken": string,
 "points": number between 1 and 5,
 "description": string/text longer than 2 characters
}
```

#### Response

```ts
{ success: true }
// or an error of
{ success: false, error: "An error occured" }
{ success: false, error: "user not found" }
{ success: false, error: "you already posted a review for this app" }
{ success: false, error: "rating can only be between 1 and 5" }
{ success: false, error: "review description is to short" }
```

### Get All Ratings For An App

#### Request

```
GET /ratings/<appid_slug>
```

#### Response

example response:

```json
{
  "appid": "bhackers.store",
  "average": 3.5,
  "ratings": [
    {
      "creationtime": 1600894422,
      "description": "very good",
      "username": "sampleUser1",
      "points": 4
    },
    {
      "creationtime": 1600799422,
      "description": "fine",
      "username": "sampleUser2",
      "points": 3
    }
  ]
}
```
