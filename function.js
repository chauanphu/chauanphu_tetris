const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const CANVAS_WIDTH = canvas.width = 600;
const CANVAS_HEIGHT = canvas.height = 600;

const playerImage = new Image();
playerImage.src = 'images/shadow_dog.png';

const spriteWidth = 575;
const spriteHeight = 523;

let frameX = 0;
let frameY = 0;
let gameFrame = 0;
let staggerFrame = 5;
const animationStates = {
    "idle": {
        frame: 6,
        y: 0
    },
    "jump": {
        frame: 6,
        y: 1
    },
}

let action = 'idle';

function animate(){
    ctx.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
    let position = Math.floor(gameFrame / staggerFrame) % 6;
    frameX = position * spriteWidth;
    frameY = animationStates[action].y * spriteHeight;
    ctx.drawImage(
        playerImage, 
        frameX, frameY * spriteHeight,
        spriteWidth, spriteHeight, 
        0, 0, 
        spriteWidth, spriteHeight, );
    gameFrame++;
    requestAnimationFrame(animate);
}

animate();