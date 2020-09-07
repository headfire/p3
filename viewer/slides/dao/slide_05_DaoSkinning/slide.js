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
	loader = new THREE.BufferGeometryLoader();
			exp_011_shape_phong_material = new THREE.MeshPhongMaterial({color:0xe51919,specular:0x333333,shininess:0.9,side: THREE.DoubleSide,transparent: true, premultipliedAlpha: true, opacity:0.7,});
			loader.load(slidePath+'exp_011_shape.json', function(geometry) {
				mesh = new THREE.Mesh(geometry, exp_011_shape_phong_material);
				mesh.castShadow = true;
				mesh.receiveShadow = true;
				zdeskScene.add(mesh);
				zdeskRender();
			});

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
	loader.load(slidePath+'exp_003_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_004_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_005_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_006_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_007_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_008_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_009_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
	loader.load(slidePath+'exp_010_wire.json', function(geometry) {
	line_material = new THREE.LineBasicMaterial({color: 0x1919e5, linewidth: 4});
	line = new THREE.Line(geometry, line_material);
	zdeskScene.add(line);
	});
}
