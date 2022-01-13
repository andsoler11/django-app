
// get search form and page links
let form = document.getElementById('search_form')
let pageLinks = document.getElementsByClassName('page-link')

// ensure form exists
if (form) {
for (i=0; pageLinks.length > i; i++){
    pageLinks[i].addEventListener('click', function (e) {
    e.preventDefault()
    // get teh data atributte
    let page = this.dataset.page;
    
    // add hidden search input to form
    form.innerHTML += `<input value=${page} name="page" hidden />`
    
    // submit form
    form.submit()
    })
}
}
