// ZDesk - Демо - График

function myColor(i) {
  if (i%7 ==0)
    return BROWN;
  if (i%7 ==1)
    return GRAY;
  if (i%7 ==2)
    return RED;
}

SetCoord(Decart(-400,-300,20));
var n = Decart(0,0,0);
Point(n);
Vect(n,Decart(600,0,0));
Vect(n,Decart(0,600,0));
Vect(n,Decart(0,0,400));

SetTransparent(GLASS);
var i,k;
for(i=1;i<10;i++)
  for(k=1;k<10;k++) {
    SetObjectColor(myColor(i+k));
    h =  (2+Math.sin(i/3+k/3))*100;
    Box(Decart(i*50,k*50,h/2),
        30,30, h
       ); 
  }

