// ZDesk - Последовательные построения

// Чертеж в Z-desk может содержать несколько кадров
// Это полезно если Вы хотите привести последовательность 
// геометрических построений по шагам
// Делается это с помощью команды SetVisible

// SetVisible(startFrame, endFrame);

// с момента действия команды до момента следующей команды SetVisible
// всем построениям задается видимость в пределах указанных кадров
// общее количество кадров устанавливается максимальным аргументом endFrame
// среди всех применений SetVisible

// по умолчанию в начале черчения SetVisible(1,1), то есть всего один кадр
// и все построения видимы только в этом кадре

// SetVisible также действует на команду Message()

//SetCoord(Decart(-100,0,100), Decart(-100,-300,300));

var a = Decart(0,0);
var b = Decart(200,0);
var c = Decart(200,200);
var d = Decart(0,200);
var e = Decart(100,330);

SetVisible(1,10);
Message('Задача: соединить точки не отрывая пера от бумаги.');
Point(a);
Point(b);
Point(c);
Point(d);
Point(e);

SetVisible(2,9);
Message('Шаг 1');
Line(a,b);

SetVisible(3,9);
Message('Шаг 2');
Line(b,c);

SetVisible(4,9);
Message('Шаг 3');
Line(c,d);
SetVisible(5,9);
Message('Шаг 4');
Line(d,a);

SetVisible(6,9);
Message('Шаг 5');
Line(a,c);

SetVisible(7,9);
Message('Шаг 6');
Line(e,c);

SetVisible(8,9);
Message('Шаг 7');
Line(e,d);

SetVisible(9,9);
Message('Шаг 8');
Line(b,d);

// ok :)