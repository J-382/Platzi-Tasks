document.addEventListener("DOMContentLoaded", () => {
    const messages = document.getElementsByClassName('flash_item')
    for (let item of messages) {
        console.log(item);
        item.addEventListener('click',function(event){
            if(event.target.tagName === 'INPUT') {
                fadeItemOut(this);
            }
        });
        setTimeout(function(){fadeItemOut(item)}, 5000);   
    }
})

function fadeItemOut(item) {
    item.classList.add("fadeout"); 
    setTimeout(() => {item.style.display = 'none'}, 1000);
}