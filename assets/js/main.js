// Richards Systems Wiki - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.querySelector('.site-sidebar');
    const overlay = document.querySelector('.sidebar-overlay');
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    
    // ========================================
    // Sidebar toggle
    // ========================================
    
    function openSidebar() {
        sidebar.classList.add('open');
        if (overlay) overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
    
    function closeSidebar() {
        sidebar.classList.remove('open');
        if (overlay) overlay.classList.remove('active');
        document.body.style.overflow = '';
    }
    
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            if (sidebar.classList.contains('open')) {
                closeSidebar();
            } else {
                openSidebar();
            }
        });
    }
    
    if (overlay) {
        overlay.addEventListener('click', closeSidebar);
    }
    
    // Close sidebar when a nav link is clicked (on mobile)
    sidebar.querySelectorAll('.nav-link').forEach(function(link) {
        link.addEventListener('click', function(e) {
            // Only close if it's not a toggle button click
            if (!e.target.closest('.nav-toggle') && window.innerWidth <= 1024) {
                closeSidebar();
            }
        });
    });
    
    // ========================================
    // Swipe to close sidebar (touch devices)
    // ========================================
    
    let touchStartX = 0;
    let touchCurrentX = 0;
    let isSwiping = false;
    
    sidebar.addEventListener('touchstart', function(e) {
        touchStartX = e.touches[0].clientX;
        isSwiping = true;
    }, { passive: true });
    
    sidebar.addEventListener('touchmove', function(e) {
        if (!isSwiping) return;
        touchCurrentX = e.touches[0].clientX;
        const diff = touchStartX - touchCurrentX;
        
        // Only track left swipes (to close)
        if (diff > 0) {
            const translateX = Math.min(diff, sidebar.offsetWidth);
            sidebar.style.transform = `translateX(-${translateX}px)`;
            sidebar.style.transition = 'none';
        }
    }, { passive: true });
    
    sidebar.addEventListener('touchend', function() {
        if (!isSwiping) return;
        isSwiping = false;
        
        const diff = touchStartX - touchCurrentX;
        sidebar.style.transition = '';
        sidebar.style.transform = '';
        
        // If swiped more than 80px to the left, close
        if (diff > 80) {
            closeSidebar();
        }
    }, { passive: true });
    
    // Swipe from left edge to open sidebar
    document.addEventListener('touchstart', function(e) {
        if (e.touches[0].clientX < 20 && !sidebar.classList.contains('open')) {
            touchStartX = e.touches[0].clientX;
            isSwiping = true;
        }
    }, { passive: true });
    
    document.addEventListener('touchmove', function(e) {
        if (!isSwiping || sidebar.classList.contains('open')) return;
        touchCurrentX = e.touches[0].clientX;
        const diff = touchCurrentX - touchStartX;
        
        if (diff > 50) {
            openSidebar();
            isSwiping = false;
        }
    }, { passive: true });
    
    // ========================================
    // Nav tree toggle (expand/collapse)
    // ========================================
    
    const navToggles = document.querySelectorAll('.nav-toggle');
    navToggles.forEach(function(toggle) {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const navItem = this.closest('.nav-item');
            const subtree = navItem.querySelector(':scope > .nav-tree');
            if (subtree) {
                subtree.classList.toggle('expanded');
                this.classList.toggle('expanded');
            }
        });
    });
    
    // Auto-expand active path in sidebar
    const activeLink = document.querySelector('.nav-link.active');
    if (activeLink) {
        let parent = activeLink.closest('.nav-tree');
        while (parent) {
            parent.classList.add('expanded');
            const navItem = parent.closest('.nav-item');
            if (navItem) {
                const toggle = navItem.querySelector(':scope > .nav-link .nav-toggle');
                if (toggle) toggle.classList.add('expanded');
            }
            parent = parent.parentElement ? parent.parentElement.closest('.nav-tree') : null;
        }
    }
    
    // ========================================
    // Smooth scroll for anchor links
    // ========================================
    
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
    
    // ========================================
    // Handle viewport resize (fix sidebar state)
    // ========================================
    
    let lastWidth = window.innerWidth;
    window.addEventListener('resize', function() {
        const newWidth = window.innerWidth;
        
        // If resized from mobile to desktop, reset sidebar
        if (lastWidth <= 1024 && newWidth > 1024) {
            closeSidebar();
            document.body.style.overflow = '';
        }
        
        lastWidth = newWidth;
    });
});
