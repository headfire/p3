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
	zdeskXCurve(slidePath+'exp_003_wire.json', 0x1919e5, 4);
	zdeskXCurve(slidePath+'exp_004_wire.json', 0x1919e5, 4);
	zdeskXCurve(slidePath+'exp_005_wire.json', 0x1919e5, 4);
	zdeskXCurve(slidePath+'exp_006_wire.json', 0x1919e5, 4);
	zdeskXCurve(slidePath+'exp_007_wire.json', 0x1919e5, 4);
	zdeskXCurve(slidePath+'exp_008_wire.json', 0x1919e5, 4);
	zdeskXCurve(slidePath+'exp_009_wire.json', 0x1919e5, 4);
	zdeskXCurve(slidePath+'exp_010_wire.json', 0x1919e5, 4);
	zdeskXShape(slidePath+'exp_011_shape.json', 0xe51919, 0x333333, 0.9, 0.3);
}
