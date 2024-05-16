const nextBtn = document.getElementById('nextBtn');
const slides = document.querySelectorAll('.slide');

let currentSlide = 0;

nextBtn.addEventListener('click', () => {
    currentSlide++;
    if (currentSlide >= slides.length) {
        currentSlide = 0;
    }
    updateCarousel();
});

function updateCarousel() {
    const offset = -currentSlide * slides[0].offsetWidth;
    document.querySelector('.carousel').style.transform = `translateX(${offset}px)`;
}
