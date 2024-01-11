function enrol (id) {   
    let gid = document.getElementById(`hgroup ${id}`).value;
   
    fetch('/enroll', {
        method: 'PUT',
        body: JSON.stringify({
        id: gid,
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        window.location.reload(); 
    })  
}
 
