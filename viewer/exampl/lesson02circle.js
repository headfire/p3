// ZDesk - Окружности

// окружность на плоскости
var r1 = 100;
var center1 = Decart(0,0);
Circle(center1, r1);
Point(center1);
Label(center1,'C1');

// окружность в пространстве
var r2 = 100;
var center2 = Decart(-100,0,100);
Circle(center2, r2);
Point(center2);
Label(center2,'C2');

// окружность с наклоном
var r3 = 100;
var center3 = Decart(100,100,200);
var lookAt = Decart(0,0,0);
Circle(center3, r3, lookAt);
Point(center3);
Label(center3,'C3');

// ok :)