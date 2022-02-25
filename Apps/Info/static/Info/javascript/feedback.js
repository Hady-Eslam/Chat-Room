document.addEventListener('DOMContentLoaded', () => {

    document.getElementById('Form').onsubmit = (event) => {

        document.getElementById('title-errors').innerText = ''
        document.getElementById('feedback-errors').innerText = ''

        UserName = document.getElementById('title');
        if ( UserName.value.length > 100 || UserName.value.length < 1 ){
            event.preventDefault();
            UserName.style.borderColor = 'red';
            document.getElementById('title-errors').innerText = 'Title Length Must Be > 0 and < 100';
        }

        Password = document.getElementById('feedback');
        if ( Password.value.length > 1000 || Password.value.length < 1 ){
            event.preventDefault();
            Password.style.borderColor = 'red';
            document.getElementById('feedback-errors').innerText = 'Feedback Length Must Be > 0 and < 1000';
        }
    }

}, false);
