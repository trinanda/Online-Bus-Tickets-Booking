#!/usr/bin/env bash
alembic downgrade base
chown -R $USER:$USER migrations/versions/
rm -rf migrations/versions/*
alembic revision --autogenerate -m 'inisialisasi database'
alembic upgrade head
