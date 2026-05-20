(function () {
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        return;
    }

    document.addEventListener('click', e => {
        const a = e.target.closest('a');
        if (!a) return;
        const href = a.getAttribute('href');
        if (!href) return;

        if (href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:')) return;
        if (a.target && a.target !== '_self') return;
        if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey || e.button === 1) return;

        try {
            const url = new URL(href, location.href);
            if (url.origin !== location.origin) return;

            if (url.pathname === location.pathname && url.search === location.search) return;
        } catch (_) {
            return;
        }

        e.preventDefault();
        document.body.classList.add('is-leaving');

        setTimeout(() => { location.href = href; }, 200);
    });

    window.addEventListener('pageshow', () => {
        document.body.classList.remove('is-leaving');
    });
})();
