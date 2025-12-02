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

    // Elements
    const scriptReviewPanel = document.getElementById('scriptReviewPanel');
    const controlsPanel = document.querySelector('.controls-panel');
    const scriptTextarea = document.getElementById('scriptTextarea');
    const approveBtn = document.getElementById('approveBtn');
    const backBtn = document.getElementById('backBtn');

    // State
    let currentScriptData = null;

    // 3. Generate Script Logic
    generateBtn.addEventListener('click', async () => {
        const topic = topicInput.value.trim();

        if (!topic) {
            log('> Error: No topic provided.', 'error');
            topicInput.focus();
            return;
        }

        // UI State: Generating Script
        generateBtn.disabled = true;
        generateBtn.querySelector('.btn-text').textContent = "WRITING SCRIPT...";

        log(`> Initializing script generation...`, 'system');
        log(`> Topic: "${topic}"`, 'info');

        try {
            const response = await fetch('/generate_script', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    topic: topic,
                    content_mode: selectedMode
                })
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || 'Script generation failed');
            }

            const data = await response.json();
            currentScriptData = data;

            // Show Review Panel
            log('> Script generated! Please review.', 'success');
            scriptTextarea.value = data.script;

            controlsPanel.style.display = 'none';
            scriptReviewPanel.style.display = 'flex';

        } catch (error) {
            log(`> Error: ${error.message}`, 'error');
        } finally {
            generateBtn.disabled = false;
            generateBtn.querySelector('.btn-text').textContent = "GENERATE SCRIPT";
        }
    });

    // 4. Approve & Generate Video Logic
    approveBtn.addEventListener('click', async () => {
        const scriptText = scriptTextarea.value;
        const modelTier = document.querySelector('input[name="model"]:checked').value;
        const topic = topicInput.value.trim();

        if (!scriptText) return;

        // UI State: Generating Video
        approveBtn.disabled = true;
        approveBtn.textContent = "PRODUCING VIDEO...";
        resultContainer.classList.add('hidden');

        log('> Script approved. Starting production...', 'system');
        log(`> Model: ${modelTier}`, 'info');

        try {
            const response = await fetch('/generate_video_from_script', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    script: scriptText,
                    visual_prompts: currentScriptData.visual_prompts,
                    topic: topic,
                    model_tier: modelTier,
                    content_mode: selectedMode
                })
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || 'Video generation failed');
            }

            const data = await response.json();

            log('> Video assets generated.', 'success');
            log('> Audio synthesized.', 'success');
            log('> Final cut assembled.', 'success');
            log('> GENERATION COMPLETE.', 'success');

            // Show Result
            const filename = data.video_path.split('/').pop();
            const videoUrl = `/output/${filename}`;

            finalVideo.src = videoUrl;
            downloadLink.href = videoUrl;
            resultContainer.classList.remove('hidden');

            // Reset View
            scriptReviewPanel.style.display = 'none';
            controlsPanel.style.display = 'flex';

        } catch (error) {
            log(`> FATAL ERROR: ${error.message}`, 'error');
        } finally {
            approveBtn.disabled = false;
            approveBtn.textContent = "APPROVE & GENERATE VIDEO";
        }
    });

    // Back Button
    backBtn.addEventListener('click', () => {
        scriptReviewPanel.style.display = 'none';
        controlsPanel.style.display = 'flex';
    });

    // Helper: Fetch Trends
    async function fetchTrends() {
        try {
            const res = await fetch('/trends');
            const trends = await res.json();

            trendChips.innerHTML = '';

            // Take top trends (limit to avoid UI clutter)
            const topTrends = trends.slice(0, 15);

            topTrends.forEach(trend => {
                // Handle both old format (string) and new format (object)
                const topicText = typeof trend === 'string' ? trend : trend.topic;
                const category = trend.category || '';

                const chip = document.createElement('span');
                chip.className = 'chip';

                // Add category class for styling
                if (category === 'meme' || category === 'story') {
                    chip.classList.add('chip-meme');
                } else if (category === 'education') {
                    chip.classList.add('chip-education');
                }

                chip.textContent = topicText;
                chip.addEventListener('click', () => {
                    topicInput.value = topicText;
                    log(`> Topic set to trending: ${topicText}`, 'info');
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
