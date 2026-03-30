import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="Streamlit Shooter JS", layout="centered")

st.title("🚀 자바스크립트 슈팅 게임")
st.write("방향키로 이동하고 **Space**로 발사하세요!")

# 2. 자바스크립트 및 HTML 소스
# 별도의 파일 없이 이 문자열 하나로 게임이 완성됩니다.
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; background: #000; overflow: hidden; font-family: sans-serif; }
        canvas { background: #080808; display: block; margin: 0 auto; border: 2px solid #333; cursor: crosshair; }
        #ui { position: absolute; top: 10px; left: 10px; color: #fff; font-size: 20px; pointer-events: none; }
    </style>
</head>
<body>
    <div id="ui">Score: 0</div>
    <canvas id="gameCanvas"></canvas>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const ui = document.getElementById('ui');

        canvas.width = 400;
        canvas.height = 600;

        let score = 0;
        let gameOver = false;
        let player = { x: 180, y: 530, w: 40, h: 40, speed: 6 };
        let bullets = [];
        let enemies = [];
        let keys = {};

        // 키 입력 감지
        document.addEventListener('keydown', e => keys[e.code] = true);
        document.addEventListener('keyup', e => {
            keys[e.code] = false;
            if (e.code === 'Space' && !gameOver) {
                bullets.push({ x: player.x + 15, y: player.y, w: 10, h: 20 });
            }
        });

        function update() {
            if (gameOver) return;

            // 플레이어 이동
            if (keys['ArrowLeft'] && player.x > 0) player.x -= player.speed;
            if (keys['ArrowRight'] && player.x < canvas.width - player.w) player.x += player.speed;

            // 총알 이동
            bullets.forEach((b, i) => {
                b.y -= 10;
                if (b.y < 0) bullets.splice(i, 1);
            });

            // 적 생성 및 이동
            if (Math.random() < 0.03) {
                enemies.push({ x: Math.random() * (canvas.width - 40), y: -40, w: 40, h: 40, speed: 3 + Math.random() * 2 });
            }

            enemies.forEach((e, ei) => {
                e.y += e.speed;
                
                // 충돌 감지: 총알 vs 적
                bullets.forEach((b, bi) => {
                    if (b.x < e.x + e.w && b.x + b.w > e.x && b.y < e.y + e.h && b.y + b.h > e.y) {
                        enemies.splice(ei, 1);
                        bullets.splice(bi, 1);
                        score += 10;
                        ui.innerText = "Score: " + score;
                    }
                });

                // 충돌 감지: 플레이어 vs 적
                if (player.x < e.x + e.w && player.x + player.w > e.x && player.y < e.y + e.h && player.y + player.h > e.y) {
                    gameOver = true;
                }

                if (e.y > canvas.height) enemies.splice(ei, 1);
            });
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 플레이어 (파란색)
            ctx.fillStyle = '#00aaff';
            ctx.fillRect(player.x, player.y, player.w, player.h);

            // 총알 (노란색)
            ctx.fillStyle = '#ffff00';
            bullets.forEach(b => ctx.fillRect(b.x, b.y, b.w, b.h));

            // 적 (빨간색)
            ctx.fillStyle = '#ff4444';
            enemies.forEach(e => ctx.fillRect(e.x, e.y, e.w, e.h));

            if (gameOver) {
                ctx.fillStyle = "white";
                ctx.font = "30px Arial";
                ctx.textAlign = "center";
                ctx.fillText("GAME OVER", canvas.width/2, canvas.height/2);
                ctx.font = "15px Arial";
                ctx.fillText("F5를 눌러 다시 시작하세요", canvas.width/2, canvas.height/2 + 40);
            }

            requestAnimationFrame(() => {
                update();
                draw();
            });
        }

        draw();
    </script>
</body>
</html>
"""

# 3. Streamlit에 HTML 컴포넌트로 주입
components.html(game_html, height=620)

st.info("이 코드는 브라우저의 리소스를 사용하므로 Streamlit Cloud에서도 안전하게 실행됩니다.")
