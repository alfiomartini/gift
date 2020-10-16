document.addEventListener("DOMContentLoaded", pagination);

// User.html pagination

function pagination() {
  const page_btns = document.querySelectorAll(".page-btn");
  page_btns.forEach((btn) => {
    if (btn) {
      btn.addEventListener("click", getRepos);
    }
  });
}

function getRepos(event) {
  event.preventDefault();
  const btn = this;
  const url = btn.href;
  console.log("url", url);
  const index = url.search("=");
  // console.log("index of = ", index);
  const page = url.substring(index + 1);
  console.log(page);
  const index_user = url.search("user/");
  const index_mark = url.search("\\?");
  // console.log("index user", index_user);
  // console.log("index_mark", index);
  const username = url.substring(index_user + 5, index_mark);
  console.log(username);

  // console.log(repos_wrapper);

  // make get request
  let csrftoken = getCookie("csrftoken");
  fetch(`js/${username}?page=${page}`, {
    method: "GET",
    headers: {
      "X-CSRFToken": csrftoken,
      Accept: "text/html",
      "Content-Type": "text/html",
    },
    credentials: "same-origin",
  })
    .then((response) => {
      // console.log(response.status);
      return response.text();
    })
    .then((html) => {
      const repos_wrapper = document.querySelector(".repos-wrapper");
      repos_wrapper.innerHTML = "";
      repos_wrapper.innerHTML = html;
      // console.log(data);
    })
    .catch((error) => {
      console.log(error);
    });
}
