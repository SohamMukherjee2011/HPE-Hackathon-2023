const number = document.querySelector('.color')
const value = number.innerText;
const convert = parseInt(value)
if (convert < 50) {
    number.classList.add('red')
}

else if (convert < 70) {
    number.classList.add('yellow')
}

else if (convert >= 70) {
    number.classList.add('green')
}