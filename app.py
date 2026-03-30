import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Streamlit Shooter", layout="centered")

st.title("🚀 JS 기반 비행기 슈팅")
st.write("방향키로 이동, **Space** 키로 발사하세요!")

# 자바스크립트 게임 엔진 코드
game_js = """
<!DOCTYPE html>
<html>
<head>
    <style>
        canvas { background: #000; display: block; margin: 0 auto; border: 2px solid #444; }
        #ui { position: absolute; top: 20px; left: 50%; transform: translateX(-50%); color: white; font-family: sans-serif; font-size: 20px; pointer-events: none; }
    </style>
</head>
<body>
    <div id="ui">Score: 0</div>
    <canvas id="g"></canvas>
    <script>
        const canvas = document.getElementById('g');
        const ctx = canvas.getContext('2d');
        const ui = document.getElementById('ui');
        canvas.width = 400; canvas.height = 600;

        let score = 0;
        let player = { x: 180, y: 540, w: 40, h: 40 };
        let bullets = [];
        let enemies = [];
        let keys = {};

        document.addEventListener('keydown', e => keys[e.code] = true);
        document.addEventListener('keyup', e => {
            keys[e.code] = false;
            if(e.code === 'Space') bullets.push({x: player.x + 15, y: player.y, w: 10, h: 20});
        });

        function update() {
            if (keys['ArrowLeft'] && player.x > 0) player.x -= 5;
            if (keys['ArrowRight'] && player.x < canvas.width - player.w) player.x += 5;

            bullets.forEach((b, i) => {
                b.y -= 8;
                if(b.y < 0) bullets.splice(i, 1);
            });

            if(Math.random() < 0.03) enemies.push({x: Math.random() * 360, y: -40, w: 40, h: 40});

            enemies.forEach((e, ei) => {
                e.y += 3;
                if(e.y > 600) enemies.splice(ei, 1);
                
                // 총알 충돌
                bullets.forEach((b, bi) => {
                    if(b.x < e.x + e.w && b.x + b.w > e.x && b.y < e.y + e.h && b.y + b.h > e.y) {
                        enemies.splice(ei, 1);
                        bullets.splice(bi, 1);
                        score += 10;
                        ui.innerText = "Score: " + score;
                    }
                });
            });
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#007bff'; ctx.fillRect(player.x, player.y, player.w, player.h); // 플레이어
            ctx.fillStyle = '#ffeb3b'; bullets.forEach(b => ctx.fillRect(b.x, b.y, b.w, b.h)); // 총알
            ctx.fillStyle = '#dc3545'; enemies.forEach(e => ctx.fillRect(e.x, e.y, e.w, e.h)); // 적
            requestAnimationFrame(() => { update(); draw(); });
        }
        draw();
    </script>
</body>
</html>
"""

# HTML 컴포넌트 삽입
components.html(game_js, height=620)
