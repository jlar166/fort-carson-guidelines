// Fort Carson EMS Guidelines - Main Application JavaScript
// Handles: Search, Recent Pages, Dark Mode, and Utilities

(function () {
    'use strict';

    // ==========================================
    // PAGE DATA - All searchable content
    // ==========================================
    const pageData = [
        { title: 'Introduction', url: 'index.html', keywords: 'introduction home welcome guidelines overview', category: 'General' },
        { title: 'Patient Determination', url: 'pages/patient-determination.html', keywords: 'patient determination assessment a002', category: 'General' },
        { title: 'Consent', url: 'pages/consent.html', keywords: 'consent implied decision making capacity a003', category: 'General' },
        { title: 'General Supportive Care', url: 'pages/supportive-care.html', keywords: 'supportive care vital signs bls als a005', category: 'General' },
        { title: 'Pediatric Overview', url: 'pages/pediatric.html', keywords: 'pediatric children infant neonate toddler vital signs a006', category: 'General' },
        { title: 'Airway Management', url: 'pages/airway.html', keywords: 'airway intubation opa npa cpap igel cricothyrotomy b002', category: 'Procedures' },
        { title: 'Pain Management', url: 'pages/pain.html', keywords: 'pain fentanyl ketamine hydromorphone acetaminophen b004', category: 'Procedures' },
        { title: 'Respiratory Emergencies', url: 'pages/respiratory.html', keywords: 'respiratory asthma copd chf dyspnea wheezing albuterol c001', category: 'Medical' },
        { title: 'Cardiac Emergencies', url: 'pages/cardiac.html', keywords: 'cardiac arrest acs stemi bradycardia tachycardia vfib vtach d001', category: 'Medical' },
        { title: 'CVA/Stroke', url: 'pages/stroke.html', keywords: 'stroke cva befast tpa e002', category: 'Medical' },
        { title: 'Seizures', url: 'pages/seizure.html', keywords: 'seizure eclampsia midazolam lorazepam ativan e003', category: 'Medical' },
        { title: 'Diabetic Emergency', url: 'pages/diabetes.html', keywords: 'diabetes hypoglycemia hyperglycemia dextrose glucagon e007', category: 'Medical' },
        { title: 'Allergy/Anaphylaxis', url: 'pages/allergic.html', keywords: 'allergy anaphylaxis epinephrine benadryl diphenhydramine e005', category: 'Medical' },
        { title: 'Standard Trauma Care', url: 'pages/trauma-general.html', keywords: 'trauma bleeding tourniquet hemorrhage f001', category: 'Trauma' },
        { title: 'Hemorrhagic Shock', url: 'pages/hemorrhagic.html', keywords: 'hemorrhagic shock txa tranexamic acid bleeding f002', category: 'Trauma' },
        { title: 'Burn Injuries', url: 'pages/burns.html', keywords: 'burns thermal chemical electrical bsa f007', category: 'Trauma' },
        { title: 'Extremity Injuries', url: 'pages/extremity.html', keywords: 'extremity fracture dislocation amputation splint f006', category: 'Trauma' },
        { title: 'Medication Overview', url: 'pages/medications.html', keywords: 'medication drug pregnancy category h000', category: 'Medications' },
        { title: 'Medication List', url: 'pages/med-list.html', keywords: 'medication list drugs emt paramedic', category: 'Medications' },
        { title: 'Pediatric Calculator', url: 'pages/calculator.html', keywords: 'calculator pediatric weight dosing dose kg', category: 'Tools' },
        { title: 'Drug Quick Cards', url: 'pages/quick-cards.html', keywords: 'quick cards drug reference', category: 'Tools' },
        { title: 'Algorithm Flowcharts', url: 'pages/algorithms.html', keywords: 'algorithm flowchart decision tree cardiac arrest', category: 'Tools' }
    ];

    // ==========================================
    // RECENTLY VIEWED PAGES
    // ==========================================
    const RECENT_KEY = 'ems_recent_pages';
    const MAX_RECENT = 5;

    function getRecentPages() {
        try {
            return JSON.parse(localStorage.getItem(RECENT_KEY)) || [];
        } catch (e) {
            return [];
        }
    }

    function saveRecentPage(title, url) {
        let recent = getRecentPages();
        // Remove if already exists
        recent = recent.filter(p => p.url !== url);
        // Add to beginning
        recent.unshift({ title, url, time: Date.now() });
        // Keep only MAX_RECENT
        recent = recent.slice(0, MAX_RECENT);
        localStorage.setItem(RECENT_KEY, JSON.stringify(recent));
    }

    function renderRecentPages() {
        const container = document.getElementById('recentPages');
        if (!container) return;

        const recent = getRecentPages();
        if (recent.length === 0) {
            container.style.display = 'none';
            return;
        }

        container.style.display = 'block';
        const list = container.querySelector('.recent-list');
        if (!list) return;

        list.innerHTML = recent.map(p => {
            const relUrl = getRelativeUrl(p.url);
            return `<li><a href="${relUrl}">${p.title}</a></li>`;
        }).join('');
    }

    // ==========================================
    // SEARCH FUNCTIONALITY
    // ==========================================
    function initSearch() {
        const searchInput = document.getElementById('searchInput');
        const searchResults = document.getElementById('searchResults');

        if (!searchInput || !searchResults) return;

        searchInput.addEventListener('input', function () {
            const query = this.value.toLowerCase().trim();

            if (query.length < 2) {
                searchResults.style.display = 'none';
                searchResults.innerHTML = '';
                return;
            }

            const results = pageData.filter(page => {
                return page.title.toLowerCase().includes(query) ||
                    page.keywords.toLowerCase().includes(query) ||
                    page.category.toLowerCase().includes(query);
            });

            if (results.length === 0) {
                searchResults.innerHTML = '<div class="no-results">No results found</div>';
            } else {
                searchResults.innerHTML = results.map(r => {
                    const relUrl = getRelativeUrl(r.url);
                    return `<a href="${relUrl}" class="search-result-item">
                        <span class="result-title">${r.title}</span>
                        <span class="result-category">${r.category}</span>
                    </a>`;
                }).join('');
            }
            searchResults.style.display = 'block';
        });

        // Close results when clicking outside
        document.addEventListener('click', function (e) {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.style.display = 'none';
            }
        });

        // Handle Enter key
        searchInput.addEventListener('keydown', function (e) {
            if (e.key === 'Enter') {
                const firstResult = searchResults.querySelector('.search-result-item');
                if (firstResult) {
                    window.location.href = firstResult.href;
                }
            }
        });
    }

    // ==========================================
    // DARK MODE
    // ==========================================
    const DARK_MODE_KEY = 'ems_dark_mode';

    function isDarkMode() {
        return localStorage.getItem(DARK_MODE_KEY) === 'true';
    }

    function setDarkMode(enabled) {
        localStorage.setItem(DARK_MODE_KEY, enabled);
        document.body.classList.toggle('dark-mode', enabled);
        updateDarkModeButton();
    }

    function toggleDarkMode() {
        setDarkMode(!isDarkMode());
    }

    function updateDarkModeButton() {
        const btn = document.getElementById('darkModeToggle');
        if (btn) {
            btn.innerHTML = isDarkMode() ? '☀️ Light' : '🌙 Dark';
        }
    }

    function initDarkMode() {
        if (isDarkMode()) {
            document.body.classList.add('dark-mode');
        }
        updateDarkModeButton();

        const btn = document.getElementById('darkModeToggle');
        if (btn) {
            btn.addEventListener('click', toggleDarkMode);
        }
    }

    // ==========================================
    // PRINT FUNCTIONALITY
    // ==========================================
    function initPrint() {
        const btn = document.getElementById('printBtn');
        if (btn) {
            btn.addEventListener('click', function () {
                window.print();
            });
        }
    }

    // ==========================================
    // UTILITIES
    // ==========================================
    function getRelativeUrl(url) {
        // Adjust URL based on current page location
        const isInPages = window.location.pathname.includes('/pages/');
        if (isInPages) {
            if (url === 'index.html') {
                return '../index.html';
            } else if (url.startsWith('pages/')) {
                return url.replace('pages/', '');
            }
        }
        return url;
    }

    function getCurrentPageInfo() {
        const path = window.location.pathname;
        const filename = path.split('/').pop() || 'index.html';
        const page = pageData.find(p => p.url.endsWith(filename));
        return page || { title: document.title, url: filename };
    }

    // ==========================================
    // MOBILE MENU (existing functionality)
    // ==========================================
    window.toggleMenu = function () {
        const navContent = document.getElementById('navContent');
        const menuToggle = document.querySelector('.menu-toggle');
        if (navContent && menuToggle) {
            navContent.classList.toggle('open');
            menuToggle.classList.toggle('active');
        }
    };

    // ==========================================
    // ACCORDION FUNCTIONALITY
    // ==========================================
    function initAccordions() {
        const accHandlers = document.getElementsByClassName("accordion-header");

        for (let i = 0; i < accHandlers.length; i++) {
            accHandlers[i].addEventListener("click", function () {
                /* Toggle between adding and removing the "active" class,
                to highlight the button that controls the panel */
                this.classList.toggle("active");

                /* Toggle between hiding and showing the active panel */
                const panel = this.nextElementSibling;
                if (panel.style.maxHeight || panel.classList.contains('open')) {
                    panel.classList.remove('open');
                    panel.style.maxHeight = null;
                } else {
                    panel.classList.add('open');
                    panel.style.maxHeight = panel.scrollHeight + "px";
                }
            });
        }

        // Handle Deep Linking / Hash Navigation
        if (window.location.hash) {
            const hash = window.location.hash.substring(1); // Remove '#'
            const targetEl = document.getElementById(hash);

            if (targetEl && targetEl.classList.contains('accordion-item')) {
                // Determine header and panel
                const header = targetEl.querySelector('.accordion-header');
                const panel = targetEl.querySelector('.accordion-panel');

                if (header && panel) {
                    // Open the panel
                    header.classList.add('active');
                    panel.classList.add('open');
                    panel.style.maxHeight = panel.scrollHeight + "px";

                    // Scroll to it
                    setTimeout(() => {
                        targetEl.scrollIntoView({ behavior: 'smooth' });
                    }, 300);
                }
            }
        }
    }

    // ==========================================
    // INITIALIZATION
    // ==========================================
    function init() {
        // Save current page to recent
        const currentPage = getCurrentPageInfo();
        if (currentPage.title) {
            saveRecentPage(currentPage.title, currentPage.url);
        }

        // Initialize features
        initSearch();
        initDarkMode();
        initPrint();
        initAccordions(); // Initialize Accordions
        renderRecentPages();

        // Register Service Worker
        if ('serviceWorker' in navigator) {
            const swPath = window.location.pathname.includes('/pages/') ? '../sw.js' : 'sw.js';
            navigator.serviceWorker.register(swPath)
                .then(reg => console.log('SW Registered'))
                .catch(err => console.log('SW Failed', err));
        }
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
