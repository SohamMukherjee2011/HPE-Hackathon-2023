const canvas = document.getElementById("Matrix");
const context = canvas.getContext("2d");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
const katakana =
  "私たちは愛する見知らぬ人ではありませんあなたはルールを知っています、そして私もそうです";
const latin = "ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-_=+{}[]|;:,<.>/?";
const nums = "0123456789";
const alphabet = katakana + latin + nums;
const fontSize = 10;
const columns = canvas.width / fontSize;
const rainDrops = [];
for (let x = 0; x < columns; x++) {
  rainDrops[x] = 1;
}
const draw = () => {
  context.fillStyle = "rgba(0, 0, 0, 0.05)";
  context.fillRect(0, 0, canvas.width, canvas.height);
  context.fillStyle = "#00FF41";
  context.font = fontSize + "px monospace";
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
const rick = document.querySelector(".rick");
const active = document.querySelector("label");
const submit = document.getElementsByClassName("submit");
const message = document.getElementById("msg");
rick.onclick = function () {
  rick.classList.add("active");
};
submit.onclick = function () {
  document.forms["changes"].submit();
};
setTimeout(function () {
  message.classList.add("visuallyhidden");
  message.addEventListener(
    "transitionend",
    function () {
      message.style.display = "none";
    },
    {
      capture: false,
      once: true,
      passive: false,
    }
  );
}, 1000);
