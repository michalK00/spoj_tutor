function redirect(query_param, query_value, elem_id) {
    if (query_value === null && elem_id != null) {
        query_value = document.getElementById(elem_id).value;
    }
    let url = window.location.search
    let new_url = updateQueryString(url, query_param, query_value);

    location.replace(decodeURIComponent(new_url));
}

function updateQueryString(url, key, value) {
    let searchParams = new URLSearchParams(url)
    if (searchParams.has(key)) {
        searchParams.set(key, value)
    } else {
        searchParams.append(key, value)
    }
    return encodeURIComponent("?" + searchParams.toString());
}