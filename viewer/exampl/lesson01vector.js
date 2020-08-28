// ZDesk - Векторы

// сначала задаем начало и конец векторов в
// декартовых координатах
var start = Decart(0,0,100);
var vA = Decart(100,-50,200);
var vB = Decart(100,50,200);
var vAB = Decart(200,0,300);

// обозначаем начльную точку
Point(start);

// чертим векторы
Vect(start, vA);
Vect(start, vB);
Vect(start, vAB);

// последний штрих - ставим метки
Label(start, 'O');
Label(vA, 'А');
Label(vB, 'B');
Label(vAB, 'A+B');

// Ок