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
	zdeskXCurve(slidePath+'exp_001_edge.json', 0x4c4c4c, 2);
	zdeskXCurve(slidePath+'exp_002_wire.json', 0x1919e5, 4);
	zdeskXPoint(0, -10, 0, 0x1919e5, 3);
	zdeskXCurve(slidePath+'exp_003_edge.json', 0xe51919, 2);
	zdeskXShape(slidePath+'exp_004_shape.json', 0xe51919, 0x333333, 0.9, 0.3);
	zdeskXPoint(33.7486, 15.1669, 0, 0xe51919, 3);
	zdeskXPoint(12.4894, -0.686428, 0, 0xe51919, 3);
	zdeskXCurve(slidePath+'exp_005_wire.json', 0xe51919, 2);
}
