# Mini Data Ingestion

## Requirements

- `Docker`
- `docker-compose`

## Setup

1.Clone repository
```shell
git clone git@github.com:ichux/mini-data-ingestion.git
cd mini-data-ingestion
```

2.. Launch `docker-compose`
Use a .env to configure the app port(default: 8000) if needed. In that case, `cp .env.example .env`

```shell
make b
```

## Usage
Your app will be available at `127.0.0.1:8000` or the port you've selected while starting it.

> Use the command `make a` to create an admin user to access the data. The default `username/password` = `(admin/admin)`
