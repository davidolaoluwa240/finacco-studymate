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
const uploadBtn = document.querySelectorAll(".upload-btn");
const uploadNoteControl = document.getElementById("upload-note-control");
const uploadsContainer = document.getElementById("uploads");
const uploadLength = document.getElementById("upload-length");
const uploadNotesForm = document.getElementById("upload-notes-form");

// Constants
let elapsedSeconds = Number.parseInt(timerControl?.dataset["timerInit"]) || 0;
let timerInterval;
let files = [];
let deleteFiles = [];

// Utils
/**
 * Handler To transcribe note
 */
const transcribeNote = () => {};

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
 * Handle open the avatar picker
 */
const handleOpenAvatarPicker = () => {
  avatarControl.click();
};

/**
 * Handle open the Note Upload picker
 */
const handleOpenNoteUploadPicker = () => {
  uploadNoteControl.click();
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
 * Handles the avatar file change event
 */
const handleAvatarFileChange = function () {
  const file = this.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function () {
      avatarImage.src = reader.result;
    };
    reader.readAsDataURL(file);
  }
};

/**
 * Handles the Upload Note file change event
 */
const handleUploadNoteFileChange = function () {
  files = [...this.files];

  // Update Upload Length
  uploadLength.textContent =
    Number.parseInt(uploadLength.dataset["initImagesLength"]) + files.length;

  // Add Image/File to Page
  files.forEach((file) => {
    imgURL = URL.createObjectURL(file);
    file.id = Date.now() + "__" + imgURL + "__" + (Math.random() * 100 + 1);

    const elm = `
      <div class="relative uploads__item" data-id="${file.id}">
        <button
          class="bg-white flex justify-center rounded-full p-1 text-center items-center absolute top-1 right-2 uploads-remove-btn"
          title="Remove image"
          type="button"
        >
          <span class="material-symbols-outlined"> cancel </span>
        </button>
        <img
          class="block rounded-md align-middle w-[200px] h-[200px]"
          src="${imgURL}"
          alt="${file.name}"
        />
      </div>
    `;

    uploadsContainer.insertAdjacentHTML("beforeend", elm);
  });
};

/**
 * Handle Remove Upload Note Image
 */
const handleRemoveUploadImage = (e) => {
  e.preventDefault();
  const elm = e.target.closest(".uploads__item");

  if (elm) {
    const fileId = elm.dataset["id"];
    const isUploadedBefore = elm.dataset["uploadedBefore"];
    files = files.filter((file) => file.id !== fileId);
    elm.remove();
    uploadLength.textContent =
      Number.parseInt(uploadLength.dataset["initImagesLength"]) + files.length;

    if (isUploadedBefore) {
      deleteFiles.push(fileId);
    }
  }
};

/**
 * Handler to upload and delete note
 */
const handleUploadAndDeleteNote = (e) => {
  e.preventDefault();

  // Transcribe and Upload
  if (files.length) {
    files.forEach(async (file) => {
      try {
        const form = new FormData();
        form.set("image", file);

        const result = await new Tesseract.recognize(
          URL.createObjectURL(file),
          "eng",
          {
            logger: (info) => console.log(info),
          }
        );

        console.log(result.data);
      } catch (err) {
        console.log(err);
      }
    });
  }

  // Delete Uploaded Notes
  if (deleteFiles.length) {
  }
};

// Event Listeners
avatarUploadButton?.addEventListener("click", handleOpenAvatarPicker);
avatarControl?.addEventListener("change", handleAvatarFileChange);
uploadNoteControl?.addEventListener("change", handleUploadNoteFileChange);
timerPlayBtn?.addEventListener("click", handleStartTimer);
timerPauseBtn?.addEventListener("click", handlePauseTimer);
timerResetBtn?.addEventListener("click", handleResetTimer);
uploadBtn?.forEach((el) =>
  el.addEventListener("click", handleOpenNoteUploadPicker)
);
uploadsContainer?.addEventListener("click", handleRemoveUploadImage);
uploadNotesForm?.addEventListener("submit", handleUploadAndDeleteNote);
