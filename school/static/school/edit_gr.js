// If add a student button is clicked, add
document.addEventListener('click', event => {

    // Find what was clicked on
    const element = event.target;

    if (element.className === 'btn btn-success') {    
        document.getElementById(`bc ${element.id}`).style.display = 'block'; 
        document.getElementById(`ab ${element.id}`).style.display = 'none'; 
    }
    
    // If add button is clicked, add the student
    if (element.className === 'btn btn-warning') {
        id = element.id.split(" ")[1];
        document.getElementById(`ab ${id}`).style.display = 'block';
        document.getElementById(`bc ${id}`).style.display = 'none';
    
        let gtitle = document.getElementById('gtitle').value;
    
        fetch('/edit_group', {
            method: 'POST',
            body: JSON.stringify({
            id: id,
            gtitle: gtitle,
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            document.getElementById(`ab ${id}`).style.display = 'block';
            document.getElementById(`grt ${id}`).innerHTML = gtitle; 
        })   
    }   
});