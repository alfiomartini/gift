document.addEventListener("DOMContentLoaded", sort_dropdown);

function sort_dropdown(){
  const usersSortOptions = document.querySelectorAll('.sort-options .dropdown-menu a');
  usersSortOptions.forEach(option  => {
    option.addEventListener('click', () =>{
      const sort = option.dataset.sort;
      const query = option.dataset.query;
      const page = option.dataset.page;
      location.assign(`/users/get/${query}/${sort}?page=${page}`);
    })
  });
}