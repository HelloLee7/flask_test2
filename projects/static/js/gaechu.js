document.addEventListener('DOMContentLoaded', function() {
    let recommendBtn = document.getElementById('recommend-btn');
    let recommendCount = document.getElementById('recommend-count');
    let count = 0;

    recommendBtn.addEventListener('click', function() {
        count++;
        recommendCount.textContent = count;
    });
});