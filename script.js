const serverValue = document.getElementById('serverValue');
const pidValue = document.getElementById('pidValue');
const lastValue = document.getElementById('lastValue');
const speedValue = document.getElementById('speedValue');
const statusBox = document.getElementById('statusBox');
const logBox = document.getElementById('logBox');
const runTestBtn = document.getElementById('runTestBtn');
const refreshBtn = document.getElementById('refreshBtn');

function log(message) {
  logBox.textContent = `${new Date().toLocaleTimeString()} — ${message}`;
}

const networkList = document.getElementById('networkList');

async function refreshStatus() {
  statusBox.textContent = 'Bağlanıyor…';
  try {
    const response = await fetch('/api/health');
    const data = await response.json();
    serverValue.textContent = data.hostname;
    pidValue.textContent = data.pid;
    statusBox.textContent = `Bağlantı aktif · ${data.addresses.join(', ')}`;
    networkList.innerHTML = `<strong>Yerel erişim adresleri:</strong><br>${data.addresses.map(addr => `<code>http://${addr}</code>`).join('<br>')}`;
    log(`Sunucu hazır: ${data.hostname}`);
  } catch (error) {
    statusBox.textContent = 'Bağlantı başarısız';
    networkList.textContent = '';
    log(`Hata: ${error.message}`);
  }
}

async function runTransferTest() {
  const size = 1024 * 1024;
  runTestBtn.disabled = true;
  statusBox.textContent = 'Test çalışıyor…';
  log(`1 MB veri aktarımı başlatıldı...`);

  const start = performance.now();
  try {
    const response = await fetch(`/api/throughput?size=${size}`);
    const arrayBuffer = await response.arrayBuffer();
    const elapsedMs = performance.now() - start;
    const bytes = arrayBuffer.byteLength;
    const megabitsPerSecond = (bytes * 8) / (elapsedMs / 1000) / 1000 / 1000;

    speedValue.textContent = `${megabitsPerSecond.toFixed(2)} Gbps`;
    lastValue.textContent = `${(bytes / 1024 / 1024).toFixed(1)} MB`;
    statusBox.textContent = 'Test tamamlandı';
    log(`Aktarım tamamlandı · ${bytes} bayt · ${megabitsPerSecond.toFixed(2)} Gbps`);
  } catch (error) {
    statusBox.textContent = 'Test başarısız';
    log(`Test hatası: ${error.message}`);
  } finally {
    runTestBtn.disabled = false;
  }
}

runTestBtn.addEventListener('click', runTransferTest);
refreshBtn.addEventListener('click', refreshStatus);

refreshStatus();
