document.addEventListener('DOMContentLoaded',()=>{
    const imgInput = document.querySelectorAll('.upload-img');

    imgInput.forEach(input => {
        input.addEventListener("change",(e)=>{
            if(e.target.files[0].size){
               postImage(e.target.files[0],input.getAttribute('data-id'))
            }
        })
    })

    function postImage(file,productId){
         const formData = new FormData();
        formData.append('image', file);

        const xhr = new XMLHttpRequest();
        xhr.open('POST', `/admin/change-image/${productId}/`, true);
        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));

        xhr.onload = function() {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.status === 'success') {
                    alert('Image updated successfully!');
                    location.reload();
                } else {
                    alert('Error updating image.');
                }
            } else {
                alert('Error updating image.');
            }
        };
        xhr.send(formData);
    }


})