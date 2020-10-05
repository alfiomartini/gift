document.addEventListener("DOMContentLoaded", search);

function search() {
  const search_btn = document.getElementById("search-btn");
  search_btn.addEventListener("click", processSearch);
}

function processSearch(event) {
  event.preventDefault();
  const input = document.getElementById("search-input");
  // get input string and remove spaces from both ends
  let value = input.value.trim();
  console.log("Just before fetch");
  const csrftoken = getCookie("csrftoken");
  fetch(`/user/get/${value}`, {
    method: "GET",
    headers: {
      "X-CSRFToken": csrftoken,
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    credentials: "same-origin",
  })
    .then((resp) => resp.json())
    .then((json) => {
      console.log(json);
    })
    .catch((error) => {
      console.log(error);
    });
}
