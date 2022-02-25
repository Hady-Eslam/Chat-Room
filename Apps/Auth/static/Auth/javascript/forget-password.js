document.addEventListener('DOMContentLoaded', () => {

    document.getElementById('Form').onsubmit = (event) => {
        
        document.getElementById('username-errors').innerText = ''
        
        UserName = document.getElementById('username');
        if ( UserName.value.length > 100 || UserName.value.length < 1 ){
            event.preventDefault();
            UserName.style.borderColor = 'red';
            document.getElementById('username-errors').innerText = 'UserName Length Must Be > 0 and < 100';
        }
    }

}, false);
