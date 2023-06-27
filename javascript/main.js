//Import the necessary libraries
const bip39 = require('bip39');
const THREE = require('three');
const BIP39Colors = require('./BIP39Colors'); // assuming the file is in the same directory

// Function to generate a BIP39 seed from a given hex string
function generateSeed(hexString) {
    let entropy = Buffer.from(hexString, 'hex');
    return bip39.entropyToMnemonic(entropy);
}

// Function to generate and render a color wheel and 3D column from a BIP39 seed
function visualize(seed) {
    // Convert the seed to BIP39 colors
    BIP39Colors.fromSeed(seed);

    // Create a scene for the 3D visualization
    let scene = new THREE.Scene();
    let camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    let renderer = new THREE.WebGLRenderer();

    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    // Create a column of colored cylinders
    let geometry = new THREE.CylinderGeometry(1, 1, 1);
    let materials = BIP39Colors.colors.map(color => new THREE.MeshBasicMaterial({ color }));
    let cylinders = materials.map(material => new THREE.Mesh(geometry, material));
    cylinders.forEach((cylinder, i) => {
        cylinder.position.y = i;
        scene.add(cylinder);
    });

    // Position the camera and animate the scene
    camera.position.z = 5;
    let animate = function () {
        requestAnimationFrame(animate);
        renderer.render(scene, camera);
    };
    animate();
}

// Generate a seed from the hex string
let hexString = '...'; // insert your 64-character hex string here
let seed = generateSeed(hexString);

// Visualize the seed
visualize(seed);
