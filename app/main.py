from fastapi import FastAPI
from app.db.database import Base, engine
from app.db.session import SessionLocal
from app.models.role import Role
from app.models.profile import Profile
from app.core.security import get_password_hash
from app.api.v1 import (
    role_api_router, profile_api_router,
    olympiad_api_router, participation_api_router,
    auth_api_router
)

app = FastAPI(title="АРМ для олимпиад")

@app.on_event("startup")
def reset_and_seed_db():
    print("🔄 Очистка базы данных...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✅ База данных очищена.")

    # Сразу создаём роли и админа
    db = SessionLocal()
    try:
        # 1. Роли
        for role_name in ["admin", "teacher", "student"]:
            if not db.query(Role).filter(Role.name == role_name).first():
                db.add(Role(name=role_name))
        db.commit()

        # 2. Админ
        admin_role = db.query(Role).filter(Role.name == "admin").first()
        if not db.query(Profile).filter(Profile.email == "admin@example.com").first():
            admin = Profile(
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                last_name="Админов",
                first_name="Админ",
                middle_name="Админович",
                role_id=admin_role.id,
                is_active=True,
            )
            db.add(admin)
            db.commit()
            print("✅ Админ создан: admin@example.com / admin123")
    finally:
        db.close()

# Подключаем роутеры
app.include_router(auth_api_router.router, prefix="/api/v1")
app.include_router(role_api_router.router, prefix="/api/v1")
app.include_router(profile_api_router.router, prefix="/api/v1")
app.include_router(olympiad_api_router.router, prefix="/api/v1")
app.include_router(participation_api_router.router, prefix="/api/v1")

