// ZDesk - Демо - ДНК

SetCoord(Decart(-400, 0, 100), Decart(500,0,700))
var i;
var a1 = Polar(100,0,0);
var a2 = Polar(100,Rad(180),0);
var b1, b2;
for (i=1;i<150;i++) {
  b1 = a1; 
  a1 = Polar(100,Rad(i*4),i*6);
  b2 = a2;
  a2 = Polar(100,Rad(i*4+180),i*6)
  SetTransparent(NORMAL);
  SetLineColor(BLUE);
  Line(a1,b1);
  Line(a2,b2);
  if (i%10 == 0) {
      Point(b1);
      Point(b2);
      SetLineColor(RED);
      SetTransparent(GLASS);
      Line(b1, b2);
  }
}