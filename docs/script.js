// Initialize Lucide icons when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    lucide.createIcons();
});

// Smooth scroll function
function scrollToSection(id) {
    const element = document.getElementById(id);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Animate elements on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fadeIn');
        }
    });
}, observerOptions);

// Observe all animated elements
window.addEventListener('load', function() {
    document.querySelectorAll('.animated').forEach((el) => observer.observe(el));
});

