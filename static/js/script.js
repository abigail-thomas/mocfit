
        // HAMBURGER !
        const hamburger = document.querySelector('.hamburger');
        const navLinks = document.querySelector('.nav-links');

        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            navLinks.classList.toggle('active');
        });

        // when u click a link, close the menu
        document.querySelectorAll('.nav-links a').forEach(link => {
            link.addEventListener('click', () => {
                hamburger.classList.remove('active');
                navLinks.classList.remove('active');
            });
        });


        // the scrolled feature,
        // since navbar is always visible, change the background from transparent to darker when scrolled down
        window.addEventListener('scroll', () => {
            const navbar = document.querySelector('.navbar');
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });


// password showing stuff
document.addEventListener("DOMContentLoaded", function () {
    console.log("in script");

    // get toggle boxes from both login and register form
    const toggleBoxes = document.querySelectorAll('#togglePasswordLogin, #togglePasswordRegister');

    toggleBoxes.forEach(toggle => {
        // if in the register form, use 2 password input
        // else use one password input
        const passwordFields = toggle.id === 'togglePasswordRegister'
        ? document.querySelectorAll('#id_password1, #id_password2')
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


        
