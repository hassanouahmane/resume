import sys,traceback
sys.path.insert(0,'.')

from app.core.database import SessionLocal
from app.services.auth_service import create_user

try:
    db = SessionLocal()
    user = create_user(db, 'test@example.com', 'testuser', 'Password123!', 'Test User')
    print('CREATED', user.id, user.email)
except Exception as e:
    print('ERROR', e)
    traceback.print_exc()
    sys.exit(1)
finally:
    try:
        db.close()
    except:
        pass
