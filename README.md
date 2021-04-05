# Guide

## Setup

### Prerequities

- PostgreSQL
- Flask

### Setup Environment Variables

Create a `.env` file with the following variables:

```shell
FLASK_APP=index.py
FLASK_ENV=development
FLASK_RUN_PORT=5000
HOST=localhost
PORT=5432
DATABASE="customers_db"
DATABASE_USERNAME="customers_admin"
DATABASE_PASSWORD="admin"
AUTHSECRET="yourauthsecret"
EXPIRESSECONDS=3000
```

### Setup the Database

- Create an admin user and a database
    ```shell
    sudo service postgresql start
    sudo -u postgres psql postgres
    \i reset.sql
    \q
    ```

- Create the schema for the database and functions

    ```shell
    psql -h localhost -p 5432 -U customers_admin -f setup_db.sql customers_db
    ```

- Insert dummy data into the database

    ```shell
    psql -h localhost -p 5432 -U customers_admin -f dummy_data.sql customers_db
    ```

### Install dependencies

- Flask_cors
- dotenv
- psycopg2
- pyjwt

### Activate venv

```shell
python3 -m venv backend
. backend/bin/activate
```

### Run

```shell
flask run
```

## API

Create a user and login to obtain a token before trying out the others apis.

[POSTMAN Documentation](https://documenter.getpostman.com/view/11560439/TzCQa6He)

[POSTMAN Collection](https://www.getpostman.com/collections/8b8a94d62a843f81724c)

## Notes

JSON object returned converts date to datetime as date is not a valid type in json.
Date is appended with "00:00:00 GMT".