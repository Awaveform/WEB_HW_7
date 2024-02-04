# WEB_HW_7

docker run --name my-post -p 5432:5432 -e POSTGRES_PASSWORD=qwe -d postgres
pip install SQLAlchemy psycopg2

poetry add alembic sqlalchemy
alembic init alembic
alembic revision --autogenerate -m 'Init'
alembic upgrade head
