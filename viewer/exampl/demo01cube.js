var a1 = Decart(-100,100);
var b1 = Decart(100,100);
var c1 = Decart(100,-100);
var d1 = Decart(-100,-100);
var a2 = Decart(-100,100,200);
var b2 = Decart(100,100,200);
var c2 = Decart(100,-100,200);
var d2 = Decart(-100,-100,200);

Point(a1);
Point(b1);
Point(c1);
Point(d1);
Line(a1, b1);
Line(b1, c1);
Line(c1, d1);
Line(d1, a1);
Label(a1, 'А1');
Label(b1, 'B1');
Label(c1, 'C1');
Label(d1, 'D1');

Point(a2);
Point(b2);
Point(c2);
Point(d2);
Line(a2, b2);
Line(b2, c2);
Line(c2, d2);
Line(d2, a2);
Label(a2, 'А2');
Label(b2, 'B2');
Label(c2, 'C2');
Label(d2, 'D2');

Line(a1,a2);
Line(b1,b2);
Line(c1,c2);
Line(d1,d2);
