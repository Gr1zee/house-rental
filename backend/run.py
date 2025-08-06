import uvicorn
import subprocess
import sys
import os

def run_migrations():
    """Применяет миграции базы данных"""
    try:
        subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], 
                      cwd=os.path.dirname(__file__), check=True)
        print("✅ Миграции успешно применены")
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при применении миграций: {e}")
        return False
    return True

if __name__ == "__main__":
    print("🚀 Запуск House Rental API...")
    
    # Применяем миграции
    if run_migrations():
        print("🌐 Запуск сервера на http://127.0.0.1:8000")
        print("📖 Документация API: http://127.0.0.1:8000/docs")
        
        # Запускаем сервер
        uvicorn.run(
            "app.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
    else:
        print("❌ Не удалось запустить приложение из-за ошибок в миграциях")
        sys.exit(1) 