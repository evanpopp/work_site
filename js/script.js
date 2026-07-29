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