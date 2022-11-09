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
	zdeskXCurve('exp_001_edge.json', 0x4c4c4c, 2);
	zdeskXCurve('exp_002_wire.json', 0x1919e5, 4);
	zdeskXPoint(0, -10, 0, 0x1919e5, 3);
	zdeskXCurve('exp_003_wire', 0x1919e5, 4);
	zdeskXCurve('exp_004_wire', 0x1919e5, 4);
	zdeskXCurve('exp_005_wire', 0x1919e5, 4);
	zdeskXCurve('exp_006_wire', 0x1919e5, 4);
	zdeskXCurve('exp_007_wire', 0x1919e5, 4);
	zdeskXCurve('exp_008_wire', 0x1919e5, 4);
	zdeskXCurve('exp_009_wire', 0x1919e5, 4);
	zdeskXCurve('exp_010_wire', 0x1919e5, 4);
	zdeskXShape('exp_011_shape', 0xe51919, 0x333333, 0.9, 0.3);
}
