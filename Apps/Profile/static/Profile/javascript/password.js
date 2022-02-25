document.addEventListener('DOMContentLoaded', () => {

    document.getElementById('Form').onsubmit = (event) => {

        document.getElementById('old-password-errors').innerText = ''
        document.getElementById('password-errors').innerText = ''
        document.getElementById('con-password-errors').innerText = ''

        Old_Password = document.getElementById('old_password');
        if ( Old_Password.value.length > 100 || Old_Password.value.length < 1 ){
            event.preventDefault();
            Old_Password.style.borderColor = 'red';
            document.getElementById('old-password-errors').innerText = 'Old Password Length Must Be > 0 and < 100';
        }

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
