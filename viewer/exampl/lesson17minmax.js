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

var num = 0;
myGraph( 'Cos(x)',
    function(x) { return Cos(x); }, 
    -PI,PI,-1,1,num++);
myGraph( 'Max(0.5,Cos(x)',
    function(x) { return Max(0.5,Cos(x)); }, 
    -PI,PI,-1,1,num++);
myGraph( 'Min(0.5,Cos(x)',
    function(x) { return Min(0.5,Cos(x)); }, 
    -PI,PI,-1,1,num++);
