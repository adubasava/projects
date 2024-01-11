// If edit button is clicked, edit the course
document.addEventListener('click', event => {

    // Find what was clicked on
    const element = event.target;

    if (element.className === 'btn btn-info') {     
        document.getElementById(`o ${element.id}`).style.display = 'none';  
        document.getElementById(`e ${element.id}`).style.display = 'block'; 
    }

    // If save button is clicked, save the course
    if (element.className === 'btn btn-warning') {
        id = element.id.split(" ")[1];
        document.getElementById(`o ${id}`).style.display = 'block';
        document.getElementById(`e ${id}`).style.display = 'none';

        let title = document.getElementById(`t ${id}`).value
        let level = document.getElementById(`l ${id}`).value
        let hours = document.getElementById(`h ${id}`).value 
        let description = document.getElementById(`tx ${id}`).value

        fetch('/edit_course', {
            method: 'POST',
            body: JSON.stringify({
            id: id,
            title: title,
            level: level,
            hours: hours,
            description: description,
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            document.getElementById(`o ${id}`).style.display = 'block'; 
            document.getElementById(`t1 ${id}`).innerHTML = title; 
            document.getElementById(`l1 ${id}`).innerHTML = level;     
            document.getElementById(`h1 ${id}`).innerHTML = hours;     
            document.getElementById(`tx1 ${id}`).innerHTML = description;               
        })        
    }   
});