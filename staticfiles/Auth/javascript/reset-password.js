document.addEventListener('DOMContentLoaded', () => {

    document.getElementById('Form').onsubmit = (event) => {
        
        document.getElementById('password-errors').innerText = ''
        document.getElementById('con-password-errors').innerText = ''
        

        Password = document.getElementById('password');
        if ( Password.value.length > 100 || Password.value.length < 1 ){
            event.preventDefault();
            Password.style.borderColor = 'red';
            document.getElementById('password-errors').innerText = 'Password Length Must Be > 0 and < 100';
        }

        Confirm_Password = document.getElementById('con-password');
        if ( Password.value != Confirm_Password.value ){
            event.preventDefault();
            Confirm_Password.style.borderColor = 'red';
            document.getElementById('con-password-errors').innerText = 'Password Does Not Match';
        }
    }

}, false);
