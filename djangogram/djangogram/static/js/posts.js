//CSRF 토큰 가져오는 것 그전에 basehtml에 session 처리 해야함 FALSE로
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

const handleLikeClick = (buttonId) => {
    console.log(buttonId);

    const likeButton = document.getElementById(buttonId);
    console.log(likeButton);

    const likeIcon = likeButton.querySelector("i");
    console.log(likeIcon);
    likeIcon.classList.replace("fa-heart-o", "fa-heart");
    // likeIcon.innerText = "Good";

    const csrftoken = getCookie('csrftoken')
    console.log(csrftoken)

    //포스트 아이디로 빼는것
    const postId = buttonId.split("-").pop();
    const url = "/posts/" + postId + "/post_like"
    //서버로 좋아요 api요청
    fetch(url,{
        method:"POST",
        mode:"same-origin",
        headers:{
            'X-CSRFToken':csrftoken
        },
    })
        .then(response => response.json())
        .then(data => {
            if(data.result === "like") {
                likeIcon.classList.replace("fa-heart-o", "fa-heart");
            }else{
                likeIcon.classList.replace("fa-heart", "fa-heart-o")
            }});

}

