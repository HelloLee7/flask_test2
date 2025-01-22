document.addEventListener('DOMContentLoaded', function() {
    const recommendBtn = document.getElementById('recommend-btn');
    const recommendCount = document.getElementById('recommend-count');
    const recommendMessage = document.getElementById('recommend-message');
    const recipeId = document.getElementById('recipe-id').value;

    if (!recommendBtn || !recommendCount || !recommendMessage || !recipeId) {
        console.error("오류: 필요한 DOM 요소들을 찾을 수 없습니다. recipe_detail.html 파일 구조를 확인하세요.");
        return; // DOM 요소 로드 실패 시, 더 이상 진행하지 않고 함수 종료
    }

    recommendBtn.addEventListener('click', function() {
        // 추천 요청 시작 시 메시지 초기화 (혹시 남아있을 에러 메시지 제거)
        recommendMessage.textContent = "";

        fetch('/recommend_recipe', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'recipe_id=' + recipeId,
        })
        .then(response => {
            if (!response.ok) { // response.status가 200-299 범위가 아니면 에러로 처리
                // 서버 응답이 에러인 경우 (401, 409, 500 등)
                return response.json().then(errorData => {
                    throw new Error(`${response.status} ${response.statusText}: ${errorData.message || '서버 오류'}`);
                });
            }
            return response.json(); // 응답이 성공인 경우 (200 OK) JSON 파싱
        })
        .then(data => {
            // 추천 완료 후 처리
            if (data.message === '추천 완료') {
                recommendCount.textContent = data.recommendation_count; // 서버에서 업데이트된 추천 수 반영
                recommendBtn.classList.add('animate__animated', 'animate__rubberBand');
                recommendBtn.addEventListener('animationend', () => {
                    recommendBtn.classList.remove('animate__animated', 'animate__rubberBand');
                }, { once: true });
            } else {
                // 추천 완료 메시지가 아닌 경우 (예: '이미 추천을 눌렀습니다', '로그인을 하지 않았습니다') - 메시지 표시
                recommendMessage.textContent = data.message;
            }
        })
        .catch(error => {
            // fetch 요청 실패 또는 서버 에러 발생 시 처리
            console.error("추천 기능 에러:", error); // 개발자 콘솔에 자세한 에러 로그 출력
            recommendMessage.textContent = `로그인 해주세요!`; // 사용자에게 간략한 오류 메시지 표시
        });
    });
});