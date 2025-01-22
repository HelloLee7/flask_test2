document.addEventListener('DOMContentLoaded', function() {
    const animatedLinks = document.querySelectorAll('.animated-link');
    const signupLink = document.querySelector('.signup-link.animated-link'); // 수정: 애니메이션 링크만 선택

    animatedLinks.forEach(link => {
        let animated = false;
        let animationClass = 'animate__flipInX';

        if (link === signupLink) {
            animationClass = 'animate__hinge';
        }

        link.addEventListener('mouseenter', function() {
            if (!animated) {
                this.classList.add('animate__animated', animationClass);
                animated = true;
            }
        });

        link.addEventListener('mouseleave', function() {
            let currentLink = this;

            function handleAnimationEnd() {
                currentLink.classList.remove('animate__animated', animationClass);
                animated = false;
                currentLink.removeEventListener('animationend', handleAnimationEnd);
            }

            currentLink.addEventListener('animationend', handleAnimationEnd);
        });
    });
});