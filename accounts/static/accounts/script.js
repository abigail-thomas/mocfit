document.addEventListener("DOMContentLoaded", function () {
    console.log("in script");

    // get toggle boxes from both login and register form
    const toggleBoxes = document.querySelectorAll('#togglePasswordLogin, #togglePasswordRegister');

    toggleBoxes.forEach(toggle => {
        // if in the register form, use 2 password input
        // else use one password input
        const passwordFields = toggle.id === 'togglePasswordRegister'
        ? document.querySelectorAll('#id_password, #id_password2')
        : document.querySelectorAll('#id_password');

        // make password text visible by changing the type to text
        toggle.addEventListener('change', function () {
            console.log("box been checked");
            passwordFields.forEach(field => {
                field.type = this.checked ? 'text' : 'password';
            });
        });
        }
    );


    
});
