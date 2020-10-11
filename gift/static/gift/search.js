document.addEventListener("DOMContentLoaded", search);

function search() {
  const search_btn = document.getElementById("search-btn");
  const select = document.getElementById("find-select");
  const input = document.querySelector('input[type="search"]');
  const main = document.querySelector(".main");
  const body = document.querySelector("body");

  search_btn.addEventListener("click", (e) => {
    main.innerHTML = "";
    const spinner = `<div class="d-flex justify-content-center spinner">
          <div class="spinner-border" role="status">
            <span class="sr-only">Loading...</span>
          </div>
        </div>`;
    main.innerHTML = spinner;
  });

  select.addEventListener("change", () => {
    const value = select.value;
    input.value = value;
    input.focus();
  });
}
