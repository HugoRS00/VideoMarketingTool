document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const topicInput = document.getElementById('topicInput');
    const trendChips = document.getElementById('trendChips');
    const generateBtn = document.getElementById('generateBtn');
    const terminalOutput = document.getElementById('terminalOutput');
    const resultContainer = document.getElementById('resultContainer');
    const finalVideo = document.getElementById('finalVideo');
    const downloadLink = document.getElementById('downloadLink');
    const modeCards = document.querySelectorAll('.mode-card');

    // State
    let selectedMode = 'MEME';

    // 1. Fetch Trends on Load
    fetchTrends();

    // 2. Mode Selection Logic
    modeCards.forEach(card => {
        card.addEventListener('click', () => {
            modeCards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');
            selectedMode = card.dataset.mode;
            log(`> Mode switched to: ${selectedMode}`, 'info');
        });
    });

    // 3. Generate Button Logic
    generateBtn.addEventListener('click', async () => {
        const topic = topicInput.value.trim();
        const modelTier = document.querySelector('input[name="model"]:checked').value;

        if (!topic) {
            log('> Error: No topic provided.', 'error');
            topicInput.focus();
            return;
        }

        // Reset UI
        resultContainer.classList.add('hidden');
        generateBtn.disabled = true;
        generateBtn.querySelector('.btn-text').textContent = "GENERATING...";

        // Start Process
        log(`> Initializing generation job...`, 'system');
        log(`> Topic: "${topic}"`, 'info');
        log(`> Mode: ${selectedMode} | Model: ${modelTier}`, 'info');

        try {
            // Simulate steps for better UX (since backend is synchronous for now)
            // In a real async backend, we'd poll status.

            log('> Step 1: Brainstorming script (GPT-5.1)...', 'system');

            const response = await fetch('/generate_video', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    topic: topic,
                    model_tier: modelTier,
                    content_mode: selectedMode
                })
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || 'Generation failed');
            }

            const data = await response.json();

            log('> Step 2: Script generated successfully.', 'success');
            log('> Step 3: Generating video assets (Vision Engine)...', 'system');
            log('> Step 4: Synthesizing audio (ElevenLabs/TTS)...', 'system');
            log('> Step 5: Assembling final cut with MoviePy...', 'system');

            // Success
            log('> GENERATION COMPLETE.', 'success');

            // Show Result
            // Note: data.video_path is a local path. We need to make sure backend serves it.
            // For now, we assume backend returns a relative path we can serve via static or a specific route.
            // Since our backend saves to 'output/', we need to expose 'output/' as static or stream it.
            // Let's assume we fix backend to serve 'output' directory.

            // Fix path for browser (assuming output dir is mounted)
            const filename = data.video_path.split('/').pop();
            const videoUrl = `/output/${filename}`;

            finalVideo.src = videoUrl;
            downloadLink.href = videoUrl;
            resultContainer.classList.remove('hidden');

        } catch (error) {
            log(`> FATAL ERROR: ${error.message}`, 'error');
        } finally {
            generateBtn.disabled = false;
            generateBtn.querySelector('.btn-text').textContent = "GENERATE ASSET";
        }
    });

    // Helper: Fetch Trends
    async function fetchTrends() {
        try {
            const res = await fetch('/trends');
            const trends = await res.json();

            trendChips.innerHTML = '';
            trends.forEach(trend => {
                const chip = document.createElement('span');
                chip.className = 'chip';
                chip.textContent = trend;
                chip.addEventListener('click', () => {
                    topicInput.value = trend;
                    log(`> Topic set to trending: ${trend}`, 'info');
                });
                trendChips.appendChild(chip);
            });
        } catch (e) {
            log('> Failed to fetch trends.', 'error');
            trendChips.innerHTML = '<span class="chip">Offline Mode</span>';
        }
    }

    // Helper: Logger
    function log(msg, type = 'info') {
        const line = document.createElement('div');
        line.className = `log-line ${type}`;
        line.textContent = msg;
        terminalOutput.appendChild(line);
        terminalOutput.scrollTop = terminalOutput.scrollHeight;
    }
});
