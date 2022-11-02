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
	zdeskXCurve('exp_001_edge', 0x4c4c4c, 2);
	zdeskXCurve('exp_002_wire', 0x1919e5, 4);
	zdeskXPoint(0, -10, 0, 0x1919e5, 3);
	zdeskXCurve('exp_003_edge', 0xe51919, 2);
	zdeskXShape('exp_004_shape', 0xe51919, 0x333333, 0.9, 0.3);
	zdeskXPoint(33.7486, 15.1669, 0, 0xe51919, 3);
	zdeskXPoint(12.4894, -0.686428, 0, 0xe51919, 3);
	zdeskXCurve('exp_005_wire', 0xe51919, 2);
}
