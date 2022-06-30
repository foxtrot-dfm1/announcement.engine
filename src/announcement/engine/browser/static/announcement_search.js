//logic of querying <announcement> portal type items via restapi

const SEARCH_QUERY_TEMPLATE = {
    "language": 'it',
    "query": [
      {
        "i": "portal_type",
        "o": "plone.app.querystring.operation.selection.any",
        "v": [
          "announcement"
        ]
      },
      {
        "i":"SearchableText",
        "o":"plone.app.querystring.operation.string.contains",
        "v": null
      }
    ]
};

const SEARCH_URL = location.origin + '/' + location.pathname.split('/')[1] + '/@querystring-search';


function executeSearchRequest(searchableText){
    let requests_structure = {
        ...SEARCH_QUERY_TEMPLATE
    };

    requests_structure['query'][1]['v'] = searchableText;

    purge_result_list();

    $.ajax({
        type: "POST",
        url: SEARCH_URL,
        data: JSON.stringify(requests_structure),
        contentType: 'application/json;',
        dataType: 'json',
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
            announcement.find('a').href = result['items'][i]['@id'];
            
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