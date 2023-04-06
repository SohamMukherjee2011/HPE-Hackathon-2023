const rick = document.querySelector('.rick');
const active = document.querySelector('label')
const submit = document.getElementsByClassName('submit');
rick.onclick = function () {
    rick.classList.add('active');
}
submit.onclick = function () {
    document.forms["changes"].submit();
}