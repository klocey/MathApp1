if (!window.dash_clientside) { window.dash_clientside = {}; }

window.dash_clientside.audio = {
    playEffects: function(submitClicks, isModalOpen, currentQuestion, themeValue, closeClicks) {
        // Look up which element actually triggered the callback update
        // (Similar to callback_context in Python Dash)
        var triggeredInput = '';
        if (window.dash_clientside.callback_context && window.dash_clientside.callback_context.triggered.length > 0) {
            triggeredInput = window.dash_clientside.callback_context.triggered[0].prop_id;
        }

        // 1. Check if the Theme Selector or the Close Modal Button was clicked
        if (triggeredInput.includes('theme-selector') || triggeredInput.includes('close-joke-btn')) {
            var clickAudio = new Audio('/assets/click.mp3');
            clickAudio.play().catch(function(e) { console.log("Audio play blocked:", e); });
            return '';
        }

        // 2. If the main Submit Button was the trigger
        if (triggeredInput.includes('submit-btn')) {
            // Did they get it right? (Modal pops open)
            if (isModalOpen === true) {
                var correctAudio = new Audio('/assets/correct.mp3');
                correctAudio.play().catch(function(e) { console.log("Audio play blocked:", e); });
            } 
            // Otherwise, it's an incorrect or empty answer submission
            else {
                var wrongAudio = new Audio('/assets/wrong.mp3');
                wrongAudio.play().catch(function(e) { console.log("Audio play blocked:", e); });
            }
            return '';
        }

        return '';
    }
};