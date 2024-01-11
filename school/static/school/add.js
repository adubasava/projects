// If add a student button is clicked, add
document.addEventListener('click', event => {    

    // Find what was clicked on
    const element = event.target;

    if (element.className === 'btn btn-outline-info') {           
        document.getElementById(`k ${element.id}`).style.display = 'block'; 
        document.getElementById(`i ${element.id}`).style.display = 'none'; 
    }
    
    // If add button is clicked, add the student
    if (element.className === 'btn btn-outline-success') {
        id = element.id.split(" ")[1];
        document.getElementById(`i ${id}`).style.display = 'block';
        document.getElementById(`k ${id}`).style.display = 'none';
    
        const user = document.getElementById('student').value;      
    
        fetch('/add_student', {
            method: 'POST',
            body: JSON.stringify({
            id: id,
            user: user,
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            window.location.reload(); 
        })   
    }   
});