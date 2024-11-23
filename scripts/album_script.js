document.addEventListener('DOMContentLoaded', function() {
    const lightbox = document.querySelector('.lightbox');
    const lightboxImage = lightbox.querySelector('.lightbox-image');
    const closeBtn = lightbox.querySelector('.lightbox-close');
    const prevBtn = lightbox.querySelector('.lightbox-prev');
    const nextBtn = lightbox.querySelector('.lightbox-next');
    const photoItems = document.querySelectorAll('.photo-item');
    
    let currentIndex = 0;
    const photos = Array.from(photoItems).map(item => ({
        src: item.querySelector('img').src,
        alt: item.querySelector('img').alt
    }));

    // Open lightbox
    photoItems.forEach((item, index) => {
        item.addEventListener('click', () => {
            currentIndex = index;
            updateLightboxImage();
            lightbox.classList.add('active');
            document.body.style.overflow = 'hidden'; // Prevent scrolling
        });
    });

    // Close lightbox
    closeBtn.addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) {
            closeLightbox();
        }
    });

    // Navigate through photos
    prevBtn.addEventListener('click', showPrevImage);
    nextBtn.addEventListener('click', showNextImage);

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (!lightbox.classList.contains('active')) return;
        
        if (e.key === 'Escape') closeLightbox();
        if (e.key === 'ArrowLeft') showPrevImage();
        if (e.key === 'ArrowRight') showNextImage();
    });

    function updateLightboxImage() {
        const photo = photos[currentIndex];
        lightbox.classList.add('loading'); // Show loading

        const img = new Image();
        img.onload = function() {
            lightboxImage.src = photo.src;
            lightboxImage.alt = photo.alt;
            lightbox.classList.remove('loading'); // Hide loading when done
        };
        img.src = photo.src;
        
        // Show/hide navigation buttons based on position
        prevBtn.style.display = currentIndex === 0 ? 'none' : 'block';
        nextBtn.style.display = currentIndex === photos.length - 1 ? 'none' : 'block';
    }

    function closeLightbox() {
        lightbox.classList.remove('active');
        document.body.style.overflow = ''; // Restore scrolling
    }

    function showPrevImage() {
        if (currentIndex > 0) {
            currentIndex--;
            updateLightboxImage();
        }
    }

    function showNextImage() {
        if (currentIndex < photos.length - 1) {
            currentIndex++;
            updateLightboxImage();
        }
    }

    // Optional: Preload adjacent images
    function preloadAdjacentImages() {
        if (currentIndex < photos.length - 1) {
            const nextImg = new Image();
            nextImg.src = photos[currentIndex + 1].src;
        }
        if (currentIndex > 0) {
            const prevImg = new Image();
            prevImg.src = photos[currentIndex - 1].src;
        }
    }
});