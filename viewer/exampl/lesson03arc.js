// ZDesk - Дуги

// Дуга задается радиусом, центром,
// начальным углом от оси Х и углом
// самой дуги (чертится против часовой стрелки)

// дуги на плоскости
var center1 = Decart(0,0);
Arc(center1,100, Rad(0),Rad(90));
Arc(center1, 150, Rad(45),Rad(90));
Arc(center1, 200, Rad(90),Rad(90));
Arc(center1, 250, Rad(270),Rad(300));
Point(center1);
Vect(center1, Decart(400,0));
Label(Decart(400,0),'X');

// дуга в пространстве
var center2 = Decart(0,0,100);
Arc(center2, 100, Rad(140), Rad(300));
Point(center2);
Label(center2,'C2');

// Дуга в пространстве с наклоном

// для этого следует применить 
// необязательный аргумент lookAt
var center3 = Decart(100,0,200);
var lookAt = Decart(0,0,400);
Arc(center3, 100, Rad(140), Rad(300), lookAt);
Point(center3);
Label(center3,'C2');


// ok :)