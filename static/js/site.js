// static/js/site.js
document.addEventListener('DOMContentLoaded', () => {
  const content = document.getElementById('content');
  const bgm = document.getElementById('bgm');
  const playPauseBtn = document.getElementById('play-pause');
  const nextBtn = document.getElementById('next');
  const prevBtn = document.getElementById('prev');
  const volumeSlider = document.getElementById('volume');
  const progressContainer = document.getElementById('progress-container');
  const progressBar = document.getElementById('progress-bar');
  const timeDisplay = document.getElementById('time-display');

  // Build playlist dynamically from <source> tags inside <audio>
  const sources = Array.from(bgm.querySelectorAll('source'));
  const playlist = sources.map(src => src.src);
  let currentTrack = 0;

  function loadTrack(index) {
    bgm.src = playlist[index];
    bgm.load();
  }

  function formatTime(seconds) {
    if (isNaN(seconds)) return "0:00";
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return m + ":" + (s < 10 ? "0" + s : s);
  }

  if (bgm) {
    // Load first track
    loadTrack(currentTrack);

    // Play/pause
    if (playPauseBtn) {
      playPauseBtn.addEventListener('click', () => {
        if (bgm.paused) {
          bgm.play().catch(()=>{});
          playPauseBtn.textContent = '⏸'; // Pause icon
        } else {
          bgm.pause();
          playPauseBtn.textContent = '▶️'; // Play icon
        }
      });
    }

    // Next track
    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        currentTrack++;
        if (currentTrack >= playlist.length) currentTrack = 0;
        loadTrack(currentTrack);
        bgm.play().catch(()=>{});
        playPauseBtn.textContent = '⏸';
      });
    }

    // Previous track
    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        currentTrack--;
        if (currentTrack < 0) currentTrack = playlist.length - 1;
        loadTrack(currentTrack);
        bgm.play().catch(()=>{});
        playPauseBtn.textContent = '⏸';
      });
    }

    // Volume control
    if (volumeSlider) {
      volumeSlider.addEventListener('input', () => {
        bgm.volume = volumeSlider.value;
      });
    }

    // Progress bar update
    bgm.addEventListener('timeupdate', () => {
      if (!isNaN(bgm.duration) && progressBar && timeDisplay) {
        const percent = (bgm.currentTime / bgm.duration) * 100;
        progressBar.style.width = percent + '%';
        timeDisplay.textContent = formatTime(bgm.currentTime) + ' / ' + formatTime(bgm.duration);
      }
    });

    // Seek
    if (progressContainer) {
      progressContainer.addEventListener('click', (e) => {
        const rect = progressContainer.getBoundingClientRect();
        const clickX = e.clientX - rect.left;
        const percent = clickX / rect.width;
        bgm.currentTime = percent * bgm.duration;
      });
    }

    // When a track ends, move to next or loop back
    bgm.addEventListener('ended', () => {
      currentTrack++;
      if (currentTrack >= playlist.length) {
        currentTrack = 0; // loop back to start
      }
      loadTrack(currentTrack);
      bgm.play().catch(()=>{});
    });

    // Autoplay on page load
    bgm.play().catch(()=>{});
    document.body.addEventListener('click', () => {
      bgm.muted = false;
      if (bgm.paused) bgm.play().catch(()=>{});
    }, { once: true });
  }

  // --- AJAX navigation (unchanged) ---
  async function ajaxNavigate(url, push=true) {
    try {
      const res = await fetch(url, {headers: {'X-Requested-With': 'XMLHttpRequest'}});
      if (!res.ok) throw new Error('Network error');
      const data = await res.json();
      if (data && data.html !== undefined) {
        if (content) content.innerHTML = data.html;
      } else {
        const text = await res.text();
        if (content) content.innerHTML = text;
      }
      if (push) history.pushState({url}, '', url);
    } catch (err) {
      console.error(err);
      window.location.href = url;
    }
  }

  document.body.addEventListener('click', (e) => {
    const a = e.target.closest('a[data-ajax]');
    if (!a) return;
    e.preventDefault();
    const url = a.getAttribute('href');
    ajaxNavigate(url);
  });

  window.addEventListener('popstate', (e) => {
    const url = (e.state && e.state.url) || location.pathname;
    ajaxNavigate(url, false);
  });
});
