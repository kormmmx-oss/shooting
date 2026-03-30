import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="JS HTML5 Shooter", layout="centered")

st.title("🚀 JavaScript 기반 비행기 슈팅")
st.write("방향키로 이동하고 **Space** 키로 발사하세요!")

# --- JavaScript/HTML5 게임 코드 정의 ---
game_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { margin: 0; padding: 0; background-color: #000; overflow: hidden; }
        canvas { display: block; background: #000; border: 2px solid #555; }
        #scoreBoard {
            position: absolute; top: 10px; left: 10px;
            color: white; font-family: Arial, sans-serif; font-size: 20px;
            pointer-events: none; /* 클릭 방지 */
        }
    </style>
</head>
<body>
    <div id="scoreBoard">Score: 0</div>
    <canvas id="gameCanvas"></canvas>

<script>
    // --- 초기 설정 ---
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    const scoreBoard = document.getElementById('scoreBoard');

    // 화면 크기 설정
    canvas.width = 480;
    canvas.height = 640;

    // 게임 상태 변수
    let score = 0;
    let isGameOver = false;
    let keys = {};

    // --- 객체 정의 (클래스 대용) ---

    // 플레이어
    const player = {
        x: canvas.width / 2 - 20,
        y: canvas.height - 70,
        width: 40,
        height: 40,
        speed: 7,
        color: '#007bff' // 파란색
    };

    // 총알 리스트
    let bullets = [];
    const bulletSettings = { width: 8, height: 18, speed: 10, color: '#ffeb3b' }; // 노란색

    // 적 리스트
    let enemies = [];
    const enemySettings = { width: 35, height: 35, color: '#dc3545', minSpeed: 2, maxSpeed: 5 }; // 빨간색

    // --- 이벤트 리스너 (조작) ---
    document.addEventListener('keydown', e => keys[e.code] = true);
    document.addEventListener('keyup', e => {
        keys[e.code] = false;
        // 스페이스바 뗐을 때 발사 (연사 방지 원하면 여기, 연사 원하면 keydown)
        if (e.code === 'Space' && !isGameOver) {
            fireBullet();
        }
    });

    // --- 게임 로직 함수 ---

    function fireBullet() {
        bullets.push({
            x: player.x + player.width / 2 - bulletSettings.width / 2,
            y: player.y,
            width: bulletSettings.width,
            height: bulletSettings.height
        });
    }

    function spawnEnemy() {
        if (isGameOver) return;
        enemies.push({
            x: Math.random() * (canvas.width - enemySettings.width),
            y: -enemySettings.height,
            width: enemySettings.width,
            height: enemySettings.height,
            speed: enemySettings.minSpeed + Math.random() * (enemySettings.maxSpeed - enemySettings.minSpeed)
        });
    }

    // 사각형 충돌 감지 함수
    function rectIntersect(r1, r2) {
        return !(r2.x > r1.x + r1.width || 
                 r2.x + r2.width < r1.x || 
                 r2.y > r1.y + r1.height ||
                 r2.y + r2.height < r1.y);
    }

    // --- 업데이트 & 그리기 루프 ---

    function update() {
        if (isGameOver) return;

        // 플레이어 이동
        if ((keys['ArrowLeft'] || keys['KeyA']) && player.x > 0) player.x -= player.speed;
        if ((keys['ArrowRight'] || keys['KeyD']) && player.x < canvas.width - player.width) player.x += player.speed;

        // 총알 업데이트 (위로 이동)
        bullets.forEach((bullet, index) => {
            bullet.y -= bulletSettings.speed;
            if (bullet.y + bullet.height < 0) bullets.splice(index, 1); // 화면 밖 제거
        });

        // 적 업데이트 (아래로 이동)
        enemies.forEach((enemy, index) => {
            enemy.y += enemy.speed;
            
            // 화면 아래로 놓친 적
            if (enemy.y > canvas.height) {
                enemies.splice(index, 1);
                // 점수 감점이나 패널티 추가 가능
            }

            // 플레이어와 적 충돌
            if (rectIntersect(player, enemy)) {
                isGameOver = true;
                alert('Game Over! Final Score: ' + score);
                // 필요시 Streamlit으로 점수 전송 가능
            }
        });

        // 충돌 감지 (총알 vs 적)
        bullets.forEach((bullet, bIndex) => {
            enemies.forEach((enemy, eIndex) => {
                if (rectIntersect(bullet, enemy)) {
                    // 충돌 시 둘 다 제거
                    bullets.splice(bIndex, 1);
                    enemies.splice(eIndex, 1);
                    score += 10;
                    scoreBoard.innerText = 'Score: ' + score;
                }
            });
        });
    }

    function draw() {
        // 화면 지우기
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // 플레이어 그리기 (간단한 비행기 모양)
        ctx.fillStyle = player.color;
        ctx.fillRect(player.x, player.y, player.width, player.height);
        // 날개 모양 추가
        ctx.fillRect(player.x - 10, player.y + 15, 60, 10);

        // 총알 그리기
        ctx.fillStyle = bulletSettings.color;
        bullets.forEach(bullet => {
            ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
        });

        // 적 그리기
        ctx.fillStyle = enemySettings.color;
        enemies.forEach(enemy => {
            ctx.fillRect(enemy.x, enemy.y, enemy.width, enemy.height);
        });

        if (isGameOver) {
            ctx.fillStyle = 'white';
            ctx.font = '40px Arial';
            ctx.textAlign = 'center';
            ctx.fillText('GAME OVER', canvas.width / 2, canvas.height / 2);
            ctx.font = '20px Arial';
            ctx.fillText('Press F5 to Restart', canvas.width / 2, canvas.height / 2 + 40);
        }
    }

    function gameLoop() {
        update();
        draw();
        requestAnimationFrame(gameLoop); // 매 프레임마다 반복 실행
    }

    // --- 게임 시작 ---
    // 적 생성 타이머 (1초마다)
    setInterval(spawnEnemy, 1000);
    
    // 게임 루프 시작
    gameLoop();

</script>
</body>
</html>
"""

# --- Streamlit에 HTML/JS components 주입 ---
# height는 canvas 높이보다 조금 여유있게 잡습니다.
components.html(game_html, height=680, scrolling=False)

st.info("이 게임은 JavaScript로 브라우저에서 직접 렌더링되므로 속도가 빠릅니다.")
