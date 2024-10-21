function updateTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();

    document.getElementById('time').textContent = timeString;
}

// Update the time immediately, and then every 1 second (1000 milliseconds)

updateTime();
setInterval(updateTime, 1000);
