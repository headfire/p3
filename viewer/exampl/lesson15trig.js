function myGraph(fname, func, 
                 amin, amax, fmin, fmax 
                  ,num) {
  var y = -400 + num*100;
  var steps = 100;
  var step = (amax - amin)/steps;
  var i, a1,z1, a2, z2;
  var k = 400/(fmax - fmin);
  Label(Decart(-600,y,100),fname);
  for (i=0;i<100;i++)  {
     a1 = amin + step * i;
     z1 = (func(a1) - fmin) * k + 10;
     a2 = amin + step * (i + 1);
     z2 = (func(a2) - fmin) * k  + 10;
     Line(Decart(-500+i*5, y, z1),
          Decart(-500+(i+1)*5,y, z2)
          );
  }
}

Label(Decart(0,500,250), 'PI = ' + PI);
Label(Decart(0,500,200), 'Deg(PI) = ' + Deg(PI));
Label(Decart(0,500,150), 'Rad(180) = ' + Rad(180));

var num = 0;
myGraph( 'Sin(x)',
    function(x) { return Sin(x); }, 
    -PI,PI,-1,1,num++);
myGraph( 'Cos(x)',
    function(x) { return Cos(x); }, 
    -PI,PI,-1,1,num++);
myGraph( 'Tan(x)',
    function(x) { return Tan(x); }, 
    -PI/2+0.3,PI/2-0.3,-3,+3,num++);
myGraph( 'ASin(x)',
    function(x) { return ASin(x);},
    -1,1,-PI/2,PI/2,num++);
myGraph( 'ACos(x)',
    function(x) { return ACos(x);},
    -1,1, 0,PI,num++);
myGraph( 'ATan(x)',
    function(x) { return ATan(x);},
    -10,10, -PI/2,PI/2,num++);
