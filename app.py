import streamlit as st
import streamlit.components.v1 as components

# 1. Streamlit 인터페이스 설정
st.set_page_config(page_title="No-Error Shooter", layout="centered")

st.title("🛸 에러 방지 슈팅 게임")
st.info("이 게임은 브라우저 독립 모드에서 실행되어 'Node Error'가 발생하지 않습니다.")

# 2. 게임 소스 코드 (HTML5 + CSS3 + JS)
# 모든 리소스를 이 안에 담아 Streamlit과의 충돌을 방지합니다.
game_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; background: #111; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; }
        canvas { background: #000; border: 3px solid #333; box-shadow: 0 0 20px rgba(0,0,0,0.5); }
        #hud { position: absolute; top: 20px; width: 380px; display: flex; justify-content: space-between; color: white; font-family: 'Courier New', monospace; font-size: 18px; pointer-events: none; }
    </style>
</head>
<body>
    <div id="hud">
        <div id="score">SCORE: 0</div>
        <div id="life">LIFE: 3</div>
    </div>
    <canvas id="ctx"></canvas>

<script>
    const canvas = document.getElementById('ctx');
    const ctx = canvas.getContext('2d');
    canvas.width = 400; canvas.height = 550;

    let score = 0;
    let lives = 3;
    let gameOver = false;
    let keys = {};

    const player = { x: 180, y: 480, w: 40, h: 40, color: '#00ffcc' };
    let bullets = [];
    let enemies = [];

    document.addEventListener('keydown', e => keys[e.code] = true);
    document.addEventListener('keyup', e => {
        keys[e.code] = false;
        if(e.code === 'Space' && !gameOver) bullets.push({x: player.x + 15, y: player.y, w: 10, h: 20});
    });

    function update() {
        if(gameOver) return;

        if(keys['ArrowLeft'] && player.x > 0) player.x -= 7;
        if(keys['ArrowRight'] && player.x < canvas.width - player.w) player.x += 7;

        bullets.forEach((b, i) => {
            b.y -= 10;
            if(b.y < 0) bullets.splice(i, 1);
        });

        if(Math.random() < 0.04) {
            enemies.push({ x: Math.random()*360, y: -40, w: 40, h: 40, s: 3 + Math.random()*3 });
        }

        enemies.forEach((e, ei) => {
            e.y += e.s;
            
            // 적과 플레이어 충돌
            if(player.x < e.x+e.w && player.x+player.w > e.x && player.y < e.y+e.h && player.y+player.h > e.y) {
                enemies.splice(ei, 1);
                lives--;
                document.getElementById('life').innerText = "LIFE: " + lives;
                if(lives <= 0) gameOver = true;
            }

            // 총알과 적 충돌
            bullets.forEach((b, bi) => {
                if(b.x < e.x+e.w && b.x+b.w > e.x && b.y < e.y+e.h && b.y+b.h > e.y) {
                    enemies.splice(ei, 1);
                    bullets.splice(bi, 1);
                    score += 10;
                    document.getElementById('score').innerText = "SCORE: " + score;
                }
            });

            if(e.y > canvas.height) enemies.splice(ei, 1);
        });
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // 플레이어
        ctx.fillStyle = player.color;
        ctx.fillRect(player.x, player.y, player.w, player.h);

        // 총알
        ctx.fillStyle = '#ffff00';
        bullets.forEach(b => ctx.fillRect(b.x, b.y, b.w, b.h));

        // 적
        ctx.fillStyle = '#ff4466';
        enemies.forEach(e => ctx.fillRect(e.x, e.y, e.w, e.h));

        if(gameOver) {
            ctx.fillStyle = "rgba(0,0,0,0.7)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "white";
            ctx.font = "30px Arial";
            ctx.textAlign = "center";
            ctx.fillText("GAME OVER", canvas.width/2, canvas.height/2);
            ctx.font = "16px Arial";
            ctx.fillText("새로고침(F5)하여 다시 시작", canvas.width/2, canvas.height/2 + 40);
        }
        requestAnimationFrame(() => { update(); draw(); });
    }
    draw();
</script>
</body>
</html>
"""

# 3. HTML 실행 (height 값을 여유 있게 주어 스크롤 바 방지)
components.html(game_code, height=600)

st.write("---")
st.caption("참고: 이 게임은 데이터 수집이나 분석 기능이 없는 순수 클라이언트 기반 예제입니다.")
