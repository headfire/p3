function loadedSlideGetParam() { 
	 var param = Object(); 
	 param.isDesk = true; 
	 param.isAxis = true; 
	 param.scaleA = 5; 
	 param.scaleB = 1; 
	 param.deskDX = 0; 
	 param.deskDY = 0; 
	 param.deskDZ = -60; 
	 return param;
}

function loadedSlideMake() { 
	zdeskXShape('exp_001_shape', 0xff593d, 0x333333, 0.9, 1);
	zdeskXShape('exp_002_shape', 0xf9ff1e, 0x333333, 0.9, 1);
}
