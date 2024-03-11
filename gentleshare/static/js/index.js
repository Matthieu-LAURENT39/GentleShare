document.getElementById('nextBtn').addEventListener('click', function() {
    const innerCarousel = document.getElementById('carouselInner');
    innerCarousel.scrollLeft += innerCarousel.offsetWidth;
});

document.getElementById('prevBtn').addEventListener('click', function() {
    const innerCarousel = document.getElementById('carouselInner');
    innerCarousel.scrollLeft -= innerCarousel.offsetWidth;
});
