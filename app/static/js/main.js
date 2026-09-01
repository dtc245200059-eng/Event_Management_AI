/**
 * Main Application JS Controller.
 * Features: Auto-scroll & Drag-to-swipe AI Recommendations + Modern Pagination.
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Theme Toggle (Dark / Light mode)
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const currentTheme = localStorage.getItem('theme') || 'dark';

    document.documentElement.setAttribute('data-theme', currentTheme);
    updateThemeIcon(currentTheme);

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const current = document.documentElement.getAttribute('data-theme');
            const nextTheme = current === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', nextTheme);
            localStorage.setItem('theme', nextTheme);
            updateThemeIcon(nextTheme);
        });
    }

    function updateThemeIcon(theme) {
        if (!themeToggleBtn) return;
        themeToggleBtn.innerHTML = theme === 'dark' ? '☀️' : '🌙';
    }

    // 2. AI Recommendations: Auto-scroll & Drag to Swipe
    const recsContainer = document.getElementById('aiRecommendationsContainer');
    if (recsContainer) {
        loadAIRecommendations(recsContainer);
    }

    // 3. Home Events Modern Pagination (6 events per page)
    initHomeEventsPagination();
});

async function loadAIRecommendations(container) {
    try {
        const response = await fetch('/api/ai/recommendations');
        const data = await response.json();

        if (data.success && data.recommendations && data.recommendations.length > 0) {
            container.innerHTML = '';
            data.recommendations.forEach(item => {
                const card = document.createElement('div');
                card.className = 'ai-slider-item';
                
                card.innerHTML = `
                    <div class="event-card clickable-event-card h-100" onclick="if(!window.aiSliderDragged) window.location.href='/events/${item.id}'">
                        <div class="event-card-img-wrapper">
                            <img src="${item.banner_url || 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=600'}" class="event-card-img" alt="${item.title}" draggable="false">
                            <span class="event-badge-category">${item.category}</span>
                            <div style="position: absolute; bottom: 8px; right: 8px; background: rgba(99, 102, 241, 0.9); color: white; font-size: 0.75rem; font-weight: 700; padding: 3px 8px; border-radius: 9999px;">
                                ✨ Phù hợp ${item.match_percentage}%
                            </div>
                        </div>
                        <div class="event-card-body d-flex flex-column">
                            <h5 class="event-card-title">${item.title}</h5>
                            <div class="event-meta-item">
                                <i class="fa-solid fa-calendar-day text-primary"></i>
                                <span>${item.start_date}</span>
                            </div>
                            <div class="event-meta-item">
                                <i class="fa-solid fa-location-dot text-danger"></i>
                                <span class="text-truncate">${item.location_address || 'Online Zoom'}</span>
                            </div>
                            <div style="font-size: 0.76rem; color: #a855f7; margin-bottom: 0.8rem;" class="text-truncate-2">
                                💡 ${item.reason}
                            </div>
                            <div class="mt-auto pt-2">
                                <a href="/events/${item.id}" class="btn btn-sm btn-primary-gradient w-100" draggable="false">Xem Chi Tiết</a>
                            </div>
                        </div>
                    </div>
                `;
                container.appendChild(card);
            });
        }
    } catch (e) {
        console.log("Could not load recommendations:", e);
    }

    // Attach Infinite Seamless Loop Auto-Scroll & Drag listeners
    setupInfiniteSeamlessScroll(container);
}

function setupInfiniteSeamlessScroll(slider) {
    if (!slider) return;

    // Clone items once for continuous infinite seamless looping
    const originalChildren = Array.from(slider.children);
    if (originalChildren.length > 0 && !slider.dataset.infiniteReady) {
        originalChildren.forEach(child => {
            const clone = child.cloneNode(true);
            slider.appendChild(clone);
        });
        slider.dataset.infiniteReady = "true";
    }

    let isDown = false;
    let startX = 0;
    let scrollLeft = 0;
    let isHovered = false;
    let animationFrameId = null;
    window.aiSliderDragged = false;
    const scrollSpeed = 0.85; // Pixels per frame (ultra smooth 60fps)

    function loopScroll() {
        if (!isDown && !isHovered) {
            slider.scrollLeft += scrollSpeed;

            // Half width represents the exact length of the original item set
            const halfWidth = slider.scrollWidth / 2;
            if (halfWidth > 0 && slider.scrollLeft >= halfWidth) {
                slider.scrollLeft -= halfWidth; // Seamless wrap with 0 glitch
            }
        }
        animationFrameId = requestAnimationFrame(loopScroll);
    }

    // Start 60fps Loop
    if (animationFrameId) cancelAnimationFrame(animationFrameId);
    animationFrameId = requestAnimationFrame(loopScroll);

    // Pause on Mouse Hover
    slider.addEventListener('mouseenter', () => {
        isHovered = true;
    });

    slider.addEventListener('mouseleave', () => {
        isHovered = false;
        if (isDown) {
            isDown = false;
            slider.classList.remove('dragging');
        }
    });

    // Mouse Drag / Swipe
    slider.addEventListener('mousedown', (e) => {
        isDown = true;
        window.aiSliderDragged = false;
        slider.classList.add('dragging');
        startX = e.pageX - slider.offsetLeft;
        scrollLeft = slider.scrollLeft;
    });

    slider.addEventListener('mouseup', () => {
        if (isDown) {
            isDown = false;
            slider.classList.remove('dragging');
            setTimeout(() => {
                window.aiSliderDragged = false;
            }, 100);
        }
    });

    slider.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - slider.offsetLeft;
        const walk = (x - startX) * 1.4; // Drag sensitivity
        if (Math.abs(x - startX) > 6) {
            window.aiSliderDragged = true;
        }
        slider.scrollLeft = scrollLeft - walk;

        // Wrap around seamlessly during drag as well
        const halfWidth = slider.scrollWidth / 2;
        if (halfWidth > 0) {
            if (slider.scrollLeft >= halfWidth) {
                slider.scrollLeft -= halfWidth;
                scrollLeft -= halfWidth;
            } else if (slider.scrollLeft <= 0) {
                slider.scrollLeft += halfWidth;
                scrollLeft += halfWidth;
            }
        }
    });

    // Touch Support for Mobile / Tablet
    slider.addEventListener('touchstart', () => {
        isHovered = true;
    }, { passive: true });

    slider.addEventListener('touchend', () => {
        setTimeout(() => {
            isHovered = false;
        }, 1200);
    }, { passive: true });
}

function initHomeEventsPagination() {
    const cardWrappers = document.querySelectorAll('.home-event-card-wrapper');
    const paginationSection = document.getElementById('homePaginationSection');
    const pageNumbersContainer = document.getElementById('homePageNumbers');
    const prevBtn = document.getElementById('homePrevPageBtn');
    const nextBtn = document.getElementById('homeNextPageBtn');
    const infoContainer = document.getElementById('homePaginationInfo');

    if (!cardWrappers || cardWrappers.length === 0 || !paginationSection) return;

    const perPage = 6;
    const totalEvents = cardWrappers.length;
    const totalPages = Math.ceil(totalEvents / perPage);

    if (totalPages <= 1) {
        paginationSection.style.display = 'none';
        return;
    }

    let currentPage = 1;

    function renderPage(page) {
        currentPage = page;
        const startIndex = (page - 1) * perPage;
        const endIndex = startIndex + perPage;

        cardWrappers.forEach((card, index) => {
            if (index >= startIndex && index < endIndex) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });

        // Update Prev / Next buttons state
        if (prevBtn) {
            prevBtn.disabled = (currentPage === 1);
            prevBtn.classList.toggle('disabled', currentPage === 1);
        }
        if (nextBtn) {
            nextBtn.disabled = (currentPage === totalPages);
            nextBtn.classList.toggle('disabled', currentPage === totalPages);
        }

        // Render Circular Page Number Buttons
        if (pageNumbersContainer) {
            pageNumbersContainer.innerHTML = '';
            for (let i = 1; i <= totalPages; i++) {
                const btn = document.createElement('button');
                btn.className = `page-btn-circle ${i === currentPage ? 'active' : ''}`;
                btn.textContent = i;
                btn.type = 'button';
                btn.addEventListener('click', () => {
                    renderPage(i);
                    scrollToSection();
                });
                pageNumbersContainer.appendChild(btn);
            }
        }

        // Update Info Text
        if (infoContainer) {
            infoContainer.innerHTML = `Hiển thị trang <strong>${currentPage}</strong> trên tổng số <strong>${totalPages}</strong> trang (Tổng cộng ${totalEvents} sự kiện)`;
        }
    }

    function scrollToSection() {
        const section = document.getElementById('upcomingEventsSection');
        if (section) {
            section.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            if (currentPage > 1) {
                renderPage(currentPage - 1);
                scrollToSection();
            }
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            if (currentPage < totalPages) {
                renderPage(currentPage + 1);
                scrollToSection();
            }
        });
    }

    // Initial render page 1
    renderPage(1);
}

// Global Click Handler for Clickable Event Cards
document.addEventListener('click', (e) => {
    const card = e.target.closest('.clickable-event-card');
    if (card && card.dataset.eventUrl) {
        // If clicked on an internal link or button, let it handle naturally
        if (e.target.closest('a') || e.target.closest('button')) {
            return;
        }
        // If user was dragging the slider, prevent navigation
        if (window.aiSliderDragged) {
            return;
        }
        window.location.href = card.dataset.eventUrl;
    }
});
