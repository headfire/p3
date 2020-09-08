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
	zdeskCurve(slidePath+'exp_001_edge.json', 0xcccccc, 1);
	zdeskCurve(slidePath+'exp_002_wire.json', 0x1919e5, 4);
	zdeskCurve(slidePath+'exp_003_wire.json', 0x1919e5, 4);
	zdeskCurve(slidePath+'exp_004_wire.json', 0x1919e5, 4);
	zdeskCurve(slidePath+'exp_005_wire.json', 0x1919e5, 4);
	zdeskCurve(slidePath+'exp_006_wire.json', 0x1919e5, 4);
	zdeskCurve(slidePath+'exp_007_wire.json', 0x1919e5, 4);
	zdeskCurve(slidePath+'exp_008_wire.json', 0x1919e5, 4);
	zdeskCurve(slidePath+'exp_009_wire.json', 0x1919e5, 4);
	zdeskCurve(slidePath+'exp_010_wire.json', 0x1919e5, 4);
	zdeskShape(slidePath+'exp_011_shape.json', 0xe51919, 0x333333, 0.9, 0.3);
}
