const correctAnswer = ['A', 'B', 'C', 'D','A', 'B', 'C', 'D', 'A', 'B'];
const form = document.querySelector('.quiz-form');
const result = document.querySelector('.result');

form.addEventListener('submit', e =>{
    e.preventDefault();
    let score = 0;
    const userAnswer = [form.q1.value, form.q2.value, form.q3.value, form.q4.value, form.q5.value, form.q6.value, form.q7.value, form.q8.value, form.q9.value, form.q10.value];

    userAnswer.forEach((answer, index) => {
        if( answer === correctAnswer[index]) {
            score += 10;
        }
    });

    
    result.classList.replace('d-none', 'd-block');
    scroll(0,0);
    
    let output = 0;
    const timer = setInterval(() => {
        result.querySelector('span').textContent = `${output}%`;
        if(output === score) {
            clearInterval(timer);
        } else {
            output++;
        }
    }, 10);

});