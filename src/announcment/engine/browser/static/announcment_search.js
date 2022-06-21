//logic of querying <announcment> portal type items via restapi

const SEARCH_QUERY_TEMPLATE = {
    "query": [
      {
        "i": "portal_type",
        "o": "plone.app.querystring.operation.selection.any",
        "v": [
          "announcment"
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
    let conteiner = $('#container_announcments');
    if (result['items_total'] > 0){
        for(let i = 0; i < result['items_total']; i++){
            conteiner.append($(`
                <div class="row pt-1">
                    <div class="card w-100">
                        <div class="card-header">
                        ${result['items'][i]['review_state']}
                        </div>
                        <div class="card-body">
                        <h5 class="card-title">${result['items'][i]['title']}</h5>
                        <p class="card-text">${result['items'][i]['description']}</p>
                        <a href="${result['items'][i]['@id']}" class="btn btn-primary">View</a>
                        </div>
                    </div>
            
                </div>
            `));
        }
    }
}

function purge_result_list(){
    $('#container_announcments').empty();
}

// bind the actions
$('#announcment_search_form').submit(function(e){
    e.preventDefault();
    executeSearchRequest(
        $('#announcment_search_form').find('input[name="SearchableText"]').val()
    );
});