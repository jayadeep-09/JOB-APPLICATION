// GLASS CARD HOVER EFFECT

const cards = document.querySelectorAll('.glass-card');

cards.forEach(card => {

    card.addEventListener('mousemove', e => {

        const rect = card.getBoundingClientRect();

        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const rotateY = (x - rect.width / 2) / 20;
        const rotateX = -(y - rect.height / 2) / 20;

        card.style.transform = `
            perspective(1000px)
            rotateX(${rotateX}deg)
            rotateY(${rotateY}deg)
            translateY(-8px)
        `;

    });


    card.addEventListener('mouseleave', () => {

        card.style.transform = `
            perspective(1000px)
            rotateX(0deg)
            rotateY(0deg)
            translateY(0px)
        `;

    });

});



// SMOOTH SCROLL

document.querySelectorAll('a[href^="#"]').forEach(anchor => {

    anchor.addEventListener('click', function (e) {

        e.preventDefault();

        document.querySelector(this.getAttribute('href'))
            .scrollIntoView({

                behavior: 'smooth'

            });

    });

});



// NAVBAR SHADOW ON SCROLL

window.addEventListener('scroll', () => {

    const navbar = document.querySelector('.custom-navbar');

    if (window.scrollY > 20) {

        navbar.style.boxShadow = '0 8px 30px rgba(0,0,0,0.25)';

    }

    else {

        navbar.style.boxShadow = 'none';

    }

});