// Richards Systems Wiki - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    var sidebar = document.querySelector('.site-sidebar');
    var overlay = document.querySelector('.sidebar-overlay');
    var sidebarToggle = document.querySelector('.sidebar-toggle');
    
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
            if (!e.target.closest('.nav-toggle') && window.innerWidth <= 1024) {
                closeSidebar();
            }
        });
    });
    
    // ========================================
    // Swipe to close sidebar (touch devices)
    // ========================================
    
    var touchStartX = 0;
    var touchCurrentX = 0;
    var isSwiping = false;
    
    sidebar.addEventListener('touchstart', function(e) {
        touchStartX = e.touches[0].clientX;
        isSwiping = true;
    }, { passive: true });
    
    sidebar.addEventListener('touchmove', function(e) {
        if (!isSwiping) return;
        touchCurrentX = e.touches[0].clientX;
        var diff = touchStartX - touchCurrentX;
        if (diff > 0) {
            sidebar.style.transform = 'translateX(-' + Math.min(diff, sidebar.offsetWidth) + 'px)';
            sidebar.style.transition = 'none';
        }
    }, { passive: true });
    
    sidebar.addEventListener('touchend', function() {
        if (!isSwiping) return;
        isSwiping = false;
        var diff = touchStartX - touchCurrentX;
        sidebar.style.transition = '';
        sidebar.style.transform = '';
        if (diff > 80) closeSidebar();
    }, { passive: true });
    
    // Swipe from left edge to open
    document.addEventListener('touchstart', function(e) {
        if (e.touches[0].clientX < 20 && !sidebar.classList.contains('open')) {
            touchStartX = e.touches[0].clientX;
            isSwiping = true;
        }
    }, { passive: true });
    
    document.addEventListener('touchmove', function(e) {
        if (!isSwiping || sidebar.classList.contains('open')) return;
        touchCurrentX = e.touches[0].clientX;
        if (touchCurrentX - touchStartX > 50) {
            openSidebar();
            isSwiping = false;
        }
    }, { passive: true });
    
    // ========================================
    // Nav tree toggle (expand/collapse)
    // ========================================
    
    document.querySelectorAll('.nav-toggle').forEach(function(toggle) {
        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            var navItem = this.closest('.nav-item');
            var subtree = navItem.querySelector(':scope > .nav-tree');
            if (subtree) {
                subtree.classList.toggle('expanded');
                this.classList.toggle('expanded');
            }
        });
    });
    
    // Auto-expand active path in sidebar
    var activeLink = document.querySelector('.nav-link.active');
    if (activeLink) {
        var parent = activeLink.closest('.nav-tree');
        while (parent) {
            parent.classList.add('expanded');
            var navItem = parent.closest('.nav-item');
            if (navItem) {
                var toggle = navItem.querySelector(':scope > .nav-link .nav-toggle');
                if (toggle) toggle.classList.add('expanded');
            }
            parent = parent.parentElement ? parent.parentElement.closest('.nav-tree') : null;
        }
    }
    
    // ========================================
    // Search functionality
    // ========================================
    
    var searchIndex = null;
    var isSubpage = window.location.pathname.includes('/pages/');
    var basePath = isSubpage ? '../' : '';
    
    // Load search index
    fetch(basePath + 'assets/search-index.json')
        .then(function(r) { return r.json(); })
        .then(function(data) { searchIndex = data; })
        .catch(function() {});
    
    // Attach to all search inputs
    document.querySelectorAll('.search-input').forEach(function(input) {
        var resultsContainer = input.parentElement.querySelector('.search-results');
        if (!resultsContainer) return;
        
        var debounceTimer;
        
        input.addEventListener('input', function() {
            var self = this;
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(function() {
                performSearch(self.value.trim(), resultsContainer);
            }, 150);
        });
        
        input.addEventListener('focus', function() {
            if (this.value.trim().length >= 2) {
                performSearch(this.value.trim(), resultsContainer);
            }
        });
        
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                resultsContainer.classList.remove('active');
                input.blur();
            }
        });
    });
    
    // Close all results when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.search-input-wrapper')) {
            document.querySelectorAll('.search-results').forEach(function(r) {
                r.classList.remove('active');
            });
        }
    });
    
    function performSearch(query, container) {
        if (!searchIndex || query.length < 2) {
            container.classList.remove('active');
            return;
        }
        
        var q = query.toLowerCase();
        var matches = searchIndex.filter(function(item) {
            return item.title.toLowerCase().includes(q) ||
                   item.snippet.toLowerCase().includes(q) ||
                   item.path.toLowerCase().includes(q);
        }).slice(0, 10);
        
        if (matches.length === 0) {
            container.innerHTML = '<div class="search-no-results">No pages found</div>';
            container.classList.add('active');
            return;
        }
        
        var html = '';
        matches.forEach(function(item) {
            var url = item.external ? item.url : (isSubpage ? item.url.replace('pages/', '') : item.url);
            var target = item.external ? ' target="_blank"' : '';
            html += '<a class="search-result-item" href="' + url + '"' + target + '>';
            html += '<div class="result-title">' + highlightMatch(item.title, query) + '</div>';
            if (item.path) {
                html += '<div class="result-path">' + item.path + '</div>';
            }
            html += '</a>';
        });
        
        container.innerHTML = html;
        container.classList.add('active');
    }
    
    function highlightMatch(text, query) {
        var idx = text.toLowerCase().indexOf(query.toLowerCase());
        if (idx === -1) return text;
        return text.substring(0, idx) + '<strong>' + text.substring(idx, idx + query.length) + '</strong>' + text.substring(idx + query.length);
    }
    
    // ========================================
    // Copy email to clipboard
    // ========================================
    
    document.querySelectorAll('.copy-email-btn').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            var email = this.getAttribute('data-email');
            navigator.clipboard.writeText(email).then(function() {
                var original = btn.innerHTML;
                var textEl = btn.querySelector('.copy-text');
                if (textEl) {
                    textEl.textContent = 'Copied!';
                    setTimeout(function() { textEl.textContent = email; }, 1500);
                }
            });
        });
    });
    
    // ========================================
    // Smooth scroll for anchor links
    // ========================================
    
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            var target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
    
    // ========================================
    // Handle viewport resize
    // ========================================
    
    var lastWidth = window.innerWidth;
    window.addEventListener('resize', function() {
        if (lastWidth <= 1024 && window.innerWidth > 1024) {
            closeSidebar();
            document.body.style.overflow = '';
        }
        lastWidth = window.innerWidth;
    });
});
