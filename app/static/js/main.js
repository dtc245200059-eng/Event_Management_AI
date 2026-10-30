/**
 * EventAI Pro - Main Application Controller.
 * Features: Apple-style Light/Dark/System Theme Controller, AI Recommendations Slider, Rounded Pagination.
 */

// Global CSRF Protection Interceptor for Fetch & AJAX Requests
(function setupCsrfInterceptor() {
    function getCsrfToken() {
        const meta = document.querySelector('meta[name="csrf-token"]');
        return meta ? meta.getAttribute('content') : '';
    }

    function isSameOrigin(url) {
        if (!url) return true;
        try {
            const parsed = new URL(url, window.location.origin);
            return parsed.origin === window.location.origin;
        } catch (e) {
            return false;
        }
    }

    const unsafeMethods = ['POST', 'PUT', 'DELETE', 'PATCH'];

    // 1. Intercept standard Fetch API
    const originalFetch = window.fetch;
    window.fetch = function(input, init) {
        init = init || {};
        let method = init.method;
        let targetUrl = '';

        if (typeof input === 'string') {
            targetUrl = input;
        } else if (input && typeof input === 'object') {
            targetUrl = input.url || '';
            if (!method && input.method) {
                method = input.method;
            }
        }
        method = (method || 'GET').toUpperCase();

        if (unsafeMethods.includes(method) && isSameOrigin(targetUrl)) {
            const token = getCsrfToken();
            if (token) {
                if (typeof Request !== 'undefined' && input instanceof Request && !init.headers) {
                    init.headers = new Headers(input.headers);
                }

                if (init.headers instanceof Headers) {
                    if (!init.headers.has('X-CSRFToken')) {
                        init.headers.set('X-CSRFToken', token);
                    }
                } else if (Array.isArray(init.headers)) {
                    const hasToken = init.headers.some(h => h[0].toLowerCase() === 'x-csrftoken');
                    if (!hasToken) {
                        init.headers.push(['X-CSRFToken', token]);
                    }
                } else {
                    init.headers = init.headers || {};
                    if (!init.headers['X-CSRFToken'] && !init.headers['x-csrftoken']) {
                        init.headers['X-CSRFToken'] = token;
                    }
                }
            }
        }
        return originalFetch.call(this, input, init);
    };

    // 2. Intercept legacy XMLHttpRequest if instantiated
    if (typeof XMLHttpRequest !== 'undefined') {
        const originalOpen = XMLHttpRequest.prototype.open;
        const originalSend = XMLHttpRequest.prototype.send;

        XMLHttpRequest.prototype.open = function(method, url) {
            this._csrf_method = (method || 'GET').toUpperCase();
            this._csrf_url = url;
            return originalOpen.apply(this, arguments);
        };

        XMLHttpRequest.prototype.send = function() {
            if (unsafeMethods.includes(this._csrf_method) && isSameOrigin(this._csrf_url)) {
                const token = getCsrfToken();
                if (token) {
                    try {
                        this.setRequestHeader('X-CSRFToken', token);
                    } catch (e) {
                        // Headers already sent or invalid state
                    }
                }
            }
            return originalSend.apply(this, arguments);
        };
    }

    window.getCsrfToken = getCsrfToken;
})();

document.addEventListener('DOMContentLoaded', () => {
    // 1. Apple-style Theme Controller (Light / Dark / Auto System)
    initThemeController();

    // 2. AI Recommendations: Auto-scroll & Drag to Swipe
    const recsContainer = document.getElementById('aiRecommendationsContainer');
    if (recsContainer) {
        loadAIRecommendations(recsContainer);
    }

    // 3. Home Events Modern Pagination (6 events per page)
    initHomeEventsPagination();

    // 4. Apple Mobile Drawer Controller (Slide-in Menu)
    initMobileDrawer();

    // 5. Apple iOS Bottom Navigation Bar (Tab active state & actions)
    initMobileNavigation();
});

/**
 * Initializes Theme Switcher supporting Light, Dark, and System modes.
 * Features: Instant sync without FOUC, butter-smooth 250ms crossfade on click,
 * accessibility aria-labels, and themeChanged event dispatch for dynamic components.
 */
function initThemeController() {
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const themeIcon = document.getElementById('themeIcon');
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

    // 1. Resolve current theme from localStorage or system fallback
    let savedTheme = localStorage.getItem('theme');
    let currentTheme = savedTheme;
    if (!currentTheme || (currentTheme !== 'light' && currentTheme !== 'dark')) {
        currentTheme = mediaQuery.matches ? 'dark' : 'light';
    }

    // 2. Synchronize DOM & icons on load without animation
    applyTheme(currentTheme, false);

    // 3. Listen for OS theme preference changes if user hasn't explicitly selected one
    mediaQuery.addEventListener('change', (e) => {
        if (!localStorage.getItem('theme')) {
            const systemTheme = e.matches ? 'dark' : 'light';
            applyTheme(systemTheme, true);
        }
    });

    // 4. Click Toggle Handler
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const activeTheme = document.documentElement.getAttribute('data-theme') || 'dark';
            const nextTheme = activeTheme === 'dark' ? 'light' : 'dark';
            try {
                localStorage.setItem('theme', nextTheme);
            } catch (err) {
                console.warn('LocalStorage unavailable for theme storage:', err);
            }
            applyTheme(nextTheme, true);
        });
    }

    function applyTheme(theme, animate = false) {
        if (animate) {
            document.documentElement.classList.add('theme-transition');
            setTimeout(() => {
                document.documentElement.classList.remove('theme-transition');
            }, 300);
        }

        document.documentElement.setAttribute('data-theme', theme);
        document.documentElement.setAttribute('data-bs-theme', theme);

        // Icon matches the active theme state
        if (themeIcon) {
            themeIcon.className = theme === 'dark' ? 'fa-solid fa-moon' : 'fa-solid fa-sun';
        }

        // Accessibility attributes for screen readers and tooltips
        if (themeToggleBtn) {
            const nextLabel = theme === 'dark' ? 'Chế độ Sáng' : 'Chế độ Tối';
            const currentLabel = theme === 'dark' ? 'Chế độ Tối' : 'Chế độ Sáng';
            themeToggleBtn.setAttribute('aria-label', `Chuyển sang ${nextLabel}`);
            themeToggleBtn.setAttribute('title', `${currentLabel} (Nhấp để chuyển sang ${nextLabel})`);
        }

        // Broadcast event for custom interactive elements (e.g. Chart.js in Dashboard)
        window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme: theme } }));
    }
}

/**
 * Loads AI event recommendations and wires smooth infinite track.
 */
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
                    <div class="apple-card clickable-event-card h-100" onclick="if(!window.aiSliderDragged) window.location.href='/events/${item.id}'" style="cursor: pointer;">
                        <div class="event-card-img-wrapper position-relative">
                            <img src="${item.banner_url || 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=600'}" class="event-card-img" alt="${item.title}" draggable="false" loading="lazy" decoding="async" width="400" height="225">
                            <span class="event-badge-category">${item.category}</span>
                            <div style="position: absolute; bottom: 8px; right: 8px; background: rgba(0, 113, 227, 0.92); color: white; font-size: 0.72rem; font-weight: 600; padding: 3px 8px; border-radius: var(--radius-pill); backdrop-filter: blur(8px);">
                                ✨ Phù hợp ${item.match_percentage}%
                            </div>
                        </div>
                        <div class="event-card-body d-flex flex-column p-4">
                            <h5 class="event-card-title mb-2" style="font-size: 1.05rem;">${item.title}</h5>
                            <div class="event-meta-item">
                                <i class="fa-solid fa-calendar-day text-primary" style="font-size: 0.85rem;"></i>
                                <span>${item.start_date}</span>
                            </div>
                            <div class="event-meta-item">
                                <i class="fa-solid fa-location-dot text-danger" style="font-size: 0.85rem;"></i>
                                <span class="text-truncate">${item.location_address || 'Online Zoom'}</span>
                            </div>
                            <div style="font-size: 0.78rem; color: var(--text-secondary); margin-bottom: 0.8rem; line-height: 1.4;" class="text-truncate-2">
                                💡 ${item.reason}
                            </div>
                            <div class="mt-auto pt-2">
                                <a href="/events/${item.id}" class="btn btn-sm btn-secondary w-100" draggable="false">Xem Chi Tiết</a>
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

    // Check user preference for reduced motion
    const prefersReducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // Clone items once for continuous infinite seamless looping (if motion allowed)
    const originalChildren = Array.from(slider.children);
    if (!prefersReducedMotion && originalChildren.length > 0 && !slider.dataset.infiniteReady) {
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
    let isIntersecting = false;
    let animationFrameId = null;
    window.aiSliderDragged = false;
    const scrollSpeed = 0.85; // Pixels per frame (ultra smooth 60fps)

    function startLoop() {
        if (prefersReducedMotion) return;
        if (!animationFrameId && isIntersecting && !document.hidden) {
            animationFrameId = requestAnimationFrame(loopScroll);
        }
    }

    function stopLoop() {
        if (animationFrameId) {
            cancelAnimationFrame(animationFrameId);
            animationFrameId = null;
        }
    }

    function loopScroll() {
        if (!isDown && !isHovered && isIntersecting && !document.hidden) {
            slider.scrollLeft += scrollSpeed;

            // Half width represents the exact length of the original item set
            const halfWidth = slider.scrollWidth / 2;
            if (halfWidth > 0 && slider.scrollLeft >= halfWidth) {
                slider.scrollLeft -= halfWidth; // Seamless wrap with 0 glitch
            }
        }
        if (isIntersecting && !document.hidden && !prefersReducedMotion) {
            animationFrameId = requestAnimationFrame(loopScroll);
        } else {
            animationFrameId = null;
        }
    }

    // 1. IntersectionObserver: Only animate when element is visible in viewport
    if ('IntersectionObserver' in window && !prefersReducedMotion) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                isIntersecting = entry.isIntersecting;
                if (isIntersecting) {
                    startLoop();
                } else {
                    stopLoop();
                }
            });
        }, { threshold: 0.1 });
        observer.observe(slider);
    } else if (!prefersReducedMotion) {
        isIntersecting = true;
        startLoop();
    }

    // 2. Page Visibility API: Stop loop when tab is backgrounded
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            stopLoop();
        } else if (isIntersecting) {
            startLoop();
        }
    });

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
            infoContainer.innerHTML = `Hiển thị trang <strong>${currentPage}</strong> / <strong>${totalPages}</strong> (Tổng cộng ${totalEvents} sự kiện)`;
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
        if (e.target.closest('a') || e.target.closest('button')) {
            return;
        }
        if (window.aiSliderDragged) {
            return;
        }
        window.location.href = card.dataset.eventUrl;
    }
});

/**
 * Apple iOS Mobile Slide-in Drawer Controller
 * Features: Smooth slide-in, backdrop blur, lock body scroll, theme switcher sync.
 */
function initMobileDrawer() {
    const openBtn = document.getElementById('mobileDrawerOpenBtn');
    const drawer = document.getElementById('appleMobileDrawer');
    const backdrop = document.getElementById('appleDrawerBackdrop');
    const closeBtn = document.getElementById('appleDrawerCloseBtn');
    const bottomNavMenuTab = document.getElementById('bottomNavMenuTab');
    const drawerThemeToggleBtn = document.getElementById('drawerThemeToggleBtn');
    const drawerThemeLabel = document.getElementById('drawerThemeLabel');

    if (!drawer || !backdrop) return;

    function openDrawer() {
        if (typeof window.closeEventAIChat === 'function') {
            window.closeEventAIChat();
        }
        drawer.classList.add('open', 'active');
        backdrop.classList.add('open', 'active');
        document.body.classList.add('mobile-drawer-open');
        updateDrawerThemeLabel();
    }

    function closeDrawer() {
        drawer.classList.remove('open', 'active');
        backdrop.classList.remove('open', 'active');
        document.body.classList.remove('mobile-drawer-open');
    }

    // Expose globally for cross-component orchestration
    window.openMobileDrawer = openDrawer;
    window.closeMobileDrawer = closeDrawer;

    function updateDrawerThemeLabel() {
        if (!drawerThemeLabel) return;
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
        drawerThemeLabel.textContent = currentTheme === 'dark' ? 'Chế độ Tối' : 'Chế độ Sáng';
    }

    if (openBtn) openBtn.addEventListener('click', openDrawer);
    if (bottomNavMenuTab) bottomNavMenuTab.addEventListener('click', openDrawer);
    if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
    if (backdrop) backdrop.addEventListener('click', closeDrawer);

    // Auto close drawer when clicking any link inside
    drawer.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            closeDrawer();
        });
    });

    // Escape key closes drawer
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && (drawer.classList.contains('open') || drawer.classList.contains('active'))) {
            closeDrawer();
        }
    });

    // Theme toggle inside drawer
    if (drawerThemeToggleBtn) {
        drawerThemeToggleBtn.addEventListener('click', () => {
            const themeToggleBtn = document.getElementById('themeToggleBtn');
            if (themeToggleBtn) {
                themeToggleBtn.click();
                updateDrawerThemeLabel();
            }
        });
    }

    window.addEventListener('themeChanged', updateDrawerThemeLabel);
    updateDrawerThemeLabel();
}

/**
 * Apple iOS Bottom Navigation Bar Controller
 * Features: Auto route highlighting, AI sparkling tab integration, haptic feedback simulation.
 */
function initMobileNavigation() {
    const currentPath = window.location.pathname;
    const homeTab = document.getElementById('bottomNavHomeTab');
    const eventsTab = document.getElementById('bottomNavEventsTab');
    const aiTab = document.getElementById('bottomNavAiTab');
    const roleTab = document.getElementById('bottomNavRoleTab');

    // Highlight active destination
    if (homeTab && currentPath === '/') {
        homeTab.classList.add('active');
    } else if (eventsTab && (currentPath.startsWith('/events') || currentPath.startsWith('/event'))) {
        eventsTab.classList.add('active');
    } else if (roleTab && (
        currentPath.startsWith('/admin') ||
        currentPath.startsWith('/checkin') ||
        currentPath.startsWith('/tickets') ||
        currentPath.startsWith('/auth')
    )) {
        roleTab.classList.add('active');
    }

    // AI Tab triggers the AI Assistant Sheet
    if (aiTab) {
        aiTab.addEventListener('click', (e) => {
            e.preventDefault();
            if (typeof window.closeMobileDrawer === 'function') {
                window.closeMobileDrawer();
            }
            if (typeof window.openEventAIChat === 'function') {
                window.openEventAIChat();
            } else {
                window.location.href = '/ai/workspace';
            }
        });
    }
}

/**
 * Global CSRF Token retriever for Fetch/AJAX requests.
 */
window.getCsrfToken = function() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? (meta.getAttribute('content') || '') : '';
};


