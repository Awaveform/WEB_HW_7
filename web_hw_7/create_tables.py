from connect_db import engine, session
from web_hw_7.models import Base


# Drop tables before creation
Base.metadata.drop_all(engine)

# Create tables in the database
Base.metadata.create_all(engine)

# Close the session
session.close()
