// ZDesk - Треугольники

// Треугольник задается тремя точками,
// можно на плоскости, можно в пространстве

// на плоскости
var a = Decart(-100,0);
var b = Decart(100,0);
var c = Decart(0,100);
Triangle(a,b,c);
Point(a);Point(b);Point(c);
Line(a,b);Line(b,c);Line(c,a);

// треугольник в пространстве
var a2 = Decart(-100,0,100);
var b2 = Decart(100,0, 100);
var c2 = Decart(0,100, 200);
Triangle(a2,b2,c2);
// оформляем
Point(a2);Point(b2);Point(c2);
Line(a2,b2);Line(b2,c2);Line(c2,a2);
Label(a2,'A');Label(b2,'B');Label(c2,'C');

//можно склеивать 
//для получения произвольных фигур
var d = Decart(-300,-200,100);
var e = Decart(-100,-200,100);
var f = Decart(-100,0,200);
var g = Decart(-300,0,200);
Triangle(d,e,f);
Triangle(d,f,g);
Point(d);Point(e);Point(f);Point(g);
Line(d,e);Line(e,f);Line(f,g);Line(g,d);


// ok :)