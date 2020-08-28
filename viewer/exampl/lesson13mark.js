// ZDesk - Метки отрезков и углов

// В геометрии принято обозначать равные
// углы и отрезки специальными отметками
// В ZDesk для этого существуют команды

// MarkLine(placeA, placeB, markCount);
// MarkAngle(placeA, placeB, placeC ,markCount);

function myTriangle(x,y,z, angle, markColor) {
  var a = Decart(x-100,y+0,z);
  var b = Decart(x+100,y+0,z);
  var c = Decart(x+50,y + Math.cos(angle)*200, z + Math.sin(angle)*200);
  Point(a);  Point(b);  Point(c);
  Line(a,b); Line(b,c);  Line(c,a);
  SetMarkColor(markColor);
  MarkLine(a,b,1); MarkLine(b,c,2);  MarkLine(c,a,3);
  MarkAngle(a,b,c,1); 
  MarkAngle(b,c,a,2);  
  MarkAngle(c,a,b,3);
}

myTriangle(-300,0,50,Rad(90),GRAY);
myTriangle(0,0,0,Rad(0), BROWN);
myTriangle(300,0,200,Rad(60),BLUE);

// ok :)