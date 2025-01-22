document.addEventListener('DOMContentLoaded', function() {
    const animatedLinks = document.querySelectorAll('.animated-link');
    const signupLink = document.querySelector('.signup-link'); // "회원가입" 링크 요소 선택

    animatedLinks.forEach(link => {
        let animated = false;
        let animationClass = 'animate__flipInX'; // 기본 애니메이션 효과

        // "회원가입" 링크인 경우 애니메이션 효과 변경
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
                currentLink.classList.remove('animate__animated', animationClass); // animationClass 변수 사용
                animated = false;
                currentLink.removeEventListener('animationend', handleAnimationEnd);
            }

            currentLink.addEventListener('animationend', handleAnimationEnd);
        });
    });
});
