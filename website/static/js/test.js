function myFunction(imgs) {
    const holderImg = document.getElementById("placeholderImg");
    // Get the expanded image
    const expandImg = document.getElementById("expandedImg");
    // Get the image text
    const imgText = document.getElementById("imgtext");
    // Use the same src in the expanded image as the image being clicked on from the grid
    expandImg.src = imgs.src;
    // Use the value of the alt attribute of the clickable image as text inside the expanded image
    imgText.innerHTML = imgs.alt;
    // Show the container element (hidden with CSS)
    holderImg.parentElement.style.display = "none";
    expandImg.parentElement.style.display = "block";
  }