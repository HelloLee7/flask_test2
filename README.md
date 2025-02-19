mysql 추가용 참고용 작성

#recipes

SELECT * FROM recipe;



SELECT * FROM cuisine;
SELECT * FROM recipe;


CREATE TABLE recipe (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    ingredients TEXT NOT NULL,
    instructions TEXT NOT NULL,
    cuisine_id INT NOT NULL,
    food_img VARCHAR(255)
);



INSERT INTO recipe (name, ingredients, instructions, cuisine_id, food_img)
VALUES
('김치찌개', '김치, 돼지고기, 두부, 양파, 파', '1. 김치를 볶는다. 2. 돼지고기를 넣고 볶는다. 3. 물을 넣고 끓인다. 4. 두부, 양파, 파를 넣고 끓인다.', 1, 'kimchi_jjigae.jpg'),
('된장찌개', '된장, 두부, 호박, 양파, 파', '1. 멸치 육수를 낸다. 2. 된장을 푼다. 3. 두부, 호박, 양파, 파를 넣고 끓인다.', 1, 'doenjang_jjigae.jpg'),
('스시', '밥, 생선, 김', '1. 밥을 만든다. 2. 생선을 손질한다. 3. 밥과 생선을 김으로 만다.', 2, 'sushi.jpg'),
('케밥', '닭가습살, 말린 표고 버섯, 파프리카, 밥, 마늘', '1.닭가슴살을 깍둑 썰어준다. 2. 파프리카와 표고도 썰고 물에 15분 담군다. 3. 양념을 이용해서 닭고기를 30분간 재운다. 4. 꼬치에 꽂은 닭고기와 채소를 굽는다.', 3, 'kebab.jpg'),
('쌀국수', '쌀국수 면, 양파, 쪽파, 숙주, 피쉬소스', '1. 시판 육수를 사용하되 쪽파와 식초, 양파를 추가로 넣는다. 2. 쌀국수 면에 고추를 조금 넣고 5분간 삶는다. 3. 기타 추가 재료(샤브샤브용 소고기)를 넣는다. 4.피쉬소스 넣은후 삶아 놓은 국수를 넣고 먹는다.', 4, 'pho.jpg'),
('짜장면', '면, 춘장, 돼지고기, 양파, 감자', '1. 춘장을 볶는다. 2. 돼지고기, 양파, 감자를 넣고 볶는다. 3. 면을 삶아 볶은 짜장에 넣는다.', 5, 'jjajangmyeon.jpg');


INSERT INTO cuisine (name) VALUES ('한식');
INSERT INTO cuisine (name) VALUES ('일식');
INSERT INTO cuisine (name) VALUES ('양식');
INSERT INTO cuisine (name) VALUES ('동남아식');
INSERT INTO cuisine (name) VALUES ('중식');




CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL
);

CREATE TABLE food_ani (
    id INT AUTO_INCREMENT PRIMARY KEY,
    food_ani VARCHAR(255)
);

INSERT INTO food_ani (id, food_ani)
VALUES
('1', 'a1.jpg'),
('2', 'a2.jpg'),
('3', 'a3.jpg'),
('4', 'b4.jpg'),
('5', 'b5.jpg'),
('6', 'b6.jpg');

DELETE FROM recipe WHERE id = 15;





