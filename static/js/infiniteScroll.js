const win = $(window);
const is_loading = false;

win.scroll(() => {
    const diff = $(document).height() - win.height();
    const search_params = new URLSearchParams(window.location.search);
    const current_page = parseInt(search_params.get('page')) || 1; 

    const next_page_url = '?page-' + (current_page + 1);
    

    $.ajax({
        type: 'GET',
        url: `http://127.0.0.1:8000/post/post-list`,
        dataType: 'json',
        success: (result) => {
            console.log(`success : ${result["next"]}`);

            if(diff>=0){
                a=fetch(next_page_url)
                console.log(a)
             
            };
  

        },
        error: (xhr, ajaxSettings, thrownError) => {
            console.log(`error : ${thrownError}`);
        },
    });
});