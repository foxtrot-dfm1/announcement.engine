//Logic of querying <announcement> portal type items via @search

const QUERY_TEMP_VAR = '%query_text%'
const SEARCH_QUERY_TEMPLATE = "SearchableText=" + QUERY_TEMP_VAR + "&portal_type=announcement";
const SEARCH_URL = PORTAL_URL + '/@search';


function executeSearchRequest(searchableText){
    let request_query = SEARCH_QUERY_TEMPLATE.replace(
        QUERY_TEMP_VAR, encodeURI(searchableText));

    purge_result_list();

    $.ajax({
        type: "GET",
        url: SEARCH_URL,
        data: request_query,
        headers: {
            'Accept': 'application/json'
        },
        success: function (result, status, xhr) {
            print_result_list(result);
        },
        error: function (xhr, status, error) {
            alert("Result: " + status + " " + error + " " + xhr.status + " " + xhr.statusText);
        }
    });
}

function print_result_list(result){
    let conteiner = $('#container_announcements');
    if (result['items_total'] > 0){
        for(let i = 0; i < result['items_total']; i++){
            let announcement = $('#announcement_row_card_tmp').clone();
            
            // populate fields
            announcement.find('.card-header')[0].innerHTML = result['items'][i]['review_state'];
            announcement.find('.card-title')[0].innerHTML = result['items'][i]['title'];
            announcement.find('.card-text')[0].innerHTML = result['items'][i]['description'];
            announcement.find('a')[0].href = result['items'][i]['@id'];

            console.log(result['items'][i]['@id']);
            
            announcement.attr('id', '');
            announcement.css('display', 'flex');

            
            conteiner.append(announcement);
        }
    }
}

function purge_result_list(){
    $('#container_announcements').empty();
}

// bind the actions
$('#announcement_search_form').submit(function(e){
    e.preventDefault();
    executeSearchRequest(
        $('#announcement_search_form').find('input[name="SearchableText"]').val()
    );
});