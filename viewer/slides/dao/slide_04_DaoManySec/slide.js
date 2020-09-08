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
	loader.load(slidePath+'exp_001_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xcccccc, linewidth: 1});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_002_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_003_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_004_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_005_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_006_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_007_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_008_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_009_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_010_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_011_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_012_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_013_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_014_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_015_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_016_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_017_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_018_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_019_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_020_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_021_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_022_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_023_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_024_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_025_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_026_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_027_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_028_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_029_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_030_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_031_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_032_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_033_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_034_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_035_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_036_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_037_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_038_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_039_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_040_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_041_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_042_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_043_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_044_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_045_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_046_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_047_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_048_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_049_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_050_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_051_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_052_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_053_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_054_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_055_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_056_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_057_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_058_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_059_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_060_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_061_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_062_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_063_edge.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0xe51919, linewidth: 2});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_064_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
}
