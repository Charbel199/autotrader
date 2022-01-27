from app.data_access.persistence.database import Session
from app.data_access.persistence.models.user import User

session = Session()

user = User(
    email="asd",
    hashed_password="asd",
    first_name="asd",
    last_name="asd"
)

session.add(user)
session.commit()
session.close()
