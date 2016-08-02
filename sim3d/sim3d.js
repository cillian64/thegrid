var noiseData = [
    0, 166, 110, 138, 88, 153, 109, 27, 176, 82, 200, 93, 120, 86, 128, 75,
    133, 153, 72, 193, 52, 0, 56, 112, 105, 131, 116, 105, 175, 119, 116, 146,
    172, 36, 144, 102, 127, 114, 212, 116, 152, 172, 196, 85, 231, 167, 138,
    106, 172, 153, 151, 63, 0, 143, 125, 144, 107, 147, 199, 102, 217, 159,
    119, 195, 106, 157, 72, 186, 60, 115, 107, 112, 83, 116, 0, 77, 115, 98,
    11, 107, 177, 113, 92, 136, 119, 159, 80, 59, 90, 43, 105, 48, 92, 133, 50,
    164, 63, 125, 119, 156, 217, 197, 132, 156, 136, 131, 50, 206, 159, 80, 57,
    128, 86, 255, 174, 142, 170, 136, 106, 146, 122, 121, 122, 204, 51, 115,
    172, 161, 86, 48, 120, 103, 60, 98, 152, 162, 157, 140, 99, 152, 114, 156,
    119, 125, 97, 124, 144, 95, 76, 174, 147, 178, 86, 86, 68, 52, 178, 151,
    145, 158, 113, 117, 18, 93, 176, 202, 185, 144, 234, 115, 126, 96, 52, 168,
    238, 114, 82, 194, 191, 114, 159, 95, 188, 98, 119, 164, 220, 49, 130, 121,
    216, 179, 178, 117, 163, 85, 94, 218, 45, 2, 154, 112, 91, 176, 130, 144,
    88, 93, 65, 235, 117, 109, 187, 100, 51, 142, 196, 206, 135, 194, 139, 88,
    48, 187, 107, 51, 108, 134, 83, 153, 85, 224, 163, 43, 206, 172, 163, 130,
    184, 174, 99, 119, 122, 113, 106, 211, 76, 156, 91, 144, 37, 94, 131, 139,
    255, 192
];

var scene, camera, renderer, clock, controls, composer, listener, noiseWave;
function init_world() {
    scene = new THREE.Scene();

    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.autoClear = false;

    camera = new THREE.PerspectiveCamera(
        75, window.innerWidth/window.innerHeight, 0.1, 1000);
    camera.position.set(0.8, -14, 5);
    camera.lookAt({x: 0.8, y: 0, z: 0});

    listener = new THREE.AudioListener();
    camera.add(listener);

    noiseWave = listener.context.createPeriodicWave(new Float32Array(noiseData), new Float32Array(noiseData));

    clock = new THREE.Clock();

    controls = new THREE.FlyControls(camera);
    controls.domElement = renderer.domElement;
    controls.rollSpeed = 1;
    controls.movementSpeed = 3;
    controls.dragToLook = true;

    composer = new THREE.EffectComposer(renderer);
    var renderPass = new THREE.RenderPass(scene, camera);
    composer.addPass(renderPass);
    var bloomPass = new THREE.BloomPass(1.5);
    var copyPass = new THREE.ShaderPass(THREE.CopyShader);
    copyPass.renderToScreen = true;
    composer.addPass(bloomPass);
    composer.addPass(copyPass);

    document.body.appendChild(renderer.domElement);
}

var poles;
function init_scene() {
    var alight = new THREE.AmbientLight(0x101010);
    scene.add(alight);

    var sky_geo = new THREE.BoxGeometry(100, 100, 100);
    var sky_mat = new THREE.MeshLambertMaterial({ color: 0x000020, side: THREE.BackSide });
    var sky_msh = new THREE.Mesh(sky_geo, sky_mat);
    scene.add(sky_msh);

    var gnd_geo = new THREE.PlaneGeometry(16, 16, 128, 128);
    var gnd_mat = new THREE.MeshLambertMaterial({ color: 0x404040 });
    var gnd_msh = new THREE.Mesh(gnd_geo, gnd_mat);
    scene.add(gnd_msh);

    var pole_geo = new THREE.CylinderGeometry(.02, .02, 2.5);
    var pole_mat = new THREE.MeshLambertMaterial({
        color: 0x666666,
        emissive: 0x000000,
        emissiveIntensity: 1,
    });

    poles = [];
    for(var i=0; i<7; i++) {
        for(var j=0; j<7; j++) {
            var pole = new THREE.Mesh(pole_geo.clone(), pole_mat.clone());
            var light = new THREE.PointLight(0x000000, 1, 1);
            var sound = new THREE.PositionalAudio(listener);
            var osc = listener.context.createOscillator();
            osc.type = 'sine';
            osc.frequency.value = 440;
            osc.start(0);
            sound.setNodeSource(osc);
            sound.setRefDistance(0.5);
            sound.setVolume(0);
            pole.rotation.set(Math.PI/2, 0, 0);
            pole.position.set(i*2-6, j*2-6, 1.25);
            light.position.set(0, -1.2, 0);
            pole.add(light);
            pole.add(sound);
            scene.add(pole);
            poles[i*7+j] = pole;
        }
    }
}

function set_pole(i, j, data) {
    var pole = poles[i*7+j];
    var light = pole.children[0];
    var sound = pole.children[1];
    var color = new THREE.Color(data[0]/255, data[1]/255, data[2]/255);
    pole.material.emissive.setHex(color.getHex());
    light.color.setHex(color.getHex());
    sound.source.frequency.value = data[4] / 255 * 6000;
    sound.setVolume(data[5] / 255);
    if(data[3] == 1) {
        sound.source.type = "sine";
    } else if(data[3] == 2) {
        sound.source.type = "square";
    } else if(data[3] == 3) {
        sound.source.type = "triangle";
    } else if(data[3] == 4) {
        sound.source.setPeriodicWave(noiseWave);
    } else {
        sound.setVolume(0);
        sound.source.type = "sine";
    }
}

function on_window_resize(event) {
    renderer.setSize(window.innerWidth, window.innerHeight);
    composer.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
}

function on_keypress(event) {
    var code = event.code;
    if(code == "Digit1") {
        camera.position.set(0.8, -14, 5);
        camera.lookAt({x: 0.8, y: 0, z: 0});
    } else if(code == "Digit2") {
        camera.position.set(0, -12, 1.8);
        camera.lookAt({x: 0, y: 0, z: 1.8});
    } else if(code == "Digit3") {
        camera.position.set(0, 0, 12);
        camera.lookAt({x: 0, y: 0, z: 0});
    } else if(code == "KeyM") {
        if(listener.getMasterVolume() > 0) {
            listener.setMasterVolume(0);
        } else {
            listener.setMasterVolume(1);
        }
    }
}

function render() {
    var delta = clock.getDelta();
    controls.update(delta);
    composer.render();
}

function update() {
}

var ws;
function init_ws() {
    var path = "ws://" + window.location.host + "/ws";
    ws = new WebSocket(path);
    ws.onclose = retry_ws;
    ws.onerror = retry_ws;
    ws.onmessage = handle_ws;
}

function handle_ws(event) {
    var status = document.getElementById('status');
    status.style.color = 'green';
    status.innerHTML = 'Connected';
    var poledata = JSON.parse(event.data);
    for(var i=0; i<7; i++) {
        for(var j=0; j<7; j++) {
            var pole = poledata[i][j];
            set_pole(i, j, pole);
        }
    }
}

function retry_ws() {
    console.log("Websocket closed/error, retrying in 1s");
    var status = document.getElementById('status');
    status.style.color = 'red';
    status.innerHTML = 'Disconnected';
    window.setTimeout(function() {
        var path = "ws://" + window.location.host + "/ws";
        ws = new WebSocket(path);
        ws.onclose = retry_ws;
        ws.onmessage = handle_ws;
    }, 1000);
}

var stats;
function init_stats() {
    stats = new Stats();
    document.body.appendChild(stats.dom);
}

function init() {
    window.addEventListener('resize', on_window_resize, false);
    window.addEventListener('keypress', on_keypress, false);
    init_world();
    init_scene();
    init_ws();
    init_stats();
}

function animate() {
    requestAnimationFrame(animate);
    stats.begin();
    update();
    render();
    stats.end();
}

init();
animate();
