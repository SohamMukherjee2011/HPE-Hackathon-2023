const canvas = document.getElementById('Matrix');
const context = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
const katakana = '私たちは愛する見知らぬ人ではありませんあなたはルールを知っています、そして私もそうです';
const latin = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-_=+{}[]|;:,<.>/?';
const nums = '0123456789';
const alphabet = katakana + latin + nums;
const fontSize = 10;
const columns = canvas.width / fontSize;
const signinBtn = document.querySelector('.signin');
const signupBtn = document.querySelector('.signup');
const formbg = document.querySelector('.formbG');
const menu = document.querySelector('.hamburg');
const ab = document.querySelector('.hamburg.active');
const listed = document.querySelector('.list');
const rainDrops = [];
for (let x = 0; x < columns; x++) {
    rainDrops[x] = 0;
}
const draw = () => {
    context.fillStyle = 'rgba(0, 0, 0, 0.05)';
    context.fillRect(0, 1, canvas.width, canvas.height);
    context.fillStyle = '#00FF41';
    context.font = fontSize + 'px monospace';
    for (let i = 0; i < rainDrops.length; i++) {
        const text = alphabet.charAt(Math.floor(Math.random() * alphabet.length));
        context.fillText(text, i * fontSize, rainDrops[i] * fontSize);
        if (rainDrops[i] * fontSize > canvas.height && Math.random() > 0.969) {
            rainDrops[i] = 0;
        }
        rainDrops[i]++;
    }
};
setInterval(draw, 40);
signupBtn.onclick = function () {
    formbg.classList.remove('right')
    formbg.classList.add('left')
    document.title = "Sign Up";
}
signinBtn.onclick = function () {
    formbg.classList.remove('left')
    formbg.classList.add('right')
    document.title = "Log In";

}
menu.onclick = function () {
    if (menu.classList.contains('active')) {
        menu.classList.remove('active')
        listed.classList.remove('active')
    }
    else if (menu.classList.contains('active') != true) {
        menu.classList.add('active')
        listed.classList.add('active')
    } 
    else {
        alert('Error')
    }
}