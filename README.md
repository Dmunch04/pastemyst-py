# PasteMyst.py

[paste.myst.rs](https://paste.myst.rs) API wrapper written in Python.

<br>

## Install

Install using pip:
```
  pip install pastemyst
```
Or if using Linux:
```
  pip3 install pastemyst
```

<br>

## Requirements

Here's the libraries used to create the wrapper:
- json
- requests
- urllib
- datetime

<br>

## Functions
#### `create_paste_myst(code: str, expires_in: str = 'never', language: str = None)`

> Alias: `CreatePasteMyst(..)`

This function creates a new PasteMyst and returns a `PasteMystInfo` object

#### `get_paste_myst(id: str)`

> Alias: `GetPasteMyst(..)`

This function gets an exisiting PasteMyst by an id. It returns the Responding `PasteMystInfo` object

<br>

## Objects
#### `PasteMystInfo`

Here's a table of the classes contents
| Variable   | Type     | Alias     | Description                                                        |
|------------|----------|-----------|--------------------------------------------------------------------|
| id         | str      | ID        | This is the PasteMyst's ID. Use this to access the PasteMyst again |
| created_at | datetime | CreatedAt | This holds the exact date and time the PasteMyst was created at    |
| code       | str      | Code      | This is the code, the PasteMyst contains                           |
| expires_in | str      | ExpiresIn | This is when the PasteMyst will expire and be deleted              |
| language   | str      | Language  | The target programming language of the PasteMyst                   |
| url        | str      | URL       | The exact URL to get to the PasteMyst                              |

<br>

## Contribution

Feel free to make a pull request! All help is appreciated!

<br>

## License

This repo is licensed under the MIT license

<br>

## Maintainers

- [Munchii](https://github.com/Dmunch04)
