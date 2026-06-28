document.addEventListener('DOMContentLoaded', () => {
    console.log("Welcome to Tool Titan API!");

    // Highlight active nav link based on current path
    const currentPath = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('.nav-links a');
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (currentPath === '' && href === 'index.html')) {
            link.classList.add('active');
        }
    });

    // Check for low-end device or reduced motion preference
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const isLowEndDevice = (navigator.hardwareConcurrency && navigator.hardwareConcurrency <= 4) || window.innerWidth <= 480;

    const animatedElements = document.querySelectorAll('.api-card, section, .glass-card');

    if (prefersReducedMotion || isLowEndDevice) {
        // Render elements immediately without animation delays for low-end devices
        animatedElements.forEach(el => {
            el.style.opacity = '1';
            el.style.transform = 'none';
        });
    } else {
        // Scroll reveal animations for high-performance devices
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -40px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        animatedElements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(15px)';
            el.style.transition = 'opacity 0.4s ease-out, transform 0.4s ease-out';
            observer.observe(el);
        });
    }
});

// Mobile Navigation Toggle
function toggleNav() {
    const navLinks = document.getElementById('nav-links') || document.querySelector('.nav-links');
    if (navLinks) {
        navLinks.classList.toggle('active');
    }
}

// Enhanced Copy to Clipboard Functionality
async function copyToClipboard(selector) {
    let textToCopy = '';
    let targetEl = document.querySelector(selector);
    
    if (!targetEl && selector === 'code') {
        targetEl = document.querySelector('.api-url-container code') || document.querySelector('code');
    }

    if (targetEl) {
        textToCopy = targetEl.textContent.trim();
    } else {
        textToCopy = selector;
    }

    try {
        await navigator.clipboard.writeText(textToCopy);
        
        // Find active button to display tactile feedback
        const btn = window.event ? window.event.currentTarget : document.activeElement;
        if (btn && (btn.classList.contains('copy-btn') || btn.tagName === 'BUTTON')) {
            const originalText = btn.innerHTML;
            btn.classList.add('copied');
            btn.innerHTML = '✓ Copied!';
            setTimeout(() => {
                btn.classList.remove('copied');
                btn.innerHTML = originalText;
            }, 2000);
        }
    } catch (err) {
        // Fallback for browsers without navigator.clipboard support
        const textArea = document.createElement('textarea');
        textArea.value = textToCopy;
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            const btn = window.event ? window.event.currentTarget : document.activeElement;
            if (btn && (btn.classList.contains('copy-btn') || btn.tagName === 'BUTTON')) {
                const originalText = btn.innerHTML;
                btn.classList.add('copied');
                btn.innerHTML = '✓ Copied!';
                setTimeout(() => {
                    btn.classList.remove('copied');
                    btn.innerHTML = originalText;
                }, 2000);
            }
        } catch (e) {
            alert('Clipboard copy failed.');
        }
        document.body.removeChild(textArea);
    }
}
