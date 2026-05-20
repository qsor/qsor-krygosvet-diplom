const Img = {
    url(seed, w = 800, h = 500) {
        const safe = encodeURIComponent(String(seed || 'qsor'));
        return `https://picsum.photos/seed/${safe}/${w}/${h}`;
    },

    tag(seed, alt = '', w = 800, h = 500) {
        const altSafe = String(alt || '').replace(/"/g, '&quot;');
        return `<img class="cover-img" alt="${altSafe}" loading="lazy" src="${this.url(seed, w, h)}">`;
    },

    bg(seed, w = 800, h = 500) {
        return `background-image: url('${this.url(seed, w, h)}'); background-size: cover; background-position: center;`;
    },
};

window.Img = Img;
