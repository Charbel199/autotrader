from sqlalchemy import create_engine
from app.data_access.persistence.config import Settings
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy import exc
from sqlalchemy import event
from sqlalchemy import select

load_dotenv()

DATABASE_CONNECTION_URL = Settings.DATABASE_URL
engine = create_engine(
    DATABASE_CONNECTION_URL,
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True,
    pool_timeout=30
)


@event.listens_for(engine, "engine_connect")
def ping_connection(connection, branch):
    if branch:
        # "branch" refers to a sub-connection of a connection,
        # we don't want to bother pinging on these.
        return

    try:
        # run a SELECT 1.   use a core select() so that
        # the SELECT of a scalar value without a table is
        # appropriately formatted for the backend
        connection.scalar(select(1))
    except exc.DBAPIError as err:
        # catch SQLAlchemy's DBAPIError, which is a wrapper
        # for the DBAPI's exception.  It includes a .connection_invalidated
        # attribute which specifies if this connection is a "disconnect"
        # condition, which is based on inspection of the original exception
        # by the dialect in use.
        if err.connection_invalidated:
            # run the same SELECT again - the connection will re-validate
            # itself and establish a new connection.  The disconnect detection
            # here also causes the whole connection pool to be invalidated
            # so that all stale connections are discarded.
            connection.scalar(select(1))
        else:
            raise


Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
