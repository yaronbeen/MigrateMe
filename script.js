document.getElementById('crawlerForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const url = document.getElementById('url').value;
    const replacePatterns = document.getElementById('replacePatterns').checked;
    const compressImages = document.getElementById('compressImages').checked;

    document.getElementById('progress').classList.remove('hidden');
    document.getElementById('result').classList.add('hidden');

    startCrawling(url, replacePatterns, compressImages);
});

function startCrawling(url, replacePatterns, compressImages) {
    fetch('/crawl', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            url: url,
            replacePatterns: replacePatterns,
            compressImages: compressImages
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            showResult(data.message);
        } else {
            showError(data.message);
        }
    })
    .catch((error) => {
        showError('An error occurred: ' + error);
    });

    simulateProgress();
}

function simulateProgress() {
    let progress = 0;
    const progressBar = document.querySelector('.progress');
    const statusElement = document.getElementById('status');

    const interval = setInterval(() => {
        progress += 1;
        progressBar.style.width = `${progress}%`;
        
        if (progress < 33) {
            statusElement.textContent = 'Crawling...';
        } else if (progress < 66) {
            statusElement.textContent = 'Downloading images...';
        } else {
            statusElement.textContent = 'Processing images...';
        }

        if (progress >= 100) {
            clearInterval(interval);
        }
    }, 100);
}

function showResult(message) {
    document.getElementById('resultMessage').textContent = message;
    document.getElementById('result').classList.remove('hidden');
    document.querySelector('.progress').style.width = '100%';
    document.getElementById('status').textContent = 'Completed';
}

function showError(message) {
    document.getElementById('resultMessage').textContent = 'Error: ' + message;
    document.getElementById('result').classList.remove('hidden');
    document.querySelector('.progress').style.width = '100%';
    document.getElementById('status').textContent = 'Error';
}