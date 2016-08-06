var scene, camera, renderer, clock, controls, composer, listener;
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
    //composer.addPass(bloomPass);
    composer.addPass(copyPass);

    document.body.appendChild(renderer.domElement);
}

var noise_buf, click_buf;
function init_sound() {
    var noise_req = new XMLHttpRequest();
    noise_req.open('GET', "noise.mp3", true);
    noise_req.responseType = 'arraybuffer';
    noise_req.onload = function() {
        listener.context.decodeAudioData(noise_req.response, function(buf) {
            noise_buf = buf;
        });
    }
    noise_req.send();

    var click_req = new XMLHttpRequest();
    click_req.open('GET', "click.mp3", true);
    click_req.responseType = 'arraybuffer';
    click_req.onload = function() {
        listener.context.decodeAudioData(click_req.response, function(buf) {
            click_buf = buf;
        });
    }
    click_req.send();
}

var poles;
function init_scene() {
    var alight = new THREE.AmbientLight(0x101010);
    scene.add(alight);

    var sky_geo = new THREE.BoxGeometry(100, 100, 100);
    var sky_mat = new THREE.MeshLambertMaterial(
        { color: 0x000020, side: THREE.BackSide });
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

function set_sound(pole) {
    var sound = pole.children[1];
    var id = pole.sound_id;
    var rawfreq = pole.sound_freq;
    var mag = pole.sound_mag;
    var freq = 2000 + (rawfreq/255) * 4000;
    sound.source.disconnect();
    if(id == 1) {
        var sine_source = listener.context.createOscillator();
        sine_source.type = "sine";
        sine_source.frequency.value = freq;
        sine_source.start();
        sound.setNodeSource(sine_source);
    } else if(id == 2) {
        var square_source = listener.context.createOscillator();
        square_source.type = "square";
        square_source.frequency.value = freq;
        square_source.start();
        sound.setNodeSource(square_source);
    } else if(id == 3) {
        var triangle_source = listener.context.createOscillator();
        triangle_type = "triangle";
        triangle_source.frequency.value = freq;
        triangle_source.start();
        sound.setNodeSource(triangle_source);
    } else if(id == 4) {
        if(noise_buf === undefined) return;
        var noise_source = listener.context.createBufferSource();
        noise_source.buffer = noise_buf;
        noise_source.loop = true;
        noise_source.start();
        sound.setNodeSource(noise_source);
    } else if(id == 5) {
        if(noise_buf === undefined) return;
        var click_source = listener.context.createBufferSource();
        click_source.buffer = click_buf;
        sound.setNodeSource(click_source);
        click_source.start();
    } else {
        sound.setVolume(0);
    }
    sound.setVolume(mag / 255);
}

function set_pole(i, j, data) {
    var pole = poles[i*7+j];
    var light = pole.children[0];
    var sound = pole.children[1];
    var color = new THREE.Color(data[0]/255, data[1]/255, data[2]/255);
    pole.material.emissive.setHex(color.getHex());
    light.color.setHex(color.getHex());

    if(   pole.sound_id   != data[3]
       || pole.sound_freq != data[4]
       || pole.sound_mag  != data[5])
    {
        pole.sound_id   = data[3];
        pole.sound_freq = data[4];
        pole.sound_mag  = data[5];
        set_sound(pole);
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
    init_sound();
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
