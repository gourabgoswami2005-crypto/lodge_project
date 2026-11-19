// Global guest count states
let adults = 2;
let children = 0;

const guestDisplay = document.getElementById('guestDisplay');
const guestDropdown = document.getElementById('guestDropdown');

// Ensure elements exist before adding listeners
if (guestDisplay && guestDropdown) {
    // Toggle dropdown visibility when clicking the display box
    guestDisplay.addEventListener('click', function(e) {
        e.stopPropagation();
        guestDropdown.classList.toggle('hidden');
    });

    // Close dropdown if user clicks outside of it
    document.addEventListener('click', function(e) {
        if (!guestDropdown.contains(e.target) && e.target !== guestDisplay) {
            guestDropdown.classList.add('hidden');
        }
    });
}

// Increment or decrement guest counts via inline button triggers
function updateGuests(type, change) {
    if (type === 'adults') {
        adults = Math.max(1, adults + change); // Minimum 1 adult
        document.getElementById('adultCount').innerText = adults;
    } else if (type === 'children') {
        children = Math.max(0, children + change); // Minimum 0 children
        document.getElementById('childCount').innerText = children;
    }
    
    // Update display text dynamically
    if (guestDisplay) {
        guestDisplay.innerText = `${adults} Adult${adults > 1 ? 's' : ''}, ${children} Child${children !== 1 ? 'ren' : ''}`;
    }
}

// Form Validation and Backend Submission Handling
const dedicatedBookingForm = document.getElementById('dedicatedBookingForm');

if (dedicatedBookingForm) {
    dedicatedBookingForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const checkIn = document.getElementById('checkInDate').value;
        const checkOut = document.getElementById('checkOutDate').value;

        if (!checkIn || !checkOut) {
            alert('Please select both check-in and check-out dates.');
            return;
        }

        const checkInDate = new Date(checkIn);
        const checkOutDate = new Date(checkOut);
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        if (checkInDate < today) {
            alert('Check-in date cannot be in the past.');
            document.getElementById('checkInDate').focus();
            return;
        }

        if (checkOutDate <= checkInDate) {
            alert('Check-out date must be after the check-in date.');
            document.getElementById('checkOutDate').focus();
            return;
        }

        // Gather all form fields into an object matching your Django backend expectations
        const formData = {
            fullName: document.getElementById('fullName').value,
            mobileNumber: document.getElementById('mobileNumber').value,
            aadhaarCard: document.getElementById('aadhaarCard').value,
            emailId: document.getElementById('emailId').value,
            voterCard: document.getElementById('voterCard').value,
            checkInDate: checkIn,
            checkOutDate: checkOut,
            adults: adults,
            children: children,
            roomType: document.getElementById('roomType').value,
            acPreference: document.getElementById('acPreference').value
        };

        try {
            // Send the data securely to your Django backend API route
            const response = await fetch('/api/book/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (response.ok && result.status === 'success') {
                alert(`Reservation Confirmed Successfully! Booking ID: #${result.booking_id}\nYour data has been saved to the database.`);
                window.location.reload(); // Refresh to clear form and update state
            } else {
                alert('Booking failed: ' + (result.message || 'Unknown server error'));
            }
        } catch (error) {
            console.error('Error submitting form:', error);
            alert('A network error occurred while submitting your booking.');
        }
    });
}