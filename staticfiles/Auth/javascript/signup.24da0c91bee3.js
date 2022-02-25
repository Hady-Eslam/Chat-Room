document.addEventListener('DOMContentLoaded', () => {

    document.getElementById('Form').onsubmit = (event) => {
        
        document.getElementById('username-errors').innerText = ''
        document.getElementById('email-errors').innerText = ''
        document.getElementById('password-errors').innerText = ''
        document.getElementById('con-password-errors').innerText = ''


        UserName = document.getElementById('username');
        if ( UserName.value.length > 100 || UserName.value.length < 1 ){
            event.preventDefault();
            UserName.style.borderColor = 'red';
            document.getElementById('username-errors').innerText = 'UserName Length Must Be > 0 and < 100';
        }

        Email = document.getElementById('email');
        if ( Email.value.length > 100 || Email.value.length < 1 ){
            event.preventDefault();
            Email.style.borderColor = 'red';
            document.getElementById('email-errors').innerText = 'Email Length Must Be > 0 and < 100';
        }
        else if ( !Email.value.match(
            /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
          ) ){
            event.preventDefault();
            Email.style.borderColor = 'red';
            document.getElementById('email-errors').innerText = 'Not Valid Email Address';
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
