function myRandom(xmin, xmax, ymin, ymax, zmin, zmax, color) {
   SetPointColor(color);
   for (i=0;i<100;i++) 
     Point( Decart ( Random(xmin,xmax),
	                 Random(ymin,ymax),
					 Random(zmin,zmax)
					 ) 
		  );
}

SetCoord(Decart(-250,-250,0));
myRandom(50,300,50,300,50,300, GRAY);
myRandom(150,500,150,500,150,500, BROWN);
