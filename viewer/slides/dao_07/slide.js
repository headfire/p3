function loadedSlideGetParam() { 
	 var param = Object(); 
	 param.isDesk = true; 
	 param.isAxis = true; 
	 param.scaleA = 1; 
	 param.scaleB = 5; 
	 param.deskDX = 0; 
	 param.deskDY = 0; 
	 param.deskDZ = -60; 
	 return param;
}

function loadedSlideMake(slidePath) { 
	zdeskXShape(slidePath+'exp_001_shape.json', 0xff593d, 0x333333, 0.9, 1);
	zdeskXShape(slidePath+'exp_002_shape.json', 0xf9ff1e, 0x333333, 0.9, 1);
	zdeskXShape(slidePath+'exp_003_shape.json', 0x8482ff, 0x333333, 0.9, 1);
}
