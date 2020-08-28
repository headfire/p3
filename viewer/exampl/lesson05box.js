// ZDesk - Box-прямоугольный параллелепипед

// Задается положением центра 
// и размерами по осям
var place = Decart(0,0,50);
var sizeX = 50;
var sizeY = 200;
var sizeZ = 100;
Box(place,sizeX,sizeY,sizeZ);

// Можно также добавить поворот параметрами
// lookAt и zAngle
var newPlace = Decart(300,0,100);
var lookAt = Decart(500,300,300);
var zAngle =45;
Box(newPlace, sizeX,sizeY,sizeZ, lookAt, zAngle);
Vect(newPlace, lookAt)

// ok :)