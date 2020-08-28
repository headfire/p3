// ZDesk - Тор

// Тор задается положением центра,
// главным радиусом и радиусом трубы.
var place = Decart(0,0,100)
var mainRadius = 200;
var tubeRadius = 50;
Torus(place, mainRadius, tubeRadius);

// Можно также добавить поворот
// параметром lookAt
var place1 = Decart(0,0,300);
var mainRadius1 = 100;
var tubeRadius1 = 30;
var lookAt = Decart(300,300,300);
Torus(place1, mainRadius1, tubeRadius1, lookAt);
Vect(place1, lookAt)

// ok :)