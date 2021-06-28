var trackedElement;

document.addEventListener("DOMContentLoaded", () => {
    const notes = document.getElementsByClassName("note");
    for(let note of notes){
        note.addEventListener('dblclick', function(event){
            trackedElement = this;
        });
    }
})

document.addEventListener('mousemove', function(event){
    const px = document.getElementById("x");
    const py = document.getElementById("y");
    px.textContent = event.clientX;
    py.textContent = event.clientY;
    if(trackedElement) {
        trackedElement.style.left = event.clientX + 'px';
        trackedElement.style.top = event.clientY + 'px';
    }
})

document.addEventListener('click', () => {
    trackedElement = null;
})