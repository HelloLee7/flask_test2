document.addEventListener('DOMContentLoaded', function() {
    let recommendBtn = document.getElementById('recommend-btn');
    let recommendCount = document.getElementById('recommend-count');
    let count = 0;

    recommendBtn.addEventListener('click', function() {
        count++;
        recommendCount.textContent = count;

        // animate__animated 클래스와 animate__rubberBand 클래스 추가
        recommendBtn.classList.add('animate__animated', 'animate__rubberBand');

        // 애니메이션이 끝나면 클래스 제거
        recommendBtn.addEventListener('animationend', () => {
            recommendBtn.classList.remove('animate__animated', 'animate__rubberBand');
        }, { once: true });
    });
});