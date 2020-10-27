document.addEventListener("DOMContentLoaded", sort_dropdown);

function sort_dropdown(){
  const repSortOptions = document.querySelectorAll('.sort-options .dropdown-menu a');
  repSortOptions.forEach(option  => {
    option.addEventListener('click', () =>{
      const sort = option.dataset.sort;
      const query = option.dataset.query;
      const page = option.dataset.page;
      location.assign(`/repos/get/${query}/${sort}?page=${page}`);
    })
  });
}