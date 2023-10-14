document.addEventListener('DOMContentLoaded', function () {
  console.log('DOM Content Loaded');

  const liElements = document.querySelectorAll('li[data-aos="fade-up"]');
  console.log(liElements);

  let delay = 100;

  liElements.forEach((li) => {
  console.log("Loop working")
    li.setAttribute('data-aos-delay', delay);
    delay += 100;
  });
});
