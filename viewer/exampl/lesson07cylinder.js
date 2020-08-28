// ZDesk - Цилиндр и конус

// Цилиндрообразные фигуры задаются положением центра,
// радиусами верха и низа, высотой.

// Если радиусы равны - получается цилиндр 
var place = Decart(0,0,150)
var topRadius = 100;
var bottomRadius = 100;
var height = 200;
Cylinder(place, topRadius, bottomRadius, height);

// Если один из радиусов 0 
// получается усеченный конус
var place1 = Decart(200,0,150);
var topRadius1 = 0;
var bottomRadius1 = 80;
var height1 = 200;
Cylinder(place1, topRadius1, bottomRadius1, height1);


// Можно также добавить поворот
// параметром lookAt
var place2 = Decart(400,0,200);
var topRadius2 = 30;
var bottomRadius2 = 90;
var height2 = 200;
var lookAt = Decart(500,100,300);
Cylinder(place2, topRadius2, bottomRadius2, height2, lookAt);
Vect(place2, lookAt)

// ok :)