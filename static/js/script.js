document.addEventListener("DOMContentLoaded", function () {
    const addButton = document.getElementById("addBoxSet");
    const markers = document.getElementById("boxSetsContainer");
    const image = document.getElementById('image');
    const coordinates = document.getElementById('coordinates');
    const container=document.getElementById('container')

    image.addEventListener('load', () => {
        const originalWidth = image.naturalWidth;
        const originalHeight = image.naturalHeight;
    });

    image.addEventListener('click', (event) => {
        // Get the bounding rectangle of the image
        const rect = image.getBoundingClientRect();

        // Calculate the click position relative to the image
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        // Display the coordinates
        coordinates.textContent = `Coordinates: (${x.toFixed(0)}, ${y.toFixed(0)})`;
    });
    
    
  });