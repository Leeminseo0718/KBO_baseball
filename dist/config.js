window.KBO_API_URL = window.KBO_API_URL || localStorage.getItem('KBO_API_URL') || '';
window.KBO_PUBLIC_SNAPSHOT_URL = window.KBO_PUBLIC_SNAPSHOT_URL ||
  (['localhost', '127.0.0.1'].includes(window.location.hostname)
    ? './data/live.json'
    : 'https://raw.githubusercontent.com/Leeminseo0718/KBO_baseball/main/dist/data/live.json');
