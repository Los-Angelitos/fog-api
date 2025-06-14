from typing import Optional, Tuple
from sqlalchemy import and_, insert, select
from iam.infrastructure.models import Device as DeviceModel
from iam.domain.entities import Device
from shared.infrastructure.database import db
from shared.infrastructure.utilities import Utilities

class DeviceRepository:

    def __init__(self):
        self.utilities = Utilities()
    
    @staticmethod
    def find_by_id_and_api_key(device_id : str, api_key : str) -> Optional[Device]:
        session = db.session
        try:
            stmt = select(DeviceModel.__table__).where(
                and_(
                    DeviceModel.__table__.c.device_id == device_id,
                    DeviceModel.__table__.c.api_key == api_key
                )
            )
            result = session.execute(stmt).fetchone()
            if result:
                row = result._mapping
                return Device(
                    device_id=row["device_id"],
                    api_key=row["api_key"]
                )
            return None
        finally:
            session.close()
        
    @staticmethod
    def create_device(data: dict) -> Optional[Device]:
        session = db.session
        try: 
            generated_api_key = Utilities.generate_api_key()
            session.execute(
                DeviceModel.__table__.insert().values(
                    device_id=data['device_id'],
                    api_key=generated_api_key
                )
            )
            session.commit()
            return Device(device_id=data['device_id'],api_key=generated_api_key)
        except Exception as e:
            session.rollback()
            print(f"Unexpected error: {str(e)}")  # Debug log
            raise e