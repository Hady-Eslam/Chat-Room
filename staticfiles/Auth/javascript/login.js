document.addEventListener('DOMContentLoaded', () => {

    document.getElementById('Form').onsubmit = (event) => {
        
        document.getElementById('username-errors').innerText = ''
        document.getElementById('password-errors').innerText = ''


        UserName = document.getElementById('username');
        if ( UserName.value.length > 100 || UserName.value.length < 1 ){
            event.preventDefault();
            UserName.style.borderColor = 'red';
            document.getElementById('username-errors').innerText = 'UserName Length Must Be > 0 and < 100';
        }

        Password = document.getElementById('password');
        if ( Password.value.length > 100 || Password.value.length < 1 ){
            event.preventDefault();
            Password.style.borderColor = 'red';
            document.getElementById('password-errors').innerText = 'Password Length Must Be > 0 and < 100';
        }
    }

}, false);
