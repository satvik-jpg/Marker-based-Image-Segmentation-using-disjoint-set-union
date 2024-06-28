document.addEventListener('DOMContentLoaded', () => {
    const image = document.getElementById('image');
    const addButton = document.getElementById("addBoxSet");
    const markers = document.getElementById("boxSetsContainer");
    const coordinates = document.getElementById('coordinates');
    const container = document.getElementById('image-container');

    // image.addEventListener('load', () => {
    //     const originalWidth = image.naturalWidth;
    //     const originalHeight = image.naturalHeight;
    //     container.style.width = parseInt(originalWidth / 2) + 'px';
    //     container.style.height = parseInt(originalHeight / 2) + 'px';
    // });

    image.addEventListener('click', (event) => {
        // Get the bounding rectangle of the image
        const rect = image.getBoundingClientRect();

        // Calculate the click position relative to the image
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        // Display the coordinates
        coordinates.textContent = `Coordinates: (${x.toFixed(0)}, ${y.toFixed(0)})`;
    });
    addButton.addEventListener("click", function () {
        const boxSet = document.createElement("div");
        boxSet.className = "box-set";
        boxSet.innerHTML = `
                  <label>x1: <input type="number" name="x1[]" required></label>
                  <label>y1: <input type="number" name="y1[]" required></label>
                  <label>x2: <input type="number" name="x2[]" required></label>
                  <label>y2: <input type="number" name="y2[]" required></label>
                  <button type="button" class="deleteBoxSet">Delete</button>
              `;
        markers.appendChild(boxSet);
  
        boxSet
          .querySelector(".deleteBoxSet")
          .addEventListener("click", function () {
            markers.removeChild(boxSet);
          });
      });
});
