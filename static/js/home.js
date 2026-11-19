// Mobile Navigation Toggle
const menuToggle = document.getElementById('menuToggle');
const mainNav = document.getElementById('mainNav');

menuToggle.addEventListener('click', () => {
    mainNav.classList.toggle('active');
});

// Language Switcher Toggle Stub
// const langToggle = document.getElementById('langToggle');
// let currentLang = 'EN';

// langToggle.addEventListener('click', () => {
//     currentLang = currentLang === 'EN' ? 'FR' : 'EN';
//     langToggle.textContent = currentLang;
// });

// Interactive User-Defined Guest Counter Logic
const guestDisplayBox = document.getElementById('guestDisplayBox');
const guestPopup = document.getElementById('guestPopup');
const guestSummaryText = document.getElementById('guestSummaryText');

const adultCountEl = document.getElementById('adultCount');
const childCountEl = document.getElementById('childCount');

const incAdults = document.getElementById('incAdults');
const decAdults = document.getElementById('decAdults');
const incChildren = document.getElementById('incChildren');
const decChildren = document.getElementById('decChildren');

let adults = 2;
let children = 0;

// Toggle popup open/close on click
guestDisplayBox.addEventListener('click', (e) => {
    e.stopPropagation();
    guestPopup.classList.toggle('active');
});

// Close popup when clicking outside
document.addEventListener('click', (e) => {
    if (!guestPopup.contains(e.target) && !guestDisplayBox.contains(e.target)) {
        guestPopup.classList.remove('active');
    }
});

// Prevent popup clicks from closing it immediately
guestPopup.addEventListener('click', (e) => {
    e.stopPropagation();
});

function updateGuestSummary() {
    adultCountEl.textContent = adults;
    childCountEl.textContent = children;
    guestSummaryText.textContent = `${adults} Adult${adults > 1 ? 's' : ''}, ${children} Child${children !== 1 ? 'ren' : ''}`;
}

incAdults.addEventListener('click', () => {
    if (adults < 10) {
        adults++;
        updateGuestSummary();
    }
});

decAdults.addEventListener('click', () => {
    if (adults > 1) {
        adults--;
        updateGuestSummary();
    }
});

incChildren.addEventListener('click', () => {
    if (children < 8) {
        children++;
        updateGuestSummary();
    }
});

decChildren.addEventListener('click', () => {
    if (children > 0) {
        children--;
        updateGuestSummary();
    }
});

// Booking Form Submission
const bookingForm = document.getElementById('bookingForm');

bookingForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const checkInValue = document.getElementById('checkIn').value;
    
    // Check if date is empty or invalid format
    if (!checkInValue) {
        alert('Please select a valid check-in date.');
        document.getElementById('checkIn').focus();
        return;
    }
    const selectedDate = new Date(checkInValue);
    const today = new Date();
    today.setHours(0, 0, 0, 0); // Reset time to compare strictly by date
    // Prevent past dates
    if (selectedDate < today) {
        alert('Check-in date cannot be in the past. Please select a future date.');
        document.getElementById('checkIn').focus();
        return;
    }
    // Proceed with submission logic...
    const room = document.getElementById('roomType');
    const roomText = room.options[room.selectedIndex].text;
    const acSelect = document.getElementById('acPreference');
    const acPreferenceText = acSelect.options[acSelect.selectedIndex].text;
    alert(`Reservation Request Captured:\nRoom: ${roomText}\nClimate: ${acPreferenceText}\nGuests: ${adults} Adults, ${children} Children\nDate: ${checkInValue}\n\nRedirecting to secure checkout gateway...`);
});
// Simple Date Placeholder Interaction
// const checkInInput = document.getElementById('checkIn');
// checkInInput.addEventListener('focus', () => {
//     if(!checkInInput.value) {
//         checkInInput.value = 'Nov 12 - Nov 15, 2026';
//     }
// });