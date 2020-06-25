import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

load_dotenv(".env")
DATABASE_URL = os.getenv('DATABASE_URL') or os.environ["SQLALCHEMY_DATABASE_URI"]

engine = create_engine(DATABASE_URL, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         expire_on_commit=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from models.user import UserModel
    from models.confirmation import ConfirmationModel
    from models.flow import FlowModel

    Base.metadata.create_all(bind=engine)
   
def restart_db():
    from models.user import UserModel
    from models.confirmation import ConfirmationModel
    from models.flow import FlowModel
    
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # Create the fixtures
    admin = UserModel(email="admin", password="123456")
    admin.save_to_db()
    new_confirmation = ConfirmationModel(user_id=admin.id)
    new_confirmation.save_to_db()
    new_confirmation.confirmed = True
    new_confirmation.save_to_db()
    
    flow = FlowModel(name="name", report="report")
    flow.save_to_db()