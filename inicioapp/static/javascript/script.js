let slideIndex = 0;
showSlides();

function showSlides() {
    const slides = document.querySelectorAll('.slide');
    if (slideIndex >= slides.length) {
        slideIndex = 0;
    }
    if (slideIndex < 0) {
        slideIndex = slides.length - 1;
    }

    // Aplica la transformación adecuada
    const offset = -slideIndex * 100;
    document.querySelector('.slides').style.transform = `translateX(${offset}%)`;
}

function moveSlide(n) {
    slideIndex += n;
    showSlides();
}

// Opcional: navegación automática
setInterval(() => {
    moveSlide(1);
}, 4000); // Cambia la imagen cada 3 segundos



