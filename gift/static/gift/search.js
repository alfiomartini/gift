document.addEventListener("DOMContentLoaded", search);

function search() {
  const search_btn = document.getElementById("search-btn");
  const select = document.getElementById("find-select");
  const input = document.querySelector('input[type="search"]');
  // const main = document.querySelector(".main");
  // const body = document.querySelector("body");
  // const tryit_btns = document.querySelectorAll(".landing-page form button");

  select.addEventListener("change", () => {
    const value = select.value;
    input.value = value;
    input.focus();
  });

  // search_btn.addEventListener("click", showSpinner);

  // tryit_btns.forEach((btn) => {
  //   if (btn) {
  //     btn.addEventListener("click", showSpinner);
  //   }
  // });

  function showSpinner(event) {
    event.preventDefault();
    const btn = this;
    const form = btn.parentElement;
    // see: https://stackoverflow.com/questions/42053775/getting-error-form-submission-canceled-because-the-form-is-not-connected
    // document.body.append(form);
    // form.style.display = "none";
    form.submit();
    main.innerHTML = "";
    const spinner = `<div class="d-flex justify-content-center spinner">
          <div class="spinner-border" role="status">
            <span class="sr-only">Loading...</span>
          </div>
        </div>`;
    main.innerHTML = spinner;
  }
}
