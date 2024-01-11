function clos (id) {   
    let result = confirm("Are you sure you want to close registration?");
    if (result) {
        fetch('/close', {
            method: 'POST',
            body: JSON.stringify({
            id: id,
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            document.getElementById(`openn ${id}`).style.display = 'block';
            document.getElementById(`close ${id}`).style.display = 'none';
        })   
    } 
}