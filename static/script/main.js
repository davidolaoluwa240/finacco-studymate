// Elements
const avatarControl = document.getElementById("avatar-control");
const avatarUploadButton = document.getElementById("avatar-upload-button");
const avatarImage = document.getElementById("avatar-image");
const timer = document.getElementById("timer");
const timerControl = document.getElementById("timer-control");
const timerPauseBtn = document.getElementById("timer-pause");
const timerPlayBtn = document.getElementById("timer-play");
const timerResetBtn = document.getElementById("timer-reset");
const studyTimeBtn = document.getElementById("study-time-btn");

// Constants
let elapsedSeconds = Number.parseInt(timerControl?.dataset["timerInit"]) || 0;
let timerInterval;

// Utils
/**
 * Format Time
 * @param {number} seconds
 * @returns
 */
const formatTime = (seconds) => {
  const hrs = String(Math.floor(seconds / 3600)).padStart(2, "0");
  const mins = String(Math.floor((seconds % 3600) / 60)).padStart(2, "0");
  const secs = String(seconds % 60).padStart(2, "0");
  return `${hrs}:${mins}:${secs}`;
};

/**
 * Update Timer Display
 */
const updateTimerDisplay = () => {
  timer.textContent = formatTime(elapsedSeconds);
  timerControl.value = formatTime(elapsedSeconds);
};

// Handlers
/**
 * Handle opens the file picker dialog
 */
const handleOpenFilePicker = () => {
  avatarControl.click();
};

/**
 * Handle starts the timer
 */
const handleStartTimer = () => {
  if (!timerInterval) {
    timerInterval = setInterval(() => {
      elapsedSeconds++;
      updateTimerDisplay();
    }, 1000);
  }
  studyTimeBtn.classList.add("hidden");
};

/**
 * Handle Pause Timer
 */
function handlePauseTimer() {
  clearInterval(timerInterval);
  timerInterval = null;
  studyTimeBtn.classList.remove("hidden");
}

/**
 * Handle Reset Timer
 */
function handleResetTimer() {
  handlePauseTimer();
  elapsedSeconds = 0;
  updateTimerDisplay();
  studyTimeBtn.classList.remove("hidden");
}

/**
 * Handles the file change event
 */
const handleFileChange = function () {
  const file = this.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function () {
      avatarImage.src = reader.result;
    };
    reader.readAsDataURL(file);
  }
};

// Event Listeners
avatarUploadButton?.addEventListener("click", handleOpenFilePicker);
avatarControl?.addEventListener("change", handleFileChange);
timerPlayBtn?.addEventListener("click", handleStartTimer);
timerPauseBtn?.addEventListener("click", handlePauseTimer);
timerResetBtn?.addEventListener("click", handleResetTimer);
