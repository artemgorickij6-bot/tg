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
    <title>F-TOP</title>
    <style>
        :root {
            --bg-color: #050505;
            --accent-neon: #0ff;
            --glass-bg: rgba(255, 255, 255, 0.03);
            --glass-border: rgba(255, 255, 255, 0.1);
        }

        body { margin: 0; background-color: var(--bg-color); color: white; font-family: 'Inter', sans-serif; overflow-x: hidden; scroll-behavior: smooth; }

        /* --- БУРГЕР --- */
        .burger { position: fixed; top: 25px; left: 30px; width: 40px; height: 30px; cursor: pointer; z-index: 1100; }
        .burger input { display: none; }
        .burger span { display: block; position: absolute; height: 4px; width: 100%; background: white; border-radius: 9px; transition: .25s ease-in-out; }
        .burger span:nth-of-type(1) { top: 0px; transform-origin: left center; }
        .burger span:nth-of-type(2) { top: 50%; transform: translateY(-50%); }
        .burger span:nth-of-type(3) { top: 100%; transform: translateY(-100%); transform-origin: left center; }
        .burger input:checked ~ span:nth-of-type(1) { transform: rotate(45deg); left: 5px; }
        .burger input:checked ~ span:nth-of-type(2) { width: 0%; opacity: 0; }
        .burger input:checked ~ span:nth-of-type(3) { transform: rotate(-45deg); top: 28px; left: 5px; }

        /* --- МЕНЮ --- */
        .side-menu { position: fixed; top: 0; left: -320px; width: 300px; height: 100%; background: rgba(0, 0, 0, 0.95); backdrop-filter: blur(20px); z-index: 1050; transition: 0.5s; padding: 120px 40px; border-right: 1px solid var(--glass-border); box-sizing: border-box; }
        .side-menu.active { left: 0; }
        .menu-link { display: block; color: white; text-decoration: none; font-size: 1.8rem; font-weight: 800; margin-bottom: 30px; transition: 0.3s; opacity: 0.5; }
        .menu-link:hover { opacity: 1; color: var(--accent-neon); transform: translateX(10px); }

        /* --- МОДАЛКА ВХОДА --- */
        .modal-overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); backdrop-filter: blur(8px); z-index: 2000; justify-content: center; align-items: center; }
        .auth-card { background: #111; padding: 40px; border-radius: 24px; border: 1px solid var(--glass-border); width: 350px; text-align: center; }
        .auth-card input { width: 100%; background: #1a1a1a; border: 1px solid #333; padding: 15px; border-radius: 12px; color: white; margin-bottom: 15px; box-sizing: border-box; outline: none; }
        .btn-auth { background: white; color: black; border: none; padding: 14px; width: 100%; border-radius: 12px; font-weight: 900; cursor: pointer; }

        /* --- ПОИСК --- */
        .search-wrapper { width: 100%; max-width: 500px; margin: 40px auto; padding: 0 20px; position: relative; z-index: 10; }
        .input-container { display: flex; border-radius: 1rem; background: linear-gradient(173deg, #23272f 0%, #14161a 100%); box-shadow: 10px 10px 20px #0e1013, -10px -10px 40px #383e4b; padding: 0.3rem; gap: 0.3rem; }
        .input-container input { border-radius: 0.8rem; background: #23272f; box-shadow: inset 5px 5px 10px #0e1013, inset -5px -5px 10px #383e4b; width: 100%; padding: 1rem; border: 1px solid transparent; color: white; transition: all 0.2s; outline: none; }
        .input-container input:focus { border: 1px solid #ffd43b; box-shadow: 0px 0px 50px rgba(255, 212, 59, 0.3); }

        /* --- КАРТОЧКИ С ССЫЛКОЙ --- */
        .projects-section { padding: 40px 20px; display: flex; flex-direction: column; align-items: center; }
        .projects-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 40px; width: 100%; max-width: 1100px; }
        
        .neon-card { 
            width: 300px; background: rgba(15, 15, 30, 0.7); border: 2px solid var(--accent-neon); 
            border-radius: 12px; overflow: hidden; transition: 0.4s; position: relative; 
            justify-self: center; cursor: pointer; /* Указатель клика */
        }
        .neon-card:hover { transform: translateY(-8px); box-shadow: 0 0 25px var(--accent-neon); }
        .neon-card img { width: 100%; height: 140px; object-fit: cover; pointer-events: none; }
        .neon-card-content { padding: 16px; pointer-events: none; }
        
        .neon-card::before { content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.2), transparent); transition: 0.9s; }
        .neon-card:hover::before { left: 100%; }

        /* --- ШАПКА --- */
        nav { position: fixed; top: 0; width: 100%; height: 80px; display: flex; justify-content: flex-end; align-items: center; padding: 0 40px; box-sizing: border-box; z-index: 100; }
        .user-pill { background: var(--glass-bg); padding: 8px 18px; border-radius: 30px; border: 1px solid var(--glass-border); backdrop-filter: blur(10px); }
        .brush-header { position: absolute; top: 0; left: 0; width: 100%; height: 350px; background: url('https://img.freepik.com') no-repeat; background-size: 100% 100%; z-index: 1; }
        .hero { position: relative; height: 380px; display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 10; }
        #typing-text { font-size: 6rem; font-weight: 900; border-right: 6px solid white; }
        @keyframes blink { 0%, 100% { border-color: transparent; } 50% { border-color: white; } }
        #typing-text { animation: blink 0.8s infinite; }


        /* Оверлей для центрирования */
.support-overlay {
  display: none;
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(0,0,0,0.9);
  backdrop-filter: blur(10px);
  z-index: 3000;
  justify-content: center;
  align-items: center;
}

/* Твой стиль контейнера */
.support-container {
  background-color: #ffffff;
  display: flex;
  width: 460px;
  height: 120px;
  position: relative;
  border-radius: 6px;
  transition: 0.3s ease-in-out;
}

.support-container:hover { transform: scale(1.03); width: 220px; }
.support-container:hover .left-side { width: 100%; }

.left-side {
  background-color: #5de2a3;
  width: 130px; height: 120px;
  border-radius: 4px;
  position: relative;
  display: flex; justify-content: center; align-items: center;
  cursor: pointer; transition: 0.3s; flex-shrink: 0; overflow: hidden;
}

.right-side {
  width: calc(100% - 130px);
  display: flex; align-items: center; overflow: hidden; cursor: pointer; justify-content: space-between; white-space: nowrap; transition: 0.3s;
}

.new { font-size: 23px; font-family: "Lexend Deca", sans-serif; margin-left: 20px; color: #333; }

.card {
  width: 70px; height: 46px; background-color: #c7ffbc; border-radius: 6px;
  position: absolute; display: flex; z-index: 10; flex-direction: column; align-items: center;
  box-shadow: 9px 9px 9px -2px rgba(77, 200, 143, 0.72);
}

.card-line { width: 65px; height: 13px; background-color: #80ea69; border-radius: 2px; margin-top: 7px; }

.buttons {
  width: 8px; height: 8px; background-color: #379e1f;
  box-shadow: 0 -10px 0 0 #26850e, 0 10px 0 0 #56be3e;
  border-radius: 50%; margin-top: 5px; transform: rotate(90deg); margin: 10px 0 0 -30px;
}

.support-container:hover .card { animation: slide-top 1.2s cubic-bezier(0.645, 0.045, 0.355, 1) both; }
.support-container:hover .post { animation: slide-post 1s cubic-bezier(0.165, 0.84, 0.44, 1) both; }

@keyframes slide-top {
  0% { transform: translateY(0); }
  50% { transform: translateY(-70px) rotate(90deg); }
  100% { transform: translateY(-8px) rotate(90deg); }
}

.post { width: 63px; height: 75px; background-color: #dddde0; position: absolute; z-index: 11; bottom: 10px; top: 120px; border-radius: 6px; overflow: hidden; }
.post-line { width: 47px; height: 9px; background-color: #545354; position: absolute; border-radius: 0px 0px 3px 3px; right: 8px; top: 8px; }
.post-line:before { content: ""; position: absolute; width: 47px; height: 9px; background-color: #757375; top: -8px; }
.screen { width: 47px; height: 23px; background-color: #ffffff; position: absolute; top: 22px; right: 8px; border-radius: 3px; }
.dollar { position: absolute; font-size: 16px; color: #4b953b; width: 100%; text-align: center; top: 0; }
.numbers { width: 12px; height: 12px; background-color: #838183; box-shadow: 0 -18px 0 0 #838183, 0 18px 0 0 #838183; border-radius: 2px; position: absolute; transform: rotate(90deg); left: 25px; top: 52px; }
.numbers-line2 { width: 12px; height: 12px; background-color: #aaa9ab; box-shadow: 0 -18px 0 0 #aaa9ab, 0 18px 0 0 #aaa9ab; border-radius: 2px; position: absolute; transform: rotate(90deg); left: 25px; top: 68px; }

@keyframes slide-post { 50% { transform: translateY(0); } 100% { transform: translateY(-70px); } }
.support-container:hover .dollar { animation: fade-in-fwd 0.3s 1s backwards; }
@keyframes fade-in-fwd { 0% { opacity: 0; transform: translateY(-5px); } 100% { opacity: 1; transform: translateY(0); } }

    </style>
</head>
<body>

    <label class="burger">
        <input type="checkbox" onchange="document.getElementById('side-menu').classList.toggle('active')">
        <span></span><span></span><span></span>
    </label>
    <div class="side-menu" id="side-menu">
        <a href="#" class="menu-link">ГЛАВНАЯ</a>
        <a href="#projects" class="menu-link">ПРОЕКТЫ</a>
        <a href="#" class="menu-link">УСЛУГИ</a>
        <a href="javascript:void(0)" class="menu-link" onclick="document.getElementById('support-modal').style.display='flex'">ПОДДЕРЖАТЬ МЕНЯ</a>
    </div>

    <nav>
        <div class="user-pill">
            <span id="user-display">Гость</span>
            <button id="auth-btn" onclick="document.getElementById('auth-modal').style.display='flex'" style="margin-left:10px; background:white; border:none; padding:5px 12px; border-radius:15px; cursor:pointer; font-weight:900; font-size:0.7rem;">ВХОД</button>
        </div>
    </nav>

    <div class="brush-header"></div>
    <section class="hero">
        <span id="typing-text"></span>
        <p id="welcome-sub" style="color: #444; margin-top: 10px; font-weight: 800; letter-spacing: 4px;">SYSTEM OPERATIONAL</p>
    </section>

    <div class="search-wrapper">
        <div class="input-container">
            <input placeholder="Поиск проектов..." type="text" onkeyup="filter(this.value)" />
        </div>
    </div>

    <section class="projects-section" id="projects">
        <div class="projects-grid">
            <!-- КАРТОЧКА 1 (Добавлен атрибут data-link) -->
            <div class="neon-card" data-name="F-Gram" data-link="https://dark-ananymous-net.onrender.com" onclick="goToProject(this)">
                <img src="https://s.widget-club.com/samples/faWO46sxkdSDwhmnfw9glwq07dI3/8JsAP01qUIuK8ATdGBG6/0057E9F6-F235-40F9-918E-24194E7AC8AC.jpg?q=70">
                <div class="neon-card-content"><h3>Мессенджер F-Gram</h3><p>гибрид ТГ и Discord в моем исполнении, постоянно обновляеться, доступен в россии и полностью анонимен.</p></div>
            </div>

            <!-- КАРТОЧКА 2 -->
            <div class="neon-card" data-name="Shield-Net" data-link="https://github.com" onclick="goToProject(this)">
                <img src="https://img.freepik.com/premium-vector/metallic-black-shield-vector-illustration-eps-10-stock-image_213497-2642.jpg" />
                <div class="neon-card-content"><h3>Защита сайтов Shield-Net</h3><p>на уровне Cloudflare.</p></div>
            </div>
        </div>
    </section>

    <script>
        // Функция перехода по ссылке
        function goToProject(card) {
            const url = card.getAttribute('data-link');
            if (url) {
                window.open(url, '_blank'); // Открыть в новой вкладке
            }
        }

        function saveUser() {
            const name = document.getElementById('username-input').value;
            if(name) { localStorage.setItem('f_top_user', name); location.reload(); }
        }

        function filter(val) {
            const cards = document.querySelectorAll('.neon-card');
            cards.forEach(c => {
                c.style.display = c.dataset.name.toLowerCase().includes(val.toLowerCase()) ? "block" : "none";
            });
        }

        const brand = "F-TOP"; let idx = 0;
        function type() {
            document.getElementById("typing-text").innerHTML = brand.substring(0, idx);
            idx++; if(idx > brand.length) idx = 0;
            setTimeout(type, 500);
        }

        window.onload = () => {
            const user = localStorage.getItem('f_top_user');
            if(user) {
                document.getElementById('user-display').innerText = user;
                const b = document.getElementById('auth-btn');
                b.innerText = "ВЫХОД";
                b.onclick = () => { localStorage.clear(); location.reload(); };
                document.getElementById('welcome-sub').innerText = `ACCESS GRANTED: ${user.toUpperCase()}`;
            }
            type();
        };
        


    </script>
    <!-- ОКНО ПОДДЕРЖКИ -->
<a href="https://sites.google.com/view/ftop-pay/%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F-%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0">
<div class="support-overlay" id="support-modal" onclick="this.style.display='none'">
    <div class="support-container" onclick="event.stopPropagation()">
        <div class="left-side">
            <div class="card">
                <div class="card-line"></div>
                <div class="buttons"></div>
            </div>
            <div class="post">
                <div class="post-line"></div>
                <div class="screen">
                    <div class="dollar">$</div>
                </div>
                <div class="numbers"></div>
                <div class="numbers-line2"></div>
            </div>
        </div>
        <div class="right-side">
            <div class="new">Поддержать</div>
            <svg viewBox="0 0 451.846 451.847" class="arrow">
                <path fill="#cfcfcf" d="M345.441 248.292L151.154 442.573c-12.359 12.365-32.397 12.365-44.75 0-12.354-12.354-12.354-32.391 0-44.744L278.318 225.92 106.409 54.017c-12.354-12.359-12.354-32.394 0-44.748 12.354-12.359 32.391-12.359 44.75 0l194.287 194.284c6.177 6.18 9.262 14.271 9.262 22.366 0 8.099-3.091 16.196-9.267 22.373z"></path>
            </svg>
        </div>
    </div>
</div>
</a>

</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_CONTENT

if __name__ == "__main__":
    # Запуск сервера на порту 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
