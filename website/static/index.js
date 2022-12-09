function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

//not actually used as of right now, href used instead
function route_to_item(id) {
  window.location.replace("/item/" + id)
}

function get_id_from_url(){
    let currentUrl = window.location.pathname
    currentUrl = currentUrl.substring(4)

}