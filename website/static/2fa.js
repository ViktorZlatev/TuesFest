const form = document.getElementById('form');
const code = document.getElementById('code')

var ok = 0

form.addEventListener('submit', e => {

    if ( ok != 1 ){
    e.preventDefault();
    ok = 0;
    }

    validateInputs();
});

const setError = (element, message) => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = message;
    inputControl.classList.add('error');
    inputControl.classList.remove('success')
}

const setSuccess = element => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = '';
    inputControl.classList.add('success');
    inputControl.classList.remove('error');
};

const validateInputs = () => {
    const codeValue = code.value.trim();

    if(codeValue === '') {
        setError(code, 'Code is required');
    } else if (codeValue.length != 6 ) {
        setError(code, 'Code must contain 6 digits.')
    } else {
        setSuccess(code);
        ok = ok + 1
    }
};