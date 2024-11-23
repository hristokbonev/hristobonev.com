document.addEventListener('DOMContentLoaded', function () {
    const sections = document.querySelectorAll('.section');
    
    // Handle hover for all sections
    sections.forEach(section => {
        const video = section.querySelector('video');
        if (!video) return; // Skip if no video element is found in the section

        // Handle video play when hovering over the section
        section.addEventListener('mouseenter', () => {
            video.play(); // Start playing the video on hover
        });

        // Handle video pause when leaving the section
        section.addEventListener('mouseleave', () => {
            video.pause(); // Pause the video when hover ends
        });
    });

    // Handle special case for performance video (start at 2 seconds)
    const performanceVideo = document.getElementById('performanceVideo');
    if (performanceVideo) {
        window.addEventListener('load', function () {
            performanceVideo.currentTime = 2; // Start the performance video 2 seconds in
        });
    }

    // Handle hover for specific bio videos
    const bioLeftVideo = document.getElementById('performercvvideo');
    const bioRightVideo = document.getElementById('developercvvideo');

    document.querySelector('.bio-left').addEventListener('mouseenter', () => {
        bioLeftVideo.play();
    });

    document.querySelector('.bio-left').addEventListener('mouseleave', () => {
        bioLeftVideo.pause();
    });

    document.querySelector('.bio-right').addEventListener('mouseenter', () => {
        bioRightVideo.play();
    });

    document.querySelector('.bio-right').addEventListener('mouseleave', () => {
        bioRightVideo.pause();
    });
});


function updateCentralVideo(src, title, description) {
    const centralVideo = document.getElementById('centralVideo');
    const centralVideoTitle = document.getElementById('centralVideoTitle');
    const centralVideoDescription = document.getElementById('centralVideoDescription');

    centralVideo.src = src;
    centralVideoTitle.textContent = title;
    centralVideoDescription.textContent = description;

    centralVideo.play();
}
