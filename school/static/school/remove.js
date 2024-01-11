function remove (id) {   
    let result = confirm("Are you sure you want to delete? This action cannot be undone!");
    if (result) {

        document.getElementById(`${id}`).parentElement.remove()

        fetch('/remove_course', {
            method: 'POST',
            body: JSON.stringify({
            id: id,
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
        })   
    } 
}