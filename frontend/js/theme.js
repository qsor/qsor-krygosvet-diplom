(function () {
    const STORAGE_KEY = 'qsor-theme';

    function getInitialTheme() {
        const saved = localStorage.getItem(STORAGE_KEY);
        if (saved === 'light' || saved === 'dark') return saved;
        const prefersDark = window.matchMedia &&
                            window.matchMedia('(prefers-color-scheme: dark)').matches;
        return prefersDark ? 'dark' : 'light';
    }

    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
    }

    applyTheme(getInitialTheme());

    window.Theme = {
        get current() {
            return document.documentElement.getAttribute('data-theme') || 'light';
        },
        toggle() {
            const next = this.current === 'dark' ? 'light' : 'dark';
            applyTheme(next);
            localStorage.setItem(STORAGE_KEY, next);

            window.dispatchEvent(new CustomEvent('theme:change', { detail: next }));
            return next;
        },
        set(theme) {
            if (theme !== 'light' && theme !== 'dark') return;
            applyTheme(theme);
            localStorage.setItem(STORAGE_KEY, theme);
            window.dispatchEvent(new CustomEvent('theme:change', { detail: theme }));
        },
    };

    if (window.matchMedia) {
        const mq = window.matchMedia('(prefers-color-scheme: dark)');
        mq.addEventListener('change', e => {
            if (!localStorage.getItem(STORAGE_KEY)) {
                applyTheme(e.matches ? 'dark' : 'light');
            }
        });
    }
})();
