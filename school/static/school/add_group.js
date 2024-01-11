// If add a student button is clicked, add
document.addEventListener('click', event => {

    // Find what was clicked on
    const element = event.target;

    if (element.className === 'btn btn-outline-info') {    
        document.getElementById(`gh ${element.id}`).style.display = 'block'; 
        document.getElementById(`x ${element.id}`).style.display = 'none'; 
    }
    
    // If add button is clicked, add group
    if (element.className === 'btn btn-outline-success') {
        id = element.id.split(" ")[1];
        document.getElementById(`x ${id}`).style.display = 'block';
        document.getElementById(`gh ${id}`).style.display = 'none';
    
        let title = document.getElementById('gtitle').value;
    
        fetch('/add_gr', {
            method: 'POST',
            body: JSON.stringify({
            id: id,
            title: title,
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            window.location.reload();
        })   
    }   
});