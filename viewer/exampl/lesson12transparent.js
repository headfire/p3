// ZDesk - Прозрачность

// Прозрачность задается функцией SetTransparent
// для всех вновь создаваемых элементов одновременно
// стандартные значения - NORMAL (непрозрачный)
// GLASS (стекло), CHOST (призрак)

// Используйте эффект прозрачности для 
// вспомогательных геометрических построений

function myTestTransparent(x, z, color, opacity) {

  SetPointColor(color);
  SetLineColor(color);
  SetLabelColor(color);
  SetObjectColor(color);
  SetTriangleColor(color);

  SetTransparent(opacity);  
  
  var a = Decart(x,-100,z);
  var b = Decart(x,100,z);
  Point(a);
  Vect(a, b);
  Sphere(Decart(x,200,z),30);
  Label(a,'VECT');
}  

myTestTransparent(-300, 100, GRAY, NORMAL);
myTestTransparent(-300, 200, GRAY, GLASS);
myTestTransparent(-300, 300, GRAY, CHOST);

myTestTransparent(-200, 100, RED, NORMAL);
myTestTransparent(-200, 200, RED, GLASS);
myTestTransparent(-200, 300, RED, CHOST);

myTestTransparent(-100, 100, GREEN, NORMAL);
myTestTransparent(-100, 200, GREEN, GLASS);
myTestTransparent(-100, 300, GREEN, CHOST);

myTestTransparent(0, 100, BLUE, NORMAL);
myTestTransparent(0, 200, BLUE, GLASS);
myTestTransparent(0, 300, BLUE, CHOST);

myTestTransparent(100, 100, MAGENTA, NORMAL);
myTestTransparent(100, 200, MAGENTA, GLASS);
myTestTransparent(100, 300, MAGENTA, CHOST);

myTestTransparent(200, 100, CYAN, NORMAL);
myTestTransparent(200, 200, CYAN, GLASS);
myTestTransparent(200, 300, CYAN, CHOST);

myTestTransparent(300, 100, YELLOW, NORMAL);
myTestTransparent(300, 200, YELLOW, GLASS);
myTestTransparent(300, 300, YELLOW, CHOST);

myTestTransparent(400, 100, BROWN, NORMAL);
myTestTransparent(400, 200, BROWN, GLASS);
myTestTransparent(400, 300, BROWN, CHOST);

// ok :)