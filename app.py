from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

# Твой HTML и CSS дизайн прямо в переменной
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Мои Проекты</title>
    <style>
        :root {
            --bg: #f4f7f6;
            --card-bg: #ffffff;
            --text: #333;
            --primary: #007bff;
            --secondary: #6c757d;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        h1 { margin-bottom: 20px; font-size: 24px; }
        .container { width: 100%; max-width: 500px; }
        .card {
            background: var(--card-bg);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }
        .card:active { transform: scale(0.98); }
        .card h3 { margin: 0 0 10px 0; color: var(--primary); }
        .card p { margin: 0 0 15px 0; font-size: 14px; color: var(--secondary); }
        .btn {
            display: block;
            text-align: center;
            background: var(--primary);
            color: white;
            text-decoration: none;
            padding: 12px;
            border-radius: 10px;
            font-weight: bold;
        }
        .btn-stars {
            background: #ffac33; /* Золотой цвет для звезд */
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <h1>🚀 Мои Приложения</h1>
    
    <div class="container">
        <!-- Карточка проекта 1 -->
        <div class="card">
            <h3>Super CRM Bot</h3>
            <p>Система для сбора жалоб и отзывов через мессенджеры.</p>
            <a href="https://t.me" class="btn">Открыть бота</a>
        </div>

        <!-- Карточка проекта 2 -->
        <div class="card">
            <h3>Analytics Dashboard</h3>
            <p>Удобный веб-интерфейс для просмотра статистики приложений.</p>
            <a href="#" class="btn">Подробнее</a>
        </div>

        <!-- Кнопка поддержки -->
        <div class="card" style="border: 2px solid #ffac33;">
            <h3>Поддержать автора</h3>
            <p>Если вам нравятся мои проекты, вы можете задонатить мне Звезды.</p>
            <a href="https://t.me?start=donate" class="btn btn-stars">⭐ Отправить звезды</a>
        </div>
    </div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_CONTENT

if __name__ == "__main__":
    # Запуск сервера на порту 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
