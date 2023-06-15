function redirect(query_param, query_value, elem_id) {
    console.log(query_value)
    if (query_value === null && elem_id != null) {
        query_value = document.getElementById(elem_id).value;
    }
    let url = window.location.search
    let new_url = updateQueryString(url, query_param, query_value);

    location.replace(decodeURIComponent(new_url));
}

function updateQueryString(url, key, value) {
    // Check if the search parameter exists in the URL
    let searchParams = new URLSearchParams(url)

    if (searchParams.has(key)) {
        console.log("has")
        searchParams.set(key, value)
    } else {
        console.log("new")
        searchParams.append(key, value)
    }

    return encodeURIComponent("?" + searchParams.toString());
}