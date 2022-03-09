function borrarNota(noteId) {
    fetch("/borrar-nota", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }