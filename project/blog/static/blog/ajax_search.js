document.addEventListener("DOMContentLoaded", function () {
    const input = document.querySelector('input[name="query"]');
    const resultsList = document.getElementById("live-results");

    let timeout = null;

    input.addEventListener("input", function () {
        clearTimeout(timeout);
        const query = this.value;

        timeout = setTimeout(() => {
            if (query.length < 2) {
                resultsList.innerHTML = "";
                return;
            }

            fetch(`/ajax/search/?query=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    resultsList.innerHTML = "";

                    if (data.length === 0) {
                        resultsList.innerHTML = "<li class='list-group-item'>No results found</li>";
                        return;
                    }

                    data.forEach(post => {
                        const li = document.createElement("li");
                        li.className = "list-group-item";
                        li.innerHTML = `<a href="/post/${post.id}/">${post.title}</a> by ${post.author__username}`;
                        resultsList.appendChild(li);
                    });
                });
        }, 300); // debounce
    });
});
