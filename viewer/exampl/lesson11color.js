// ZDesk - Цвет

// Цвета задаются отдельно для
// точек, линий, объектов и меток
// это сделано для того, чтобы
// настроив цвета чертежа больше 
// к этому не возвращатся

function myTestColor(x, color, colorName) {

  SetPointColor(color);
  SetLineColor(color);
  SetLabelColor(color);
  SetObjectColor(color);
  SetTriangleColor(color);
  
  var a = Decart(x,-100,100);
  var b = Decart(x,100,100);
  Point(a);
  Vect(a, b);
  Label(Decart(x,-100,50),colorName);
  Sphere(Decart(x,0,200),30);
  Triangle( Decart(x-20,0,50),
            Decart(x+20,0,50),
		    Decart(x,40,50)
			);
}

myTestColor(-300, GRAY,'GRAY');
myTestColor(-200, RED,'RED');
myTestColor(-100, GREEN,'GREEN');
myTestColor(0, BLUE,'BLUE');
myTestColor(100, MAGENTA,'MAGENTA');
myTestColor(200, CYAN,'CYAN');
myTestColor(300, YELLOW,'YELLOW');
myTestColor(400, BROWN,'BROWN');

// ok :)