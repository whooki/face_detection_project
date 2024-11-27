document.getElementById("fileInput").addEventListener("change", previewImage);

async function uploadImage() {
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Proszę wybrać plik!");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("http://localhost:8000/upload/", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Nie udało się przetworzyć obrazu.");
        }

        const data = await response.json();

        // Sprawdzenie, czy wykryto twarze
        if (data.faces.length === 0) {
            alert(data.message || "Nie wykryto twarzy.");
            return;
        }

        // Wyświetlenie obrazu z prostokątami
        displayImageWithBoxes(file, data.faces);
    } catch (error) {
        console.error("Błąd:", error);
        alert(error.message);
    }
}

function previewImage(event) {
    const file = event.target.files[0];

    if (!file) {
        alert("Proszę wybrać plik!");
        return;
    }

    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");

    const img = new Image();
    img.onload = function () {
        const maxWidth = 800; // Maksymalna szerokość canvas
        const scaleFactor = Math.min(maxWidth / img.width, 1);

        canvas.width = img.width * scaleFactor;
        canvas.height = img.height * scaleFactor;

        ctx.drawImage(img, 0, 0, canvas.width, canvas.height); // Rysowanie obrazu na canvasie
    };

    img.src = URL.createObjectURL(file); // Ustawienie źródła obrazu na plik
}

function displayImageWithBoxes(file, faces) {
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");

    const img = new Image();
    img.onload = function () {
        const maxWidth = 800; // Maksymalna szerokość
        const scaleFactor = Math.min(maxWidth / img.width, 1);

        canvas.width = img.width * scaleFactor;
        canvas.height = img.height * scaleFactor;

        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

        // Rysowanie prostokątów
        faces.forEach(face => {
            const [x, y, width, height] = face.box.map(coord => coord * scaleFactor);
            ctx.strokeStyle = "red";
            ctx.lineWidth = 2;
            ctx.strokeRect(x, y, width, height);
        });
    };
    img.src = URL.createObjectURL(file);
}

let videoStream = null; // To track the video stream

// Start the camera and show the video feed
function startCamera() {
    const video = document.getElementById("video");
    const cameraSection = document.getElementById("cameraSection");
    const startCameraButton = document.getElementById("startCameraButton");

    // Hide the start camera button and show the camera section
    startCameraButton.style.display = "none";
    cameraSection.style.display = "block";

    // Access the user's camera
    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            videoStream = stream;
            video.srcObject = stream;
        })
        .catch((error) => {
            console.error("Error accessing camera:", error);
            alert("Unable to access the camera.");
            // Show the start camera button again in case of error
            startCameraButton.style.display = "block";
            cameraSection.style.display = "none";
        });
}

// Stop the camera when not needed
function stopCamera() {
    if (videoStream) {
        videoStream.getTracks().forEach((track) => track.stop());
        videoStream = null;
    }
}

// Capture an image from the video feed
function captureImage() {
    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");

    // Set the canvas size to match the video feed
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw the current video frame on the canvas
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert the image to a Blob (for uploading)
    canvas.toBlob((blob) => {
        console.log("Captured image blob:", blob);
        uploadCapturedImage(blob); // Upload the image to the server
    });

    // Stop the camera after taking the picture
    stopCamera();

    // Hide the camera section and show the start button again
    document.getElementById("cameraSection").style.display = "none";
    document.getElementById("startCameraButton").style.display = "block";
}

// Upload the captured image to the server
function uploadCapturedImage(blob) {
    const formData = new FormData();
    formData.append("file", blob, "captured_image.png");

    fetch("http://localhost:8000/upload/", {
        method: "POST",
        body: formData,
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.faces.length === 0) {
                alert(data.message || "No faces detected.");
                return;
            }
            console.log("Detected faces:", data.faces);
            drawBoundingBoxes(data.faces);
        })
        .catch((error) => {
            console.error("Error uploading captured image:", error);
        });
}

// Draw bounding boxes for detected faces
function drawBoundingBoxes(faces) {
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");

    // Draw bounding boxes on the canvas
    faces.forEach((face) => {
        const [x, y, width, height] = face.box;
        ctx.strokeStyle = "red";
        ctx.lineWidth = 2;
        ctx.strokeRect(x, y, width, height);
    });
}
