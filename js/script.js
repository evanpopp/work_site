function openModal(text) {
  const overlay = document.getElementById('modalOverlay');
  const modalText = document.getElementById('modalText');
  
  if (overlay && modalText) {
    modalText.innerHTML = text;
    overlay.classList.add('active'); // Adds the CSS class to fade it in
  }
}

function closeModal() {
  const overlay = document.getElementById('modalOverlay');
  if (overlay) {
    overlay.classList.remove('active'); // Removes the class to fade it out
  }
}

function shareResume() {
  // Check if the browser supports the native Web Share API
  if (navigator.share) {
    navigator.share({
      title: 'Evan Popp - Resume',
      text: 'Check out the resume of Evan Popp, Electrical Engineer (Photonics).',
      url: 'https://evanpopp.me/',
    })
    .then(() => console.log('Successfully shared'))
    .catch((error) => console.log('Error sharing:', error));
  } else {
    // Fallback for older browsers (like copying to clipboard)
    navigator.clipboard.writeText('https://evanpopp.me/');
    alert('Link copied to clipboard!');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  // Attach event listeners to all modal trigger buttons/links
  const modalTriggers = document.querySelectorAll('.modal-trigger');
  
  modalTriggers.forEach(trigger => {
    trigger.addEventListener('click', (event) => {
      event.preventDefault(); // Prevent default link navigation
      
      const targetId = trigger.getAttribute('data-target');
      const template = document.getElementById(targetId);
      
      if (template) {
        // Pass the template's inner HTML to your openModal function
        openModal(template.innerHTML);
      }
    });
  });
});

document.addEventListener('DOMContentLoaded', () => {
  // Target your backdrop overlay element
  const modalOverlay = document.querySelector('.modal-overlay');

  if (modalOverlay) {
    modalOverlay.addEventListener('click', (event) => {
      // Check if the click target is the overlay itself (and not the inner modal content)
      if (event.target === modalOverlay) {
        closeModal();
      }
    });
  }
});

// Close modal when pressing the Escape key
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') {
    closeModal();
  }
});

document.addEventListener('DOMContentLoaded', () => {
  const shareBtn = document.getElementById('share-btn');

  if (shareBtn) {
    shareBtn.addEventListener('click', async () => {
      const shareData = {
        title: 'Evan Popp - Electrical Engineer',
        text: 'Check out Evan Popp\'s portfolio and resume:',
        url: 'https://evanpopp.me/'
      };

      // 1. Try native Web Share API (Works on Mobile Safari, Android Chrome, Mac Safari)
      if (navigator.share) {
        try {
          await navigator.share(shareData);
        } catch (err) {
          // Triggers if the user cancels the share dialog
          console.log('Share dismissed:', err);
        }
      } 
      // 2. Fallback for desktop browsers without Web Share support (e.g. Windows Chrome)
      else {
        try {
          await navigator.clipboard.writeText('https://evanpopp.me/');
          alert('Link copied to clipboard!');
        } catch (err) {
          console.error('Failed to copy link:', err);
        }
      }
    });
  }
});

document.addEventListener('DOMContentLoaded', () => {
  const perfBtn = document.getElementById('perf-toggle-btn');
  
  // Only run if the button actually exists on the page
  if (perfBtn) {
    const btnText = perfBtn.querySelector('span');
    const body = document.body;
    let isPerfMode = false;
    
    // 1. Defensively check localStorage (Catches SecurityErrors)
    try {
      if (localStorage.getItem('performanceMode') === 'true') {
        isPerfMode = true;
        body.classList.add('performance-mode');
        btnText.textContent = 'Enable Animations';
      }
    } catch (error) {
      console.warn('Storage access blocked by security settings.');
    }
    
    // 2. Listen for clicks on the toggle button
    perfBtn.addEventListener('click', () => {
      body.classList.toggle('performance-mode');
      isPerfMode = body.classList.contains('performance-mode');
      
      // Update the button text
      btnText.textContent = isPerfMode ? 'Enable Animations' : 'Disable Animations';
      
      // Defensively attempt to save the preference
      try {
        localStorage.setItem('performanceMode', isPerfMode);
      } catch (error) {
        // Fail silently if blocked, button still works for the current session
      }
    });
  }
});