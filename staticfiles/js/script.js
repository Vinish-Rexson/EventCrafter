document.addEventListener('scroll', function() {
    const card = document.querySelector('._1');
    const rect = card.getBoundingClientRect();
    const windowHeight = window.innerHeight;

    if (rect.top < windowHeight && rect.bottom >= 0) {
      card.classList.add('visible');
    }
  });
  document.addEventListener('scroll', function() {
    const cards = document.querySelectorAll('._2, ._3, ._4');

    cards.forEach(card => {
      const rect = card.getBoundingClientRect();
      const windowHeight = window.innerHeight;

      if (rect.top < windowHeight && rect.bottom >= 0) {
        card.classList.add('visible');
      }
    });
  });
  // Select the elements
const bookCons = document.querySelector('.book-cons');
const arrow3 = document.querySelector('.arrow3');

// Add event listeners to handle hover effect
bookCons.addEventListener('mouseover', () => {
  arrow3.classList.add('move-right');
});

bookCons.addEventListener('mouseout', () => {
  arrow3.classList.remove('move-right');
});
