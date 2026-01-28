document.addEventListener('DOMContentLoaded', () => {

    // 1. Smooth Scroll Handler
    const internalLinks = document.querySelectorAll('a[href^="#"]');

    internalLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                const offsetPosition = targetElement.offsetTop - 100;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // 2. Scroll-Triggered Reveal (Intersection Observer)
    const revealOptions = {
        threshold: 0.15,
        rootMargin: "0px 0px -50px 0px"
    };

    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target); // Only animate once
            }
        });
    }, revealOptions);

    const fadeElements = document.querySelectorAll('.fade-in-up');
    fadeElements.forEach(el => revealObserver.observe(el));

    // 3. Header Logic (Shrink and Blur on Scroll)
    const headerPill = document.querySelector('.glass-pill');
    const hamburger = document.getElementById('hamburger-menu');
    const mobileNav = document.getElementById('mobile-nav');

    // Hamburger Toggle
    hamburger.addEventListener('click', () => {
        mobileNav.classList.toggle('active');
        const spans = hamburger.querySelectorAll('span');
        if (mobileNav.classList.contains('active')) {
            spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
            spans[1].style.opacity = '0';
            spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
        } else {
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        }
    });

    // Close mobile nav on link click
    mobileNav.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            mobileNav.classList.remove('active');
            hamburger.querySelectorAll('span').forEach(s => s.style.transform = 'none');
            hamburger.querySelectorAll('span')[1].style.opacity = '1';
        });
    });

    window.addEventListener('scroll', () => {
        const currentScrollY = window.scrollY;

        if (currentScrollY > 50) {
            headerPill.style.height = '50px';
            headerPill.style.padding = '0 20px';
            headerPill.style.backdropFilter = 'blur(25px)';
            headerPill.style.backgroundColor = 'rgba(255, 255, 255, 0.9)';
        } else {
            headerPill.style.height = '60px';
            headerPill.style.padding = '0 30px';
            headerPill.style.backdropFilter = 'blur(15px)';
            headerPill.style.backgroundColor = 'rgba(255, 255, 255, 0.7)';
        }
    });

    // Extra touch: subtle parallax on hero image
    window.addEventListener('scroll', () => {
        const heroImage = document.querySelector('.hero-visual img');
        if (heroImage) {
            const scroll = window.pageYOffset;
            heroImage.style.transform = `scale(1.05) translateY(${scroll * 0.05}px)`;
        }
    });

});
