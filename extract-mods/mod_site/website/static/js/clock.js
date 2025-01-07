function updateCountdown() {
    const now = new Date();
    const nextSession = getNextSunday20CET(now);

    // Calculate the difference in milliseconds
    const timeRemaining = nextSession - now;

    // Convert milliseconds into days, hours, minutes, and seconds
    const seconds = Math.floor((timeRemaining / 1000) % 60);
    const minutes = Math.floor((timeRemaining / 1000 / 60) % 60);
    const hours = Math.floor((timeRemaining / 1000 / 60 / 60) % 24);
    const days = Math.floor(timeRemaining / (1000 * 60 * 60 * 24));

    // Update the HTML with the calculated values
    document.getElementById('days').textContent = String(days).padStart(2, '0');
    document.getElementById('hours').textContent = String(hours).padStart(2, '0');
    document.getElementById('minutes').textContent = String(minutes).padStart(2, '0');
    document.getElementById('seconds').textContent = String(seconds).padStart(2, '0');
}

// Function to get the next Sunday at 20:00 CET
function getNextSunday20CET(currentDate) {
    // Find current day of the week (0 = Sunday, 6 = Saturday)
    const currentDay = currentDate.getUTCDay();
    const daysUntilSunday = (7 - currentDay) % 7;
    
    // Create next Sunday date and set time to 20:00 CET (19:00 UTC)
    const nextSunday = new Date(currentDate);
    nextSunday.setUTCDate(currentDate.getUTCDate() + daysUntilSunday);
    nextSunday.setUTCHours(19, 0, 0, 0); // 20:00 CET is 19:00 UTC
    
    // If today is already Sunday and past 20:00, set to next Sunday
    if (daysUntilSunday === 0 && currentDate.getUTCHours() >= 19) {
        nextSunday.setUTCDate(nextSunday.getUTCDate() + 7);
    }
    
    return nextSunday;
}

// Update countdown every second
setInterval(updateCountdown, 1000);

// Initialize the countdown on page load
updateCountdown();
